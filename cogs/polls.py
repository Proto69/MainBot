import discord
from discord.ext import commands
from discord.ui import View, Modal
from datetime import *

class PollEmbed(discord.Embed):
    def __init__(self, user: discord.Member, options: list[str]):
        super().__init__(title=f"Poll by {user.name}", color=discord.Color.blue())
        self.timestamp = datetime.now()
        i = 1
        for option in options:
            self.add_field(name=f"Опция {i}:", value=option, inline=False)
            i += 1

class PollModal(Modal):
    def __init__(self, count: int = 2, *args, **kwargs):
        super().__init__(*args, **kwargs, title=f"Poll with {count} options")

        for i in range(count):
            self.add_item(discord.ui.InputText(label=f"Enter Option {i+1}", placeholder=f"Option {i+1}"))

    async def callback(self, interaction: discord.Interaction):
        a = []
        b = 0
        for i in self.children:
            b += 1
            a.append(i.value)
        message = await interaction.response.send_message(embed = PollEmbed(interaction.user, a))
        msg = await message.original_message()
        await msg.add_reaction("1️⃣")
        await msg.add_reaction("2️⃣")
        if b >= 3:
            await msg.add_reaction("3️⃣")
            if b >= 4:
                await msg.add_reaction("4️⃣")
                if b == 5:
                    await msg.add_reaction("5️⃣")


class PollView(View):
    def __init__(self):
        super().__init__(timeout=None)
    
    @discord.ui.button(label="2 choices",style=discord.ButtonStyle.green, custom_id="create_poll_2")
    async def create_poll2(self, button, interaction):
        await interaction.response.send_modal(PollModal(2))

    @discord.ui.button(label="3 choices",style=discord.ButtonStyle.green, custom_id="create_poll_3")
    async def create_poll3(self, button, interaction):
        await interaction.response.send_modal(PollModal(3))

    @discord.ui.button(label="4 choices",style=discord.ButtonStyle.green, custom_id="create_poll_4")
    async def create_poll4(self, button, interaction):
        await interaction.response.send_modal(PollModal(4))

    @discord.ui.button(label="5 choices",style=discord.ButtonStyle.green, custom_id="create_poll_5")
    async def create_poll5(self, button, interaction):
        await interaction.response.send_modal(PollModal(5))

class Poll(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.slash_command(name="createpoll", description="Create a new poll message.")
    async def create_poll(self, interaction):
        embed = discord.Embed(title="📊 **Polls** 📊",
        color=discord.Color.gold(),
        timestamp=datetime.now(),
        fields=[
             discord.EmbedField(name="БГ:", value="Използвай бутоните отдолу за да създадеш гласуване! Можеш да имаш до 5 опции!", inline=False),
             discord.EmbedField(name="EN:", value="Use the buttons below to choose the number of choices! The maximum number is 5!", inline=False),
             ]
        )
        embed.set_thumbnail(url='https://avatars.slack-edge.com/2020-05-09/1112549471909_7543dde099089941d3c3_512.png')
        
        await interaction.channel.send(embed = embed, view=PollView())

def setup(client):
    client.add_cog(Poll(client))