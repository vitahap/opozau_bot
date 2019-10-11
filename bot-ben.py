import vk_api
import requests

vk_session = vk_api.VkApi(token='тd7fcf86df09f05206858c136929452058ef7e960f9c8d340eb1d5ace05916d5255973faca163fc10b8496')
from vk_api.longpoll import VkLongPoll, VkEventType
longpoll = VkLongPoll(vk_session)
vk = vk_session.get_api()
for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
   #Слушаем longpoll, если пришло сообщение то:
        if event.text == 'Первый вариант фразы' or event.text == 'Второй вариант фразы': #Если написали заданную фразу
            if event.from_user: #Если написали в ЛС
                vk.messages.send( #Отправляем сообщение
                    user_id=event.user_id,
                    message='Ваш текст'
		)
            elif event.from_chat: #Если написали в Беседе
                vk.messages.send( #Отправляем собщение
                    chat_id=event.chat_id,
                    message='Ваш текст'
		)