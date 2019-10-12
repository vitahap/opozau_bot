import vk_api
import requests
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import random

token = '35f7d6acf45a0b152ccd84adee764a1d493fe35b7a632eee9a74535be4641714cd8979071df7fc1b8d824'  # здесь вы должны написать свой access_token

vk_session = vk_api.VkApi(token = '35f7d6acf45a0b152ccd84adee764a1d493fe35b7a632eee9a74535be4641714cd8979071df7fc1b8d824')
longpoll = VkLongPoll(vk_session)

vk = vk_session.get_api()   
opozdauArr = ['Опоздаю', 'опоздаю', 'задержусь', 'Задержусь']
minutesArr = ['мин', 'Минут', 'минут', 'Мин']   

while True: 
   for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
            for i in opozdauArr:
                if i in event.text:
                    msgArr = event.text.split()
                    for i in msgArr:
                        if i in minutesArr:
                            index = msgArr.index(i) - 1

                    if event.from_user: #Если написали в ЛС
                        vk.messages.send( #Отправляем сообщение
                            user_id = event.user_id,
                            random_id = random.randint(100000000, 200000000),
                            message = 'Ты опоздаешь на {0} минут'.format(msgArr[index]),

                    )
                    elif event.from_chat: #Если написали в Беседе
                        vk.messages.send( #Отправляем собщение
                        chat_id = event.chat_id,
                        random_id = random.randint(100000000, 200000000),
                        peer_id = 2000000000 - event.chat_id,
                        message = 'Ты опоздаешь на {0} минут'.format(msgArr[index])
                    )
