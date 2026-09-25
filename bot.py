import discord
from discord.ext import commands
import os
import sys
from pathlib import Path
import config

# Configuração do bot
intents = discord.Intents.default()
intents.members = True
intents.guilds = True
intents.message_content = True

bot = commands.Bot(command_prefix='/', intents=intents)

@bot.event
async def on_ready():
    """Evento disparado quando o bot está pronto."""
    print(f'\n✅ Bot conectado como {bot.user}')
    print(f'📊 Bot está em {len(bot.guilds)} servidor(es)')
    
    # Sincroniza comandos slash
    try:
        synced = await bot.tree.sync()
        print(f'✅ {len(synced)} comando(s) slash sincronizado(s)')
    except Exception as e:
        print(f'❌ Erro ao sincronizar comandos: {e}')
    
    # Define status
    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.watching,
            name="verificações do Transformice"
        )
    )
    print('═' * 50)

async def load_cogs():
    """Carrega todos os cogs (extensions) do bot."""
    cogs_dir = Path('cogs')
    
    if not cogs_dir.exists():
        print("❌ Diretório 'cogs' não encontrado!")
        return
    
    for cog_file in cogs_dir.glob('*.py'):
        if cog_file.name.startswith('_'):
            continue
        
        try:
            await bot.load_extension(f'cogs.{cog_file.stem}')
            print(f'✅ Cog carregado: {cog_file.stem}')
        except Exception as e:
            print(f'❌ Erro ao carregar {cog_file.stem}: {e}')
            sys.exit(1)

async def main():
    """Função principal."""
    async with bot:
        await load_cogs()
        
        try:
            print('\n🚀 Iniciando bot...')
            await bot.start(config.DISCORD_TOKEN)
        except KeyboardInterrupt:
            print('\n🛑 Bot desligado pelo usuário')
        except Exception as e:
            print(f'\n❌ Erro ao iniciar bot: {e}')
            sys.exit(1)

if __name__ == '__main__':
    try:
        import asyncio
        asyncio.run(main())
    except KeyboardInterrupt:
        print('\n🛑 Encerrando...')
