# coding=utf8
import sys
import discord
from discord.ext import commands
import pandas
from discord import CategoryChannel
from time import sleep
import sqlite3
import datetime
import asyncio
import os
import random


import EleDiscordLib
import EleImageGenerator
import EleAuditLog
import EleVoiceTimeTracking
import EleCycleActions


from CommandLibs import EleUtilityCommands, EleDebugCommands, EleModerationCommands, EleAbuseCommands

import AbuseProtection
import CommandCooldown
import TicketFunctions

import FakeAdvanced_Commands






intents = discord.Intents.all()
bot = commands.Bot(command_prefix='-+', intents=intents)
print('bot exists! awaiting trigger.', end='')






################################################################################################################################################
################################################################################################################################################
####################################################### ABUZS ##################################################################################




####################################################### ABUZS ##################################################################################
################################################################################################################################################
################################################################################################################################################


##############################################################################################################################################
################################################################# EVENTS #####################################################################
@bot.event
async def on_voice_state_update(member, before, after):
    await EleVoiceTimeTracking.TrackVoiceTime(bot, member, before, after)
    await AbuseProtection.ProcessAbuse(bot, member, before, after)




@bot.event
async def on_guild_channel_create(channel):
    for role in channel.guild.roles:
        if 'anagement' in str(role) or 'Head of Programmers' in str(role):
            await channel.set_permissions(role, read_messages=True, manage_channels=True,
                                          manage_permissions=True, manage_webhooks=True,
                                          create_instant_invite=True, send_messages=True, embed_links=True,
                                          attach_files=True, add_reactions=True, use_external_emojis=True,
                                          mention_everyone=True, manage_messages=True,
                                          read_message_history=True, send_tts_messages=True, connect=True, speak=True,
                                          stream=True, move_members=True, deafen_members=True, mute_members=True,
                                          use_voice_activation=True,
                                          reason='Admin Channel Perm Setter')

@bot.event
async def on_raw_reaction_add(payload):
    #Check if a ticket should be opened
    await TicketFunctions.CheckIfTicketShouldBeOpened(bot, payload)


################################################################### EVENTS #####################################################################
################################################################################################################################################
################################################################ Debug Commands ################################################################



@bot.command()
async def ManuallySaveAuditLogCacheForAllGuilds(ctx,):
    await EleDebugCommands.Util_ManuallySaveAuditLogCacheForAllGuilds(bot, ctx)



@bot.command(aliases=['C', 'c'])
async def Cleanup(ctx):
    await EleDebugCommands.Util_Cleanup(bot, ctx)


@bot.command()
async def PrintGetChannelAsHtmlString(ctx):
    await EleDebugCommands.Util_PrintGetChannelAsHtmlString(bot, ctx)



@bot.command()
async def PrintCache(ctx):
    await EleDebugCommands.Util_PrintCache(bot, ctx)


@bot.command()
async def PrintIDCache(ctx):
    await EleDebugCommands.Util_PrintIDCache(bot, ctx)


@bot.command()
async def CreateTicketCreatorMessage(ctx):
    await EleDebugCommands.Util_CreateTicketCreatorMessage(bot, ctx)

@bot.command(aliases=['GVCOU'])
async def GetVoiceChannelOfUser(ctx, Member: discord.Member, From, To):
    VoiceChannels = await EleVoiceTimeTracking.GetTop5VoiceChannelsOfUser(bot, ctx, Member, From, To)
    Text = ''
    for C in VoiceChannels:
        Text = Text + f'<#{C[2]}> for {EleDiscordLib.TurnSecondsIntoDayHourMinuteSecond(C[0])}\n'
    await ctx.send(Text)

@bot.command()
async def SendMeMaagarKodesh(ctx):
    await ctx.send(f'http://kodesh.snunit.k12.il/images/menu/header.jpg')
############################################################### Debug Commands ################################################################
###############################################################################################################################################
################################################################# COMMANDS ####################################################################

@bot.command(aliases=['CMD'])
async def cmd(ctx):
    await EleUtilityCommands.Util_EleCMD(bot, ctx)


@bot.command(aliases=['permit', 'p', 'P'])
async def Permit(ctx, PermitMember: discord.Member):
    if 'ticket-' in ctx.message.channel.name:
        if EleDiscordLib.isCommandAllowedOnChannel('-+Permit', ctx.channel):
            if EleDiscordLib.IsMemberARole(ctx.author, ['Helper', 'Staff Manager', ' | Admin']):
                await ctx.message.channel.set_permissions(PermitMember, view_channel=True, send_messages=True, add_reactions=True, reason=f'Add Permission to handle {ctx.message.channel}')
                await ctx.send(embed=discord.Embed(title='', description=f"<@{ctx.message.author.id}> permitted <@{PermitMember.id}>", color=0xBC4ACE))


@bot.command(aliases=['CST'])
async def CreateStaffTemplate(ctx):
    await EleUtilityCommands.Util_EleStaffTemplate(bot, ctx)



@bot.command(aliases=['audit', 'A'])
async def Audit(ctx, AuditMember: discord.Member, FromDate = '1111/11/11', ToDate = '1111/11/12'):
    await EleModerationCommands.ModCmd_Audit(bot, ctx, AuditMember, FromDate, ToDate, 'A')



@bot.command(aliases=['auditall', 'AA'])
async def AuditAll(ctx, FromDate = '1111/11/11', ToDate = '1111/11/12'):
    for MEMBER in ctx.guild.members:
        if EleDiscordLib.IsMemberARole(MEMBER, ['helper']):
            await EleModerationCommands.ModCmd_Audit(bot, ctx, MEMBER, FromDate, ToDate, 'AA')


@bot.command(aliases=['PAR'])
async def PrintAllRecords(ctx, AuditMember : discord.Member, FromDate = '1111/11/11', ToDate = '1111/11/12', Type = 'All'):
    await EleModerationCommands.ModCmd_PrintAllRecords(bot, ctx, AuditMember, FromDate, ToDate)


@bot.command()
async def ClearUser(ctx, MemberToClear: discord.Member, Amount: int):
    await EleModerationCommands.ModCmd_ClearUser(bot, ctx, MemberToClear, Amount)


@bot.command(aliases=['CTV'])
async def CreateTrackableVote(ctx, TimeoutMinutes: int):
    await EleUtilityCommands.CreateTrackableVote(bot, ctx, TimeoutMinutes * 60)




####################################### Advanced Commands
@bot.command(aliases=['AddAdvCmt'])
async def AddAdvancedCommmet(ctx, TargetMember: discord.Member):
    Words = ctx.message.content.split(' ')
    await FakeAdvanced_Commands.InsertAdvCommentIntoDatabase(bot, ctx, ctx.message.author, TargetMember, Words[2].lower(), ' '.join(Words[3:]))


@bot.command(aliases=['RemAdvCmt'])
async def RemoveAdvancedCommmet(ctx, ID: int):
    await FakeAdvanced_Commands.RemoveAdvCommentIntoDatabase(bot, ctx, ID)

@bot.command(aliases=['ListAdvCmt'])
async def ListAdvancedCommmet(ctx, Target: discord.Member):
    await FakeAdvanced_Commands.ListAdvCommentIntoDatabase(bot, ctx, Target)

@bot.command()
async def TagMissingHelpersInStaffCall(ctx):
    await EleModerationCommands.TagMissingHelpersInStaffCall(ctx)

@bot.command()
async def TagMissing(ctx, RoleString, ChannelID: int):
    await EleModerationCommands.TagMissing(ctx, bot, RoleString, ChannelID)

@bot.command()
async def SetNick(ctx, Member: discord.Member, nick):
    await Member.edit(nick=ctx.message.content[33:])



@bot.command()
async def SaveChannel(ctx):
    if EleDiscordLib.IsMemberARole(ctx.author, ['anag', 'owner']) == False:
        return

    HtmlCodeOfChannel = await TicketFunctions.GetChannelAsHtmlString(ctx.channel)
    with open(f'transcript-Ticket-ManualCommand.html', 'w', encoding='utf-8') as TranscriptFile:
        TranscriptFile.write(HtmlCodeOfChannel)
    TanscriptFile = open(f'transcript-Ticket-ManualCommand.html', 'r', encoding='utf-8')
    await ctx.channel.send(file=discord.File(TanscriptFile))
    TanscriptFile.close()
    os.remove(f'transcript-Ticket-ManualCommand.html')



# ################################################################## COMMANDS ####################################################################
################################################################################################################################################
################################################################ Fun Commands ##################################################################


@bot.command(aliases=['MovCnlMemsFrmTo', 'MCMFT'])
async def MoveChannelMembersFromTo(ctx, FromChannelID: int, ToChannelID: int):
    await EleAbuseCommands.MoveChannelMembersFromTo(bot, ctx, FromChannelID, ToChannelID)
#

@bot.command()
async def RandomMove(ctx, Member: discord.Member, ReapeatTimes: int = 1):
    if ctx.author.id != 134156783450062848:
        return

    AllVoiceChannels = []
    for channel in ctx.guild.channels:
        if str(channel.type) == 'voice':
            if 'TALK'.lower() in str(channel.name).lower():
                AllVoiceChannels.append(channel)
    for X in range(ReapeatTimes):
        try:
            C = random.choice(AllVoiceChannels)
            await Member.move_to(C)
            print(f'Moveing {Member.nick} to {str(C)}.')
        except:
            pass
        await asyncio.sleep(1)




@bot.command()
async def GhostPing(ctx, Target: discord.Member, Times: int = 1):
    await EleAbuseCommands.AbuzCmd_GhostPing(bot, ctx, Target, Times)





@bot.command()
async def DC(ctx, Target: discord.Member, Times: int = 1):
    await EleAbuseCommands.AbuzCmd_KeepDisconnected(ctx, Target, Times)

@bot.command(aliases=['ביקורמדינה'])
async def Trow(ctx, Target: discord.Member, Times: int = 1):
    await EleAbuseCommands.AbuzCmd_Trow(bot, ctx, Target, Times)




@bot.command(aliases=['SMBC'])
async def SetMonthBestColor(ctx, HexCode: discord.Color):
    await EleUtilityCommands.SetMonthBestColor(ctx, HexCode)

@bot.command(aliases=['GAR', 'הפצצתרולים'])
async def GibAllRoles(ctx, VictimCheck: discord.Member):
    await EleAbuseCommands.GibAllRoles(ctx, VictimCheck)




################################################################ Fun Commands ##################################################################
################################################################################################################################################
############################################################### Handle messages ################################################################



@bot.event
async def on_message(message):

    ##################################################################################################
    # "Catch" the ticket for helpers

    #if channel is a ticket
    if isinstance(message.channel, discord.channel.DMChannel) == False:

        #Catch tickets
        await TicketFunctions.CatchTicketForFirstHelper(message)


        #COMMANDS
        await EleAuditLog.HandleTempmuteWarnInfractionsInEleAuditLog(bot, message)

        # MESSAGES
        await EleAuditLog.HandleTupalAvarInEleAuditLog(message)

        await bot.process_commands(message)






############################################################### Handle messages ################################################################
################################################################################################################################################


async def RunOnSecondProcessEveryMinute(bot):
    pass

    MinutesPassed = 0
    while True:
        MinutesPassed = MinutesPassed + 1
        for ProcessTimer in range(6):
            #print(f'ProcessTimer = {ProcessTimer}')
            await EleAuditLog.CheckLast50AuditLogs_Of_All_Guilds(bot)
            await EleCycleActions.KeepRolaxRole(bot)
            await EleCycleActions.EnforceEleChannelPerms(bot)



            if ProcessTimer == 0:
                await EleAuditLog.SaveEleAuditLogCacheIntoDb(bot)


            await asyncio.sleep(10)
        #print(f'MinutesPassed = {MinutesPassed}')
        if MinutesPassed == 5:
            await EleCycleActions.TagHelpersInOldTickets(bot)
            pass
        elif MinutesPassed == 61:
            MinutesPassed = 0




################################################################################################################################################
############################################################### Run Bot ########################################################################


def Runbot(bot):
    @bot.event
    async def on_ready():
        print(' . . . ', end='')
        await bot.change_presence(status=discord.Status.do_not_disturb, activity=discord.Game("Removal of Elephant's will to live"))
        EleDiscordLib.clearAllOpenTicketFiles(bot)
        # for Guild in bot.guilds:
        #     await Guild.chunk()
        # print(' chunked all guilds...', end='')

        #Remove all records of open tickets
        bot.loop.create_task(RunOnSecondProcessEveryMinute(bot))
        print(f'And Logged in as {bot.user.name}')


    bot.run(' ### TOKEN HERE ###') #Elemodbot



Runbot(bot)