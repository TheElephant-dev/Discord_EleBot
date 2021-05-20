import discord
from discord.ext import commands
import asyncio
import os
import math
import sqlite3
import datetime
import random

import EleDiscordLib

async def InsertAdvCommentIntoDatabase(bot: commands.Bot(command_prefix='-+'), ctx, Commenter: discord.Member, TargetMember: discord.Member, CommentType: str, Comment: str):

    if EleDiscordLib.IsMemberARole(ctx.author, ['Head Of Advanced', 'Advanced Judge', 'Advanced tester', 'program']) == False:
        await ctx.send('You are not a Tester, Judge or Head Of Advanced!')
        return

    if EleDiscordLib.IsMemberARole(ctx.author, ['Advanced tester']) and EleDiscordLib.IsMemberARole(TargetMember, ['Head Of Advanced', 'Advanced Judge', 'Advanced tester']):
        await ctx.send('You cannot comment on other testers!')
        return

    # Filter User Input to make sure it will match the correct format
    if CommentType not in ['good', 'bad']:
        await ctx.send(f'{CommentType} is not "Good" or "Bad".')
        return



    #Make sure user wants to add this at its current form.
    ConfirmEmbededMsgTemplate = discord.Embed(title=f'Advanced Comment Confirmation', description='Are you sure you want to add this?', color=0x1EC45C)
    ConfirmEmbededMsgTemplate.add_field(name='Commenter:', value=f'<@{Commenter.id}>', inline=True)
    ConfirmEmbededMsgTemplate.add_field(name='Target:', value=f'<@{TargetMember.id}>', inline=True)
    ConfirmEmbededMsgTemplate.add_field(name='Type:', value=f'{CommentType}', inline=True)
    ConfirmEmbededMsgTemplate.add_field(name='Comment Itself:', value=f'{Comment}', inline=True)

    ConfirmationMessage = await ctx.send(embed=ConfirmEmbededMsgTemplate)



    # Add the reactions
    await ConfirmationMessage.add_reaction('❌')
    await ConfirmationMessage.add_reaction('✅')

    def check(reaction, user):
        if str(reaction.emoji) in ['❌', '✅']:
            if reaction.message.id == ConfirmationMessage.id:
                return ConfirmationMessage.author and reaction


    # wait for user comfirmation and time out after 60 seconds
    try:
        ClickerID = None
        while ClickerID != Commenter.id:
            reaction, user = await bot.wait_for('reaction_add', timeout=60.0, check=check)
            ClickerID = user.id

            if user.bot == False:
                await ConfirmationMessage.remove_reaction(reaction, user)

    except asyncio.TimeoutError:
        print('  Advanced Comment Confirmation Timed out...')

    else:
        #print('Proceed....')
        await ConfirmationMessage.delete()
        if str(reaction) == '✅':
            DataBasePath = f'./Logs/{ctx.guild.id}/AdvancedComments.db'


            # check if the guild has a  advanced comments database
            if os.path.exists(DataBasePath) == False:
                Connection = sqlite3.connect(DataBasePath)
                Cursor = Connection.cursor()
                try:
                    # Try to Create table
                    Cursor.execute(
                        '''CREATE TABLE AdvandedComments (datetime text, ID int, UserID int, CommentType text, Target int, Comment text)''')
                    print(f'>Created a new Advanced Comments database for guild({ctx.guild}) as {DataBasePath}..')
                except:
                    # print(f'>EleSQLFunctions: Failed to create new database, likely "{Name}" already exists.')
                    pass
                Connection.commit()
                Connection.close()


            # Add entry to database
            DTN = datetime.datetime.now()
            DTNNoMili = str(DTN.date()) + ' ' + str(DTN.hour) + ':' + str(DTN.minute)

            print(f'  > {DTN} >SQL Inserted Data into:{DataBasePath}')
            Connection = sqlite3.connect(DataBasePath)
            Cursor = Connection.cursor()


            #Extract Highest ID
            for X in Cursor.execute(f'SELECT MAX(ID) AS Biggest FROM AdvandedComments;'):
                for Y in X:
                    if Y != None:
                        AdvCmtID = int(Y) + 1
                    else:
                        AdvCmtID = 0

            Cursor.executemany('INSERT INTO AdvandedComments VALUES (?,?,?,?,?,?)', [[DTNNoMili, AdvCmtID, Commenter.id, CommentType, TargetMember.id, Comment]])
            Connection.commit()
            Connection.close()







async def RemoveAdvCommentIntoDatabase(bot, ctx, ID):
    if EleDiscordLib.IsMemberARole(ctx.author, ['Head Of Advanced', 'Advanced Judge', 'program']) == False:
        await ctx.send('You are not a Judge or Head Of Advanced!')
        return

    DataBasePath = f'./Logs/{ctx.guild.id}/AdvancedComments.db'

    #Get Entry from ID
    Connection = sqlite3.connect(DataBasePath)
    Cursor = Connection.cursor()
    SelectedEntry = None
    for X in Cursor.execute(f'SELECT * FROM AdvandedComments WHERE ID={ID};'):
        SelectedEntry = X
    Connection.commit()
    Connection.close()


    #if the Database doesnt have an entry with this ID skip everything
    if SelectedEntry == None:
        await ctx.send(embed=discord.Embed(title=f'No Entry with ID #{ID} Found!', color=0x1EC45C))
        return



    #Pull Data from database on the entry
    ConfirmEmbededMsgTemplate = discord.Embed(title=f'Advanced Comment Confirmation', description=f'Are you sure you want to **Remove** Entry #{SelectedEntry[1]} from the database?', color=0x1EC45C)
    ConfirmEmbededMsgTemplate.add_field(name='At:', value=f'{SelectedEntry[0]}', inline=True)
    ConfirmEmbededMsgTemplate.add_field(name='Commenter:', value=f'<@{SelectedEntry[2]}>', inline=True)
    ConfirmEmbededMsgTemplate.add_field(name='Target:', value=f'<@{SelectedEntry[4]}>', inline=True)
    ConfirmEmbededMsgTemplate.add_field(name='Type:', value=f'{SelectedEntry[3]}', inline=True)
    ConfirmEmbededMsgTemplate.add_field(name='Comment Itself:', value=f'{SelectedEntry[5]}', inline=False)
    ConfirmationMessage = await ctx.send(embed=ConfirmEmbededMsgTemplate)

    # Add the re
    # actions
    await ConfirmationMessage.add_reaction('❌')
    await ConfirmationMessage.add_reaction('✅')


    # wait for user comfirmation and time out after 60 seconds
    def check(reaction, user):
        if str(reaction.emoji) in ['❌', '✅']:
            if reaction.message.id == ConfirmationMessage.id:
                return ConfirmationMessage.author and reaction


    try:
        ClickerID = None
        while ClickerID != ctx.message.author.id:
            reaction, user = await bot.wait_for('reaction_add', timeout=60.0, check=check)
            ClickerID = user.id

            if user.bot == False:
                await ConfirmationMessage.remove_reaction(reaction, user)

    except asyncio.TimeoutError:
        print('  Advanced Comment Confirmation Timed out...')

    else:

        self = ctx.guild.get_member(789942343619969074)
        if str(reaction) == '✅':
            # remove the bot's reactions
            await ConfirmationMessage.remove_reaction('❌', self)
            await ConfirmationMessage.remove_reaction('✅', self)
            await ConfirmationMessage.edit(embed=discord.Embed(title=f'Advanced Comment Removed', description=f'Advanced Comment #{SelectedEntry[1]} Was Removed by <@{ctx.message.author.id}>.\n', color=0x1EC45C))
            try:
                Connection = sqlite3.connect(DataBasePath)
                Cursor = Connection.cursor()
                Cursor.execute(f'DELETE FROM AdvandedComments WHERE ID={ID};')
                Connection.commit()
                Connection.close()
            except:
                pass
        else:
            await ConfirmationMessage.delete()



async def ListAdvCommentIntoDatabase(bot, ctx, Target):

    if EleDiscordLib.IsMemberARole(ctx.author, ['Head Of Advanced', 'Advanced Judge', 'Advanced tester', 'program']) == False:
        await ctx.send('You are not a part of the advanced staff!')
        return

    DataBasePath = f'./Logs/{ctx.guild.id}/AdvancedComments.db'

    #Get Entry from ID
    Connection = sqlite3.connect(DataBasePath)
    Cursor = Connection.cursor()
    DatabaseEntries = []
    for X in Cursor.execute(f'SELECT * FROM AdvandedComments WHERE Target={Target.id};'):
        DatabaseEntries.append(X)
    Connection.commit()
    Connection.close()

    # Filter Entries into 2 lists. good and bad.
    Good_DatabaseEntries = []
    Bad_DatabaseEntries = []
    for Entry in DatabaseEntries:
        if Entry[3] == 'bad':
            Bad_DatabaseEntries.append(Entry)
        elif Entry[3] == 'good':
            Good_DatabaseEntries.append(Entry)

    await SendEntriesmessages(ctx, Good_DatabaseEntries, 'Good', 0x34D100)
    await SendEntriesmessages(ctx, Bad_DatabaseEntries, 'Bad', 0xD12900)



async def SendEntriesmessages(ctx, Array, State, Color):
    X = 0
    # Split the entries into sections of 4
    for Y in range(math.ceil(len(Array) / 4)):
        EntriesToSend = []
        for Z in range(4):
            try:
                EntriesToSend.append(Array[X])
            except:
                pass
            X = X + 1

        EntriesMessage = discord.Embed(title=f'{State} Entries #{X-4}-{X}', description='**"-+RemAdvCmt ID"** to remove a comment.\nID being the IDnumber.', color=Color)
        for EntryNum in range(len(EntriesToSend)):
            E = EntriesToSend[EntryNum]
            EntriesMessage.add_field(name=f'-------Entry #{X + EntryNum} At {E[0]}, with ID: {E[1]}---------', value=f'<@{E[2]}> Said the following **{E[3]}** comment about <@{E[4]}>\n"\n{E[5]}\n"', inline=False)
        await ctx.send(embed=EntriesMessage)











