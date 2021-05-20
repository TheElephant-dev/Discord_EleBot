


import EleDiscordLib
import EleAuditLog
import discord
import TicketFunctions



async def Util_ManuallySaveAuditLogCacheForAllGuilds(bot, ctx):
    if EleDiscordLib.IsMemberARole(ctx.author, ['program']):
        if EleDiscordLib.isCommandAllowedOnChannel('-+ManuallySaveAuditLogCacheForAllGuilds', ctx.channel):
            await EleAuditLog.SaveEleAuditLogCacheIntoDb(bot)



async def Util_Cleanup(bot, ctx):
    if EleDiscordLib.IsMemberARole(ctx.author, ['program']):
        # Delete channels in spam category and all tickets on server the command was ran on.
        try:
            for channel in ctx.message.channel.guild.channels:
                if 'ticket' in str(channel) and 'log' not in str(channel):
                    await channel.delete()
                if 'SPAM' in str(channel.category):
                    await channel.delete()
        except:
            pass

    
    
async def Util_PrintGetChannelAsHtmlString(bot, ctx):
    if EleDiscordLib.IsMemberARole(ctx.author, ['program']):
        print(f'printing {ctx.message.channel} as html')
        HTMLDATA = await TicketFunctions.GetChannelAsHtmlString(ctx.message.channel)
        with open(f'{ctx.channel}.html', 'w', encoding='utf-8-sig') as File:
            File.write(HTMLDATA)
        File = open(f'{ctx.channel}.html', 'r', encoding='utf-8')
        await ctx.channel.send(file=discord.File(File))
        File.close()
        os.remove(f'{ctx.channel}.html')
        print(f'Done printing {ctx.message.channel} as html')




async def Util_PrintCache(bot, ctx):
    print(EleAuditLog.GetEleAuditLogCache())
    if EleDiscordLib.isCommandAllowedOnChannel('-+PrintCache', ctx.channel):
        if EleDiscordLib.IsMemberARole(ctx.message.author, ['program', 'Staff Manager', 'Management', 'Owner']) == False:
            await ctx.send('You cannot use this command.(Supervisor+)')
            return
        await ctx.send(EleAuditLog.GetEleAuditLogCache())




async def Util_PrintIDCache(bot, ctx):
    if EleDiscordLib.isCommandAllowedOnChannel('-+PrintIDCache', ctx.channel):
        if EleDiscordLib.IsMemberARole(ctx.message.author, ['program', 'Staff Manager', 'Management' 'Owner']) == False:
            await ctx.send('You cannot use this command.(Supervisor+)')
            return

        Y = EleAuditLog.GetCurrentCacheAuditLogIds()
        for X in Y:
            print(X)
        await ctx.send(EleAuditLog.GetCurrentCacheAuditLogIds())



async def Util_CreateTicketCreatorMessage(bot, ctx):
    if EleDiscordLib.IsMemberARole(ctx.message.author, ['program', 'Management', 'Owner', 'Head of Programmers']) == True:
        TEXT = '📥אם אתם מעוניינים ברול כלשהו.\n'
        TEXT = TEXT + '📋 אם יש לכם שאלה/בקשה/רעיון כללי.\n'
        TEXT = TEXT + '✍️אם אתם רוצים שינוי שם.\n'
        TEXT = TEXT + '🗣️ אם אתם רוצים לדווח על משהו/מישהו'
        TEXT = TEXT + '\n\n'
        TEXT = TEXT + '📥 If youre interested in any role.\n'
        TEXT = TEXT + '📋 If you have a question/request/general idea.\n'
        TEXT = TEXT + '✍️If you want a nickname change.\n'
        TEXT = TEXT + '🗣️ if you want to report something/someone.ו'

        MSG = await ctx.send(embed=discord.Embed(title='לחצו על הריאקשן המתאים לפי הצורך שלכם בעזרה!', description=TEXT, color=0x2B2B2B))
        await MSG.add_reaction('📥')
        await MSG.add_reaction('📋')
        await MSG.add_reaction('✍️')
        await MSG.add_reaction('🗣️')