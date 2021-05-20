import sqlite3
import datetime
import os
import asyncio
import numpy as np


import EleDiscordLib



async def TrackVoiceTime(bot, member, before, after):


    #Skip if the member isnt Elephant
    # if member.id != 155360532482752512:
    #     return
    ActionMemberDid = ''
    if before.channel == None and  after.channel != None:
        ActionMemberDid = 'Connect to Voice Channel'
        await ProecessJoiningVoice(bot, after.channel, member)
    elif before.channel != None and after.channel == None:
        ActionMemberDid = 'Leave Voice Channel'
        await ProecessLeavingVoice(bot, before.channel, member)
    elif before.channel != None and after.channel != None:
        ActionMemberDid = 'Move Voice Channel'
        await ProecessLeavingVoice(bot, before.channel, member)
        await ProecessJoiningVoice(bot, after.channel, member)

    #print(f'{member} Did {ActionMemberDid}')







async def ProecessJoiningVoice(bot, channel, member):
    FilePath = f'./Logs/{channel.guild.id}/{datetime.date.today().strftime("%Y-%m-%d")} VoiceActivity.db'
    MakeSureVoiceActivityDatabasesExists(channel, FilePath)
    Connection = sqlite3.connect(FilePath)
    Cursor = Connection.cursor()

    Cursor.execute(f'DELETE FROM VoiceActivityLastSeenTable WHERE UserID = {member.id} AND ChannelID = {channel.id};')
    Cursor.execute('INSERT INTO VoiceActivityLastSeenTable VALUES (?,?,?)', [datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), member.id, channel.id])


    Connection.commit()
    Connection.close()
    #print('ProecessJoiningVoice')





async def ProecessLeavingVoice(bot, channel, member):
    TotalTimeInSeconds = 0

    # Entries = EleDiscordLib.GetSQLDataFromFileAndQuery(f'./Logs/{746740620445483008}/AdvancedComments.db', f'SELECT * FROM AdvandedComments WHERE Target={338475813160747018};')
    FilePath = f'./Logs/{channel.guild.id}/{datetime.date.today().strftime("%Y-%m-%d")} VoiceActivity.db'
    
    #Grab the time the user joined that voice channel from Database.
    MakeSureVoiceActivityDatabasesExists(channel, FilePath)
    Connection = sqlite3.connect(FilePath)
    Cursor = Connection.cursor()
    
    LastVoice = None
    for x in Cursor.execute(f'SELECT * FROM VoiceActivityLastSeenTable WHERE UserID = {member.id} AND ChannelID = {channel.id};'):
        LastVoice = x
    Cursor.execute(f'DELETE FROM VoiceActivityLastSeenTable WHERE UserID = {member.id} AND ChannelID = {channel.id};')
    Connection.commit()
    Connection.close()
    
    if LastVoice == None:
        return
    #Calculate how many seconds he has been on that voice channel
    DatetimeOfLastVoiceJoin = datetime.datetime.strptime(LastVoice[0], '%Y-%m-%d %H:%M:%S') #without decimals
    DatetimeOfLastVoiceLeave = datetime.datetime.strptime(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), '%Y-%m-%d %H:%M:%S') #without decimals
    DatetimeDifference = DatetimeOfLastVoiceLeave - DatetimeOfLastVoiceJoin
    # print(f'DatetimeOfLastVoiceJoin = {DatetimeOfLastVoiceJoin}, type({type(DatetimeOfLastVoiceJoin)})')
    # print(f'DatetimeOfLastVoiceLeave = {DatetimeOfLastVoiceLeave}, type({type(DatetimeOfLastVoiceLeave)})')
    # print(f'DatetimeDifference = {DatetimeDifference}, type({type(DatetimeDifference)})')
    TimeDifferenceInSeconds = DatetimeDifference.total_seconds()
    #print(f'TimeDifferenceInSeconds = {TimeDifferenceInSeconds}, type({type(TimeDifferenceInSeconds)})')


    #Grab Seconds on record already
    Connection = sqlite3.connect(FilePath)
    Cursor = Connection.cursor()
    TimeStoredEntryForThatChannel = None
    for x in Cursor.execute(f'SELECT * FROM VoiceActivityTimeStorageTable WHERE UserID = {member.id} AND ChannelID = {channel.id};'):
        TimeStoredEntryForThatChannel = x
    if TimeStoredEntryForThatChannel != None:
        TotalTimeInSeconds =TimeStoredEntryForThatChannel[0] + TimeDifferenceInSeconds
    else:
        TotalTimeInSeconds = TimeDifferenceInSeconds
    Cursor.execute(f'DELETE FROM VoiceActivityTimeStorageTable WHERE UserID = {member.id} AND ChannelID = {channel.id};')
    Cursor.execute('INSERT INTO VoiceActivityTimeStorageTable VALUES (?,?,?)', [TotalTimeInSeconds, member.id, channel.id])

    Connection.commit()
    Connection.close()

    # X = EleDiscordLib.TurnSecondsIntoDayHourMinuteSecond(TotalTimeInSeconds)
    # print(f'{member}, was on {channel}, for: {X[0]} Days, {X[1]} Hours, {X[2]} Minutes, {X[3]} Seconds')




    #print('ProecessLeavingVoice')










def MakeSureVoiceActivityDatabasesExists(guild, DataBasePath):
    if os.path.exists(DataBasePath) == False:
        Connection = sqlite3.connect(DataBasePath)
        Cursor = Connection.cursor()
        try:
            # Try to Create table
            Cursor.execute('''CREATE TABLE VoiceActivityLastSeenTable (datetime text, UserID int, ChannelID int)''')
            Cursor.execute('''CREATE TABLE VoiceActivityTimeStorageTable (TotalSeconds int, UserID int, ChannelID int)''')
            print(f'>Created a new Advanced Comments database for guild({guild}) as {DataBasePath}..')
        except:
            # print(f'>EleSQLFunctions: Failed to create new database, likely "{Name}" already exists.')
            pass
        Connection.commit()
        Connection.close()










async def GetVoiceChannelsOfUser(bot, ctx, member, From, To):
    # before = datetime.datetime.strptime(From, '%Y/%m/%d')
    # after = datetime.datetime.strptime(To, '%Y/%m/%d')
    Dates = EleDiscordLib.ReturnListOfDatesBetweenDateAandDateB(From, To)

    AllEntries = []


    # Grab Entries from files
    for Date in Dates:
        FilePath = f'./Logs/{ctx.guild.id}/{Date} VoiceActivity.db'
        if os.path.exists(FilePath):
            #print(f'Checking {FilePath}')
            await asyncio.sleep(0.1)
            Connection = sqlite3.connect(FilePath)
            Cursor = Connection.cursor()

            for X in Cursor.execute(f'SELECT * FROM VoiceActivityTimeStorageTable WHERE UserID = {member.id};'):
                AllEntries.append(X)

            Connection.commit()
            Connection.close()

    # Shrink list across days
    AllEntries = ShrinkList(AllEntries)
    # Sort Entries From Highest Time to Lower Time
    AllEntries = EleDiscordLib.SelectionSort(AllEntries)
    return AllEntries






def ShrinkList(arr):
    arr = np.array(arr)
    repeating = {}
    for i in range(len(arr[:, 2])):
        elem = arr[i, 2]
        if elem in repeating.keys():
            repeating[elem].append(arr[i, 0])
        else:
            repeating[elem] = [arr[i, 0]]

    new_arr = []
    for elem in arr:
        if elem[2] in repeating.keys():
            new_arr.append([np.sum(repeating[elem[2]]), elem[1], elem[2]])
            del repeating[elem[2]]
        else:
            np.append(new_arr, elem)

    return new_arr
