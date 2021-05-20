


import EleDiscordLib
import EleAuditLog
import discord
import TicketFunctions
import CommandCooldown
import asyncio
import datetime










async def ModCmd_Audit(bot, ctx, AuditMember: discord.Member, FromDate = '1111/11/11', ToDate = '1111/11/12', AllMode = 'A'):
    print(bot, ctx, AuditMember, FromDate, ToDate, AllMode)
    PrintMessage = ' '


    ## -------- CHECK IF COMMAND IS RAN ON PROPER CHANNEL ------- ###
    if await EleDiscordLib.isCommandAllowedOnChannel('-+Audit', ctx.channel) == False:
        PrintMessage = 'Error: Cannot use this command in this room. please type the command in the proper channel !'

    ## -------- CHECK AUDIT LEVEL PERMITTED ------- ###
    PermLevel = 'Autist'

    if EleDiscordLib.IsMemberARole(ctx.message.author, ['Staff Manager', 'Management', 'Co Owner', 'Owner', 'gramm']) == True:
        PrintMessage = f'<@{ctx.message.author.id}> you are a Supervisor or above! requesting Full audit! :white_check_mark:'
        PermLevel = 'Staff Manager'

    elif EleDiscordLib.IsMemberARole(ctx.message.author, ['Helper']) == True:
        PrintMessage = f'<@{ctx.message.author.id}>, you are a Helper! requesting Partial audit! :white_check_mark:'
        PermLevel = 'Helper'
        if ctx.message.author.id != AuditMember.id:
            PrintMessage = f'Error: {PrintMessage}... But you may only Audit <@{ctx.message.author.id}>, Canceling audit request! :x:'
        X = CommandCooldown.DidUserPassCooldownTimeFor(ctx.message.author.id, ctx.message.channel.guild, 'Audit')
        if X[0] == False:
            PrintMessage = f'Error: {PrintMessage}... But you may only Audit every 36 hours! (last time was {X[1]} hours ago) Canceling audit request! :x:'
            return



    elif EleDiscordLib.IsMemberARole(ctx.message.author, ['Member']) == True:
        PrintMessage = 'Members cannot use this command! :x:'
        PermLevel = 'Member'
        return
    await ctx.send(PrintMessage)
    if PrintMessage.split(' ')[0] == 'Error:':
        return



    await EleAuditLog.Auditinguser(ctx, AuditMember, FromDate, ToDate, PermLevel, bot)



async def ModCmd_PrintAllRecords(bot, ctx, AuditMember : discord.Member, FromDate = '1111/11/11', ToDate = '1111/11/12', Type = 'All'):
    if await EleDiscordLib.isCommandAllowedOnChannel('-+PrintAllRecords', ctx.channel):
        if EleDiscordLib.IsMemberARole(ctx.message.author, ['Staff Manager', 'Management', 'Co Owner', 'Owner']) == False:
            await ctx.send('You cannot use this command.(Mod+)')
            #return
        await ctx.send('Getting all the audit logs from user <@!' + str(AuditMember.id) + '>!')
        Data = await EleDiscordLib.GetAllAuditsFromUserOfType(ctx, AuditMember, FromDate, ToDate, bot, Type)

        Messages = []
        CurrentMessage = ''
        MessageCounter = 0
        for Entry in Data:
            EntryCharNum = len(Entry)
            CurrentMessageCharNum = len(CurrentMessage)
            # print(f'  EntryCharNum:{EntryCharNum}\n  CurrentMessageCharNum:{CurrentMessageCharNum}')

            if CurrentMessageCharNum + EntryCharNum < 2000:
                CurrentMessage = CurrentMessage + Entry
            else:
                Messages.append(CurrentMessage)
                CurrentMessage = Entry
        Messages.append(CurrentMessage)

        CurrentMessgaeNumber = 0
        # print(f'Messages amount: {len(Messages)}')
        # print(f'0x00ff00 Type: {type(0x00ff00)}')
        for Message in Messages:
            CurrentMessgaeNumber = CurrentMessgaeNumber + 1
            EmbedName = f"----------- Entrylist #{CurrentMessgaeNumber}"

            Green = 0
            Blue = 0
            Red = 20 * CurrentMessgaeNumber
            if Red > 255:
                Red = 254
                Blue = 20 * (CurrentMessgaeNumber - 12)
            if Blue > 255:
                Blue = 254
                Green = 20 * (CurrentMessgaeNumber - 24)
            if Green > 255:
                Green = 254
            Color = discord.Color.from_rgb(Red, Blue, Green)
            AidsPrintGetChannelAsHtmlString = discord.Embed(title=EmbedName, description=f"{Message}", color=Color)
            await ctx.send(embed=AidsPrintGetChannelAsHtmlString)
        try:
            pass

        except:
            print('Failed to Extract Logs in PrintAllAuditFromUser')
    else:
        print('not allowed on this channel')


async def ModCmd_ClearUser(bot, ctx, MemberToClear: discord.Member, Amount: int):
    #print(f'Amount = {Amount}')
    MsgAmount = 0
    MsgAmount = Amount + 2
    # Filter Message COunt
    if Amount > 100:
        MsgAmount = 100
    else:
        MsgAmount = Amount

    #Filter Permissions
    if EleDiscordLib.IsMemberARole(ctx.message.author, ['Clear Perm','𝐇𝐢𝐠𝐡 𝐒𝐭𝐚𝐟𝐟', 'program', 'Staff Manager']):
        if EleDiscordLib.IsMemberARole(MemberToClear, ['𝐒𝐭𝐚𝐟𝐟']):
            if EleDiscordLib.IsMemberARole(ctx.message.author, ['program','𝐇𝐢𝐠𝐡 𝐒𝐭𝐚𝐟𝐟']):
                pass
            else:
                await ctx.send('You cannot clear messages from other staff members!')
                return
    else:
        await ctx.send('You cannot use this command.')
        return
    Delmsg = await ctx.send(f'<@{ctx.author.id}> looked in the last {MsgAmount} messages and removed all messages from <@{MemberToClear.id}>')
    # MsgCount = 0
    # print('Deleting message number...')

    #Delete Messages
    msgs = []
    async for message in ctx.channel.history(limit=MsgAmount):
        # MsgCount = MsgCount + 1
        # print(f'{MsgCount}, ', end='')
        if message.author == MemberToClear:
            msgs.append(message)
    await ctx.channel.delete_messages(msgs)

    # print('Done.')
    await asyncio.sleep(3)
    try:
        await Delmsg.delete(delay=3)
    except:
        pass


async def ModCmd_NukeChannel(bot, ctx):
    print('Nuking')
    if EleDiscordLib.IsMemberARole(ctx.message.author, ['owner']) == False:
        return
    KeepGoing = True
    while KeepGoing == True:
        _14daysAgo = datetime.datetime.now() + datetime.timedelta(days=-14)
        msgs = []
        async for message in ctx.channel.history(limit=100):


            if _14daysAgo < message.created_at:
                #print(f'{_14daysAgo} is before \n{message.created_at}')
                msgs.append(message)
            else:
                #print(f'{_14daysAgo} is after \n{message.created_at}\n')
                pass

        await ctx.channel.delete_messages(msgs)

        KeepGoing = False
        async for message in ctx.channel.history(limit=1):
            if _14daysAgo < message.created_at:
                KeepGoing = True
        print(f'Drop Another Nuke? {KeepGoing}')
    await ctx.send(f'<@{ctx.author.id}> Nuked this channel!')







async def TagMissingHelpersInStaffCall(ctx):
    if EleDiscordLib.IsMemberARole(ctx.author, ['anag', 'owner']) == False:
        return


    # get the list of users who have the role "helper"
    HelperMemberIDs = []
    for M in ctx.guild.members:
        if EleDiscordLib.IsMemberARole(M, ['helper']):
            HelperMemberIDs.append(M.id)

    # get the staff call channel
    STAFFCALLCHANNEL = None
    for C in ctx.guild.channels:
        if str(C.type) == 'voice':
            # print(f'VoiceChannel = {C}')
            if '「🔊」שיחת צוות' == str(C.name):
                STAFFCALLCHANNEL = C


    # get the list of users in the staff call
    CallMemberIDs = []
    for X in STAFFCALLCHANNEL.members:
        CallMemberIDs.append(X.id)

    # generate printstring
    printstring = '**The Following <@&746748255068487770>s are not in <#799283340396986378>** :\n\n'
    for H in HelperMemberIDs:
        if H not in CallMemberIDs:
            printstring = printstring + f'<@{H}>\n'

    await ctx.send(printstring)





async def TagMissing(ctx, bot, RoleString = 'Helper', ChannelID = 799283340396986378):
    if EleDiscordLib.IsMemberARole(ctx.author, ['anag', 'owner']) == False:
        return


    # get the list of users who have the role "helper"
    HelperMemberIDs = []
    for M in ctx.guild.members:
        if EleDiscordLib.IsMemberARole(M, [RoleString]):
            if RoleString in str(M.name).lower() or RoleString in str(M.nick).lower():
                HelperMemberIDs.append(M.id)

    # get the staff call channel
    STAFFCALLCHANNEL = bot.get_channel(ChannelID)


    # get the list of users in the staff call
    CallMemberIDs = []
    for X in STAFFCALLCHANNEL.members:
        CallMemberIDs.append(X.id)

    # generate printstring
    X = 0
    printstring = ''
    for H in HelperMemberIDs:
        if H not in CallMemberIDs:
            X = X + 1
            printstring = printstring + f'<@{H}>, '

            if X > 50:
                X = 0
                await ctx.send(printstring)
                printstring = ''
    await ctx.send(printstring)






async def Dvir_IsGay(bot, ctx, channelID, word):


    if EleDiscordLib.IsMemberARole(ctx.author, ['anag', 'owner']) == False:
        return


    C = bot.get_channel(channelID)

    AllMessagesWithWord = []
    D = datetime.datetime.now()



    async def ProcessDeleteMessages(Date, Msgs):
        if len(Msgs) != 0:
            await ctx.send(f'Deleting {len(Msgs)} Messages from Day {Date}')
            try:
                await C.delete_messages(Msgs)
            except:
                for M in Msgs:
                    await M.delete()



    #async for message in C.history(limit=None, after=datetime.datetime.now() + datetime.timedelta(days=-13)):
    CD = datetime.datetime.now()
    async for message in C.history(limit=None):
        # if message is on a new date. tell them the currntly reading-from date
        CD = datetime.datetime.strptime(str(message.created_at), '%Y-%m-%d %H:%M:%S.%f')



        #if the message
        if word in str(message.content):
            print(f'word = {word} and message.content = {message.content}')
            #Add the message to the message list
            AllMessagesWithWord.append(message)


        if CD.day != D.day:
            D = CD
            TempMsg = await ctx.send(f'Currently reading **"{word}"** from day {D.day}-{D.month}-{D.year}...')
            await TempMsg.delete(delay=3)

            await ProcessDeleteMessages(D, AllMessagesWithWord)
            AllMessagesWithWord = []

    await ProcessDeleteMessages(D, AllMessagesWithWord)
    AllMessagesWithWord = []
    await ctx.send(f'Done reading **"{word}"** day {D.day}-{D.month}-{D.year} till {CD.day}-{CD.month}-{CD.year}!')
    print('Done')


