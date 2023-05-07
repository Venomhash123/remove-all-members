'''
this code by yeuda by https://t.me/m100achuz


pip install Pyrogram
https://github.com/pyrogram/pyrogram.git
'''

import os
from pyrogram import Client
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

app_id = int(os.environ.get("API_ID", 12345))
app_key = os.environ.get('API_HASH')
token = os.environ.get('BOT_TOKEN')
channel_id = os.environ.get("CHANNEL_ID")
app = Client("remove", app_id, app_key, bot_token=token)


STARTED = 'start removing users...'
FINISH = 'done, {} users were removed from group'
ERROR = 'something failed!'
ADMIN_NEEDED = "i need to be admin!"
PRIVATE = '''Hi, I'm a robot to help you remove all users from your group.

Now add me to a group and don't forget to give me the permissions.
Then send /kick in the group and I will start my work.'''

@app.on_message(filters.group & filters.command("kick"))
def main(_, msg: Message):
    chat = msg.chat
    me = chat.get_member(app.get_me().id)
    if chat.get_member(msg.from_user.id).can_manage_chat and me.can_restrict_members and me.can_delete_messages:
        try:
            msg.reply(STARTED.format(chat.members_count))
            count_kicks = 0
            for member in chat.iter_members():
                if not member.can_manage_chat:
                    chat.kick_member(member.user.id)
                    count_kicks += 1
            msg.reply(FINISH.format(count_kicks))
        except Exception as e:
            msg.reply(ERROR.format(str(e)))
    else:
        msg.reply(ADMIN_NEEDED)


# @app.on_message(filters.group & filters.service, group=2)
# def service(c, m):
#     m.delete()


@app.on_message(filters.private)
def start(_, msg: Message):
    msg.reply(PRIVATE, reply_markup=InlineKeyboardMarkup([[
        InlineKeyboardButton("Source Code", url="https://www.github.com/samadii/remove-all-members")]]))


app.run()
