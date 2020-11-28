from edu_community import socketio, mongoDB, sqlDB
from flask import session
from flask_login import current_user
from datetime import datetime
from bson import json_util 
from flask_socketio import emit, join_room, leave_room, rooms
from edu_community.sql_models import *
from bson.objectid import ObjectId

@socketio.on('joined', namespace='/text_channel')
def joined(message):
    print(message)
    text_channel = sqlDB.session.query(Text_Channel).filter_by(code=message['message']['channel_code']).first()
    text_channel.community.members_online += 1
    sqlDB.session.commit()
    if text_channel:
        room=text_channel.mongodb_chat_history_id 
        join_room(room)
        msg_history = mongoDB.channel_messages.find_one(
            {
                "_id": ObjectId(room)
            }
        )
        msg_history_json = {}
        index = 0
        for msg in msg_history['msgs']:
            msg_history_json[str(index)] = generate_message_json(text=msg['text'], time=msg['time'], user_code=msg['user'])
            index += 1
        emit('messages', {'msgs': msg_history_json}, room=room)

@socketio.on('msg', namespace='/text_channel')
def text(message):
    print(message)
    text_channel = sqlDB.session.query(Text_Channel).filter_by(code=message['message']['channel_code']).first()
    room=text_channel.mongodb_chat_history_id
    time=datetime.utcnow()
    mongoDB.channel_messages.update(
        {
            "_id" : ObjectId(room)
        },
        {
            '$push': { 'msgs' : {
                    'text' : message['message']['text'],
                    'time' : time,
                    'user' : current_user.code,
                }
            }
        })
    msg = generate_message_json(text=message['message']['text'],time=time,user_code=current_user.code)
    emit('message', {'msg':msg}, room=room)

@socketio.on('disconnect', namespace='/text_channel')
def disconnect(message):
    text_channel = sqlDB.session.query(Text_Channel).filter_by(code=message['message']['channel_code']).first()
    text_channel.community.members_online -= 1
    sqlDB.session.commit()
    leave_room(room)
    emit('status', {'msg': session.get('name') + ' has left the room.'}, room=text_channel.mongodb_chat_history_id)


def generate_message_json(text, time, user_code):
    temp_user = sqlDB.session.query(User).filter_by(code=user_code).first()
    json = {
        'text':text,
        'time':str(time),
        'user':{
            'name':temp_user.name,
            'code':temp_user.code
        }
    }
    return json

