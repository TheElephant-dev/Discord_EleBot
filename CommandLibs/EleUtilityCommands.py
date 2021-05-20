


import EleDiscordLib
import discord
import asyncio
from datetime import datetime


async def Util_EleStaffTemplate(bot, ctx):

    if await EleDiscordLib.isCommandAllowedOnChannel('-+CreateStaffTemplate', ctx.channel):
        #print('Can be used in this channel')
        pass
    else:
        await ctx.send('You cannot use this command in this channel.')
        return
    if EleDiscordLib.IsMemberARole(ctx.message.author, ['program', 'Staff Manager', 'Management', 'Co Owner', 'Owner']):
        #print('Can be used as this role')
        pass
    else:
        await ctx.send('You cannot use this command.(Management+)')
        return


    print(f' > {ctx.message.author.nick} Creating Staff Template')

    PrintString = ''
    Owners = []
    Co_Owners = []
    Managements = []
    StaffMngs = []
    # Supervisors = []
    # Moderators = []
    Helpers = []
    for Member in ctx.message.channel.guild.members:
        if EleDiscordLib.IsMemberARole(Member, ['| Owner']) == True:
            Owners.append(Member)

        if EleDiscordLib.IsMemberARole(Member, ['Co Owner']) == True:
            Co_Owners.append(Member)

        if EleDiscordLib.IsMemberARole(Member, ['Management']) == True:
            Managements.append(Member)

        if EleDiscordLib.IsMemberARole(Member, ['Staff Manager']) == True:
            StaffMngs.append(Member)

        # if EleDiscordLib.IsMemberARole(Member, ['Supervisor']) == True:
        #     Supervisors.append(Member)
        #
        # if EleDiscordLib.IsMemberARole(Member, ['Moderator']) == True:
        #     Moderators.append(Member)

        if EleDiscordLib.IsMemberARole(Member, ['Helper']) == True:
            Helpers.append(Member)

    PrintString = PrintString + '```'

    PrintString = PrintString + f'\n**({len(Owners)}) Server Owners:**\n'
    for Owner in Owners:
        PrintString = PrintString + f'| <@{Owner.id}> '

    PrintString = PrintString + f'\n\n**({len(Co_Owners)}) Co Owners:**\n'
    for Co_Owner in Co_Owners:
        PrintString = PrintString + f'| <@{Co_Owner.id}> '

    PrintString = PrintString + f'\n\n**({len(Managements)}) Managements::**\n'
    for Management in Managements:
        PrintString = PrintString + f'| <@{Management.id}> '

    PrintString = PrintString + f'\n\n**({len(StaffMngs)}) Staff Managers:**\n'
    for StaffMng in StaffMngs:
        PrintString = PrintString + f'| <@{StaffMng.id}> '

    # PrintString = PrintString + f'\n\n**({len(Supervisors)}) Supervisors:**\n'
    # for Supervisor in Supervisors:
    #     PrintString = PrintString + f'| <@{Supervisor.id}> '
    #
    #
    # PrintString = PrintString + f'\n\n**({len(Moderators)}) Moderators:**\n'
    # for Moderator in Moderators:
    #     PrintString = PrintString + f'| <@{Moderator.id}> '

    PrintString = PrintString + f'\n\n**({len(Helpers)}) Helpers:**\n'
    for Helper in Helpers:
        PrintString = PrintString + f'| <@{Helper.id}> '

    PrintString = PrintString + f'\n\n** כמות חברי הצוות : {len(Owners) + len(Co_Owners) + len(Managements) + len(Helpers)}**'
    PrintString = PrintString + '```'



    correctedString = ''
    for line in PrintString.splitlines():
        C_Line = ''
        if line[:1] == '|':
            C_Line = line[1:] + '\n'

        else:
            C_Line = line
        correctedString = correctedString + C_Line + '\n'

    await ctx.send(correctedString)





async def Util_EleCMD(bot, ctx):

    if await EleDiscordLib.isCommandAllowedOnChannel('-+cmd', ctx.channel):
        if EleDiscordLib.IsMemberARole(ctx.message.author, ['Helper', 'Staff Manager', 'Management', 'Owner']) == False:
            await ctx.send('You cannot use this command!.(Helper+)')
            return


        ###################################################### Main Commands
        CommandEntries = [[], []]
        CommandsEmbedMsg = discord.Embed(title="EleModBot Commands:",
                                         description="a list of commands that can be ran using Elephant's moderation robot",
                                         color=0x00ff00)
        CommandEntries[0].append('-+cmd -+CMD')
        CommandEntries[1].append('→ shows this command list')
        CommandEntries[0].append('-+Permit -+permit, -+p, -+P')
        CommandEntries[1].append('→ lets you permit a member into a ticket.')
        CommandEntries[0].append('-+Audit -+A')
        CommandEntries[1].append('→ prints an audit of a given user.')
        CommandEntries[0].append('-+ClearUser')
        CommandEntries[1].append('→ checks up the channel for messages(100 max) made by user, and deletes them')
        CommandEntries[0].append('-+PrintAllRecords -+PAR')
        CommandEntries[1].append('→ prints all audit log entries that a user was involved with.\n for example: "-+PrintAllRecords @bLe#0001 2021/1/1 2021/3/3 Abuse", not using any type of record will print all types.\n Possible Records:\n  -LockedTicket -DeletedTicket\n -ServerMuted -ServerUnmuted\n -ServerDeafen -ServerUndeafen\n -member_move -member_disconnect\n -Manual_Nickname\n -InvitesCreated\n -usedInfractions -warn -tempmute\n -message_delete\n -Passed16_18Plus -AskForHelp_Tupal\n -Audit -Abuse\n -AddedRole -RemovedRole\n -Channel_Update -CreatedPermOverwrite\n -UpdatePermOverwrite -DeletePermOverwrite\n')
        CommandEntries[0].append('-+CreateStaffTemplate -+CST')
        CommandEntries[1].append('→ Creates a template for the updated staff list.')

        for EntryNum in range(len(CommandEntries[0])):
            # print(f'CommandEntries[0] = {CommandEntries[0]}\nCommandEntries[1] = {CommandEntries[1]}\n\n')
            CommandsEmbedMsg.add_field(name=CommandEntries[0][EntryNum], value=CommandEntries[1][EntryNum],
                                       inline=False)
        CommandsEmbedMsg.set_thumbnail(url=bot.get_user(134156783450062848).avatar_url)
        await ctx.send(embed=CommandsEmbedMsg)









        ###################################################### Advanced Commands
        AdvancedEmbedMsg = discord.Embed(title="EleModBot Advanced Commands:",
                                      description="a list of commands that can be ran by the advanced team using Elephant's bot",
                                      color=0x00E100)
        AdvancedCommandEntries = [[], []]

        AdvancedCommandEntries[0].append('-+AddAdvancedCommmet, -+AddAdvCmt')
        AdvancedCommandEntries[1].append('→ Usage: -+AddAdvancedCommmet MEMBER_TAG good/bad words.......')
        AdvancedCommandEntries[0].append('-+RemoveAdvancedCommmet, -+RemAdvCmt')
        AdvancedCommandEntries[1].append('→ Usage: -+RemoveAdvancedCommmet Comment_ID')
        AdvancedCommandEntries[0].append('-+ListAdvancedCommmet, -+ListAdvCmt')
        AdvancedCommandEntries[1].append('→ Usage: -+ListAdvancedCommmet MEMBER_TAG')

        for EntryNum in range(len(AdvancedCommandEntries[0])):
            # print(f'CommandEntries[0] = {DebugCommandEntries[0]}\nCommandEntries[1] = {DebugCommandEntries[1]}\n\n')
            AdvancedEmbedMsg.add_field(name=AdvancedCommandEntries[0][EntryNum], value=AdvancedCommandEntries[1][EntryNum],
                                    inline=False)
        AdvancedEmbedMsg.set_thumbnail(url=bot.get_user(134156783450062848).avatar_url)
        await ctx.send(embed=AdvancedEmbedMsg)











        ###################################################### Debug Commands
        DebugEmbedMsg = discord.Embed(title="EleModBot Debug:",
                                      description="Debug commands to be used to find issues with the bot.",
                                      color=0x008200)
        DebugCommandEntries = [[], []]
        DebugCommandEntries[0].append('-+PrintCache')
        DebugCommandEntries[1].append('→ prints the current action cache')
        DebugCommandEntries[0].append('-+PrintIDCache')
        DebugCommandEntries[1].append('→ prints the current audit log IDs cache')
        DebugCommandEntries[0].append('-+ManuallySaveAuditLogCacheForAllGuilds')
        DebugCommandEntries[1].append('→ if you cant understand what it does from its name... i cannot help you')
        DebugCommandEntries[0].append('-+Cleanup, -+c')
        DebugCommandEntries[1].append(
            '→ Deletes every channel with the name "ticket" excluding "ticket-log", and deletes every channel if on a catagory called "spam".')
        DebugCommandEntries[0].append('-+CreateTicketCreatorMessage')
        DebugCommandEntries[1].append('→ if you cant understand what it does from its name... i cannot help you')
        DebugCommandEntries[0].append('-+PrintGetChannelAsHtmlString')
        DebugCommandEntries[1].append('→ turn the last 1000 messages on a channel into an html file. and send it in chat.')

        for EntryNum in range(len(DebugCommandEntries[0])):
            # print(f'CommandEntries[0] = {DebugCommandEntries[0]}\nCommandEntries[1] = {DebugCommandEntries[1]}\n\n')
            DebugEmbedMsg.add_field(name=DebugCommandEntries[0][EntryNum], value=DebugCommandEntries[1][EntryNum],
                                    inline=False)
        DebugEmbedMsg.set_thumbnail(url=bot.get_user(134156783450062848).avatar_url)
        DebugEmbedMsg.set_image(url=bot.get_user(134156783450062848).avatar_url)
        DebugEmbedMsg.set_footer(text=f"-See? i can make embeds too. i still hate them tho !\n-TheElephant")
        await ctx.send(embed=DebugEmbedMsg)




async def CreateTrackableVote(bot: discord.ext.commands.Bot, ctx, TimeoutSeconds: int):
    if EleDiscordLib.IsMemberARole(ctx.message.author, ['Owner', 'Management', 'Staff Man', 'rogram']) == False:
        return


    votestartdatetime = datetime.now()
    VoteOver = False


    # Get Vote Content
    WordsInCommand = ctx.message.content.split(' ')
    VoteContent = ''
    for x in range(len(WordsInCommand)):
        if x not in [0, 1]:
            VoteContent = VoteContent + WordsInCommand[x] + ' '


    # Delete command message
    try:
        await ctx.message.delete()
    except:
        pass

    #Create the EmbededMessage message function
    def GetEmbeded(Votes = [[], []], VoteLeftSecs = 0):

        EmbededMessage = discord.Embed(title=f'{VoteContent}\nYou have {round(TimeoutSeconds / 60)} Minutes to vote!', description=f"", color=0xD32F2F)
        EmbededMessage.set_thumbnail(url='https://imgur.com/iaN1wB3.png')
        EmbededMessage.set_footer(text=f"{ctx.message.author} opened an unchaneable vote")



        YesVotersString = ''
        NoVotersString = ''
        for YesVoter in Votes[0]:
            YesVotersString = YesVotersString + YesVoter + '\n'
        for NoVoter in Votes[1]:
            NoVotersString = NoVotersString + NoVoter + '\n'

        YesVotersString = YesVotersString + '-----'

        NoVotersString = NoVotersString  + '-----'
        EmbededMessage.add_field(name="Voted Yes", value=YesVotersString, inline=True)
        EmbededMessage.add_field(name="Voted No", value=NoVotersString, inline=True)


        if VoteOver == True:
            EmbededMessage.add_field(name="Vote time ran out.", value=f'\nYes Votes: {len(PeopleWhoVotedYes)}\nNo Votes: {len(PeopleWhoVotedNo)}', inline=False)
        else:
            X = EleDiscordLib.TurnSecondsIntoDayHourMinuteSecond(VoteLeftSecs)
            EmbededMessage.add_field(name="Vote time left:", value=f'{X[1]} Hours, {X[2]} Minutes, and {X[3]} seconds untill it will reach 0',inline=False)


        return EmbededMessage




    # Create Fake Votes
    PeopleWhoVotedYes = []
    PeopleWhoVotedNo = []

    #Create Message and react to it.
    VoteMessage = await ctx.send(embed=GetEmbeded(Votes = [PeopleWhoVotedYes,PeopleWhoVotedNo], VoteLeftSecs=int(TimeoutSeconds - int(divmod((datetime.now() - votestartdatetime).total_seconds(), 1)[0]))))
    await VoteMessage.add_reaction('✅')
    await VoteMessage.add_reaction('❌')


#





    while True:
        SecondsPassedFromVoteStart = int(divmod((datetime.now() - votestartdatetime).total_seconds(), 1)[0])
        if SecondsPassedFromVoteStart > TimeoutSeconds:
            VoteOver = True


        def check(reaction, user):
            if str(reaction.emoji) in ['✅', '❌']:
                if reaction.message == VoteMessage:
                    return VoteMessage.author and reaction


        #Wait for reaction
        try:
            reactorID =789942343619969074
            while reactorID == 789942343619969074:
                reaction, user = await bot.wait_for('reaction_add', timeout=TimeoutSeconds, check=check)
                reactorID = user.id
            await VoteMessage.remove_reaction(reaction, user)
        # reaction timed out
        except asyncio.TimeoutError:
            #print('Timeout')
            pass

        else:
            #print(f'{user}, Voted {reaction}')



            #print(f'{SecondsPassedFromVoteStart} Seconds passed from vote start, {TimeoutSeconds - SecondsPassedFromVoteStart} seconds untill it will reach {TimeoutSeconds}')


            if str(user) not in PeopleWhoVotedYes and str(user) not in PeopleWhoVotedNo:
                if str(reaction.emoji) == '✅':
                    PeopleWhoVotedYes.append(str(user))
                elif str(reaction.emoji) == '❌':
                    PeopleWhoVotedNo.append(str(user))
            else:
                VoteAgainMessage = await ctx.send(f'<@{user.id}> you CANNOT vote again! you already voted!')
                await VoteAgainMessage.delete(delay=5)



        await VoteMessage.edit(embed=GetEmbeded(Votes = [PeopleWhoVotedYes,PeopleWhoVotedNo], VoteLeftSecs=int(TimeoutSeconds - int(divmod((datetime.now() - votestartdatetime).total_seconds(), 1)[0]))))
        if VoteOver == True:
            break
            return








async def SetMonthBestColor(ctx, HexCode):


    if await EleDiscordLib.isCommandAllowedOnChannel('SetMonthBestColor', ctx.channel) == False:
        # X = await ctx.send(embed=discord.Embed(title="Denied.", description=f'Wrong Channel.', color=0x7C0200))
        # await X.delete(delay=10)
        return

    if EleDiscordLib.IsMemberARole(ctx.author, ['🌟 | מצטיין/ת החודש']) == False:
        X = await ctx.send(embed=discord.Embed(title="Denied.", description=f'You are not "מצטיין/ת החודש" !', color=0x7C0200))
        await X.delete(delay=10)
        return



    for role in ctx.guild.roles:
        if '🌟 | מצטיין/ת החודש' in str(role):
            await ctx.send(f'0x{HexCode}')
            await role.edit(reason='מצטיין/ת החודש ביקש זאת מהבוט!', color=HexCode)

