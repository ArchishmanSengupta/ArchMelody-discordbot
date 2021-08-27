import discord
from discord.ext import commands
import youtube_dl 

bot = discord.ext.commands.Bot(command_prefix = "?");

class music(commands.Cog):
  def __init__(self,client):
    self.client=client


  @bot.command(name="join")

  #joining
  async def join(self,ctx):
    if ctx.author.voice is None:
      await ctx.send("Dude get your a$$ first to the voice chanel!")
    voice_channel=ctx.author.voice.channel
    if ctx.voice_client is None:
      await voice_channel.connect()
    else:
      await ctx.voice_client.move_to(voice_channel)


  # Disconnecting
  @bot.command(name="disconnect")
  async def disconnect(self,ctx):
    await ctx.voice_client.disconnect()

  # Stops song if a song is already playing
  @bot.command(name="play")
  async def play(self,ctx,url):
    ctx.voice_client.stop()
    # FFMPEG
    FFMPEG_OPTIONS={'before_options':'-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5','options':'-vn'}
    YDL_OPTIONS={'format':"bestaudio"}
    vc=ctx.voice_client

    with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
      info= ydl.extract_info(url,download=False)
      # Creates stream to plat the audio
      url2=info['formats'][0]['url']
      source= await discord.FFmpegOpusAudio.from_probe(url2,**FFMPEG_OPTIONS)
      vc.play(source)

  # Pause the audio
  @bot.command(name="pause")
  async def pause(self,ctx):
    await ctx.voice_client.pause()
    await ctx.send("paused ⏸")

  # Resume the audio
  @bot.command(name="resume")
  async def resume(self,ctx):
    await ctx.voice_client.resume()
    await ctx.send("Playing 🎶 ")


def setup(client):
  client.add_cog(music(client))