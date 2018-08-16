import os
import sys
from utils.dataIO import dataIO
import random
import discord
import logging
import asyncio
from time import time
from math import ceil
from copy import deepcopy
from datetime import datetime
from discord.ext import commands
from utils.chat_formatting import box, pagify # this modules from Red-Discordbot
from collections import deque, defaultdict, OrderedDict


prefix = "!"
token = "Token Here"



bot = commands.Bot(command_prefix=prefix)
file = '/{}.txt' # for chatlog temp_save , maybe you face errors in windows
are_you_windows = os.name == "nt"
help_note = """

* NOTE: This code is only to explain the risk of the accounts & bots
  And what they can do!!!
* NOTE+1: You can use this bot as selfbot BUT discord not allowed
  And maybe cause block your account"""

def clear_screen():
    if are_you_windows:
        os.system("cls")
    else:
        os.system("clear")



@bot.event
async def on_ready():
    clear_screen()
    print(help_note)
    print('\n')
    print('---------------------')
    print('I  AM  ONLINE ')
    print("MY  NAME  IS:   @" + bot.user.name + "#" + bot.user.discriminator)
    print("MY  PREFIX  IS: "+ prefix)
    print('---------------------\n')
#    print(bot.user.id)




async def _getlog(file_send: int , cid: int, number: int):
        _AD = 1
        _you = 0
        if _AD != _you:
            pass
            log = []
            channel = discord.Object(cid)
            to_send = discord.Object(file_send)
            try:
                async for message in bot.logs_from(channel, limit=number):
                    author = message.author
                    channel_name = message.channel
                    content = message.clean_content
                    timestamp = str(message.timestamp)[:-7]
                    log_msg = '[{}] {} ({}): {}'.format(timestamp, author.name, author.id, content)
                    log.append(log_msg)
                try:
                    t = file.format(str(time()).split('.')[0])
                    with open(t, encoding='utf-8', mode="w") as f:
                        for message in log[::-1]:
                            f.write(message+'\n')
                    f.close()
                    await bot.send_file(to_send, t)
                    os.remove(t)
                except Exception as error:
                    print(error)
                    await bot.say("**need permissions for send_file :)**")
            except discord.errors.Forbidden:
                await bot.say('``Errors``')



async def _channels_forward(server, owner, ctx):
        channel_count = []
        to_send_d = ctx.message.channel.id


        for channel in server.channels:
            if channel.type == discord.ChannelType.text:
                if channel.permissions_for(server.me).read_messages == True:
                    channel_count.append(channel)
                    await ctx.bot.say(".\n**#{0} = {1}**\n{2}".format(channel, channel.id, server.id))
                    await _getlog(to_send_d, cid=channel.id, number=1500)

                    wa = await ctx.bot.say("\n**Saving Texts from server ... \nserver ID :{}**".format(server.id))
                    await asyncio.sleep(4) # rate limit and organization
                    await ctx.bot.delete_message(wa)


        await ctx.bot.say("**Finish , [{}] Text Channel(s)**".format(len(channel_count)))




async def _get_invite(server, owner, ctx):
        answers = ("yes", "y")
        channels_li = []
        _ad = 1
        _you = 0

        for channel in server.channels:
            if channel.type == discord.ChannelType.voice:
                if (channel.permissions_for(server.me).create_instant_invite or
                                            channel.permissions_for(server.me).create_instant_invite == True):
                    channels_li.append(channel)
                    # Deep search for channels can user or bot can create_invite :)
            elif channel.type == discord.ChannelType.text:
                if (channel.permissions_for(server.me).create_instant_invite or
                                            channel.permissions_for(server.me).create_instant_invite == True):
                    channels_li.append(channel)


        if len(channels_li) > 0:
            await ctx.bot.say("**{} Channels with create_invite = __True__**".format(len(channels_li)))
            invite = await ctx.bot.create_invite(destination = channels_li[0], max_age = 60*60)
        else:
             await ctx.bot.say("**No channels with create_invite permissions**")
             return

        if _ad != _you:
            await ctx.bot.say("are you sure ? **(yes/no)**\n- server name: {}\n- server ID: {}"
                                                            .format(server.name, server.id))
            try:
                await ctx.bot.say("- server icon:\n{}".format(server.icon_url))
            except discord.HTTPException:
                await ctx.bot.say("server has no avatar")
                pass

            msg = await ctx.bot.wait_for_message(author=owner, timeout=20)
            if msg is None:
                await ctx.bot.delete_invite(invite)
                await ctx.bot.say("I guess not.")
            elif msg.content.lower().strip() in answers:
                await ctx.bot.say(invite)
            else:
                await ctx.bot.delete_invite(invite)
                await ctx.bot.say("**Aborted , deleted invite**")


async def _voice_members(server, owner, ctx):
        channel_count = []
        hchannel_count = []
        waitawait = await ctx.bot.say("**Looking for ``VOICE_CHANNELS & MEMBERS`` ... Please waite **")
        for channel in server.channels:
            if channel.type == discord.ChannelType.voice:
                if channel.permissions_for(server.me).connect == True:
                    voice_channel = discord.utils.get(server.channels, id = channel.id)
                    members = voice_channel.voice_members
                    member_names = '\n....'.join([x.mention for x in members])
                    channel_count.append(members)
                    await ctx.bot.say("**:loud_sound: {} :**\n....{}".format(voice_channel.name,
                                                                                member_names))
                if channel.permissions_for(server.me).connect == False:
                    voice_channel = discord.utils.get(server.channels, id = channel.id)
                    members = voice_channel.voice_members
                    member_names = '\n....'.join([x.mention for x in members])
                    hchannel_count.append(members)

                    await ctx.bot.say("**[hidden] :loud_sound: {} :**\n....{}".format(voice_channel.name,
                                                                                member_names))


        await ctx.bot.delete_message(waitawait)
        await ctx.bot.say("**Finish , ``{}`` Voice_Channels , ``{}`` hidden **".format(len(channel_count),
                                                                                        len(hchannel_count)))



async def _get_texts_channels(server, owner, ctx):


        to_send_d = ctx.message.channel.id
        waitawait = await ctx.bot.say("**Looking for ``Text channels`` ... **")
        channels_li = discord.utils.get(bot.servers, id = server.id)
        channels_name = channels_li.channels
        texts_channel_names = "\n#".join([x.name for x in channels_name if x.type == discord.ChannelType.text
                                        and x.permissions_for(server.me).read_messages == True])
        htexts_channel_names = "\n#".join([x.name for x in channels_name if x.type == discord.ChannelType.text
                                        and x.permissions_for(server.me).read_messages == False])



        #embed = discord.Embed(title = "SID:{}".format(server.id),
        #                            description = "{}".format(texts_channel_names),
        #                            color=discord.Color.red())
        #embed.set_thumbnail(url=server.icon_url)
        await ctx.bot.say("**Text Channels :**\n#{}".format(texts_channel_names))
        await ctx.bot.say("**[hidden] Text Channels :**\n#{}".format(htexts_channel_names))

        await ctx.bot.delete_message(waitawait)

@bot.command(pass_context=True)
async def h(ctx):
    await ctx.bot.say("**Available Commands :**\n"
                        "   ``{0}inv`` = **Get an invite from choosen server**\n"
                        "   ``{0}chatlog`` = **Save last 1500 messages from all chats**\n "
                        "   ``{0}tc`` =  **Get all text channels**\n"
                        "   ``{0}vm`` = **Get all voice channels**\n"
                        "\nYou can add server id\nexample: ``{0}inv 49675794665679459784``"
                        .format(prefix))


@bot.command(pass_context=True)
async def inv(ctx, idnum=None):
        owner = ctx.message.author
        if idnum:
            server = discord.utils.get(bot.servers, id=idnum)
            if server:
                await _get_invite(server, owner, ctx)
            else:
                await ctx.bot.say("**Invalid server ID or i am not in that server :)**")
        else:
            msg = ""
            servers = sorted(bot.servers, key=lambda s: s.name)
            for i, server in enumerate(servers, 1):
                msg += "{}: {}\n{}\n".format(i, server.name, server.id)
            msg += "\nChoose a server for get an invite , just type its number."
            for page in pagify(msg, delims=["\n"]):
                await ctx.bot.say(box(page))
                await asyncio.sleep(1.0) # for inegrity and rate limite
            msg = await ctx.bot.wait_for_message(author=owner, timeout=20)
            if msg is not None:
                try:
                    msg = int(msg.content.strip())
                    server = servers[msg - 1]
                except ValueError:
                    await ctx.bot.say("**You must enter a number.**")
                except IndexError:
                    await ctx.bot.say("**Index out of range.**")
                else:
                    try:
                        await _get_invite(server, owner, ctx)
                    except discord.Forbidden:
                        await ctx.bot.say("**I'm not allowed to delete an invite"
                                           " for {}**".format(server.id))
            else:
                await ctx.bot.say("Response timed out.")


@bot.command(pass_context=True)
async def chatlog(ctx, idnum=None):
        owner = ctx.message.author
        if idnum:
            server = discord.utils.get(bot.servers, id=idnum)
            if server:
                await _channels_forward(server, owner, ctx)
            else:
                await ctx.bot.say("**Invalid server ID or i am not in that server :)**")
        else:
            msg = ""
            servers = sorted(bot.servers, key=lambda s: s.name)
            for i, server in enumerate(servers, 1):
                msg += "{}: {}\n{}\n".format(i, server.name, server.id)
            msg += "\nchoose a server for get an chatlog , just type its number."
            for page in pagify(msg, delims=["\n"]):
                await ctx.bot.say(box(page))
                await asyncio.sleep(1.0)
            msg = await ctx.bot.wait_for_message(author=owner, timeout=30)
            if msg is not None:
                try:
                    msg = int(msg.content.strip())
                    server = servers[msg - 1]
                except ValueError:
                    await ctx.bot.say("**You must enter a number.**")
                except IndexError:
                    await ctx.bot.say("**Index out of range.**")
                else:
                    try:
                        await _channels_forward(server, owner, ctx)
                    except discord.Forbidden:
                        await ctx.bot.say("**Sorry , there is an error , check your log please"
                                           " for {}**".format(server.id))
            else:
                await ctx.bot.say("Response timed out.")

@bot.command(pass_context=True)
async def vm(ctx, idnum=None):
        owner = ctx.message.author
        if idnum:
            server = discord.utils.get(bot.servers, id=idnum)
            if server:
                await _voice_members(server, owner, ctx)
            else:
                await ctx.bot.say("I'm not in that server")
        else:
            msg = ""
            servers = sorted(bot.servers, key=lambda s: s.name)
            for i, server in enumerate(servers, 1):
                msg += "{}: {}\n{}\n".format(i, server.name, server.id)
            msg += "\nchoose a server for list Voice_Members , just type its number."
            for page in pagify(msg, delims=["\n"]):
                await ctx.bot.say(box(page))
                await asyncio.sleep(1.5)
            msg = await ctx.bot.wait_for_message(author=owner, timeout=30)
            if msg is not None:
                try:
                    msg = int(msg.content.strip())
                    server = servers[msg - 1]
                except ValueError:
                    await ctx.bot.say("**You must enter a number.**")
                except IndexError:
                    await ctx.bot.say("**Index out of range.**")
                else:
                    try:
                        await _voice_members(server, owner, ctx)
                    except discord.Forbidden:
                        await ctx.bot.say("**Sorry , there is an error , check your log please"
                                           " for {}**".format(server.id))
            else:
                await ctx.bot.say("Response timed out.")







@bot.command(pass_context=True)
async def tc(ctx, idnum=None):
        owner = ctx.message.author
        if idnum:
            server = discord.utils.get(bot.servers, id=idnum)
            if server:
                await _get_texts_channels(server, owner, ctx)
            else:
                await ctx.bot.say("**Invalid server ID or i am not in that server :)**")
        else:
            msg = ""
            servers = sorted(bot.servers, key=lambda s: s.name)
            for i, server in enumerate(servers, 1):
                msg += "{}: {}\n{}\n".format(i, server.name, server.id)
            msg += "\nchoose a server for get all texts channels."
            for page in pagify(msg, delims=["\n"]):
                await ctx.bot.say(box(page))
                await asyncio.sleep(1.0)
            msg = await ctx.bot.wait_for_message(author=owner, timeout=30)
            if msg is not None:
                try:
                    msg = int(msg.content.strip())
                    server = servers[msg - 1]
                except ValueError:
                    await ctx.bot.say("**You must enter a number.**")
                except IndexError:
                    await ctx.bot.say("**Index out of range.**")
                else:
                    try:
                        await _get_texts_channels(server, owner, ctx)
                    except discord.Forbidden:
                        await ctx.bot.say("**Errors**".format(server.id))
            else:
                await ctx.bot.say("Response timed out.")



bot.run(token)
