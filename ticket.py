import discord
from discord.ui import Button, View
from discord.ext import commands
import asyncio

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

GUILD_ID = 0 # Server ID eintragen! 
TEAM_ROLE = 0 # Die Rolle, welches die Tickets sehen soll! 
TICKET_CHANNEL = 0 # Der Channel, wo Tickets geöffnet werden sollen! 
CATEGORY_ID = 0 # Die Kategorie, wo die Tickets erstellt werden sollen! 

@bot.event
async def on_ready():
    print("Ticket Bot ist online!")

@bot.command()
@commands.is_owner()
async def ticketmsg(ctx):
    button1 = Button(label="Ticket öffnen!", style=discord.ButtonStyle.blurple, custom_id="ticket_button")
    view = View()
    view.add_item(button1)
    embed = discord.Embed(description=f"Hier kommt deine Beschreibung rein!", title=f"Ticket System")
    channel = bot.get_channel(TICKET_CHANNEL)
    await channel.send(embed=embed, view=view)
    await ctx.reply("Gesendet!")

@bot.event
async def on_interaction(interaction):
    if interaction.channel.id == TICKET_CHANNEL:
        if "ticket_button" in str(interaction.data):
            guild = bot.get_guild(GUILD_ID)
            for ticket in guild.channels:
                if str(interaction.user.id) in ticket.name:
                    embed = discord.Embed(description=f"Du kannst nur ein Ticket gleichzeitig öffnen!\nHier hast du bereits ein Ticket offen! {ticket.mention}")
                    await interaction.response.send_message(embed=embed, ephemeral=True)
                    return

            category = bot.get_channel(CATEGORY_ID)
            ticket_channel = await guild.create_text_channel(f"ticket-{interaction.user.id}", category=category,
                                                            topic=f"Ticket von {interaction.user} \nClient-ID: {interaction.user.id}")

            await ticket_channel.set_permissions(guild.get_role(TEAM_ROLE), send_messages=True, read_messages=True, add_reactions=False,
                                                embed_links=True, attach_files=True, read_message_history=True,
                                                external_emojis=True)
            await ticket_channel.set_permissions(interaction.user, send_messages=True, read_messages=True, add_reactions=False,
                                                embed_links=True, attach_files=True, read_message_history=True,
                                                external_emojis=True)
            embed = discord.Embed(description=f'Willkommen im Ticket {interaction.user.mention}!\n'
                                            f'Hier packst du deine Beschreibung rein!\n'
                                            f'Ticket mit `!close` schließen!',
                                color=62719)
            embed.set_author(name=f'Neues Ticket!')
            mess_2 = await ticket_channel.send(embed=embed)
            embed = discord.Embed(title="📬 | Ticket geöffnet!",
                                description=f'Dein Ticket wurde erstellt! {ticket_channel.mention}',
                                color=discord.colour.Color.green())

            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

@bot.command()
async def close(ctx):
    if "ticket-" in ctx.channel.name:
        embed = discord.Embed(
                description=f'Ticket schließt in 5 Sekunden automatisch!',
                color=16711680)
        await ctx.channel.send(embed=embed)
        await asyncio.sleep(5)
        await ctx.channel.delete()

bot.run("") # Hier den Token rein setzen!