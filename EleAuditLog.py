import datetime
import os
import sqlite3
import EleDiscordLib
import EleVoiceTimeTracking
import discord
import pandas
from discord.ext import commands
import datetime
from datetime import date, timedelta


AuditCache = []
CurrentCacheAuditLogIds = [[], [], []]
AuditLogUpdateFirstRun = True


########################################################################################
########## General Functions ###########################################################
########################################################################################

async def SaveEleAuditLogCacheIntoDb(bot):
    global AuditCache
    print('----- A Minute has Passed! Updating, Saving, and Switching databases..\n')

    #make sure there is a databse file that you can write into for that day
    for CurrentGuild in bot.guilds:
        DatabaseFilePath = f'./Logs/' + str(CurrentGuild.id)
        try:
            os.makedirs(DatabaseFilePath)
        except:
            pass
        TryToCreateSQLEntryWithFile(DatabaseFilePath + f'/{datetime.date.today().strftime("%Y-%m-%d")} database.db')

    #write all data to all databases
    SaveCachedData(bot, AuditCache)

    #clear cache
    AuditCache = []




########################################################################################
######################## Trackers ######################################################
########################################################################################

# Handle tempmute infractions and warns in EleAuditLog
async def HandleTempmuteWarnInfractionsInEleAuditLog(bot, message):
    if message.content.startswith('!tempmute') or message.content.startswith('!warn') or message.content.startswith('!infractions') or message.content.startswith('-+Audit'):

        ListOfWordsInCommand = message.content.split()
        remainingWords = ''

        # '''CREATE TABLE EleAuditLog(datetime text, UserID int, ActionType text, Target text, content text, extra text)''')
        # ('2011-11-01 18:21:57', '134156783450062848', 'Mute', 424150309858705420, 'None', 'None'),

        if await EleDiscordLib.isCommandAllowedOnChannel(ListOfWordsInCommand[0], message.channel):
            if message.content.startswith('!tempmute'):
                if len(ListOfWordsInCommand) > 2:
                    Action = ListOfWordsInCommand[0][1:]
                    TargetUser = EleDiscordLib.getUserFromUserIDString(bot, ListOfWordsInCommand[1])
                    if len(ListOfWordsInCommand) > 3:
                        for X in range(len(ListOfWordsInCommand)):
                            if X >= 3:
                                remainingWords = remainingWords + ListOfWordsInCommand[X] + ' '
                    print(f'  > {datetime.datetime.now()} >Adding to record that {message.author} {Action} {TargetUser} for {ListOfWordsInCommand[2]} because: "{remainingWords}"')
                    AddEntryToEleAuditLogCache([message.channel.guild.id, [EleDiscordLib.GetCurrentDateAndHourMinute(), message.author.id, Action, TargetUser.id, message.content, 'TIME:' + ListOfWordsInCommand[2] + ' REASON:' + remainingWords]])

            elif message.content.startswith('!warn'):
                if len(ListOfWordsInCommand) > 1:
                    Action = ListOfWordsInCommand[0][1:]
                    TargetUser = EleDiscordLib.getUserFromUserIDString(bot, ListOfWordsInCommand[1])
                    if len(ListOfWordsInCommand) > 2:
                        for X in range(len(ListOfWordsInCommand)):
                            if X >= 2:
                                remainingWords = remainingWords + ListOfWordsInCommand[X] + ' '
                    print(f'  > {datetime.datetime.now()} >Adding to record that {message.author} {Action} {TargetUser} because: "{remainingWords}"')
                    AddEntryToEleAuditLogCache([message.channel.guild.id, [EleDiscordLib.GetCurrentDateAndHourMinute(), message.author.id, Action, TargetUser.id, message.content, 'REASON:' + remainingWords]])

            elif message.content.startswith('!infractions'):
                if len(ListOfWordsInCommand) > 1:
                    Action = ListOfWordsInCommand[0][1:]
                    TargetUser = EleDiscordLib.getUserFromUserIDString(bot, ListOfWordsInCommand[1])
                    print(f"  > {datetime.datetime.now()} >Adding to record that {message.author.id} checked {TargetUser.id}'s {Action}")
                    AddEntryToEleAuditLogCache([message.channel.guild.id, [EleDiscordLib.GetCurrentDateAndHourMinute(), message.author.id, Action, TargetUser.id, message.content, None]])

# Handle Tupal and Avar in EleAuditLog
async def HandleTupalAvarInEleAuditLog(message):
    try:
        if 'בקשה' in str(message.channel.name):
            if 'טופל' in str(message.content):
                print(
                    f'  > {datetime.datetime.now()} >Adding to record that {message.author} responded to a AskForHelp_Tupal request.')
                AddEntryToEleAuditLogCache([message.channel.guild.id, [EleDiscordLib.GetCurrentDateAndHourMinute(), message.author.id, 'AskForHelp_Tupal', None, message.content, None]])

    except:
        pass
    try:
        if 'עברו' in str(message.channel.name):
            if 'עבר' in str(message.content):
                ListOfWordsInMessage = message.content.split()
                UserID = ''
                for Char in ListOfWordsInMessage[0]:
                    if Char.isnumeric() == True:
                        UserID = UserID + Char

                print(
                    f'  > {datetime.datetime.now()} >Adding to record that {message.author.id} Passed {UserID} in {message.channel.name}.')
                # print(f'Trying to add: {str([message.channel.guild.id, [EleDiscordLib.GetCurrentDateAndHourMinute(), message.author.id, "Passed16_18Plus", UserID, message.content, message.channel.name]])}')
                AddEntryToEleAuditLogCache([message.channel.guild.id, [EleDiscordLib.GetCurrentDateAndHourMinute(), message.author.id, "Passed16_18Plus", UserID, message.content, message.channel.name]])

    except:
        pass


########################################################################################
########## Ineractions with AuditCache #################################################
########################################################################################

def AddEntryToEleAuditLogCache(Entry):
    #print('Heeeyaaa')
    global AuditCache
    AuditCache.append(Entry)

    #print(f'  ► {datetime.datetime.now()} ►DEBUG: {Entry}')
    
def GetEleAuditLogCache():
    global AuditCache
    return AuditCache




def GetCurrentCacheAuditLogIds():
    global CurrentCacheAuditLogIds
    return CurrentCacheAuditLogIds










########################################################################################
########## Save Database ###############################################################
########################################################################################


def SaveCachedData(bot, DataToSave):
    for GUILD in bot.guilds:
        GuildEntryArray = []

        #print('GUILD =', GUILD)
        for Entry in DataToSave:
            #print('Entry =', Entry[0])
            if Entry[0] == GUILD.id:
                GuildEntryArray.append(Entry[1])
        SaveEntryArraysIntoDatabase(f'./Logs/{GUILD.id}/{datetime.date.today().strftime("%Y-%m-%d")} database.db', GuildEntryArray)

def SaveEntryArraysIntoDatabase(FileToSaveInto, DataToSave):

    print(f'  > {datetime.datetime.now()} >SQL Inserted Data into:{FileToSaveInto}')
    Connection = sqlite3.connect(FileToSaveInto)
    Cursor = Connection.cursor()

    Cursor.executemany('INSERT INTO EleAuditLog VALUES (?,?,?,?,?,?)', DataToSave)
    Connection.commit()
    Connection.close()

def TryToCreateSQLEntryWithFile(Name):
    Connection = sqlite3.connect(Name)
    Cursor = Connection.cursor()
    try:
        # Try to Create table
        Cursor.execute('''CREATE TABLE EleAuditLog(datetime text, UserID int, ActionType text, Target text, content text, extra text)''')
        print(f'>EleSQLFunctions: Created new database, {Name}.')
    except:
        #print(f'>EleSQLFunctions: Failed to create new database, likely "{Name}" already exists.')
        pass
    Connection.commit()
    Connection.close()






########################################################################################
########## GetDatabase #################################################################
########################################################################################
async def CheckLast50AuditLogs_Of_All_Guilds(bot):
    GuildNumber = 0
    for Guild in bot.guilds:
        #print(f'Checking Last 50 Audit Logs for {Guild}...')
        await CheckLast50AuditLogs_Of_One_Guild(bot, Guild, GuildNumber)
        GuildNumber = GuildNumber + 1
    global AuditLogUpdateFirstRun
    AuditLogUpdateFirstRun = False

async def CheckLast50AuditLogs_Of_One_Guild(bot, CurrentGuild, GuildNumber):
    global CurrentCacheAuditLogIds
    #print(f'CurrentCacheAuditLogIds = {CurrentCacheAuditLogIds}')
    try:
        Old_Entry_Ids = CurrentCacheAuditLogIds[GuildNumber]
        CurrentCacheAuditLogIds[GuildNumber] = []
        #print('-----------------------------------------------------------------NoError')
    except:
        Old_Entry_Ids = []
        #print('-----------------------------------------------------------------YesError')
    #print(f'Old_Entry_Ids = {Old_Entry_Ids}')
    #print(f'print{CurrentGuild.name} with guild number {GuildNumber}')
    EntryIds = []
    NewEntriesInGuild = []
    async for Entry in CurrentGuild.audit_logs(limit=50):
        EntryIds.append(Entry.id)
        if Entry.id in Old_Entry_Ids:
            #print(f'> {Entry.id} Found in old list {Old_Entry_Ids}')
            pass
        else:
            #print(f'> {Entry.id} NOT Found in old list {Old_Entry_Ids}')
            if AuditLogUpdateFirstRun == False:
                NewEntriesInGuild.append(Entry)
    try:
        CurrentCacheAuditLogIds[GuildNumber] = EntryIds
        #print('\n>>>Success Adding Ids to CurrentCacheAuditLogIds!!')
    except:
        #print('\n>>>Failed Adding Ids to CurrentCacheAuditLogIds!!')
        pass
    if len(NewEntriesInGuild) != 0:
        #print(f'New Audit Logs in {CurrentGuild}:')
        for Entry in NewEntriesInGuild:
            #print(f'Entry: {Entry.action} by: {Entry.user}')
            AddnewAuditLogToDB(bot, CurrentGuild, Entry)


def AddnewAuditLogToDB(bot, Guild, Entry):
    # '''CREATE TABLE EleAuditLog(datetime text, UserID int, ActionType text, Target text, content text, extra text)''')
    # ('2011-11-01 18:21:57', '134156783450062848', 'Mute', 424150309858705420, 'None', 'None'),

    if Entry.user.bot == False:

        if str(Entry.action) == 'AuditLogAction.ban' or str(Entry.action) == 'AuditLogAction.kick':
            print(
                f'  > {datetime.datetime.now()} >Adding to record that {Entry.user} {Entry.action[0]} with id {str(Entry.target)}')
            # print(f'Trying to add: {str([Guild.id, [EleDiscordLib.GetCurrentDateAndHourMinute(), Entry.user.id, Entry.action[0], Entry.target.id, None, None]])}')
            AddEntryToEleAuditLogCache([Guild.id,
                                                    [EleDiscordLib.GetCurrentDateAndHourMinute(), Entry.user.id,
                                                     Entry.action[0], Entry.target.id, None, None]])



        elif str(Entry.action) == 'AuditLogAction.invite_create':
            print(
                f'  > {datetime.datetime.now()} >Adding to record that {Entry.user} {Entry.action[0]} with id {str(Entry.target)}')
            # print(f'Trying to add: {str([Guild.id, [EleDiscordLib.GetCurrentDateAndHourMinute(), Entry.user.id, Entry.action[0], str("Invite ID:" + str(Entry.target)), None, None]])}')
            AddEntryToEleAuditLogCache([Guild.id,
                                                    [EleDiscordLib.GetCurrentDateAndHourMinute(), Entry.user.id,
                                                     Entry.action[0], str("Invite ID:" + str(Entry.target)), None,
                                                     None]])

        elif str(Entry.action) == 'AuditLogAction.member_disconnect':
            print(f'  > {datetime.datetime.now()} >Adding to record that {Entry.user} {Entry.action[0]} A user.')
            # print(f'Trying to add: {str([Guild.id, [EleDiscordLib.GetCurrentDateAndHourMinute(), Entry.user.id, Entry.action[0], None, None, None]])}')
            AddEntryToEleAuditLogCache([Guild.id,
                                                    [EleDiscordLib.GetCurrentDateAndHourMinute(), Entry.user.id,
                                                     Entry.action[0], None, None, None]])

        elif str(Entry.action) == 'AuditLogAction.member_move':
            print(
                f'  > {datetime.datetime.now()} >Adding to record that {Entry.user} {Entry.action[0]} a user to {Entry.extra.channel}.')
            AddEntryToEleAuditLogCache([Guild.id,
                                                    [EleDiscordLib.GetCurrentDateAndHourMinute(), Entry.user.id,
                                                     Entry.action[0], None, None, f'{Entry.extra.channel}']])

        elif str(Entry.action) == 'AuditLogAction.message_delete':
            print(
                f'  > {datetime.datetime.now()} >Adding to record that {Entry.user} {Entry.action[0]} Of {Entry.target}.')
            # print(f'Trying to add: {str([Guild.id, [EleDiscordLib.GetCurrentDateAndHourMinute(), Entry.user.id, Entry.action[0], Entry.target.id, None, None]])}')
            AddEntryToEleAuditLogCache([Guild.id,
                                                    [EleDiscordLib.GetCurrentDateAndHourMinute(), Entry.user.id,
                                                     Entry.action[0], Entry.target.id, None, None]])

        elif str(Entry.action) == 'AuditLogAction.member_update':
            Member_Update_Type_Found = False
            ActualAction = 'Unknown'
            Content = 'None'
            try:
                # Check for voice MUTE
                # Member muted by server mute
                if (Entry.before.mute is False) and (Entry.after.mute is True):
                    ActualAction = 'ServerMuted'

                # Member unmuted by server mute
                elif (Entry.before.mute is True) and (Entry.after.mute is False):
                    ActualAction = 'ServerUnmuted'

                Content = 'Voice State Update'
                Member_Update_Type_Found = True
            except:
                pass

            try:
                # Check for voice DEAD
                # Member deafen by server mute
                if (Entry.before.deaf is False) and (Entry.after.deaf is True):
                    ActualAction = 'ServerDeafen'

                # Member undeafen by server mute
                elif (Entry.before.deaf is True) and (Entry.after.deaf is False):
                    ActualAction = 'ServerUndeafen'
                Content = 'Voice State Update'
                Member_Update_Type_Found = True
            except:
                pass

            try:
                # Check for nickname change
                Content = f'From {Entry.before.nick} To:{Entry.after.nick}'
                ActualAction = 'Nickname_Change'
                Member_Update_Type_Found = True
            except:
                pass

            if Member_Update_Type_Found == False:
                print('     #####################################################################################################')
                print(f'     ################## Unknown Member Update of types (Before: {Entry.before} and After:{Entry.after})')
                print('     #####################################################################################################')

            print(f'  > {datetime.datetime.now()} >Adding to record that {Entry.user} {ActualAction} {Entry.target}.')
            # print(f'Trying to add: {str([Guild.id, [EleDiscordLib.GetCurrentDateAndHourMinute(), Entry.user.id, ActualAction, Entry.target.id, Content, None]])}')
            AddEntryToEleAuditLogCache([Guild.id,
                                                    [EleDiscordLib.GetCurrentDateAndHourMinute(), Entry.user.id,
                                                     ActualAction, Entry.target.id, Content, None]])


        elif str(Entry.action) == 'AuditLogAction.member_role_update':
            AddOrRemove = ''
            Roles = []
            if Entry.before.roles == []:
                AddOrRemove = 'AddedRole'
                for role in Entry.after.roles:
                    Roles.append(str(role.name))
            elif Entry.after.roles == []:
                AddOrRemove = 'RemovedRole'
                for role in Entry.before.roles:
                    Roles.append(str(role.name))
            print(
                f'  > {datetime.datetime.now()} >Adding to record that {Entry.user} {AddOrRemove} {Roles} For {Entry.target}.')
            # print(f'Trying to add: {str([Guild.id, [EleDiscordLib.GetCurrentDateAndHourMinute(), Entry.user.id, AddOrRemove, Entry.target.id, f"{AddOrRemove} {Roles}", None]])}')
            AddEntryToEleAuditLogCache([Guild.id,
                                                    [EleDiscordLib.GetCurrentDateAndHourMinute(), Entry.user.id,
                                                     AddOrRemove, Entry.target.id, f"{AddOrRemove} {Roles}", None]])



        elif str(Entry.action) == 'AuditLogAction.channel_update':
            print(
                f'  > {datetime.datetime.now()} >Adding to record that {Entry.user} {Entry.action} For {Entry.target}. with Changes: From:{Entry.before}  To:{Entry.after}')
            # print(f'Trying to add: {str([Guild.id, [EleDiscordLib.GetCurrentDateAndHourMinute(), Entry.user.id, "Channel_Update", Entry.target.id, f"From:{Entry.before}  To::{Entry.after}", None]])}')
            AddEntryToEleAuditLogCache([Guild.id,
                                                    [EleDiscordLib.GetCurrentDateAndHourMinute(), Entry.user.id,
                                                     "Channel_Update", Entry.target.id,
                                                     f"From:{Entry.before}  To:{Entry.after}", None]])


        elif str(Entry.action) == 'AuditLogAction.overwrite_create':
            try:
                TARGETNAME = discord.utils.get(Guild.roles, id=Entry.after.id)
            except:
                TARGETNAME = bot.get_user(Entry.after.id)
            print(
                f'  > {datetime.datetime.now()} >Adding to record that {Entry.user} {Entry.action} For {Entry.target}. for PermID({Entry.after}) being {TARGETNAME}')
            # print(f'Trying to add: {str([Guild.id, [EleDiscordLib.GetCurrentDateAndHourMinute(), Entry.user.id, "CreatedPermOverwrite", Entry.target.id, f"To:{Entry.after.id}", None]])}')
            AddEntryToEleAuditLogCache([Guild.id,
                                                    [EleDiscordLib.GetCurrentDateAndHourMinute(), Entry.user.id,
                                                     "CreatedPermOverwrite", Entry.target.id, f"To:{Entry.after.id}",
                                                     None]])


        elif str(Entry.action) == 'AuditLogAction.overwrite_delete':
            try:
                TARGETNAME = discord.utils.get(Guild.roles, id=Entry.before.id)
            except:
                TARGETNAME = bot.get_user(Entry.before.id)
            print(
                f'  > {datetime.datetime.now()} >Adding to record that {Entry.user} {Entry.action} For {Entry.target}. for PermID({Entry.before}) being {TARGETNAME}')
            # print(f'Trying to add: {str([Guild.id, [EleDiscordLib.GetCurrentDateAndHourMinute(), Entry.user.id, "DeletePermOverwrite", Entry.before.id, f"To:{Entry.before.id}", None]])}')
            AddEntryToEleAuditLogCache([Guild.id,
                                                    [EleDiscordLib.GetCurrentDateAndHourMinute(), Entry.user.id,
                                                     "DeletePermOverwrite", Entry.before.id, f"To:{Entry.before.id}",
                                                     None]])


        elif str(Entry.action) == 'AuditLogAction.overwrite_update':
            print(
                f'  > {datetime.datetime.now()} >Adding to record that {Entry.user} {Entry.action} For {Entry.target}. before: {Entry.before} after:{Entry.after})')
            # print(f'Trying to add: {str([Guild.id, [EleDiscordLib.GetCurrentDateAndHourMinute(), Entry.user.id, "UpdatePermOverwrite", Entry.target.id, f" From: {Entry.before} To:{Entry.after}", None]])}')
            AddEntryToEleAuditLogCache([Guild.id,
                                                    [EleDiscordLib.GetCurrentDateAndHourMinute(), Entry.user.id,
                                                     "UpdatePermOverwrite", Entry.target.id,
                                                     f" From: {Entry.before} To:{Entry.after}", None]])



        elif str(Entry.action) in ['AuditLogAction.channel_create', 'AuditLogAction.channel_delete']:
            pass  # Ignored



        else:
            print('     ####################################################################################################################################')
            print(f'     ##### Passed in un-accounted for entry type!\n     ##### Did: {Entry.action}\n     ##### by: {Entry.user}\n     ##### Entry: {Entry}')
            print('     ####################################################################################################################################')
            pass

    pass











########################################################################################
########## Generate Audit ##############################################################
########################################################################################





async def Auditinguser(ctx, AuditMember : discord.Member, FromDate, ToDate, PermLevel='Member', bot = commands.Bot(command_prefix='-+')):
    AuditRequestMessage = ctx.message
    AuditRequestChannel = ctx.message.channel
    AuditRequestGuild = ctx.message.channel.guild
    AuditRequester = ctx.message.author
    # ==== # ==== # ==== # ==== # ==== # ==== # ==== # ==== # ==== # ==== #
    # COMMAND CHECKS




    # ==== # ==== # ==== # ==== # ==== # ==== # ==== # ==== # ==== # ==== #
    ### -------- MEMBER STATS VARIABLES ------- ###
    # TICKETS
    TicketsLocked = 0
    TicketsUnlocked = 0
    TicketsSaved = 0
    TicketsDeleted = 0
    EstimatedTicketsHandled = 0
    InvitesCreated = 0
    # ASKFORHELP
    AskForHelp_Tupal = 0
    # COMMANDS
    TempmuteGiven = 0
    WarnGiven = 0
    usedInfractions = 0
    UsedAudit = 0
    # VOICE
    VoiceActiveHours = 0
    # MANUAL ACTIONS
    Manual_MuteUnmute = [0, 0]
    Manual_DeafenUnDeafen = [0, 0]
    Manual_Nickname = 0
    Manual_Disconnect = 0
    Manual_MemberMoveToInvestRoom = 0
    Manual_MemberMoves = 0
    # MESSAGES
    MessagesDeleted = 0
    MessagesSent = 0
    # ROLES
    Passed16_18Plus = 0
    RoleAdded = 0
    RoleRemoved = 0

    # CHANNELS
    ChannelInfoUpdates = 0
    CreatedChannelPerm = 0
    UpdatedChannelPerm = 0
    DeletedChannelPerm = 0


    # ADMIN ACTIONS
    MembersBannedCount = [0, '']
    MembersKickedCount = [0, '']




    #######################################################################################
    # SET DATES
    Nowtime = datetime.datetime.now()
    LastWednesday = EleDiscordLib.GetLastWednesday()


    BotCheckBefore = Nowtime
    BotCheckAfter = datetime.datetime.combine(LastWednesday, datetime.datetime.min.time())


    ListOfDatesInSearchRange = EleDiscordLib.ReturnListOfDatesBetweenDateAandDateB(BotCheckAfter, BotCheckBefore)
    #print(f'ListOfDatesInSearchRange: {ListOfDatesInSearchRange}')

    if FromDate != '1111/11/11':
        try:
            # Convert FromDate&ToDate from strings to datetime.
            FromDateSplit = FromDate.split('/')
            print(FromDateSplit)
            FromDate = date(int(FromDateSplit[0]), int(FromDateSplit[1]), int(FromDateSplit[2]))
            ToDateSplit = ToDate.split('/')
            ToDate = date(int(ToDateSplit[0]), int(ToDateSplit[1]), int(ToDateSplit[2]))

            BotCheckAfter = FromDate
            BotCheckBefore = ToDate
        except:
            await ctx.send(f'Error Loading up Dates!\nPlease use the format below:'
                           '```diff\n-+Audit @User ????/??/?? ????/??/??```'
                           'For Example:'
                           '```CSS\n-+Audit #TrunkMaster#8008 2020/12/29 2020/12/30```'
                           'Using default dates range!')

    #######################################################################################
    # VALID LOG FOLDERS
    ListOfValidFoldersToLookIn = []
    GuildName = str(ctx.message.channel.guild).replace(' ', '_')
    for CurrentFolder in os.listdir('./Logs/'):
        NameAndDate = CurrentFolder.split(' ')
        if NameAndDate[0] == GuildName:
            if NameAndDate[1] in ListOfDatesInSearchRange:
                ListOfValidFoldersToLookIn.append(CurrentFolder)

    # ==== # ==== # ==== # ==== # ==== # ==== # ==== # ==== # ==== # ==== #

    VoiceChannels = None
    try:
        VoiceChannels = await EleVoiceTimeTracking.GetVoiceChannelsOfUser(bot, ctx, AuditMember, BotCheckAfter, BotCheckBefore)
    except:
        pass

    if True == True:

        AuditLogDataOfAuditMember = EleDiscordLib.returnActionAmountByUserIDFromTimeRangeInDatabaseFile(ctx.message.channel.guild, AuditMember.id, BotCheckAfter, BotCheckBefore)
        # Counter = 0
        # for Entry in AuditLogDataOfAuditMember:
        #     print(f'Entry #{Counter} ► {Entry}')
        #     Counter = Counter + 1
        ### Entry = [Time, UserID, Action, Target, Content, Extra]
        for Entry in AuditLogDataOfAuditMember:
            if Entry[2] == 'LockedTicket':
                TicketsLocked = TicketsLocked + 1
            elif Entry[2] == 'UnlockedTicket':
                TicketsUnlocked = TicketsUnlocked + 1
            elif Entry[2] == 'SavedTicket':
                TicketsSaved = TicketsSaved + 1
            elif Entry[2] == 'DeletedTicket':
                TicketsDeleted = TicketsDeleted + 1


            elif Entry[2] == 'ServerMuted':
                Manual_MuteUnmute[0] = Manual_MuteUnmute[0] + 1
            elif Entry[2] == 'ServerUnmuted':
                Manual_MuteUnmute[1] = Manual_MuteUnmute[1] + 1
            elif Entry[2] == 'ServerDeafen':
                Manual_DeafenUnDeafen[0] = Manual_DeafenUnDeafen[0] + 1
            elif Entry[2] == 'ServerUndeafen':
                Manual_DeafenUnDeafen[1] = Manual_DeafenUnDeafen[1] + 1
            elif Entry[2] == 'member_move':
                Manual_MemberMoves = Manual_MemberMoves + 1
                if 'חקירות' in f'{Entry[5]}':
                    Manual_MemberMoveToInvestRoom = Manual_MemberMoveToInvestRoom + 1
            elif Entry[2] == 'Nickname_Change':
                Manual_Nickname = Manual_Nickname + 1
            elif Entry[2] == 'invite_create':
                InvitesCreated = InvitesCreated + 1
            elif Entry[2] == 'infractions':
                usedInfractions = usedInfractions + 1
            elif Entry[2] == 'warn':
                WarnGiven = WarnGiven + 1
            elif Entry[2] == 'tempmute':
                TempmuteGiven = TempmuteGiven + 1
            elif Entry[2] == 'member_disconnect':
                Manual_Disconnect = Manual_Disconnect + 1
            elif Entry[2] == 'message_delete':
                MessagesDeleted = MessagesDeleted + 1
            elif Entry[2] == 'Passed16_18Plus':
                Passed16_18Plus = Passed16_18Plus + 1
            elif Entry[2] == 'AskForHelp_Tupal':
                AskForHelp_Tupal = AskForHelp_Tupal + 1



            elif Entry[2] == 'Audit':
                UsedAudit = UsedAudit + 1


            elif Entry[2] == 'AddedRole':
                RoleAdded = RoleAdded + 1
            elif Entry[2] == 'RemovedRole':
                RoleRemoved = RoleRemoved + 1


            elif Entry[2] == 'Channel_Update':
                ChannelInfoUpdates = ChannelInfoUpdates + 1
            elif Entry[2] == 'CreatedPermOverwrite':
                CreatedChannelPerm = CreatedChannelPerm + 1
            elif Entry[2] == 'UpdatePermOverwrite':
                UpdatedChannelPerm = UpdatedChannelPerm + 1
            elif Entry[2] == 'DeletePermOverwrite':
                DeletedChannelPerm = DeletedChannelPerm + 1


            elif Entry[2] == 'ban':
                MembersBannedCount[0] = MembersBannedCount[0] + 1
                MembersBannedCount[1] = MembersBannedCount[1] + f"<@{Entry[3]}>, "
            elif Entry[2] == 'kick':
                MembersKickedCount[0] = MembersKickedCount[0] + 1
                MembersKickedCount[1] = MembersKickedCount[1] + f"<@{Entry[3]}>, "



            else:
                print(f'Un-accounted for Entry ► {Entry}')


        Logdates = pandas.date_range(BotCheckAfter - timedelta(days=1), BotCheckBefore, freq='d')
        for X in Logdates:
            FilePath = f'./Logs/{ctx.message.channel.guild.id}/{X.strftime("%Y-%m-%d")} MsgCounter.log'
            if os.path.exists(FilePath):
                LogFile = open(FilePath, 'r')
                for Line in LogFile:
                    if Line == f'{AuditMember.id}\n':
                        MessagesSent = MessagesSent + int(LogFile.readline())
                        break





    if True == True:
        B = BotCheckBefore
        A = BotCheckAfter
        Botprint = ''
        #Botprint = Botprint + '** THIS IS A TEST BUILD AND THE INFORMATION IN THIS AUDIT IS NOT VALID**\n'
        Botprint = Botprint + ('<@!' + str(AuditMember.id) + '>') + f"**'s Audit During {A.year}.{A.month}.{A.day} - {B.year}.{B.month}.{B.day}:**\n"

        Reports = EleDiscordLib.ReturnListFromPermLevel(bot, PermLevel, AuditMember, TicketsLocked, TicketsUnlocked, TicketsSaved, TicketsDeleted, AskForHelp_Tupal, InvitesCreated, WarnGiven, TempmuteGiven, UsedAudit, usedInfractions, Manual_MemberMoves, Manual_MemberMoveToInvestRoom, Manual_MuteUnmute, Manual_DeafenUnDeafen, Manual_Disconnect, Manual_Nickname, MessagesDeleted, MessagesSent, Passed16_18Plus, RoleAdded, RoleRemoved, ChannelInfoUpdates, CreatedChannelPerm, UpdatedChannelPerm, DeletedChannelPerm, MembersKickedCount, MembersBannedCount, VoiceChannels)
        R = Botprint + Reports[0]
        Reports = [R, Reports[1]]





        for report in Reports:
            await ctx.send(report)
        # print('MOVES TO INVESTEGATION-ROOM COUNT:', MovesEntryCount)

    print(
        f'-----------------------------------Audit of {AuditMember} Finished-----------------------------------\n\n\n')


