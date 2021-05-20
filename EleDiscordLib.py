import discord
from discord.ext import commands
from time import sleep
import datetime
from datetime import date, timedelta
import os
import pandas
import sqlite3
import asyncio
import json











def returnActionAmountByUserIDFromTimeRangeInDatabaseFile(Guild, UserID, AfterDatetime, BeforeDatetime):
    dates = pandas.date_range(AfterDatetime-timedelta(days=0),BeforeDatetime,freq='d')
    #print(f'{AfterDatetime} All the way to {BeforeDatetime} is:\n{dates}')
    Data = []
    for date in dates:
        CurrentFilePath = f'./Logs/{Guild.id}/{date.strftime("%Y-%m-%d")} database.db'
        if os.path.exists(CurrentFilePath):
            try:

                Connection = sqlite3.connect(CurrentFilePath)
                Cursor = Connection.cursor()
                for Entry in Cursor.execute(f'SELECT * FROM EleAuditLog WHERE UserID={UserID};'):
                    Data.append(Entry)

                Connection.close()
                #print(f'Reading file ({CurrentFilePath}) !')
            except:
                #print(f'Failed to read file ({CurrentFilePath}) !')
                pass
        else:
            #print(f'"{CurrentFilePath}" Does not Exist!')
            pass
    return Data






def ReturnListOfDatesBetweenDateAandDateB(DateA = date(1000, 1, 1), DateB = date(1000, 1, 2)):
    PandaDateRange = pandas.date_range(start=DateA, end=DateB)
    returnlist = []
    for X in range(len(PandaDateRange)):
        Date = str(PandaDateRange[X]).split(' ')
        returnlist.append(Date[0])
    return returnlist










def IsMemberARole(Member, StringsRolesArray):
    for X in StringsRolesArray:
        for role in Member.roles:
            #print(f'Checking {role}')
            if X.lower() in str(role).lower():
                #print(f'{X.lower()}, ***is*** {str(role).lower()}')
                return True
            else:
                pass
                #print(f'{X.lower()}, is not {str(role).lower()}')

    return False



def GetLastWednesday():
    today = date.today()
    offset = (today.weekday() - 2) % 7
    last_Wednesday = today - timedelta(days=offset)
    return last_Wednesday


def GetCurrentDateAndHourMinute():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M")



def getUserFromUserIDString(bot, UserIdString):
    userID = ''
    for Char in UserIdString:
        if Char.isnumeric() == True:
            userID = userID + Char
    try:
        return bot.get_user(int(userID))
    except:
        print('  > Failed to get UserID({userID}) in getUserFromUserIDString!')




async def isCommandAllowedOnChannel(CommandSent: str, ChannelSent: discord.channel):
    AllowedChannelsForCommand = [['!tempmute', ['מיוטים-ואזהרות']],
                                 ['!warn', ['מיוטים-ואזהרות']],
                                 ['!infractions', ['מיוטים-ואזהרות']],
                                 ['-+Audit', ['elechannel', 'פקודות', ]],
                                 ['-+Audit', ['elechannel', 'programmer','פעילות-הלפרים',  'פקודות-מודים', ]],
                                 ['-+ManuallySaveAuditLogCacheForAllGuilds', ['elechannel', 'programmer']],
                                 ['-+PrintCache', ['elechannel', 'programmer']],
                                 ['-+PrintIDCache', ['elechannel', 'programmer']],
                                 ['-+cmd', ['elechannel', 'פקודות']],
                                 ['-+Permit', ['elechannel', 'ticket']],
                                 ['-+Permit', ['elechannel', 'ticket']],
                                 ['-+CreateStaffTemplate', ['elechannel','פעילות-הלפרים',  'פקודות', ]],
                                 ['-+RussianRoulette', ['elechannel', 'ommand', 'פקודות', ]],
                                 ['-+SetMonthBestColor', ['elechannel', 'ommand', 'פקודות', ]],
                                 ['-+PrintAllRecords', ['elechannel', 'programmer', 'פקודות-מודים']]]
    for Permit in AllowedChannelsForCommand:
        if CommandSent == Permit[0]:
            print('Command Found!')
            for Channel in Permit[1]:
                if Channel in str(ChannelSent):
                    print('Allowed!')
                    return True
    print('Not Allowed')
    return False










async def GetAllAuditsFromUserOfType(ctx, AuditMember : discord.Member, FromDate, ToDate, bot = commands.Bot(command_prefix='-+'), EntryTypeRequested = 'All'):
    # SET DATES
    Nowtime = datetime.datetime.now()
    LastTuesday = GetLastWednesday()

    BotCheckBefore = Nowtime
    BotCheckAfter = datetime.datetime.combine(LastTuesday, datetime.datetime.min.time())

    if FromDate != '1111/11/11':
        try:
            # Convert FromDate&ToDate from strings to datetime.
            FromDateSplit = FromDate.split('/')
            FromDate = datetime.date(int(FromDateSplit[0]), int(FromDateSplit[1]), int(FromDateSplit[2]))
            ToDateSplit = ToDate.split('/')
            ToDate = datetime.date(int(ToDateSplit[0]), int(ToDateSplit[1]), int(ToDateSplit[2]))

            BotCheckAfter = FromDate
            BotCheckBefore = ToDate
        except:
            print('Error Loading up Dates! - GetAllAuditsFromUser')
            await ctx.send(f'Error Loading up Dates!\nPlease use the format below:'
                           '```diff\n-+PrintAllAuditFromUser @User ????/??/?? ????/??/??```'
                           'For Example:'
                           '```CSS\n-+PrintAllAuditFromUser #TrunkMaster#8008 2020/12/29 2020/12/30```'
                           'Sending nothing!')
            return ['']
    else:
        return ['Please use Dates with this command!\n\n -+PrintAllAuditFromUser @User ????/??/?? ????/??/??']




    ListOfDatesInSearchRange = ReturnListOfDatesBetweenDateAandDateB(BotCheckAfter, BotCheckBefore)


    # VALID LOG FOLDERS
    ListOfValidFoldersToLookIn = []
    GuildName = str(ctx.message.channel.guild).replace(' ', '_')
    for CurrentFolder in os.listdir('./Logs/'):
        NameAndDate = CurrentFolder.split(' ')
        if NameAndDate[0] == GuildName:
            if NameAndDate[1] in ListOfDatesInSearchRange:
                ListOfValidFoldersToLookIn.append(CurrentFolder)

    dates = pandas.date_range(BotCheckAfter - timedelta(days=1), BotCheckBefore, freq='d')
    # print(f'{AfterDatetime} All the way to {BeforeDatetime} is:\n{dates}')
    Data = []
    for date in dates:
        CurrentFilePath = f'./Logs/{ctx.message.channel.guild.id}/{date.strftime("%Y-%m-%d")} database.db'
        if os.path.exists(CurrentFilePath):
            #print(f'CurrentFilePath"{CurrentFilePath}')
            try:

                Connection = sqlite3.connect(CurrentFilePath)
                Cursor = Connection.cursor()
                SQLData = []
                if EntryTypeRequested == 'All':
                    for X in Cursor.execute(
                            f"SELECT * FROM EleAuditLog WHERE UserID LIKE '%{AuditMember.id}%' OR Target LIKE '%{AuditMember.id}%' OR content LIKE '%{AuditMember.id}%' OR extra LIKE '%{AuditMember.id}%'"):
                        SQLData.append(X)
                else:
                    for X in Cursor.execute(
                            f"SELECT * FROM EleAuditLog WHERE UserID LIKE '%{AuditMember.id}%' AND ActionType LIKE '%%{EntryTypeRequested}'"):
                        SQLData.append(X)
                for Entry in SQLData:

                    OriginAlt = str(Entry[1])
                    TargetAlt = str(Entry[3])


                    # print(f'Entry[1] type={type(Entry[1])} and of Value:{Entry[1]}')
                    # print(f'bot.getmember.me:{bot.get_user(134156783450062848)}')
                    # print(f'bot.getmember.them:{bot.get_user(Entry[1])}')

                    #print(f'Adding string:({Entry[0]} <@{OriginAlt}> {Entry[2]} <@{TargetAlt}> {Entry[4]} {Entry[5]})')
                    Data.append(f'{Entry[0]} <@{OriginAlt}> {Entry[2]} <@{TargetAlt}> {Entry[4]} {Entry[5]}\n')


                Connection.close()
                #print(f'Reading file ({CurrentFilePath}) !')
            except:
                #print(f'Failed to read file ({CurrentFilePath}) !')
                pass
        else:
            #print(f'"{CurrentFilePath}" Does not Exist!')
            pass


    return Data













def ReturnListFromPermLevel(bot, PermLevel, AuditMember, TicketsLocked, TicketsUnlocked, TicketsSaved, TicketsDeleted, AskForHelp_Tupal, InvitesCreated, WarnGiven, TempmuteGiven, UsedAudit, usedInfractions, Manual_MemberMoves, Manual_MemberMoveToInvestRoom, Manual_MuteUnmute, Manual_DeafenUnDeafen, Manual_Disconnect, Manual_Nickname, MessagesDeleted, MessagesSent, Passed16_18Plus, RoleAdded, RoleRemoved, ChannelInfoUpdates, CreatedChannelPerm, UpdatedChannelPerm, DeletedChannelPerm, MembersKickedCount, MembersBannedCount, VoiceChannels):
    Report1 = ''
    Report2 = ''
    print(f'PermLevel Gotten: {PermLevel}')
    if PermLevel == 'Staff Manager':
        Report1 = Report1 + '**Response:**\n'
        # TicketsLocked
        Report1 = Report1 + f'   -Tickets Locked: {TicketsLocked}\n'
        # TicketsUnlocked
        Report1 = Report1 + f'   -Tickets Unlocked: {TicketsUnlocked}\n'
        # TicketsSaved
        Report1 = Report1 + f'   -Tickets Saved: {TicketsSaved}\n'
        # TicketsDeleted
        Report1 = Report1 + f'   -Tickets Deleted: {TicketsDeleted}\n'
        # EstimatedTicketsHandled
        Report1 = Report1 + f'   -Estimated Tickets: {((TicketsLocked + TicketsDeleted) / 2)}\n'
        # AskForHelp_Tupal
        Report1 = Report1 + f'   -Help Requests: {AskForHelp_Tupal}'

        Report1 = Report1 + '\n**Action:**\n'
        # InvitesCreated
        Report1 = Report1 + f'   -Invites Created: {InvitesCreated}\n'
        # WarnGiven
        Report1 = Report1 + f'   -Warns Given: {WarnGiven}\n'
        # TempmuteGiven
        Report1 = Report1 + f'   -Tempmutes Given: {TempmuteGiven}\n'
        # usedInfractions
        Report1 = Report1 + f'   -Infractions Checked: {usedInfractions}\n'
        # UsedAudit
        Report1 = Report1 + f'   -Audits Requested: {UsedAudit}\n'
        Report1 = Report1 + '\n**Activity:**\n'
        Report1 = Report1 + f'   **-Voice Activity:** \n'
        # VoiceActiveHours
        if VoiceChannels != None:
            for I in range(20):
                try:
                    X = TurnSecondsIntoDayHourMinuteSecond(VoiceChannels[I][0])
                    Report2 = Report2 + f'         **<#{VoiceChannels[I][2]}>**    for {X[0]} Days, {X[1]} Hours, {X[2]} Minutes and {X[3]} Seconds.\n'
                except:
                    pass
        else:
            Report1 = Report1 + f'         **NO Voice Hours Found.**\n'

        # Manual_MemberMoves
        Report1 = Report1 + f'       -Manual Moves: {Manual_MemberMoves}\n'
        # Manual_MemberMoveToInvestRoom
        Report1 = Report1 + f'       -Manual Moves To Investigation Room: {Manual_MemberMoveToInvestRoom}\n'

        Report1 = Report1 + f'   \n**-Voice Control:** \n'
        # Manual_MuteUnmuteDeafenUndeafen
        Report1 = Report1 + f'       -Manual Mute: {Manual_MuteUnmute[0]}\n'
        Report1 = Report1 + f'       -Manual Unmute: {Manual_MuteUnmute[1]}\n'
        Report1 = Report1 + f'       -Manual Deafen: {Manual_DeafenUnDeafen[0]}\n'
        Report1 = Report1 + f'       -Manual UnDeafen: {Manual_DeafenUnDeafen[1]}\n'
        # Manual_Disconnect
        Report1 = Report1 + f'       -Manual Disconnect: {Manual_Disconnect}\n'

        Report1 = Report1 + f'   \n**-Chat Control:** \n'
        # Manual_Nickname
        Report1 = Report1 + f'       -Nickname Change: {Manual_Nickname}\n'
        # MessagesDeleted
        Report1 = Report1 + f'       -Messages Deleted: {MessagesDeleted}\n'
        # MessagesSent
        Report1 = Report1 + f'       -Messages Sent: {MessagesSent}\n'

        Report1 = Report1 + f'   \n**-Role Updates::** \n'
        # Passed16_18Plus
        Report1 = Report1 + f'       -Passing 16+/18+: {Passed16_18Plus}\n'
        #RoleAdded
        Report1 = Report1 + f'       -Amount of roles given: {RoleAdded}\n'
        #RoleRemoved
        Report1 = Report1 + f'       -Amount of roles taken away: {RoleRemoved}\n'


        Report1 = Report1 + f'   \n**-Channel Updates:** \n'
        # ChannelInfoUpdates
        Report1 = Report1 + f'       -Channel Info Updates: {ChannelInfoUpdates}\n'
        # CreatedChannelPerm
        Report1 = Report1 + f'       -Created Channel Perm: {CreatedChannelPerm}\n'
        # UpdatedChannelPerm
        Report1 = Report1 + f'       -Updated Channel Perm: {UpdatedChannelPerm}\n'
        # DeletedChannelPerm
        Report1 = Report1 + f'       -Deleted Channel Perm: {DeletedChannelPerm}\n'

        Report1 = Report1 + f'   \n**-Administrative Actions:** \n'
        # MembersKickedCount
        Report1 = Report1 + f'       -Kicks: {MembersKickedCount[0]}\n'
        Report1 = Report1 + f'       -Kicked users: {MembersKickedCount[1]}\n'
        # MembersBannedCount
        Report1 = Report1 + f'       -Bans: {MembersBannedCount[0]}\n'
        Report1 = Report1 + f'       -Banned users: {MembersBannedCount[1]}\n'

        Talnick = bot.get_user(523055019914952714).name
        EleNick = bot.get_user(134156783450062848).name
        OriNick = bot.get_user(424150309858705420).name
        Report1 = Report1 + f'\n\n ``` ```***Audit Made by {EleNick}.♥*** with the gracious help of {OriNick} hosted by {Talnick}!``` ```'

        pass
    elif PermLevel == 'Helper':
        Report1 = Report1 + '**Response:**\n'
        Report1 = Report1 + f'   -Estimated Tickets: {((TicketsLocked + TicketsDeleted) / 2)}\n'
        Report1 = Report1 + f'   -Help Requests: {AskForHelp_Tupal}\n'
        Report1 = Report1 + '\n**Action:**\n'
        Report1 = Report1 + f'   -Tempmutes/WarnGiven Given: {TempmuteGiven + WarnGiven}\n'
        Report1 = Report1 + '\n**Activity:**\n'
        # VoiceActiveHours
        if VoiceChannels != None:
            for I in range(3):
                try:
                    X = TurnSecondsIntoDayHourMinuteSecond(VoiceChannels[I][0])
                    Report2 = Report2 + f'         **<#{VoiceChannels[I][2]}>**    for {X[0]} Days, {X[1]} Hours, {X[2]} Minutes and {X[3]} Seconds.\n'
                except:
                    pass
        else:
            Report1 = Report1 + f'         **NO Voice Hours Found.**\n'

        Report1 = Report1 + f'       -Manual Moves: {Manual_MemberMoves}\n'
        Report1 = Report1 + f'   \n**-Voice Control:** \n'
        Report1 = Report1 + f'       -Manual Mute/Unmute: {Manual_MuteUnmute[0] + Manual_MuteUnmute[1]}\n'
        Report1 = Report1 + f'       -Manual Deafen/UnDeafen: {Manual_DeafenUnDeafen[0] + Manual_DeafenUnDeafen[1]}\n'
        Report1 = Report1 + f'       -Manual Disconnect: {Manual_Disconnect}\n'
        Report1 = Report1 + f'   \n**-Chat Control:** \n'
        Report1 = Report1 + f'       -Nickname Change: {Manual_Nickname}\n'
        Report1 = Report1 + f'       -Passing 16+/18+: {Passed16_18Plus}'

        Talnick = bot.get_user(523055019914952714).name
        EleNick = bot.get_user(134156783450062848).name
        OriNick = bot.get_user(424150309858705420).name
        Report1 = Report1 + f'\n\n ``` ```***Audit Made by {EleNick}.♥*** with the gracious help of {OriNick} hosted by {Talnick}!``` ```'
        pass



    return [Report1, Report2]




# async def MakeSureElephantHasCorrectRoles(bot):
#     print('MakeSureElephantDoesntHaveAFriendlyRole')
#     for Guild in bot.guilds:
#         if 'Among' in str(Guild):
#             ElephantMember = Guild.get_member(134156783450062848)
#             RolesElephantShouldHave = [746740620445483008, 776594907200356414, 771013219610656798, 749738561166639227,
#                                        762070315802034186, 770753756853043251, 786680178423365674, 764203298265628682,
#                                        758397246730666026, 746748197342412912, 758071269999509569, 758806118775390210,
#                                        806193503918620683, 786680175537684501]
#             for role in ElephantMember.roles:
#                 #print(f'---------- Checking {role}')
#                 RolesToRemove = []
#                 if role.id not in RolesElephantShouldHave:
#                     RolesToRemove.append(role)
#                     print(f'Trying to remove role {role} from {ElephantMember}')
#                 sleep(0.5)
#                 await ElephantMember.remove_roles(*RolesToRemove)



def UpdateConfigFileOfServer(ServerID='000000', Entries=[['MissingEntryKey', 'MissingEntryValue']]):
    FilePath = f'./Logs/{ServerID}/{ServerID}_Config.json'
    if os.path.exists(FilePath) == False:
        print(f'{FilePath} Does not Exist!')
        with open(FilePath, 'w') as f:
            f.write('{\n    \n}')
    else:
        print(f'{FilePath} Exists!')
    # WriteIntoFile
    with open(FilePath, 'r') as f:
        data = json.load(f)
        for Entry in Entries:
            data[f'{Entry[0]}'] = f'{Entry[1]}'  # <--- add `id` value.
    os.remove(FilePath)
    with open(FilePath, 'w') as f:
        json.dump(data, f, indent=4)

def rgb_to_hex(rgb):
    return '%02x%02x%02x' % rgb



def clearAllOpenTicketFiles(bot):
    for G in bot.guilds:
        FilesList = os.listdir(f'./Logs/{G.id}')
        for F in FilesList:
            if F[:11] == 'TicketOpen_':
                os.remove(f'./Logs/{G.id}/{F}')


def TurnSecondsIntoDayHourMinuteSecond(Seconds):
  time = float(Seconds)
  day = int(time // (24 * 3600))
  time = time % (24 * 3600)
  hour = int(time // 3600)
  time %= 3600
  minutes = int(time // 60)
  time %= 60
  seconds = int(time)
  return [day, hour, minutes, seconds]

def SelectionSort(Array):
    A = Array
    for i in range(len(A)):
        # Find the minimum element in remaining
        # unsorted array
        min_idx = i
        for j in range(i + 1, len(A)):
            if A[min_idx] < A[j]:
                min_idx = j
                # Swap the found minimum element with
        # the first element
        A[i], A[min_idx] = A[min_idx], A[i]
    return A

def GetSQLDataFromFileAndQuery(File: str, Query: str):
    DatabaseEntries = []

    Connection = sqlite3.connect(File)
    Cursor = Connection.cursor()

    DatabaseEntries = []
    for X in Cursor.execute(Query):
        DatabaseEntries.append(X)

    Connection.commit()
    Connection.close()

    return DatabaseEntries






