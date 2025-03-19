import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv
import os

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="/", intents=intents)

class RegistroModal(discord.ui.Modal, title="Formulário de Registro"):
    nick = discord.ui.TextInput(label="Nick+Tag", required=True)
    classes = discord.ui.TextInput(label="Sua classe ou Main", required=True)
    tracker = discord.ui.TextInput(label="URL do tracker", required=True)
    adicionais = discord.ui.TextInput(label="Mais informações", style=discord.TextStyle.paragraph, required=True)

    async def on_submit(self, interaction: discord.Interaction):
        canal_destino = bot.get_channel(int(os.getenv('CANAL_DESTINO_ID')))
        embed = discord.Embed(title="Jogador procurando time", description=f"Entrar em contato com {interaction.user.mention}", color=0x2F3136)
        embed.add_field(name="Nick#Tag", value=self.nick.value, inline=False)
        embed.add_field(name="Classe/Main", value=self.classes.value, inline=False)
        embed.add_field(name="Tracker", value=self.tracker.value, inline=False)
        embed.add_field(name="Adicionais", value=self.adicionais.value if self.adicionais.value else "Nenhum", inline=False)
        embed.set_thumbnail(url=interaction.user.avatar.url if interaction.user.avatar else interaction.user.default_avatar.url)
        embed.set_author(name=f"Player @{interaction.user.name}", icon_url=interaction.user.avatar.url if interaction.user.avatar else interaction.user.default_avatar.url)
        await canal_destino.send(embed=embed)
        await interaction.response.send_message("Registro enviado com sucesso!", ephemeral=True)

@bot.event
async def on_ready():
    print(f"Bot conectado como {bot.user}")
    try:
        synced = await bot.tree.sync()
        print(f"Comandos sincronizados: {len(synced)}")
    except Exception as e:
        print(e)

@app_commands.command(name="registrar", description="Formulário de registro")
async def registrar(interaction: discord.Interaction):
    await interaction.response.send_modal(RegistroModal())

async def setup_hook():
    bot.tree.add_command(registrar)

bot.setup_hook = setup_hook

bot.run(os.getenv('DISCORD_TOKEN'))