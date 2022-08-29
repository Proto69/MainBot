import discord
from discord.ext import commands
import sqlite3

class Example(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.slash_command(name="ping", description="Responds with Pong!")
    async def self(self, ctx):
        await ctx.respond("Pong!", ephemeral = True)

    # @commands.slash_command(name="commit", description="Inserts info in database!", guild=discord.Object(924913459592839238))
    # async def wef(self, ctx, type: str, id: int):
    #     db = sqlite3.connect("main.sqlite")
    #     cursor = db.cursor()
    #     sql = ("INSERT INTO main(type, id) VALUES(?, ?)")
    #     val = (type, id)
    #     cursor.execute(sql, val)
    #     db.commit()
    #     cursor.close()
    #     db.close()

def setup(client):
    client.add_cog(Example(client))
