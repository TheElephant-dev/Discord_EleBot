import discord
import EleDiscordLib
import EleImageGenerator
import asyncio
import EleAuditLog
import datetime


async def ProtectUser(bot, MemberToProtect, AbuserMember):
    if MemberToProtect != AbuserMember:
        AbuserUser = bot.get_user(AbuserMember.id)
        Protectionuser = bot.get_user(MemberToProtect.id)

        await AbuserMember.move_to(None)


        #Change Nick Of Abuser
        NewNickOfAbuser = f'{AbuserMember.nick} Abuz'
        try:
            #await Abuser.edit(nick=NewNickOfAbuser[:32], reason='Protection from abuse (Disconnects abuser. removes servermute\deafen. and adds "Abuz" to the Abusers nickname.) (protects high staff and programmers) - Approved by Tails the admins and Dror')
            pass
        except:
            pass

        # Unmute\Undeafen the victim
        for x in range(5):
            try:
                await MemberToProtect.edit(mute=False, deafen=False, reason='Protection from abuse')
            except:
                await asyncio.sleep(1)
                pass

        AbuserNick = ''
        VictimNick = ''
        try:
            AbuserTag = f'<@{AbuserMember.id}>'
            AbuserNick = f'{AbuserMember.nick}'
            VictimTag = f'<@{MemberToProtect.id}>'
            VictimNick = f'{MemberToProtect.nick}'
        except:
            pass

        try:
            DontSendPmToUserIDs = [523055019914952714]
            if MemberToProtect.id not in DontSendPmToUserIDs:
                await MemberToProtect.send(file=discord.File(rf'{EleImageGenerator.GetFilePathOfImageMessage(AbuserNick, VictimNick, MessageType="AbuseMessageToVictim")}'))
                await MemberToProtect.send(f'<@{AbuserMember.id}> Abuz!')
        except:
            print(f'Failed to send a message to Victim({MemberToProtect})')
        try:
            await AbuserMember.send(file=discord.File(rf'{EleImageGenerator.GetFilePathOfImageMessage(AbuserNick, VictimNick, MessageType="AbuseMessageToAbuser")}'))
        except:
            print(f'Failed to send a message to Abuser({AbuserMember})')

        #print(f'  > Protecting {MemberToProtect.name} From {AbuserMember.name}')

        for X in range(5):
            try:
                await AbuserMember.move_to(None)
            except:
                pass
            await asyncio.sleep(1)



async def GetAbuser(bot, VictimMember, before, after):
    try:
        async for Entry in bot.get_channel(before.channel.id).guild.audit_logs(limit=1):
            if isActionMuteOrDeafenOrDisconnect(Entry) == True:
                #print('Action was Mute or deafen')

                ID = 0
                try:
                    ID = before.channel.id
                except:
                    pass
                try:
                    ID = after.channel.id
                except:
                    pass
                Guild = bot.get_channel(ID).guild

                if Entry.target.id == VictimMember.id:
                    return Guild.get_member(Entry.user.id)
            try:
                pass
            except:
                pass
    except:
        #print('Failed to get abuser')
        pass

    return None







async def ProcessAbuse(bot, member, before, after):
    Abuser = await GetAbuser(bot, member, before, after)
    if Abuser != None:
        Mode = 'Normal'
        if 'adv' in (before.channel.name).lower():
            Mode = 'AdvancedRoom'

        A, V = [GetProtectionPriorityOfMember(member, Mode), GetProtectionPriorityOfMember(Abuser, Mode)]
        if A > V: #               A = Priority of Abuser           V = Priority of Victim
            # dont protect in abuse was done to user in advancec channels
            await ProtectUser(bot, member, Abuser)
            print(f'  > Protected {member}({A}) from {Abuser}({V})')
            print(f'  > {datetime.datetime.now()} >Adding to record that {member}({A}) Was Abused by {Abuser}({V}).')
            #print(f'Trying to add: {str([before.channel.guild.id, [EleDiscordLib.GetCurrentDateAndHourMinute(), Abuser.id, "Abuse", member.id, None, None]])}')
            EleAuditLog.AddEntryToEleAuditLogCache([before.channel.guild.id, [EleDiscordLib.GetCurrentDateAndHourMinute(), Abuser.id, 'Abuse', member.id, None, None]])
        else:
            print(f'  > Didnt protect {member}({A}) from {Abuser}({V})')





def isActionMuteOrDeafenOrDisconnect(Entry):
    try:
        if (Entry.before.deaf is False) and (Entry.after.deaf is True):
            return True
    except:
        pass
    try:
        if (Entry.before.mute is False) and (Entry.after.mute is True):
            return True
    except:
        pass
    return False










def GetProtectionPriorityOfMember(Member: discord.Member, Mode = 'NormalMode'):


    Priority = 0
    if EleDiscordLib.IsMemberARole(Member, ['co-owner']):
        Priority = 30

    if EleDiscordLib.IsMemberARole(Member, ['owner']):
        Priority = 35
    # elif EleDiscordLib.IsMemberARole(Member, ['head of pro']):
    #     Priority = 25
    elif EleDiscordLib.IsMemberARole(Member, ['Management']):
        Priority = 25
    elif EleDiscordLib.IsMemberARole(Member, ['Staff Manager']):
        Priority = 20
    elif EleDiscordLib.IsMemberARole(Member, ['Programming Manager']):
        Priority = 15
    elif EleDiscordLib.IsMemberARole(Member, ['program']):
        Priority = 10
    elif EleDiscordLib.IsMemberARole(Member, ['MVP', 'Honor +']):
        Priority = 10
    elif EleDiscordLib.IsMemberARole(Member, ['Legendary Supporter']):
        Priority = 6
    elif EleDiscordLib.IsMemberARole(Member, ['Ban Perm']):
        Priority = 6
    elif EleDiscordLib.IsMemberARole(Member, ['Helper']):
        Priority = 4


    #Filter for advanced rooms
    if Mode == 'AdvancedRoom':
        if EleDiscordLib.IsMemberARole(Member, ['Head Of Advanced']):
            Priority = 22
        elif EleDiscordLib.IsMemberARole(Member, ['Advanced Judge', 'Advanced Tester']):
            Priority = 6



    if EleDiscordLib.IsMemberARole(Member, ['🏆']):
        Priority += 1



    #Master Overwrite

    if Member.id in [134156783450062848, 523055019914952714, 336887146717773826]: # Elephant, Tails, AmitD, Dror
        Priority = 40


    # Elephant, EleBot
    if Member.id in [789942343619969074]: # Elephant, EleBot
        Priority = 99


    # Mikey
    # elif Member.id in [319478655568838657]:
    #     Priority = 3

    #Rolax
    # elif Member.id in [778702186946756669]: # Rolax
    #     Priority = 5
	
    # Baba
    # elif Member.id in [392296943751266305]:  # Baba
    #     Priority = 3

    # Jeff
    # elif Member.id in [715195484863463445]:  # Jeff
    #     Priority = 26

    # Dvir
    # elif Member.id in [557618550089449503]:  # Dvir
    #     Priority = 27



    return Priority





async def CanAbuseTarget(ctx, Abuser, Victim):
    AbuserP, VictimP = [GetProtectionPriorityOfMember(Abuser, 'Normal'), GetProtectionPriorityOfMember(Victim, 'Normal')]
    #print(f'AbuserP = {AbuserP}, VictimP = {VictimP}')
    if AbuserP <= VictimP:

        X = await ctx.send(embed=discord.Embed(title="Denied.", description=f"You Cannot Abuse someone with a higher or same priority then you!", color=0x7C0200))
        await X.delete(delay=10)
        return False
    return True










