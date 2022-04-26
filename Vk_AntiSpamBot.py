import requests
import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import random
import time
import re

TOKEN = "d2d867ce25500706d02f248f6dc416eafeb36e5d31ca68ca3fa339a9439234e555768e45407707cfc3a19"

prefix = ":"
lst = []

"""commands = {
    mute: {
        Name: 'mute',
        Alt: 'мьют',
        Description: "Блокирует возможность пользователя общаться. Пример работы :mute, :мьют"
    },

    ban: {
        Name: 'ban',
        Alt: 'бан',
        Description: "Полностью исключить игрока из беседы без возможности возврата обратно. Пример работы :ban, :бан"
    },

    kick: {
        Name: 'kick',
        Alt: 'кик',
        Description: "Исключает пользователя из беседы (он может вернуться обратно). Пример работы :kick, :кик"
    },

    slowmode: {
        Name: 'slowmode',
        Alt: 'слоумод',
        Description: "Делает slowmode (от англ. медленный режим). Пользователи не смогут общаться быстрее, "
                     "чем выбранное вами значение. Принимает аргументы: время. Пример работы: slowmode 2, слоумод 2"
    },

    antispam: {
        Name: 'antispam',
        Alt: 'антисам',
        Description: "Схож с командой slowmode, но в отличии от неё, анти спам блокирует слишком быстрый спам "
                     "сообщениями. Принимает аргументы: время и количество сообщений. Пример работы: antispam 2 10, "
                     "антиспам 3 5 "
    },

    antispampunishnent: {
        Name: 'antispampunishment',
        Alt: 'антисамнаказание',
        Description: "Наказание, выдающиеся при спаме. Принимает аргументы: mute/ban/kick. Пример работы: "
                     "antispampunishment mute, антиспамнаказание kick "
    },

    say: {
        Name: 'say',
        Alt: 'сказать',
        Description: "Сказать сообщение от лица бота. Пример работы: say Привет, сказать Как дела?"
    },

    message: {
        Name: 'message',
        Alt: 'сообщать',
        Description: "Говорит сообщение в определенное количество времени. Принимает аргументы: 'сообщение', "
                     "время (в минутах). Пример работы: message 'Привет' 10, сообщать 'Помыть посуду' 120 "
    },

    cmds: {
        Name: 'cmds',
        Alt: 'команды',
        Description: "Написать список команд."
    },

    cube: {
        Name: 'cube',
        Alt: 'кубик',
        Description: "Генерирует рандомное число от 1 до 8"
    },
    ball: {
        Name: 'ball',
        Alt: 'шар',
        Description: "Задаете вопрос - он отвечает."
    },
    coin: {
        Name: 'coin',
        Alt: 'Монетка',
        Description: "Кидаете монетку и вам выпадает орёл или решка."
    time: {
        Name: 'time',
        Alt: 'время',
        Description: "Скажет время в городе"
    },
    rate: {
        Name: 'rate',
        Alt: 'курс',
        Description: "Скажет курс евро или доллара"
    },
}
"""

userTable = {
    "Spam": {

    }
}

activatedCommands = {
    "AntiSpam": False,
    "Slowmode": {
        "Time": 0,
        "Users": []
    },
    "LoopSay": '',
    "Ball": [
        'Мало вероятно',
        'Возможно',
        'Не знаю, спроси позже',
        'Даже не спрашивай это у меня',
        'Да',
        'Нет',
        'Скорее всего',
        'Определенно',
        'Безусловно',
        'Думаю - нет',
        'Думаю - да',
        'Хехехе',
        'Не понял вопроса',
        '¯\_(o_o)_/¯',
    ]
}


def main():
    global vk

    vk_session = vk_api.VkApi(token=TOKEN)
    longpoll = VkBotLongPoll(vk_session, 194730971)
    a = 1

    for event in longpoll.listen():

        mute_list = open("mute_list.txt", encoding="utf8")
        for i in mute_list.readlines():

            if str(event.obj.message["from_id"]) not in i:

                a = 1
            else:

                a = 0

        if a == 1:
            file = open("admin_list.txt", encoding="utf8")

            for j in file.readlines():

                if str(event.obj.message["from_id"]) in j:

                    b = 1
                else:

                    b = 0

                if b == 1:

                    if event.obj.message["text"] == ":admin":

                        if b != 1:

                            file.close()

                            with open("admin_list.txt", "a") as f:
                                f.write(str(event.obj.message["from_id"]) + "\n")

                            vk = vk_session.get_api()

                            vk.messages.send(chat_id=event.chat_id,
                                             message="Поздравляем, вы теперь админ",
                                             random_id=random.randint(0, 2 ** 64))

                        else:

                            vk = vk_session.get_api()

                            vk.messages.send(chat_id=event.chat_id,
                                             message="Вы уже являетесь админом",
                                             random_id=random.randint(0, 2 ** 64))

                    elif event.obj.message["text"] == ":cmds":

                        vk = vk_session.get_api()
                        documentary = open("documentary.txt", encoding="utf8")

                        for line in documentary.readlines():
                            vk.messages.send(chat_id=event.chat_id,
                                             message=line,
                                             random_id=random.randint(0, 2 ** 64))

                    elif ':antispam' in event.obj.message['text']:

                        try:

                            text = event.obj.message['text']
                            split = text.split(':antispam ')
                            arg = split[1]

                            mainarg = int(arg)

                            if mainarg == 1:
                                mainarg = True
                            else:
                                mainarg = False

                            activatedCommands['AntiSpam'] = arg

                            vk.messages.send(chat_id=event.chat_id,
                                             message='Антиспам был включен.',
                                             random_id=random.randint(0, 2 ** 64))

                        except ValueError:

                            vk.messages.send(chat_id=event.chat_id,
                                             message='Ошибка, введите число!',
                                             random_id=random.randint(0, 2 ** 64))

                    elif ':slowmode' in event.obj.message['text']:

                        try:

                            text = event.obj.message['text']
                            split = text.split(':slowmode ')
                            arg = split[1]
                            mainarg = int(arg)

                            if mainarg > 0:
                                activatedCommands['Slowmode']['Time'] = mainarg

                                vk.messages.send(chat_id=event.chat_id,
                                                 message='Медленный режим был включен.',
                                                 random_id=random.randint(0, 2 ** 64))

                            else:

                                activatedCommands['Slowmode']['Time'] = 0
                                vk.messages.send(chat_id=event.chat_id,
                                                 message='Медленный режим был выключен.',
                                                 random_id=random.randint(0, 2 ** 64))

                        except ValueError:

                            vk.messages.send(chat_id=event.chat_id,
                                             message='Ошибка, введите число!',
                                             random_id=random.randint(0, 2 ** 64))

                    elif ":say" in event.obj.message["text"]:

                        msg = event.obj.message["text"]
                        split = msg.split(":say ")
                        text = split[1]
                        vk = vk_session.get_api()

                        """vk.messages.delete(
                            delete_for_all=1,
                            peer_id=event.obj.message['peer_id'],
                            cmids=event.obj.message['conversation_message_id']
                        )"""

                        vk.messages.send(chat_id=event.chat_id,
                                         message=text,
                                         random_id=random.randint(0, 2 ** 64))

                    elif ":pinmsg" in event.obj.message["text"]:

                        msg = event.obj.message["text"]
                        split = msg.split(":pinmsg ")
                        text = split[1]
                        vk = vk_session.get_api()

                        vk.messages.send(chat_id=event.chat_id,
                                         message=text,
                                         random_id=random.randint(0, 2 ** 64))
                        vk.messages.pin(peer_id=event.obj.message['peer_id'],
                                        conversation_message_id=event.obj.message['conversation_message_id'] + 1,
                                        )

                    elif ":mute" in event.obj.message["text"]:

                        msg = event.obj.message["text"]
                        split = msg.split(":mute ")
                        id_mute = split[1]
                        mute = open("mute_list.txt", encoding="utf8")
                        c = 0

                        for n in mute.readlines():
                            if str(id_mute) in n:
                                c = 1
                            else:
                                c = 0

                        if c == 0:

                            with open("mute_list.txt", "a") as mute:
                                mute.write(str(id_mute) + "\n")

                            vk = vk_session.get_api()

                            vk.messages.send(chat_id=event.chat_id,
                                             message=f"{id_mute} был замьючен",
                                             random_id=random.randint(0, 2 ** 64))

                        else:

                            vk = vk_session.get_api()

                            vk.messages.send(chat_id=event.chat_id,
                                             message=f"Данный человек уже замьючен",
                                             random_id=random.randint(0, 2 ** 64))

                    elif ":unmute" in event.obj.message["text"]:

                        msg = event.obj.message["text"]
                        split = msg.split(":unmute ")
                        id_unmute = split[1]
                        unmute = open("mute_list.txt", encoding="utf8")
                        d = 0

                        for m in unmute.readlines():
                            if str(id_unmute) in m:
                                d = 1
                            else:
                                d = 0

                        if d == 1:

                            unmute = open("mute_list.txt", "r")
                            lines = unmute.readline()
                            unmute.close()
                            unmute = open("mute_list.txt", "w")
                            for line in lines:
                                if line != str(id_unmute) + "\n":
                                    unmute.write(line)
                            vk = vk_session.get_api()

                            vk.messages.send(chat_id=event.chat_id,
                                             message=f"{id_unmute} был размьючен",
                                             random_id=random.randint(0, 2 ** 64))
                        else:

                            vk = vk_session.get_api()
                            vk.messages.send(chat_id=event.chat_id,
                                             message=f"Данный человек не замьючен",
                                             random_id=random.randint(0, 2 ** 64))

                    elif ":rate" in event.obj.message['text']:

                        msg = event.obj.message["text"]
                        split = msg.split(":rate ")
                        item = split[1]
                        vk = vk_session.get_api()

                        rate = 'Ошибка ввода. ("доллар" или "евро")'

                        if item == 'доллар':
                            request = requests.get('http://www.floatrates.com/daily/rub.json')
                            json_req = request.json()
                            rate = json_req['usd']['inverseRate']
                            rate = int(rate)
                        elif item == 'евро':
                            request = requests.get('http://www.floatrates.com/daily/rub.json')
                            json_req = request.json()
                            rate = json_req['eur']['inverseRate']
                            rate = int(rate)

                        vk.messages.send(chat_id=event.chat_id,
                                         message="Курс рубля к " + item + ' : ' + str(rate),
                                         random_id=random.randint(0, 2 ** 64))

                    elif ':ball' in event.obj.message['text']:

                        vk.messages.send(chat_id=event.chat_id,
                                         message=random.choice(activatedCommands['Ball']),
                                         random_id=random.randint(0, 2 ** 64))

                    elif ':coin' in event.obj.message['text']:

                        if random.randint(1, 2) == 1:

                            vk.messages.send(chat_id=event.chat_id,
                                             message='Решка',
                                             random_id=random.randint(0, 2 ** 64))
                        else:

                            vk.messages.send(chat_id=event.chat_id,
                                             message='Орел',
                                             random_id=random.randint(0, 2 ** 64))

                    elif ":time" in event.obj.message['text']:

                        msg = event.obj.message["text"]
                        split = msg.split(":курс ")
                        item = split[1]
                        vk = vk_session.get_api()

                        time = 'Ошибка ввода. Город не найден!'

                        try:
                            request = requests.get('https://time100.ru/' + item)
                            text = request.text
                            split1 = text.split('data-format="%H:%i:%s">')[1]
                            split2 = split1.split('</span></h3>')[0]
                            time = split2
                        except:
                            pass

                        vk.messages.send(chat_id=event.chat_id,
                                         message="Время в " + item + ' : ' + str(time),
                                         random_id=random.randint(0, 2 ** 64))

                    elif ":kick" in event.obj.message["text"]:

                        msg = event.obj.message["text"]
                        split = msg.split(":kick ")
                        kick_id = split[1]
                        vk = vk_session.get_api()

                        vk.messages.removeChatUser(chat_id=event.chat_id,
                                                   user_id=kick_id)

                    elif ":cube" in event.obj.message["text"]:

                        msg = event.obj.message["text"]
                        split = msg.split(":cube ")
                        cube = split[1]
                        vk = vk_session.get_api()
                        cube = int(cube)

                        for i in range(1, cube + 1):
                            vk.messages.send(chat_id=event.chat_id,
                                             message="Выпало число: " + str(random.randint(1, 8)),
                                             random_id=random.randint(0, 2 ** 64))


                    elif str(event.obj.message['from_id']) not in j:

                        vk = vk_session.get_api()

                        vk.messages.send(chat_id=event.chat_id,
                                         message="У вас нет прав на данное действие",
                                         random_id=random.randint(0, 2 ** 64))

                    elif event.obj.message["text"][0] == ":":

                        vk = vk_session.get_api()

                        vk.messages.send(chat_id=event.chat_id,
                                         message="Ошибкa: неизвестная команда!",
                                         random_id=random.randint(0, 2 ** 64))

                if event.type == VkBotEventType.MESSAGE_NEW:

                    if activatedCommands['Slowmode']['Time'] > 0:
                        if event.obj.message['from_id'] in activatedCommands['Slowmode']['Users']:

                            vk = vk_session.get_api()
                            sm_time = 0
                            activatedCommands['Slowmode']['Users'].append(event.obj.message['from_id'])
                            time.sleep(activatedCommands['Slowmode']['Time'])

                            if sm_time > activatedCommands['Slowmode']['Time']:

                                vk.messages.delete(
                                    delete_for_all=1,
                                    peer_id=event.obj.message['peer_id'],
                                    cmids=event.obj.message['conversation_message_id']
                                )
                                sm_time = 0
                            else:

                                sm_time += 1
                            activatedCommands['Slowmode']['Users'].remove(event.obj.message['from_id'])

                    if activatedCommands['AntiSpam']:

                        if event.obj.message['from_id'] in userTable['Spam']:

                            userTable['Spam'][event.obj.message['from_id']] += 1
                            print(userTable['Spam'][event.obj.message['from_id']])

                            if userTable['Spam'][event.obj.message['from_id']] > 5:
                                vk = vk_session.get_api()
                                vk.messages.send(user_id=event.obj.message['from_id'],
                                                 message=f"Пользователь {event.obj.message['from_id']} спамит!",
                                                 random_id=random.randint(0, 2 ** 64))

                            time.sleep(2)

                            userTable['Spam'][event.obj.message['from_id']] -= 1

                        else:

                            userTable['Spam'][event.obj.message['from_id']] = 1


        elif a == 0:
            vk = vk_session.get_api()
            vk.messages.delete(
                delete_for_all=1,
                peer_id=event.obj.message['peer_id'],
                cmids=event.obj.message['conversation_message_id']
            )


if __name__ == '__main__':
    main()
