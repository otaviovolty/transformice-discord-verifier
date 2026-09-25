import discord
from discord.ext import commands
from discord import app_commands
import config
from database import (
    get_verified_user, remove_verification, add_verified_user,
    get_session, VerifiedUser
)

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name="verify_user", description="[ADMIN] Verificar um usuário manualmente")
    @app_commands.checks.has_permissions(administrator=True)
    @app_commands.describe(
        user="O usuário do Discord a verificar",
        username="O username do Transformice"
    )
    async def verify_user(self, interaction: discord.Interaction, user: discord.User, username: str):
        """Verifica um usuário manualmente (apenas admin)."""
        await interaction.response.defer(ephemeral=True)
        
        if add_verified_user(str(user.id), username):
            try:
                guild = self.bot.get_guild(config.GUILD_ID)
                member = guild.get_member(user.id)
                role = guild.get_role(config.VERIFIED_ROLE_ID)
                
                if member and role:
                    await member.add_roles(role)
            except Exception as e:
                print(f"Erro ao adicionar role: {e}")
            
            embed = discord.Embed(
                title="✅ Usuário Verificado",
                description=f"{user.mention} foi verificado como **{username}**",
                color=discord.Color.green()
            )
            await interaction.followup.send(embed=embed, ephemeral=True)
        else:
            embed = discord.Embed(
                title="❌ Erro",
                description="Não foi possível verificar o usuário.",
                color=discord.Color.red()
            )
            await interaction.followup.send(embed=embed, ephemeral=True)
    
    @app_commands.command(name="remove_verification", description="[ADMIN] Remover verificação de um usuário")
    @app_commands.checks.has_permissions(administrator=True)
    @app_commands.describe(user="O usuário do Discord")
    async def remove_verification(self, interaction: discord.Interaction, user: discord.User):
        """Remove a verificação de um usuário."""
        await interaction.response.defer(ephemeral=True)
        
        if remove_verification(str(user.id)):
            try:
                guild = self.bot.get_guild(config.GUILD_ID)
                member = guild.get_member(user.id)
                role = guild.get_role(config.VERIFIED_ROLE_ID)
                
                if member and role:
                    await member.remove_roles(role)
            except Exception as e:
                print(f"Erro ao remover role: {e}")
            
            embed = discord.Embed(
                title="✅ Verificação Removida",
                description=f"A verificação de {user.mention} foi removida.",
                color=discord.Color.green()
            )
            await interaction.followup.send(embed=embed, ephemeral=True)
        else:
            embed = discord.Embed(
                title="❌ Usuário Não Encontrado",
                description=f"{user.mention} não está verificado.",
                color=discord.Color.red()
            )
            await interaction.followup.send(embed=embed, ephemeral=True)
    
    @app_commands.command(name="verification_list", description="[ADMIN] Ver todas as verificações")
    @app_commands.checks.has_permissions(administrator=True)
    async def verification_list(self, interaction: discord.Interaction):
        """Lista todas as verificações do servidor."""
        await interaction.response.defer(ephemeral=True)
        
        session = get_session()
        try:
            users = session.query(VerifiedUser).all()
            
            if not users:
                embed = discord.Embed(
                    title="📭 Nenhuma Verificação",
                    description="Nenhum usuário verificado ainda.",
                    color=discord.Color.blue()
                )
                await interaction.followup.send(embed=embed, ephemeral=True)
                return
            
            embed = discord.Embed(
                title="📋 Lista de Verificações",
                description=f"Total de usuários verificados: **{len(users)}**",
                color=discord.Color.blue()
            )
            
            for user in users[:25]:  # Limita a 25 por embed
                embed.add_field(
                    name=f"<@{user.discord_id}>",
                    value=f"Username: `{user.transformice_username}`\nData: {user.verified_at.strftime('%d/%m/%Y %H:%M')}",
                    inline=False
                )
            
            if len(users) > 25:
                embed.set_footer(text=f"Mostrando 25 de {len(users)} usuários")
            
            await interaction.followup.send(embed=embed, ephemeral=True)
        finally:
            session.close()
    
    @app_commands.command(name="resync_roles", description="[ADMIN] Resincronizar roles de todos os usuários")
    @app_commands.checks.has_permissions(administrator=True)
    async def resync_roles(self, interaction: discord.Interaction):
        """Resincroniza as roles de todos os usuários verificados."""
        await interaction.response.defer(ephemeral=True)
        
        session = get_session()
        try:
            users = session.query(VerifiedUser).all()
            guild = self.bot.get_guild(config.GUILD_ID)
            role = guild.get_role(config.VERIFIED_ROLE_ID)
            
            count = 0
            for user in users:
                try:
                    member = guild.get_member(int(user.discord_id))
                    if member and role:
                        if role not in member.roles:
                            await member.add_roles(role)
                            count += 1
                except Exception as e:
                    print(f"Erro ao sincronizar usuário {user.discord_id}: {e}")
            
            embed = discord.Embed(
                title="✅ Sincronização Concluída",
                description=f"Roles adicionadas/sincronizadas: **{count}/{len(users)}** usuários",
                color=discord.Color.green()
            )
            await interaction.followup.send(embed=embed, ephemeral=True)
        finally:
            session.close()

async def setup(bot):
    await bot.add_cog(Admin(bot))
