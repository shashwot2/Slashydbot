
# client = discord.client(intents=discord.Intents.default())
@client.command(name="pirate-ai", help="This command will pretend it's pirate AI using openai's GPT-3.5")
async def pirate_ai(context, *, message: str):
    persona = "You are a pirate that plunders loot over the high seas and likes to drink rum"
    if len(message) > 75:
        await context.channel.send("Please keep your message under 75 characters")
        return
    response = await chatgpt(message, persona)
    await context.channel.send(response)


# This function returns the version of the bot to the user, also displays the owner the bot
@client.command(name="version")
async def version(context):
    VersionEmbed = discord.Embed(
        title="Current version", description="The bot is in beta", color=0x00f01)
    VersionEmbed.add_field(name="Owner", value="Slashd0t", inline=False)
    await context.channel.send(embed=VersionEmbed)


@client.command()
async def join(ctx):
    channel = ctx.message.author.voice.channel
    voice = get(client.voice_clients, guild=ctx.guild)
    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()

# This discord play feature is forked from : https://github.com/eric-yeung/Discord-Bot


@client.command()
async def play(ctx, url):
    DL_OPTIONS = {'format': 'bestaudio/best',
                  'noplaylist': True,
                  'extractaudio': True,
                  'audioformat': 'mp3'
                  }
    FFMPEG_OPTIONS = {
        'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_deplay_max 5',
        'options': '-vn'
    }
    voice = get(client.voice_clients, guild=ctx.guild)

    if not voice.is_playing():
        with YoutubeDL(DL_OPTIONS) as ydl:
            info = ydl.extract_info(url, download=False)
        URL = info['url']
        voice.play(discord.FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
        voice.is_playing()
        await ctx.send('bot is playing')

    else:
        await ctx.send("Bot is already playing")
        return


@client.command(name='resume', help='Resumes the song')
async def resume(ctx):
    voice = ctx.message.guild.voice_client
    if voice.is_paused():
        voice.resume()
        await ctx.send("Resuming")
    else:
        await ctx.send("The bot was not playing anything before this. Use play command")


@client.command()
async def pause(ctx):
    voice = get(client.voice_clients, guild=ctx.guild)

    if voice.is_playing():
        voice.pause()
        await ctx.send('Bot has been paused')


@client.command(name='stop', help='Stops the song')
async def stop(ctx):
    voice = ctx.message.guild.voice_client
    if voice.is_playing():
        voice.stop()
        await ctx.send("The bot is stopping")
    else:
        await ctx.send("The bot is not playing anything at the moment.")
