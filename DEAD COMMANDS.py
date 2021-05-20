@bot.command()
async def SendMeHello(ctx):
    await ctx.message.author.send(f'http://kodesh.snunit.k12.il/images/menu/header.jpg')
    await ctx.message.author.send(file=discord.File(rf'{EleImageGenerator.GenerateAbuseWarningImage("AName", "BName")}'))

@bot.command()
async def SMTU(ctx,  VictimMember: discord.Member, Message):
    await VictimMember.send(f'{ctx.message.author} Said: {ctx.message.content[29:]}')
    print(f'{ctx.message.author} Said: {ctx.message.content[29:]}')


@bot.command()
async def SENDMSG(ctx):
    await bot.get_channel(790397266753093632).send(f'{ctx.message.content[10:]}')
    for X in range(10):
        await bot.get_channel(758332202810998805).send(f'{ctx.message.content[10:]}')
        sleep(1)

@bot.command()
async def ROLECHECK(ctx):
    await EleDiscordLib.MakeSureElephantHasCorrectRoles(bot)


@bot.command()
async def KeepName(ctx,  VictimMember: discord.Member, newNick):
    if ctx.message.author.id == 134156783450062848:
        await ctx.send('KK. doing it!')
        for x in range(100):
            if VictimMember.nick != newNick:
                await VictimMember.edit(nick=newNick, reason=f'{newNick} is {newNick}')
            await asyncio.sleep(5)
    else:
        await ctx.send('You are not my BOSS !')

@bot.command()
async def GimmiePerm(ctx, ChannelID: int):
    if EleDiscordLib.IsMemberARole(ctx.author, ['gramm']):
        CHANNEL = bot.get_channel(ChannelID)
        MEMBER = ctx.author
        await CHANNEL.set_permissions(MEMBER, read_messages=True, manage_channels=True, manage_permissions=True,
                                      manage_webhooks=True, create_instant_invite=True, send_messages=True,
                                      embed_links=True, attach_files=True, add_reactions=True, use_external_emojis=True,
                                      mention_everyone=True, manage_messages=True, read_message_history=True,
                                      send_tts_messages=True, connect=True, stream=True, speak=True, move_members=True,
                                      deafen_members=True, mute_members=True, priority_speaker=True,
                                      use_voice_activation=True, reason=f'Injecting {MEMBER} into {CHANNEL}')




@bot.command()
async def DenyVoiceActionForUserInChannel(ctx, User: discord.Member, ID):
    ChannelID = int(ID)
    channel = bot.get_channel(ChannelID)
    print(type(ChannelID))
    print(type(User))
    sleep(1)
    await channel.set_permissions(User, move_members=False, deafen_members=False, mute_members=False,)

@bot.command()
async def AllowVoiceActionForUserInChannel(ctx, User: discord.Member, ID):
    ChannelID = int(ID)
    channel = bot.get_channel(ChannelID)
    print(type(ChannelID))
    print(type(User))
    sleep(1)
    await channel.set_permissions(User, move_members=True, deafen_members=True, mute_members=True, view_channel=True, connect=True, reason='Injecting Myself into tails Crib')



@bot.command()
async def Shank(ctx, Victim: discord.Member, times: int, reason: str):
    for X in range(times):
        await ctx.send(f'**Shanking {Victim.nick}** because {reason}')



@bot.command()
async def Speak(ctx, GuildID, ChannelID):
    for guild in bot.guilds:
        if guild.id == int(GuildID):
            for channel in guild.channels:
                if channel.id == int(ChannelID):
                    await channel.send(f'{ctx.message.content[46:]}')




@bot.event
async def on_member_update(before, after):
    if before.id == 778702186946756669:
        if before.nick != after.nick:
            Logs = []
            async for Entry in before.guild.audit_logs(limit=1):

                if Entry.user.id not in [134156783450062848, 789942343619969074]:
                    RudePerson = before.guild.get_member(Entry.user.id)
                    print(f"{RudePerson} the retard actually tried to change his name")
                    await before.edit(nick=before.nick)




@bot.command()
async def GimmieMod(ctx):
    member = ctx.message.author
    if member.id == 134156783450062848:
        for role in ctx.message.channel.guild.roles:
            if role.id == 758071269999509569:
                await member.add_roles(role)




    if member.id == 342781709441564672:
        if after.channel != None:
            await member.move_to(None)




@bot.event
async def on_member_update(before, after):
    if before.id == 778702186946756669:
        if before.nick != after.nick:
            Logs = []
            async for Entry in before.guild.audit_logs(limit=1):

                if Entry.user.id not in [134156783450062848, 789942343619969074]:
                    RudePerson = before.guild.get_member(Entry.user.id)
                    print(f"{Entry.user} actually tried to change {before.nick}'s nick to {after.nick}")
                    await before.edit(nick=before.nick)


@bot.command()
async def SetNick(ctx, Member: discord.Member, nick):
    await Member.edit(nick=ctx.message.content[33:])





@bot.command(aliases=['SILC'])
async def SayInLargeChars(ctx):
    Words = ctx.message.content.split(' ')
    del Words[0]
    await EleAbuseCommands.SayInLargeChars(bot, ctx, '_'.join(Words))

async def SayInLargeChars(bot, ctx, Text: str):
    # List_of_Fonts = ['3-d', '3x5', '5lineoblique', 'acrobatic', 'alligator', 'alligator2', 'alphabet', 'avatar',
    #                  'banner', 'banner3-D', 'banner3', 'banner4', 'barbwire', 'basic', 'bell', 'big', 'bigchief',
    #                  'binary', 'block', 'bubble', 'bulbhead', 'calgphy2', 'caligraphy', 'catwalk', 'chunky', 'coinstak',
    #                  'colossal', 'computer', 'contessa', 'contrast', 'cosmic', 'cosmike', 'cricket', 'cyberlarge',
    #                  'cybermedium', 'cybersmall', 'diamond', 'digital', 'doh', 'doom', 'dotmatrix', 'drpepper',
    #                  'eftichess', 'eftifont', 'eftipiti', 'eftirobot', 'eftitalic', 'eftiwall', 'eftiwater', 'epic',
    #                  'fender', 'fourtops', 'fuzzy', 'goofy', 'gothic', 'graffiti', 'hollywood', 'invita', 'isometric1',
    #                  'isometric2', 'isometric3', 'isometric4', 'italic', 'ivrit', 'jazmine', 'jerusalem', 'katakana',
    #                  'kban', 'larry3d', 'lcd', 'lean', 'letters', 'linux', 'lockergnome', 'madrid', 'marquee',
    #                  'maxfour', 'mike', 'mini', 'mirror', 'mnemonic', 'morse', 'moscow', 'nancyj-fancy',
    #                  'nancyj-underlined', 'nancyj', 'nipples', 'ntgreek', 'o8', 'ogre', 'pawp', 'peaks', 'pebbles',
    #                  'pepper', 'poison', 'puffy', 'pyramid', 'rectangles', 'relief', 'relief2', 'rev', 'roman', 'rot13',
    #                  'rounded', 'rowancap', 'rozzo', 'runic', 'runyc', 'sblood', 'script', 'serifcap', 'shadow',
    #                  'short', 'slant', 'slide', 'slscript', 'small', 'smisome1', 'smkeyboard', 'smscript', 'smshadow',
    #                  'smslant', 'smtengwar', 'speed', 'stampatello', 'standard', 'starwars', 'stellar', 'stop',
    #                  'straight', 'tanja', 'tengwar', 'term', 'thick', 'thin', 'threepoint', 'ticks', 'ticksslant',
    #                  'tinker-toy', 'tombstone', 'trek', 'tsalagi', 'twopoint', 'univers', 'usaflag', 'weird']

    List_of_Fonts = ['roman', 'univers', 'doh']

    for Font in List_of_Fonts:
        for Char in Text:
            ToPrint = pyfiglet.Figlet(font=Font).renderText(Char)
            print(ToPrint)
            await ctx.send(ToPrint)

    # for Char in Text:
    #     X = str(pyfiglet.Figlet(font='slant').renderText(Char))
    #     print(X)
    #     await ctx.send(X)



VoiceState = None
@bot.command()
async def Play(ctx, FilePath: str, Times: int):
    AllPossibleFiles = os.listdir(FilePath)





    global VoiceState
    print(FilePath)
    CurrentVC = ctx.author.voice.channel

    try:
        VoiceState = await CurrentVC.connect()
    except:
        pass
    #await VoiceState.play(discord.ffmpegPCMaudio(FilePath))
    for X in range(Times):
        VoiceState.stop()
        SoundFile = random.choice(AllPossibleFiles)
        print(f'Playing {SoundFile}')
        VoiceState.play(discord.FFmpegPCMAudio(f'{FilePath}\{SoundFile}'))
        await asyncio.sleep(random.randint(3, 7) / 10)




MembersNotAllowedToOpenTickets = [479121588281933834]
@bot.event
async def on_guild_channel_create(channel):
    if 'ticket' in str(channel):
        UserThatOpenedTheTicket = None
        for RoleOrUser in channel.overwrites:
            UserThatOpenedTheTicket = RoleOrUser.id
            if UserThatOpenedTheTicket in MembersNotAllowedToOpenTickets:
                print(f'{RoleOrUser} opened a ticket...', end='')
                await channel.delete()
                print(f'Deleted!')

                for C in channel.guild.channels:
                    if 'general' in str(C).lower():
                        print(C)
                        await C.send(f'<@{UserThatOpenedTheTicket}> Y U OPEN TICKET?')


@bot.command()
async def MuteDeafenCycle(ctx, Victim: discord.Member):
    while True:
        await asyncio.sleep(1)
        await Victim.edit(mute=True, deafen=False, reason='Abuz Venoman')
        await asyncio.sleep(1)
        await Victim.edit(mute=False, deafen=True, reason='Abuz Venoman')

@bot.command()
async def GimmeSilence(ctx, Seconds: int = 10):
    Victims = ctx.author.voice.channel.members
    Victims.remove(ctx.author)
    for Victim in Victims:
        try:
            await Victim.edit(mute=True)
        except discord.errors.HTTPException:
            print('Error: user Left Voice, cannot mute.')
    await asyncio.sleep(Seconds)
    for Victim in Victims:
        try:
            await Victim.edit(mute=False)
        except discord.errors.HTTPException:
            print('Error: user Left Voice, cannot unmute.')