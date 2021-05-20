import EleDiscordLib
import datetime
import asyncio
import discord
import AbuseProtection
import random
import EleAuditLog

async def MoveChannelMembersFromTo(bot, ctx, FromChannelID: int, ToChannelID: int):
    if EleDiscordLib.IsMemberARole(ctx.author, ['anag', 'owner']) == False:
        return

    F = bot.get_channel(FromChannelID)
    T = bot.get_channel(ToChannelID)
    for M in F.members:
        try:
            await M.move_to(T)
        except:
            pass


async def TurnMutedintoJewLovers(bot, ctx):
    print('Turning them into jews!')
    JewCounter = 0
    for M in ctx.guild.members:
        if EleDiscordLib.IsMemberARole(M, ['Muted']):
            JewCounter = JewCounter + 1
            if 'JewLover' not in str(M.nick):
                print(f'JewLover{JewCounter}')
                try:
                    await M.edit(nick=f'JewLover{JewCounter}', reason='Dror Approved')
                except discord.errors.Forbidden:
                    print(f"No perm to change {M}'s name into a jew.")




async def SwapChannelMembers(ctx, Channel1ID: int, Channel2ID: int):
        if EleDiscordLib.IsMemberARole(ctx.author, ['anag', 'owner']) == False:
            return

        Channel1 = bot.get_channel(Channel1ID)
        Channel2 = bot.get_channel(Channel2ID)
        Channel1Members = Channel1.members
        Channel2Members = Channel2.members

        for M in Channel1Members:
            try:
                await M.move_to(Channel2)
            except:
                pass
        for M in Channel2Members:
            try:
                await M.move_to(Channel1)
            except:
                pass



async def AbuzCmd_Trow(bot, ctx, Target: discord.Member, T: int):


    #Filter command to only be sent in a room inside the ""programmer" catagory
    if 'Programmer' not in str(ctx.channel.category) and 'פקודות-מנהלים' not in str(ctx.channel):
        return

    # Filter that allows only owners and programmers to run the command
    if EleDiscordLib.IsMemberARole(ctx.author, ['owner', 'gramm']) == False:
        await ctx.send(embed=discord.Embed(title="Denied.", description=f"You are not a server-owner. so you cannot use this command - <@187237265079009280>'s request", color=0x7C0200))
        return

    #Filter Based on Abuse priority
    if await AbuseProtection.CanAbuseTarget(ctx, ctx.author, Target)== False:
        return

    # Limit How many time it can be ran
    Times = 0
    MaxAllowed = AbuseProtection.GetProtectionPriorityOfMember(ctx.author, 'Normal')
    if T > MaxAllowed:
        Times = MaxAllowed
    else:
        Times = T

    #Add Action To Audit Log
    EleAuditLog.AddEntryToEleAuditLogCache([ctx.guild.id, [EleDiscordLib.GetCurrentDateAndHourMinute(), ctx.author.id, 'GhostPing', Target.id, Times, ctx.message.content]])

    #Run
    #print(f'{ctx.author} Requested the bot Trows {Target} {Times} Times!')
    await ctx.send(f'{ctx.author} Requested the bot Trows {Target} {Times} Times!')

    #Get All the empty voice channels
    EmptyVoiceChannels = []
    for C in ctx.guild.voice_channels:
        if len(C.members) == 0:
            EmptyVoiceChannels.append(C)

    #Make sure an empty channel exists
    if len(EmptyVoiceChannels) == 0:
        await ctx.send('Sorry, cannot do that. the server currently doesnt have an empty voice channel!')
        return

    #Move That member to the empty voice channel and back the ampunt of times reqested!
    TargetCurrentChannel = Target.voice.channel
    for T in range(Times):
        R_C = random.choice(EmptyVoiceChannels)
        print(f'{" " * T}Moved {Target} to {R_C}')
        try:
            await Target.move_to(R_C)
        except discord.errors.HTTPException:
            print(f'{Target} Tried to escape the bot!')
        await asyncio.sleep(0.5)

    await Target.move_to(TargetCurrentChannel)

    print(f'Moved {Target} back to {R_C}')




async def AbuzCmd_GhostPing(bot, ctx, Target: discord.Member, T: int):


    # Filter command to only be sent in a room inside the ""programmer" catagory
    if 'Programmer' not in str(ctx.channel.category) and 'פקודות-מנהלים' not in str(ctx.channel):
        await ctx.send(f'This command can only be used in "פקודות-מנהלים" or any channel under the "Programmer" Category')
        return


    
    # Filter Based on Abuse priority
    if await AbuseProtection.CanAbuseTarget(ctx, ctx.author, Target) == False:
        await ctx.send(f'You cannot Ghostping someone with a higher abuse protection priority.')
        return

    # Limit How many time it can be ran
    Times = 0
    MaxAllowed = round(AbuseProtection.GetProtectionPriorityOfMember(ctx.author, 'Normal') / 3)
    if T > MaxAllowed:
        Times = MaxAllowed
    else:
        Times = T

    # Add Action To Audit Log
    EleAuditLog.AddEntryToEleAuditLogCache([ctx.guild.id, [EleDiscordLib.GetCurrentDateAndHourMinute(), ctx.author.id, 'GhostPing', Target.id, Times, ctx.message.content]])


    #Run
    ValidTextChannels = []

    InvalidCatagoryNames = ['logs', 'Private', 'Giveaway', 'Important']
    InvalidChannelNames = ['עדכונ', 'update', 'עברו', 'update']


    for C in ctx.guild.text_channels:
        IsValidChannel = True
        for InvalidCatag in InvalidCatagoryNames:
            if InvalidCatag.lower() in str(C.category).lower():
                IsValidChannel = False

        for InvalidChann in InvalidChannelNames:
            if InvalidChann.lower() in str(C).lower():
                IsValidChannel = False

        if IsValidChannel == True:
            ValidTextChannels.append(C)



    await ctx.send(f'{ctx.author} Requested the bot GhostPings {Target} {Times} Times in all {len(ValidTextChannels)} Channels!')
    print(f'{ctx.author} Requested the bot ghostpings {Target} {Times} Times in all {len(ValidTextChannels)} Channels!')



    for Time in range(Times):
        TimesGostPinged = -1

        for C in ValidTextChannels:
            MSG = None
            try:
                TimesGostPinged = TimesGostPinged + 1
                MSG = await C.send(f'<@{Target.id}> **Yeet!**')
                print(f'{" " * TimesGostPinged}{" " * Time}{TimesGostPinged}.GhostPinging {Target} at {C}')
            except AttributeError:
                print(f'{" " * TimesGostPinged}{" " * Time}{TimesGostPinged}.Could not find a channel with the ID "{C_id}"')

            try:
                await MSG.delete()
            except:
                #print(f'{" " * TimesGostPinged}{" " * Time}Could not find the message to delete!')
                pass





async def AbuzCmd_CreateRussianRoulette(bot, ctx, RequestedTimes: int):

    if await EleDiscordLib.isCommandAllowedOnChannel('-+RussianRoulette', ctx.channel) == False:
        return


    # Filter max amount of shots to be taken
    Times = 10
    if RequestedTimes < 10:
        Times = RequestedTimes


    #Create the Pistol Message
    RouletteMember = ctx.author
    PistolEmbed = discord.Embed(title="Russian Roulette",description=f"<@{RouletteMember.id}> Picked up the pistol, with the intention of shooting it **{Times}** times!",color=0xD32F2F)
    PistolMessgae = await ctx.send(embed=PistolEmbed)


    #await PistolMessgae.add_reaction('🔒')

    def CheckIfGunFired(reaction, user):
        if reaction.message.id == PistolMessgae.id:
            if str(reaction.emoji) == '🔫':
                return PistolMessgae.author and reaction


    for T in range(Times):
        # Check if user clicked the lock reaction
        try:
            # print('Waiting For a reaction...')
            await PistolMessgae.add_reaction('🔫')

            #     and make sure the bot isnt reacting to itself out of desync
            reaction, user = None, None
            ShooterMemberID = 789942343619969074
            while ShooterMemberID != RouletteMember.id:
                reaction, user = await bot.wait_for('reaction_add', timeout=10.0, check=CheckIfGunFired)
                ShooterMemberID = user.id
            await PistolMessgae.remove_reaction(reaction, user)
        except asyncio.TimeoutError:
            print('Timed out with no correct reaction!')
            PistolEmbed.add_field(name=f'Timed Out..', value=f"<@{RouletteMember.id}>'s hand shook too much, the gun fell from their hand!", inline=False)
            await PistolMessgae.edit(embed=PistolEmbed)
            break
            pass
        else:
            #Choose What Chamber the bullet is in
            BulletLocation = random.randint(0, 5)
            ShouldDisconnet = False

            # Act based on what Chamber the bullet is in
            if BulletLocation == 0:
                if RouletteMember.id == 134156783450062848:
                    ShotResultText = f'The Gun fired and.... <@{RouletteMember.id}> Was unharmed, as they are immortal!'
                else:
                    ShotResultText = f'<@{RouletteMember.id}> Was Shot!'
                    ShouldDisconnet = True

                    print(f'>>>>>>>>>>>>>>>>>>>>>>> DISCONNECTED {RouletteMember}')
            else:
                ShotResultText = f'Sadly, <@{RouletteMember.id}> Survived.'


            #Edit the original Message to keep track of what happend
            PistolEmbed.add_field(name=f'In Shot #{T + 1} the Bullet was in chamber Number #{BulletLocation}...', value=ShotResultText, inline=False)
            await PistolMessgae.edit(embed=PistolEmbed)


            if ShouldDisconnet == True:
                for X in range(10):
                    try:
                        await RouletteMember.move_to(None)
                    except:
                        pass
                    await asyncio.sleep(0.5)






#DisconnectableUsers
async def AbuzCmd_KeepDisconnected(ctx, Target: discord.Member, T: int):
    # Filter command to only be sent in a room inside the ""programmer" catagory
    if 'Programmer' not in str(ctx.channel.category) and 'פקודות-מנהלים' not in str(ctx.channel):
        await ctx.send(
            f'This command can only be used in "פקודות-מנהלים" or any channel under the "Programmer" Category')
        return

    # Filter Based on Abuse priority
    if await AbuseProtection.CanAbuseTarget(ctx, ctx.author, Target) == False:
        return

    Time = 10
    if T < 10:
        Time = T
    for X in range(Time * 2):
        try:
            await Target.move_to(None)
            print(f'{ctx.author} DC-Disconnected {Target}')
        except:
            pass
        await asyncio.sleep(0.5)



async def GibAllRoles(ctx, Target):

    #Filter command to only be sent in a room inside the ""programmer" catagory
    if 'Programmer' not in str(ctx.channel.category) and 'פקודות-מנהלים' not in str(ctx.channel):
        return

    #Filter Based on Abuse priority
    if await AbuseProtection.CanAbuseTarget(ctx, ctx.author, Target)== False:
        Victim = ctx.author
        X = await ctx.send(embed=discord.Embed(title="Denied.",description=f"You Cannot Give roles to someone with a Higher protection!\n\n **Y E E T !** take the roles yourself!",color=0x7C0200))
        await X.delete(delay=10)
    else:
        Victim = Target




    # add all the allowed roles into the list
    RolesToGiveNames = ['otif', 'voice ', 'chat', 'DJ', '16+', '18+', 'project', 'GTA', 'fortnite', 'Among', 'Brawl','Legends', 'valorant', 'active']
    BlackListedRoles = ['owner', 'Among Us ']

    RolesToAddList = []
    for role in ctx.guild.roles:
        ShouldAddRole = False
        for AR in RolesToGiveNames:
            if AR.lower() in str(role).lower():
                if role not in Victim.roles:
                    ShouldAddRole = True

        for RR in BlackListedRoles:
            if RR.lower() in str(role).lower():
                ShouldAddRole = False


        if ShouldAddRole:
            RolesToAddList.append(role)
            print(f'Adding >>>{role}<<< to the list of roles to add!')

    #Actually add the roles from the list to the user
    await Victim.add_roles(*RolesToAddList)
    print(f'DONE. Added All those roles to {Victim}')
