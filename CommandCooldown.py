import datetime
import os
import json
from time import sleep


def DidUserPassCooldownTimeFor(UserID, guild, Action):
    UserPassedCooldown = False
    returnTime = 99999
    userFound = False

    AllUsersData = GetCommandsJsonAsArray(f'./Logs/{guild.id}/CommandsCooldowns.json')
    if Action == 'Audit':
        for userNumData in range(len(AllUsersData)):
            if int(AllUsersData[userNumData][0]) == UserID:
                userFound = True
                File_STR_datetime = AllUsersData[userNumData][1]
                File_Datetime = datetime.datetime.strptime(File_STR_datetime, '%Y-%m-%d %H:%M:%S.%f')
                TimeDifferenceInHours = round(((datetime.datetime.now() - File_Datetime).total_seconds() / 60) / 60, 2)
                if TimeDifferenceInHours >= 36:
                    AllUsersData[userNumData][1] = str(datetime.datetime.now())
                    SetAllDataToFile(AllUsersData, f'./Logs/{guild.id}/CommandsCooldowns.json')
                    #print('Allowing audit')
                    UserPassedCooldown = True
                    returnTime = TimeDifferenceInHours


                else:
                    #print(f'Cooldown TimeDifferenceInHours({TimeDifferenceInHours}) is less then 12. so returning false!')
                    UserPassedCooldown = False
                    returnTime = TimeDifferenceInHours
        if userFound == False:
            #print('User Not found in commands file')
            AllUsersData.append([UserID, str(datetime.datetime.now())])
            SetAllDataToFile(AllUsersData, f'./Logs/{guild.id}/CommandsCooldowns.json')
            UserPassedCooldown = True
            returnTime = 0



    return [UserPassedCooldown, returnTime]














def GetCommandsJsonAsArray(FilePath):
    Data = []
    #Check if the accounbts.json exist
    if os.path.exists(FilePath):
        AllUsers = []

        # Opening JSON file (returns JSON object as)
        File = open(FilePath)
        # a dictionary
        FileData = json.load(File)
        # Iterating through the json accounts and get each account as list
        for Account in FileData['Users']:
            CurentUser = []
            # print(Account)
            CurentUser.append(Account['UserID'])
            CurentUser.append(Account['LastTimeUsedAudit'])
            AllUsers.append(CurentUser)
            CurrentAccount = []
        File.close()

        return AllUsers


    else:
        print(f'Error: Could not load up {FilePath} -GetArrayOfUserInfoFromFile\n\n')
        return []







def SetAllDataToFile(Data, FilePath):
    data = {}
    data['Users'] = []

    for Entry in Data:
        data['Users'].append({
            'UserID': Entry[0],
            'LastTimeUsedAudit': Entry[1]
        })


    with open(FilePath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)







