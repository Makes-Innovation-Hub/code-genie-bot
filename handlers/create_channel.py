
import os
import requests
from telegram import Update
import json 
from dotenv import load_dotenv
from telegram.ext import CallbackContext
from telethon import TelegramClient, events,functions,types

async def add_bot_as_admin(client, channel_id, bot_username):
    try:
        # Ensure the client is connected
        if not client.is_connected():
            await client.connect()

        # If the client is not authorized, reauthorize it
        if not await client.is_user_authorized():
            await client.start()
        await client(functions.channels.InviteToChannelRequest(
            channel=channel_id,
            users=[bot_username]
        ))

        await client(functions.channels.EditAdminRequest(
            channel=channel_id,
            user_id=bot_username,
            admin_rights=types.ChatAdminRights(
                post_messages=True,
                add_admins=False,
                change_info=False,
                delete_messages=False,
                ban_users=False,
                invite_users=True,
                pin_messages=True,
                edit_messages=True,
                manage_call=True
            ),
            rank='Admin'  
        ))
    except Exception as e:
        print(e)


async def send_message_to_channel(client, channel_id, message):
    async with client:
        await client.send_message(channel_id, message)


async def invite_members_to_channel(bot, channel_id, user):
    if not bot.is_connected():
        await bot.connect()

    await bot(functions.channels.InviteToChannelRequest(
        channel=channel_id,
        users=[user]
    ))


from telethon import events

async def check_users_and_monitor_ready_messages(bot, channel_id):
    participants = await bot.get_participants(channel_id)
    if len(participants) != 3:
        await send_message_to_channel(bot, channel_id, "There must be two participants beside the bot in the channel.")
        return

    user1 = participants[0]
    user2 = participants[1]
    ready_users = set()
    print(user1)
    print(user2)
    

    @bot.on(events.NewMessage(chats=channel_id))
    async def handler(event):
        if event.sender_id in [user1.id, user2.id] and event.text.lower() == "ready":
            ready_users.add(event.sender_id)
            if len(ready_users) == 2:
                await bot.send_message(channel_id, "Both users are ready! The better one wins.")
                ready_users.clear()

    print(f"Monitoring messages in channel {channel_id}...")

#fuction that send invitation link to the secound user
# in case we want to send an invitation link not to join them dirctly  
async def send_invite_link_to_user(client: TelegramClient, user_identifier: str, invite_link: str) -> None:
    try:
        if not client.is_connected():
            await client.connect()

        if not await client.is_user_authorized():
            await client.start()

        user_entity = await client.get_input_entity(user_identifier)
        
        await client.send_message(user_entity, f"Here is your invite link: {invite_link}")
        print(f"Invite link sent to {user_identifier}")
        
    except Exception as e:
        print(f"Failed to send invite link to {user_identifier}: {str(e)}")
