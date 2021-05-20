# coding=utf8
import discord
import asyncio
import os
import EleDiscordLib
import EleAuditLog
import datetime
import json
from time import sleep


async def GetChannelAsHtmlString(ChannelToPhrase: discord.channel):
    SaveUser = 'GenericSaveUser'
    Guild = ChannelToPhrase.guild
    returnstring = ''
    returnstring = returnstring + '<body style="background-color:#36393F;">' \
                                  f'<h1 style="text-align: center;"><img style="display: block; margin-left: auto; margin-right: auto;" src="{Guild.icon_url}" alt="" width="326" height="256" /><strong>{Guild.name}</strong></h1>' \
                                  f'<h2 style="text-align: center;"><strong>{ChannelToPhrase.name}</strong></h2>'
    MessageArray = []
    async for Message in ChannelToPhrase.history(limit = 1000):
        MessageArray.append(Message)
    for Message in reversed(MessageArray):
        Member = Message.author
        MessageSentAt = Message.created_at.strftime("%Y-%m-%d %H:%M")

        MemberNick = ''
        try:
            MemberNick = Member.nick
        except:
            MemberNick = (f'Def:{str(Member)}')

        if Message.author.id != 789942343619969074:
            returnstring = returnstring + f'<table style="width: 80%; border-collapse: collapse; margin-left: auto; margin-right: auto; height: 10px;"><tbody><tr style="height: 19px;">' \
                                          f'<td style="width: 1%; height: 10px;"><img src="{Member.avatar_url}" alt="" width="60" height="60" />&nbsp;</td>' \
                                          f'<td style="width: 80%; height: 10px;"><table style="border-collapse: collapse; width: 100%;"><tbody><tr>' \
                                          f'<td style="width: 100%; height: 17px;"><strong><span style="color: #AD5F00;">{MemberNick}</span> </strong><span style="color: #994F00;"> {Member}</span><span style="color: #824500;"> {MessageSentAt}</span></td>' \
                                          f'</tr><tr><td style="width: 100%;"><table style="width: 90%; border-collapse: collapse; float: left;" cellpadding="10">' \
                                          f'<tbody><tr><td style="width: 90%;"><span style="color: #FFDEC2;">{Message.content}</span></td></tr></tbody></table></td></tr></tbody></table></td></tr></tbody></table>'


    returnstring = returnstring + '</body>'
    return returnstring












async def CheckIfTicketShouldBeOpened(bot, payload):
    TicketShouldpen = False
    # Check if the channel where a user reacted in is a ticketopening channel
    channel = await bot.fetch_channel(payload.channel_id)
    if '𝖲upport' in str(channel):
        # Check if the reaction type is correct
        if str(payload.emoji.name) in ['📥', '📋', '🗣️', '✍️']:
            if payload.user_id != 789942343619969074:
                TicketShouldpen = True







        if TicketShouldpen == True:
            ReactedOnMessage = await channel.fetch_message(payload.message_id)
            # Check if the TicketOpening message was sent by the bot itelf.
            if ReactedOnMessage.author.id == 789942343619969074:
                # remove the reaction
                await ReactedOnMessage.remove_reaction(payload.emoji, payload.member)

                # Check if user already has a ticket open
                if os.path.exists(f'./Logs/{payload.guild_id}/TicketOpen_{payload.user_id}'):
                    # print('TicketAlreadyOpen')
                    return
                else:
                    # print('No Ticket Open')
                    with open(f'./Logs/{payload.guild_id}/TicketOpen_{payload.user_id}', 'w') as file:
                        pass

                    async def WaitThenDeleteFile():
                        await asyncio.sleep(60)
                        os.remove(f'./Logs/{payload.guild_id}/TicketOpen_{payload.user_id}')

                    try:
                        bot.loop.create_task(WaitThenDeleteFile())
                    except TypeError:
                        pass


                # open the ticket
                await ProcessTicketOpening(payload.member, channel.guild, bot, str(payload.emoji.name))



async def ProcessTicketOpening(MemberOpenedTicket: discord.Member, guild, bot, reaction):
    # check if a ticket was ever opened on this guild. and if not create the file

    TicketNumFilePath = f'./Logs/{guild.id}/TicketNum'
    if os.path.exists(TicketNumFilePath) == False:
        with open(TicketNumFilePath, 'w') as File:
            print(f'Writing to {TicketNumFilePath}')
            File.write('0')
            pass
    # read from the last ticket opened file
    TicketNumber = 0000
    with open(TicketNumFilePath, 'r') as File:
        #print(f'{TicketNumFilePath} Exists!')
        TicketNumber = int(File.read()) + 1

    #write to file the new latest ticket number
    with open(TicketNumFilePath, 'w') as File:
        File.write(str(TicketNumber))


    #open ticket task
    await OpenTicket(bot, MemberOpenedTicket, TicketNumber, guild, reaction)

def GetTicketTypeFromReaction(reaction = 'X'):
    if reaction == '📥':
        return "Role Request"
    elif reaction == '📋':
        return "General question"
    elif reaction == '✍️':
        return "Nickname Change"
    elif reaction == '🗣️':
        return "Report"
    return reaction


async def OpenTicket(bot, MemberOpenedTicket: discord.Member, TicketNumber, guild: discord.guild, reaction):
    TicketType = GetTicketTypeFromReaction(reaction)
    # Init the ticket number to be used inside internal defs
    OpenTicket.TicketNum = TicketNumber

    print(f'  > {datetime.datetime.now()} >Adding to record that {MemberOpenedTicket} Opened Ticket-{OpenTicket.TicketNum}')

    #get the "help" category of this server
    for Category in guild.categories:
        if 'HELP REQUEST' in str(Category).upper():
            HelpCategory = Category



    # make sure everyone cannot see the ticket
    for role in guild.roles:
        if 'everyone' in role.name:
            EveryoneRole = role

    # Create a new ticket channel
    overwrites = {
        EveryoneRole: discord.PermissionOverwrite(view_channel=False, read_messages=False, send_messages=False, attach_files=False)
    }
    TicketChannel = await guild.create_text_channel(overwrites=overwrites, name=f'Ticket-{TicketNumber}', category=HelpCategory, position=len(HelpCategory.channels) + 100, reason=f'Opening Ticket Number {TicketNumber}')

    # Add permissions for all the staff roles
    namesOfRolesAllowedToSeeTickets = ['Helper', 'Staff Manager', 'Programming Manager', 'MVP', '𝐇𝐢𝐠𝐡 𝐒𝐭𝐚𝐟𝐟']
    RolesAllowedToSeeTickets = []
    EveryoneRole = None
    for role in guild.roles:
        for name in namesOfRolesAllowedToSeeTickets:
            if name in str(role):
                RolesAllowedToSeeTickets.append(role)

    for role in RolesAllowedToSeeTickets:
        await TicketChannel.set_permissions(role, view_channel=True, read_messages=True, send_messages=True, embed_links=True, attach_files=True, add_reactions=True, use_external_emojis=True, read_message_history=True, reason=f'Allow Staff to see Ticket {TicketNumber}')

    # Say what kind of ticket this is
    await TicketChannel.send(embed=discord.Embed(title=f"{TicketType}", description=f"By: {MemberOpenedTicket}\n<@{MemberOpenedTicket.id}>", color=0x2B2B2B))

    # Allow Ticket opening member to see the ticket
    await TicketChannel.set_permissions(MemberOpenedTicket, view_channel=True, attach_files=True, read_messages=True, send_messages=True, reason=f'Allow Ticket Opener to see{TicketNumber}')

    #Init the First actors of the ticket.
    OpenTicket.FirstHelperToLockTicket = None
    OpenTicket.FirstHelperToDeleteTicket = None

    #get Ticket-Log Channel and ticket help channel
    LogChannel: discord.channel
    TicketHelpChannel: discord.channel
    for channel in TicketChannel.guild.channels:
        if 'ticket-log' in channel.name:
            LogChannel = channel
        elif '𝖧elp-𝖶ith-𝖳icket' in channel.name:
            TicketHelpChannel = channel

    await LogChannel.send(embed=discord.Embed(title=f'Opened Ticket-{TicketNumber}', description=f"<@{MemberOpenedTicket.id}> {MemberOpenedTicket}", color=0x1EC45C))


    # Say what kind of ticket this is
    #await TicketHelpChannel.send(embed=discord.Embed(title=f'Opened Ticket-{TicketNumber}', description=f"<@{MemberOpenedTicket.id}> {MemberOpenedTicket}", color=0x1EC45C))



    #Create Embeded Messages for ticket

    OpeningMessageTextTemplate = discord.Embed(title=f"Ticket Number {TicketNumber}", description="צוות תמיכה יגיע בהקדם האפשרי על מנת לעזור :hearts:\n כדי לסגור את הטיקט תלחץ על ה:lock:", color=0x1EC45C)
    LockedMessageTextTemplate = discord.Embed(title="Locked Ticked", description=":page_with_curl: שמירת היסטוריית הצאט \n:unlock: לפתוח מחדש את הטיקט \n:no_entry: למחוק את הטיקט לצמיתות", color=0xD32F2F)
    def CustomMessage(DescriptionText = 'NoText', Color = 0x00ff00):
        return discord.Embed(title="", description=DescriptionText, color=Color)

    OpeningMessage = None
    LockedMessage = None






    async def ProcessTicketStarting():
        # Create Check For Reaction Type
        def checkIfLocked(reaction, user):
            if str(reaction.emoji) == '🔒':
                if reaction.message.id == OpeningMessage.id:
                    return OpeningMessage.author and reaction


        # Check if user clicked the lock reaction
        try:
            # print('Waiting For a reaction...')
            await OpeningMessage.add_reaction('🔒')

            #     and make sure the bot isnt reacting to itself out of desync
            LockerID = 789942343619969074
            while LockerID == 789942343619969074:
                reaction, user = await bot.wait_for('reaction_add', check=checkIfLocked)
                LockerID = user.id
        except asyncio.TimeoutError:
            print('Timed out with no correct reaction!')
            pass
        else:
            # Record the first staff who locked the ticket in EleAuditLog
            if OpenTicket.FirstHelperToLockTicket == None:
                if EleDiscordLib.IsMemberARole(user, ['𝐒𝐭𝐚𝐟𝐟']):
                    OpenTicket.FirstHelperToLockTicket = user
                    EleAuditLog.AddEntryToEleAuditLogCache([reaction.message.channel.guild.id, [EleDiscordLib.GetCurrentDateAndHourMinute(), user.id, 'LockedTicket', 'Ticket-' + str(OpenTicket.TicketNum), TicketType, None]])
                    print(f'  > {datetime.datetime.now()} >Adding to record that {MemberOpenedTicket} Locked Ticket-{OpenTicket.TicketNum}')

            # Lock the ticket
            if EleDiscordLib.IsMemberARole(MemberOpenedTicket, ['Staff Manager', 'MVP', '𝐇𝐢𝐠𝐡 𝐒𝐭𝐚𝐟𝐟']) == False:
                await TicketChannel.set_permissions(MemberOpenedTicket, view_channel=True, read_messages=False, send_messages=False,reason=f'Add Permission to handle ticket {TicketNumber}')


            await OpeningMessage.remove_reaction(reaction, user)
            await ProcessTicketFinishing(user)


    async def ProcessTicketFinishing(LockedUser):
        # Process when the user locked the message
        await TicketChannel.send(embed=CustomMessage(f'Ticket-{TicketNumber}  Locked By <@{LockedUser.id}>\nTheir ID:{LockedUser.id}', 0xFBFE32))
        await LogChannel.send(embed=discord.Embed(title=f'Locked Ticket-{TicketNumber}', description=f"<@{LockedUser.id}> {LockedUser}\nTheir ID:{LockedUser.id}", color=0xFBFE32))
        LockedMessage = await TicketChannel.send(embed=LockedMessageTextTemplate)

        async def TicketCloseWaitForReaction():
            # Create Check For Reaction Type
            def checkIfSaveReopenOrDeleted(reaction, user):
                if str(reaction.emoji) in ['🔓', '📑', '⛔']:
                    if reaction.message.id == LockedMessage.id:
                        return LockedMessage.author and reaction
                        # else:
                        #     print(f'Ticket Unlocker ID is{LockedMessage.author.id} of ({LockedMessage.author})')
                # else:
                #     print(f"{reaction.emoji} is not in {['🔓', '📑', '⛔']}")

            # Check if ticket should be Saved, unlocked, or deleted.
            try:
                # print('Waiting For a reaction...')

                # Add 3 reactions
                await LockedMessage.add_reaction('🔓')
                await LockedMessage.add_reaction('📑')
                await LockedMessage.add_reaction('⛔')

                # wait for the ['🔓', '📑', '⛔'] reaction.
                #     and make sure the bot isnt reacting to itself out of desync
                userId = 789942343619969074
                while userId == 789942343619969074:
                    reaction, user = await bot.wait_for('reaction_add', check=checkIfSaveReopenOrDeleted)
                    userId = user.id

            except asyncio.TimeoutError:
                print('Timed out with no correct reaction!')
            else:
                # print(f'{user} clicked {reaction}')
                # remove reacted reaction
                await LockedMessage.remove_reaction(reaction, user)

                # Act based on what reaction a user reacted with
                if str(reaction) == '🔓':
                    # Record the staff who Unlocked the ticket in EleAuditLog
                    if EleDiscordLib.IsMemberARole(user, ['𝐒𝐭𝐚𝐟𝐟']):
                        EleAuditLog.AddEntryToEleAuditLogCache([reaction.message.channel.guild.id,[EleDiscordLib.GetCurrentDateAndHourMinute(), user.id, 'UnlockedTicket', 'Ticket-' + str(OpenTicket.TicketNum), TicketType, None]])
                        print(f'  > {datetime.datetime.now()} >Adding to record that {MemberOpenedTicket} Unlock Ticket-{OpenTicket.TicketNum}')

                    # if the ticket was unlocked. delete locked message. say it was unlocked. and restart-ticket process
                    #print('Ticket Unlocked')
                    #Unlock the ticket
                    await LogChannel.send(embed=discord.Embed(title=f'Unlocked Ticket-{TicketNumber}', description=f"<@{user.id}> {user}\nTheir ID:{user.id}", color=0x1EC45C))
                    await TicketChannel.set_permissions(MemberOpenedTicket, view_channel=True, read_messages=True, send_messages=True, reason=f'Add Permission to handle ticket {TicketNumber}')
                    await LockedMessage.delete()
                    await TicketChannel.send(embed=CustomMessage(f'Ticket-{TicketNumber}  Unlocked By <@{user.id}>', 0x1EC45C))
                    await ProcessTicketStarting()

                elif str(reaction) == '📑':
                    # Record the staff who Saved the ticket in EleAuditLog
                    if EleDiscordLib.IsMemberARole(user, ['𝐒𝐭𝐚𝐟𝐟']):
                        EleAuditLog.AddEntryToEleAuditLogCache([reaction.message.channel.guild.id, [EleDiscordLib.GetCurrentDateAndHourMinute(), user.id, 'SavedTicket', 'Ticket-' + str(OpenTicket.TicketNum), TicketType, None]])
                        print(f'  > {datetime.datetime.now()} >Adding to record that {MemberOpenedTicket} Saved Ticket-{OpenTicket.TicketNum}')
                    #print('Ticket Saved')
                    await LogChannel.send( embed=discord.Embed(title=f'Saved Ticket-{TicketNumber}', description=f"<@{user.id}> {user}\nTheir ID:{user.id}", color=0x0955B1))

                    # if the ticket was saved. create html transcript. send it in the ticket and in ticket log. then delete the file and  restart-ticket locking process.
                    HtmlCodeOfChannel = await GetChannelAsHtmlString(TicketChannel)
                    with open(f'transcript-Ticket-{TicketNumber}.html', 'w', encoding='utf-8') as TranscriptFile:
                        TranscriptFile.write(HtmlCodeOfChannel)
                    TanscriptFile = open(f'transcript-Ticket-{TicketNumber}.html', 'r', encoding='utf-8')
                    await TicketChannel.send(file=discord.File(TanscriptFile))
                    await LogChannel.send(file=discord.File(TanscriptFile))
                    TanscriptFile.close()
                    os.remove(f'transcript-Ticket-{TicketNumber}.html')

                    await TicketCloseWaitForReaction()

                elif str(reaction) == '⛔':
                    # Record the first staff who deleted the ticket in EleAuditLog
                    if OpenTicket.FirstHelperToDeleteTicket == None:
                        if EleDiscordLib.IsMemberARole(user, ['𝐒𝐭𝐚𝐟𝐟']):
                            OpenTicket.FirstHelperToDeleteTicket = user
                            EleAuditLog.AddEntryToEleAuditLogCache([reaction.message.channel.guild.id, [EleDiscordLib.GetCurrentDateAndHourMinute(), user.id, 'DeletedTicket', 'Ticket-' + str(OpenTicket.TicketNum), TicketType, None]])
                            print(f'  > {datetime.datetime.now()} >Adding to record that {MemberOpenedTicket} Deleted Ticket-{OpenTicket.TicketNum}')

                    # if the ticket was deleted. say who deleted it and delete it in 10 seconds.
                    await LogChannel.send(embed=discord.Embed(title=f'Deleted Ticket-{TicketNumber}', description=f"<@{user.id}> {user}\nTheir ID:{user.id}", color=0xD32F2F))
                    BeingDeletedMessage = await TicketChannel.send(embed=CustomMessage(f'Ticket-{TicketNumber} Deleted By <@{user.id}>.\nwill be gone in 5 seconds...', 0xD32F2F))
                    for x in range(5):
                        await BeingDeletedMessage.edit(embed=CustomMessage(f'Ticket-{TicketNumber} Deleted By <@{user.id}>.\nwill be gone in {5 - x} seconds...', 0xD32F2F))
                        await asyncio.sleep(1)


                    await TicketChannel.delete()
                    #print('Ticket Deleted')

        await TicketCloseWaitForReaction()



    #Tag the ticket opening member in the ticket
    GhostTag = await TicketChannel.send(f'<@{MemberOpenedTicket.id}>')
    await GhostTag.delete()

    # Create Ticket Opening Message
    OpeningMessage = await TicketChannel.send(embed=OpeningMessageTextTemplate)
    await OpeningMessage.add_reaction('🔒')
    await ProcessTicketStarting()









async def CatchTicketForFirstHelper(message):
    if 'ticket-' in message.channel.name:
        TicketChannel = message.channel

        # if ticket responder is a helper
        if EleDiscordLib.IsMemberARole(message.author, ['Helper']):

            # For each role in the channel permissions
            for RoleOrUser in TicketChannel.overwrites:

                # if the role is helper
                if 'Helper' in str(RoleOrUser.name):
                    PermSet = TicketChannel.overwrites_for(RoleOrUser)

                    # for perm type in channel perms
                    for Perm in PermSet:

                        # if helper is allowed to send messages
                        if Perm[0] == 'send_messages':
                            if Perm[1] == True:
                                print(f'{RoleOrUser} CAN {Perm[0]} on {TicketChannel}!')

                                # allow first responder to send messages and deny helper role from sending message.
                                await TicketChannel.set_permissions(message.author, send_messages=True,
                                                                    add_reactions=True, attach_files=True,
                                                                    reason=f'Add Permission to handle {TicketChannel}')
                                await TicketChannel.set_permissions(RoleOrUser, send_messages=False,
                                                                    add_reactions=False, view_channel=True,
                                                                    reason=f'Add Permission to handle {TicketChannel}')
                                # Pevent non-helpers from writing in the ticket:
                                for Member in message.guild.members:
                                    if EleDiscordLib.IsMemberARole(Member, [
                                        'Programming Manager']) and EleDiscordLib.IsMemberARole(Member, ['helper']):
                                        await TicketChannel.set_permissions(Member, view_channel=True, send_messages=False, reason=f'Add Permission to handle {message.channel}')
