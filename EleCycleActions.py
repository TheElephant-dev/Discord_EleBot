import EleDiscordLib
import asyncio
import discord
from discord.ext import commands
from datetime import datetime


async def KeepRolaxRole(bot):
    Rolax = None
    Legendary_Supporter_Role = None
    G = bot.get_guild(746740620445483008)
    Rolax = G.get_member(778702186946756669)
    for role in G.roles:
        if 'Legendary Supporter' in str(role):
            Legendary_Supporter_Role = role
    if EleDiscordLib.IsMemberARole(Rolax, ['Legendary Supporter']) == False:
        await Rolax.add_roles(Legendary_Supporter_Role, reason='Rolax IS a Legendary Supporter. - Tails.')


EnforceEleChannelPermsFirstRun = True
async def EnforceEleChannelPerms(bot):
    global EnforceEleChannelPermsFirstRun
    if EnforceEleChannelPermsFirstRun == True:
        EnforceEleChannelPermsFirstRun = False
        return

    #Grab EleChannel
    AUIguild = bot.get_guild(746740620445483008)
    elechannel = AUIguild.get_channel(790397266753093632)


    #Add inalid perm settings into Array
    ValidPermNames = ['@everyone', '[🤖] EIeBot🐘#9398','DemonHunter#5248','♕ | Management',  '♔ | Co Owner', 'ඞ | Owner', '🍲 | Head of Programmers', 'Hartetan#1111']
    InvalidPermsRoleOrMember = []
    for UserOrRole in elechannel.overwrites:
        if str(UserOrRole) not in ValidPermNames:
                InvalidPermsRoleOrMember.append(UserOrRole)


    #Remove all perms for invalid roles or members
    for InvalidRoleOrMember in InvalidPermsRoleOrMember:
        await elechannel.set_permissions(InvalidRoleOrMember, overwrite=None, reason='Yeet! elechannel is for bot testing.')
        print(f'Removeed {InvalidRoleOrMember}s perm from elechannel')



    AidsPeopleIDs = [338475813160747018]
    for AidsPersonID in AidsPeopleIDs:

        # Get Aids Person
        AidsPerson = AUIguild.get_member(AidsPersonID)
        if AidsPerson == None:
            return

        # Get The correct Perm set for aids people.
        AidspeoplePerm = discord.PermissionOverwrite()
        AidspeoplePerm.send_messages = False # Send messages
        AidspeoplePerm.manage_channels = False # edit channel name ect
        AidspeoplePerm.manage_roles = False # edit channel perms

        ShouldEdit = False
        PermSet = elechannel.overwrites_for(AidsPerson)
        if PermSet != None:
            for Perm in PermSet:
                if str(Perm[0]) in ['send_messages', 'manage_channels', 'manage_roles'] and Perm[1] != False:
                    ShouldEdit = True
        else:
            ShouldEdit = True



        #Enforce the change
        if ShouldEdit == True:
            # Check who did it
            AidsPermitter = None
            async for Entry in AUIguild.audit_logs(limit=20):
                if AidsPermitter == None:
                    if 'overwrite' in str(Entry.action):
                        if 'elechannel' in str(Entry.target):
                            if 789942343619969074 != Entry.user.id:
                                AidsPermitter = Entry.user
                            else:
                                print('editor was elebot')
                        else:
                            print('no elechannel in target')
                    else:
                        print('no overwrite in action')


            print(f"{AidsPermitter} Edited {AidsPerson}'s perms for Elechannel. editing back !")
            await elechannel.set_permissions(AidsPerson, overwrite=AidspeoplePerm, reason="Enforcing elechannel's purpose. elephant's bot testing room.")
            await elechannel.send(f"<@{AidsPermitter.id}>, your'e a sneaky one arent you? editing {AidsPerson}'s permissions like that... well imma gonna have to say ***Nope***.")





















async def TagHelpersInOldTickets(bot: commands.Bot):
    for guild in bot.guilds:
        HelpWithTicketsChannel = None
        for channel in guild.channels:
            if '𝖧elp-𝖶ith-𝖳icket' in str(channel):
                HelpWithTicketsChannel = channel

        for channel in guild.channels:
            if 'ticket' in str(channel) and 'log' not in str(channel) and 'help' not in str(channel):
                TimePassedFromTicketOpening = round((datetime.now() - channel.created_at).total_seconds() / 60) - 180 # 180 is the time difference between discord server and bot server
                print(f'{channel}, in {guild}, was created at {channel.created_at}, aprox {TimePassedFromTicketOpening} Minutes ago!')

                if TimePassedFromTicketOpening > 4:
                    if 'waiting' not in str(channel):
                        print('has no waiting')
                        await channel.send(f'<@&746748255068487770>')
                        await channel.edit(name=(channel.name + '-waiting'))
                    else:
                        print('has waiting')
                        await HelpWithTicketsChannel.send(f'<@&746748255068487770>, {channel} is still open!')

                if TimePassedFromTicketOpening > 600:
                    print(f'Deleted {str(channel)} for inactivity after 10 hours!')
                    await channel.delete()


