import vk_api
import requests
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import random
import time

token = '35f7d6acf45a0b152ccd84adee764a1d493fe35b7a632eee9a74535be4641714cd8979071df7fc1b8d824' 

vk_session = vk_api.VkApi(token = '35f7d6acf45a0b152ccd84adee764a1d493fe35b7a632eee9a74535be4641714cd8979071df7fc1b8d824')
longpoll = VkBotLongPoll(vk_session, 187472672) # второй аргумент - id группы

data = requests.get('https://api.vk.com/method/messages.getLongPollServer',
                    params={'access_token': token, 'group_id': 187472672, 'v' : 5.102}).json()['response']  # получение ответа от сервера

vk = vk_session.get_api()   
opozdauArr = ['Опоздаю', 'опоздаю', 'задержусь', 'Задержусь'] # массивы для фильтрации входящих сообщений (не реализовано)
minutesArr = ['мин', 'Минут', 'минут', 'Мин']   

while True:
    response = requests.get('https://{server}?act=a_check&key={key}&ts={ts}&wait=20&mode=2&version=2'.format(server=data['server'],
             key=data['key'], ts=data['ts'])).json()  # отправление запроса на Long Poll сервер со временем ожидания 20 и опциями ответа 2
    updates = response['updates']
    if updates:  # проверка, были ли обновления
        for element in updates:  # проход по всем обновлениям в ответе
            action_code = element[0]  # запись в переменную кода события 
                                      # код 4 - входящее/исходящее сообщение
            if action_code == 4:      # проверка кода события

                '''
                Строки до 40 включительно - побитовая проверка для отсеивания только входящих сообщений
                не разбирался как работает, инфа будет в статье по ссылке
                https://habr.com/ru/post/335106/
                '''
                summands = []         # массив, где мы будем хранить слагаемые
                flag = element[2]  # флаг сообщения
                for number in [1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 65536]:  # проходим циклом по возможным слагаемым
                    if flag & number:  # проверяем, является ли число слагаемым с помощью побитового И
                        summands.append(number)  # если является, добавляем его в массив
                if 2 not in summands:
                    #пока не понимаю почему, но программа не реагирует на сообщения в групповых чатах
                    if element[3] - 2000000000 > 0:  # проверяем, было ли отправлено сообщение в беседе
                        print('go5')
                        user_id = element[6]['from']  # id отправителя
                        chat_id = element[3] - 2000000000  # id беседы
                        chat = requests.get('https://api.vk.com/method/messages.getChat',
                                            params = {'chat_id': chat_id,
                                            'access_token': token, 'v' : 5.102}).json()['response']['title']  # получение названия беседы
                        user = requests.get('https://api.vk.com/method/users.get',
                                            params = {'user_ids': user_id,
                                            'name_case': 'gen', 'v' : 5.102}).json()['response'][0]  # получение имени и фамилии пользователя, отправившего сообщение
                        time_ = element[4]  # время отправления сообщения
                        text = element[5]  # текст сообщения
                        if text:  # проверяем, что сообщение содержит текст
                            print('go6')
                            print(time.ctime(time_).split()[3] + ':', 'Сообщение от', user['first_name'],
                                                                    user['last_name'], 'в беседе "{}"'.format(chat) + ':', text)
                    else: # если сообщение пришло в личные сообщения
                        user_id = element[3]  # id собеседника
                        user = requests.get('https://api.vk.com/method/users.get',
                                            params={'access_token': token, 
                                            'user_ids': user_id, 'name_case': 'gen', 'v' : 5.102}).json()['response'][0]
                        # получение имени и фамилии пользователя, отправившего сообщение
                        time_ = element[4]  # время отправления сообщения
                        text = element[5]  # текст сообщения
                        if text:  # проверяем, что сообщение содержит текст
                            print(time.ctime(time_).split()[3] + ':', 'Сообщение от', user['first_name'], user['last_name'] + ':', text)
                            # отправка сообщения
                            vk.messages.send( 
                                user_id = user_id,
                                random_id = random.randint(100000000, 200000000),
                                message = 'Сообщение от '+ user['first_name'] + ' ' + user['last_name'] + ': '+ text)
        data['ts'] = response['ts']  # обновление номера последнего обновления