import discord
from discord.ext import commands
from datetime import datetime, timedelta
import config
from database import (
    add_verified_user, get_verified_user, VerificationCode,
    VerificationLog, get_session
)
from utils.code_generator import CodeGenerator
from utils.validators import Validators

class Verification(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.code_generator = CodeGenerator()
        self.validators = Validators()
    
    @discord.app_commands.command(name="verify", description="Gera um código para verificar sua conta do Transformice")
    async def verify(self, interaction: discord.Interaction):
        """Gera um código de verificação para o usuário."""
        await interaction.response.defer(ephemeral=True)
        
        discord_id = str(interaction.user.id)
        
        # Verifica se o usuário já está verificado
        existing_user = get_verified_user(discord_id)
        if existing_user:
            embed = discord.Embed(
                title="❌ Já Verificado",
                description=f"Sua conta Transformice já está verificada como **{existing_user.transformice_username}**",
                color=discord.Color.red()
            )
            embed.add_field(name="Quer reverificar?", value="Use `/reverify` para gerar um novo código")
            await interaction.followup.send(embed=embed, ephemeral=True)
            return
        
        # Gera novo código
        code = self.code_generator.generate_code(config.CODE_LENGTH)
        expires_at = datetime.now() + timedelta(minutes=config.CODE_EXPIRATION_MINUTES)
        
        session = get_session()
        try:
            verification_code = VerificationCode(
                code=code,
                discord_id=discord_id,
                expires_at=expires_at,
                used=False
            )
            session.add(verification_code)
            session.commit()
        finally:
            session.close()
        
        # Envia o código ao usuário
        embed = discord.Embed(
            title="✅ Código de Verificação Gerado",
            description="Siga os passos abaixo para verificar sua conta:",
            color=discord.Color.green()
        )
        embed.add_field(
            name="1️⃣ Seu Código",
            value=f"```{code}```",
            inline=False
        )
        embed.add_field(
            name="2️⃣ Próximos Passos",
            value="""Vá para o **fórum do Transformice** e adicione este código ao seu perfil:
• Faça login no fórum
• Acesse seu perfil
• Cole o código no campo de verificação
• Salve as alterações""",
            inline=False
        )
        embed.add_field(
            name="3️⃣ Confirme no Discord",
            value="Use `/confirm` para validar a verificação",
            inline=False
        )
        embed.set_footer(text=f"⏰ Código expira em {config.CODE_EXPIRATION_MINUTES} minutos")
        
        await interaction.followup.send(embed=embed, ephemeral=True)
    
    @discord.app_commands.command(name="confirm", description="Confirma sua verificação após adicionar o código ao fórum")
    @discord.app_commands.describe(username="Seu nome de usuário no Transformice")
    async def confirm(self, interaction: discord.Interaction, username: str):
        """Confirma a verificação do usuário."""
        await interaction.response.defer(ephemeral=True)
        
        discord_id = str(interaction.user.id)
        username = self.validators.sanitize_username(username)
        
        # Valida o username
        if not self.validators.is_valid_transformice_username(username):
            embed = discord.Embed(
                title="❌ Username Inválido",
                description="O username do Transformice deve conter apenas letras, números e underscores (1-20 caracteres)",
                color=discord.Color.red()
            )
            await interaction.followup.send(embed=embed, ephemeral=True)
            return
        
        session = get_session()
        try:
            # Busca um código válido e não usado
            code_entry = session.query(VerificationCode).filter_by(
                discord_id=discord_id,
                used=False
            ).first()
            
            if not code_entry:
                embed = discord.Embed(
                    title="❌ Nenhum Código Ativo",
                    description="Nenhum código de verificação ativo encontrado. Use `/verify` para gerar um novo.",
                    color=discord.Color.red()
                )
                await interaction.followup.send(embed=embed, ephemeral=True)
                return
            
            # Verifica se o código expirou
            if datetime.now() > code_entry.expires_at:
                code_entry.used = True
                session.commit()
                
                embed = discord.Embed(
                    title="❌ Código Expirado",
                    description="Seu código de verificação expirou. Use `/verify` para gerar um novo.",
                    color=discord.Color.red()
                )
                await interaction.followup.send(embed=embed, ephemeral=True)
                return
            
            # Marca o código como usado e adiciona o usuário
            code_entry.used = True
            session.commit()
            
            # Adiciona ao banco de dados
            if add_verified_user(discord_id, username):
                # Adiciona role
                try:
                    guild = self.bot.get_guild(config.GUILD_ID)
                    member = guild.get_member(int(discord_id))
                    role = guild.get_role(config.VERIFIED_ROLE_ID)
                    
                    if member and role:
                        await member.add_roles(role)
                except Exception as e:
                    print(f"Erro ao adicionar role: {e}")
                
                # Log da verificação bem-sucedida
                log_entry = VerificationLog(
                    discord_id=discord_id,
                    action="verify",
                    status="success",
                    notes=f"Username: {username}"
                )
                session.add(log_entry)
                session.commit()
                
                embed = discord.Embed(
                    title="✅ Verificação Concluída!",
                    description=f"Sua conta Transformice (**{username}**) foi verificada com sucesso!",
                    color=discord.Color.green()
                )
                embed.add_field(name="Status", value="✅ Verificado", inline=True)
                embed.add_field(name="Username", value=f"**{username}**", inline=True)
                embed.set_footer(text="Você agora tem acesso aos canais verificados!")
                
                await interaction.followup.send(embed=embed, ephemeral=True)
            else:
                embed = discord.Embed(
                    title="❌ Erro na Verificação",
                    description="Ocorreu um erro ao processar sua verificação. Tente novamente.",
                    color=discord.Color.red()
                )
                await interaction.followup.send(embed=embed, ephemeral=True)
        finally:
            session.close()

async def setup(bot):
    await bot.add_cog(Verification(bot))
