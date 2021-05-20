# Discord_EleBot
A discord Moderation, Staff Activity Tracking, Ticket System, Music, Staff Abuse Protection, - bot for discord.
A discord bot that relays on Role\Channel names rather then IDs. as to avoid the "setup" part of adding a bot.
The bot was originally made to run on 1 server, but made in a way that can run on any server by avoiding Hard-coded IDs.


- -+cmd - will print all the commends users should\can use in the discord server.

Moderation Command list:    
- -+ Audit - [Audit] - the original reason for the bot creation, it displays the following:
   Response:
      - Tickets Locked:
      - Tickets Unlocked: 
      - Tickets Saved: 
      - Tickets Deleted: 
      - Estimated Tickets: 
      - Help Requests: 
   Action:
      - Invites Created: 
      - Warns Given: 
      - Tempmutes Given: 
      - Infractions Checked: 
      - Audits Requested: 
   
   Activity:
      - Voice Activity: 
          - Manual Moves: 
          - Manual Moves To Investigation Room: 
   
   - Voice Control: 
          - Manual Mute:
          - Manual Unmute:
          - Manual Deafen:
          - Manual UnDeafen:
          - Manual Disconnect: 
   
   - Chat Control: 
          - Nickname Change: 
          - Messages Deleted: 
          - Messages Sent: 
   
   - Role Updates:
          - Passing 16+/18+: 
          - Amount of roles given: 
          - Amount of roles taken away: 
   
   - Channel Updates: 
          - Channel Info Updates: 
          - Created Channel Perm: 
          - Updated Channel Perm: 
          - Deleted Channel Perm: 
   
   - Administrative Actions: 
          - Kicks: 
          - Kicked users: 
          - Bans: 
          - Banned users:

- -+ GetVoiceChannelOfUser - [Audit] -  will send in chat all the names of voice channels a given user was on, and for how many days\hours\minutes\seconds.Such as the following:
         - #『🔒』Private 3    for 0 Days, 2 Hours, 10 Minutes and 14 Seconds.
         - #⭐Management⭐    for 0 Days, 2 Hours, 2 Minutes and 10 Seconds.
         - #👮🏼 Staff Talk 👮🏼    for 0 Days, 1 Hours, 57 Minutes and 22 Seconds.
         - #『🔒』Private 2    for 0 Days, 1 Hours, 49 Minutes and 45 Seconds.
         - #💫 Helpers 💫    for 0 Days, 0 Hours, 59 Minutes and 26 Seconds.
         - #『🔊』Talk 3    for 0 Days, 0 Hours, 52 Minutes and 45 Seconds.
     
- -+ CreateStaffTemplate - will create a copy-able ``` message that displays all the staff of a server, split into category of their roles.
- -+ AuditAll - [Audit] - Will Audit All the staff.
- -+ PrintAllRecords - [Audit] - Will print every entry of every action done by or that mentions @User. such as:
    - 2021-03-31 15:35 @[♙] Rotem RemovedRole @Adi RemovedRole [':video_game: | Gaming Notifications'] None
    - 2021-03-31 15:35 @[♗] Boaz AddedRole @Adi AddedRole [':mega: | Update Notifications'] None
    - 2021-03-31 02:16 @[♗] Daniel Nickname_Change @A...Venoבץ From [♙] Abu Shado To:[♙] Yaakubu None
    - 2021-03-31 02:18 @[♗] Daniel member_move <@None> None :confetti_ball: Event Staff :confetti_ball: <@826631736213504020> From: <AuditLogDiff deny=<Permissions value=0>                                                                                             deny_new='0'> To:<AuditLogDiff deny=<Permissions value=29360128> deny_new='29360128'> None
    - 2021-03-31 17:23 @[♗] Sagi member_move <@None> None :police_officer_tone2: Staff Talk :police_officer_tone2:
    - 2021-03-31 17:45 @[♗] Yuval member_move <@None> None 『:axe:』Fortnite
    
- -+ ClearUser - will delete the last 100 messages of a user within a given channel. (to be used by moderators with no ban perm.)
- -+ TagMissingHelpersInStaffCall - will tag every member with a "Helper" role not in the "staff meeting" channel.
- -+ TagMissing - will tag every member with a given role if not in a given voice chat.
- -+ SetNick - will set the nickname of a user, in a way that prevents anyone other then the bot itself or the command runner from reverting.
   
   
Misc Command list:
- -+ CreateTicketCreatorMessage - will generate a message to react to in order to open tickets.
- -+ SaveChannel - will send back an HTML file transcript of the entire channel history, images, and colors(with a max of 1000 messages.)
- -+ CreateTrackableVote - Creates an ibneded live-edited message with a given text (a question, suggestion or some other thing to vote on) that adds reactions to itelf then once a user reacts yes\no they cannot react again to change their vote. with a list of who voted what inside the original message, an internal countdown timer, and result.



General messing around Command list:
- -+ SendMeMaagarKodesh - will send a meme from the original server this bot was made for.
- -+ AddAdvancedCommmet - a way to keep notes on members in the server, that all staff has access to.
- -+ RemoveAdvancedCommmet - ^
- -+ ListAdvancedCommmet - ^
- -+ MoveChannelMembersFromTo - will move all members from a given channel to a given channel.
- -+ RandomMove\Trow - will randmly move a member between empty channels a given set amount of times, then return them to the original channel when done
- -+ GhostPing - will tag then delete a given member once in every non-essential text channel.
- -+ DC - will disconnect a user from any voice channel for a given amount of seconds.
- -+ SetMonthBestColor - will allow any user with the "month's best employee" role to change the role's color(and thus their display color) VIA a given Hex code.
- -+ GibAllRoles - will give all meaningless roles to a given user(roles with no permissions)



Debug Command list:
- -+ ManuallySaveAuditLogCacheForAllGuilds -  will save a the current staff action cache into the correct database file.
- -+ Cleanup - will delete all "ticket" channels that currently exist.
- -+ PrintCache - will print the current staff action cache into the console.
- -+ PrintIDCache - will print the current Audit Log IDs from cache to console.
- -+ PrintGetChannelAsHtmlString - will save an HTML file transcript of the entire channel history, images, and colors on the server the bot is running on.




Will also:
- Keep track of every action, message, or voice activity of a given user and save it on a daily database saved every minute.
- Give high staff all perms in every new channel opens of any kind by default.
- prevent low staff from using their power against high staff VIA retaliation, a private-custom-made image as a warning. and a note to that high staff member.
