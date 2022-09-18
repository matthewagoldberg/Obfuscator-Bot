import discord
from discord.ext import commands
import os
import requests
from subprocess import check_output

bot = commands.Bot(command_prefix="!")
bot.remove_command("help")

file_path = os.path.abspath(os.path.dirname(__file__))


def obfuscate(url):
    input_file = f'{file_path}/temp/input.lua'

    if os.path.exists(input_file):
        os.remove(input_file)

    file_data = requests.get(url).content
    with open(input_file, "wb") as file:
        file.write(file_data)

    p = check_output(["./Obfuscator/run.js"])

    x = "Azure Obfuscator"
    y = "Azure Obfuscated Script"
    with open(f"{file_path}/temp/output-1.lua", 'r') as file :
        filedata = file.read()
    filedata = filedata.replace(x, y)
    with open(f"{file_path}/temp/output-1.lua", 'w') as file:
        file.write(filedata)

@bot.event
async def on_ready():
    print(f"{bot.user} is online ✔️")
    await bot.change_presence(status=discord.Status.online, activity=discord.Game(name="Ready to obfuscate"))

@bot.event
async def on_message(message: discord.Message):
    if message.guild is None and not message.author.bot:
        
            if message.attachments:
                if '.lua' not in message.attachments[0].url:
                    embed=discord.Embed(title=f"***Wrong file extension!***", description=f"only ``.lua`` allowed", color=0xFF3357)
                    await message.channel.send(embed=embed)
                else:
                    print(message.attachments[0].url)
                    obfuscate(message.attachments[0].url)
                    embed=discord.Embed(title="File has been obfuscated", color=0x3357FF)
                    await message.channel.send(embed=embed, file=discord.File(f"{file_path}/temp/output-1.lua"))
 

       
              

bot.run("TOKEN")
