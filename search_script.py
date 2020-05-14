# coding=utf-8
#from main.py import api
#from main import api
from datetime import datetime
import time

def send_message(api, user_id, message, **kwargs):
    data_dict = {
        'user_id': user_id,
        'message': message,
    }
    data_dict.update(**kwargs)
    return api.messages.send(**data_dict)


def get_group_subscribers(groupid):  # возвращает список!
    result = api.groups.getMembers(group_id=groupid, count=1000, offset=0)
    # numOfSubs = result[0][0]
    subscribers = []  # подписчики группы
    numOfSubs = result['count']  # количество подписчиков
    if numOfSubs <= 1000:
        result = api.groups.getMembers(group_id=groupid, count=1000, offset=0)
        subscribers = result['items']
        # print(subscribers)
        return subscribers

    else:
        ofs = 0
        i = (numOfSubs // 1000) + 1  # количество необходимых запросов по тысяче человек к ВК
        while (i != 0):
            # смещение при поиске, по умолчанию нулевое, каждую итерацию растет на 1000
            result = api.groups.getMembers(group_id=groupid, count=1000, offset=ofs)

            subscribers.extend(result['items'])
            ofs = ofs + 1000
            i = i - 1
            time.sleep(0.8)
            pass
        # print(subscribers)
        return subscribers
pass


def get_all_user_info(userid):
    fullfields = ["first_name", "last_name", "is_closed", "bdate", "user_image", "about", "activities", "career", "city",
                  "connections", "contacts", "education", "exports", "interests", "last_seen", "military", "personal",
                  "relatives", "relation", "schools", "sex", "universities"]
    smallfields = []


# меняет цифрыXXX в списке на ссылки в вк вида vk.com/idXXX, при использовании приравняй к другому списку!
def linkify(users):
    result = []
    for user in users:
        result.append("vk.com/id" + str(user))
        pass
    pass
    print(result)
    return (result)


# берем словарь, выданный ВК, проставляем по списку полей недостающие данные
def repair_social_data(vk_answer, fields):
    # итерируем все элементы списка fields и используя их как ключи, берем выданные данные из словаря userdict
    # если нет совпадения, пишем "не указано"
    for f in fields:
        try:
            print(vk_answer[f])
        except Exception as e:
            print("произошло исключение!")
            print(e)
            vk_answer[f] = "Unknown"
    return vk_answer


def get_friends(id):
    friends = []
    try:
        friends = api.users.get(user_id=id, order="hints", count=50, offset=0,
                                fields=["photo_100", "city", "education"], name_case="nom")
        print(friends)
    except Exception as e:
        print(e)


    return friends
    pass

# генерирует js-список для отрисовки графа из ответа на friends.get
def graph_gen_nodes(friends):
    items = friends['items']
    result = []
    for friend in items:
        friend_dict = {}
        #test = {id: 1, shape: "image", image: "https://sun9-2.userapi.com/c848524/v848524775/8249b/u7czxpksecA.jpg?ava=1", label: "Vladimir Zhuravlev"}
        friend_dict['id'] = friend['id']
        friend_dict['label'] = friend['first_name'] + " " + friend['last_name']
        friend_dict['image'] = friend['photo_100']
        friend_dict['shape'] = "image"
        result.append(friend_dict)
    return result

connection_list = [1,2,]
# так можно сразу в такой формат и записывать!
def graph_gen_edges(connection_list):
    # edges = [{ from: 1, to: 2 }, { from: 2, to: 3 }]
    # OR
    # edges = [{ "from": 1, "to": 2 }, { "from": 2, "to": 3 }]
    result = []
    return result

# создание словаря с человекочитаемыми описаниями из вывода вк
def social_to_human(vk_answer):
    social_answer = []
    if 'id' in vk_answer.keys():
        social_answer.append("Ссылка на профиль: vk.com/id{}".format(vk_answer['id']))
        pass
    if 'first_name' in vk_answer.keys():
        social_answer.append("Имя: {}".format(vk_answer['first_name']))
        pass
    if 'last_name' in vk_answer:
        social_answer.append("Фамилия: {}".format(vk_answer['last_name']))
        pass
    if 'is_closed' in vk_answer:
        if vk_answer['is_closed'] == 1:
            social_answer.append("Профиль закрытый")
        if vk_answer['is_closed'] == 0:
            social_answer.append("Профиль открытый")
        pass
    if 'bdate' in vk_answer:
        social_answer.append("Дата рождения: {}".format(vk_answer['bdate']))
        pass

    if 'about' in vk_answer:
        social_answer.append("О себе: {}".format(vk_answer['about']))
        pass
    if 'activities' in vk_answer:
        social_answer.append("Деятельность: {}".format(vk_answer['activities']))
        pass
    if 'career' in vk_answer:
        for wrk in vk_answer['career']:
            if ('group_id' in wrk) and ('position' in wrk):
                social_answer.append("Работал/работает в vk.com/club{} на должности {}".format(wrk['group_id'], wrk['position']))
            else:
                social_answer.append("Работал/работает в vk.com/club{}".format(wrk['group_id']))
        pass

    if 'city' in vk_answer:
        social_answer.append("Город: {}".format(vk_answer['city']['title']))

    if 'mobile_phone' in vk_answer:
        social_answer.append("Мобильный телефон: {}".format(vk_answer['mobile_phone']))

    if 'home_phone' in vk_answer:
        social_answer.append("Домашний телефон: {}".format(vk_answer['home_phone']))

    if 'skype' in vk_answer:
        social_answer.append("Скайп: {}".format(vk_answer['skype']))

    if 'interests' in vk_answer:
        social_answer.append("Заинтересован в: {}".format(vk_answer['interests']))

    if 'last_seen' in vk_answer:
        msktime = vk_answer['last_seen']['time'] + 10800
        social_answer.append("Последний раз заходил в: {}".format(datetime.utcfromtimestamp(msktime).strftime('%d-%m-%Y %H:%M:%S')))
        if vk_answer['last_seen']['platform'] == 1:
            social_answer.append("Последнее устройство: {}".format("мобильная версия"))
        elif vk_answer['last_seen']['platform'] == 2:
            social_answer.append("Последнее устройство: {}".format("приложение для iPhone"))
        elif vk_answer['last_seen']['platform'] == 3:
            social_answer.append("Последнее устройство: {}".format("приложение для iPad"))
        elif vk_answer['last_seen']['platform'] == 4:
            social_answer.append("Последнее устройство: {}".format("приложение для Android"))
        elif vk_answer['last_seen']['platform'] == 5:
            social_answer.append("Последнее устройство: {}".format("приложение для Windows Phone"))
        elif vk_answer['last_seen']['platform'] == 6:
            social_answer.append("Последнее устройство: {}".format("приложение для Windows 10"))
        elif vk_answer['last_seen']['platform'] == 7:
            social_answer.append("Последнее устройство: {}".format("полная версия сайта"))

    if 'military' in vk_answer:
        pass

    # 'personal': {'political': 2, 'langs': ['Русский', 'English', 'Español'], 'religion': 'Дискордианство',
    #              'inspired_by': 'Вдохновляют: field', 'people_main': 5, 'life_main': 5, 'smoking': 2, 'alcohol': 5},

    if 'personal' in vk_answer:
        if 'political' in vk_answer['personal']:
            pol = {1: "коммунистические", 2: "социалистические", 3: "умеренные", 4: "либеральные", 5: "консервативные", 6: "монархические", 7: "ультраконсервативные", 8: "индифферентные", 9: "либертарианские"}
            social_answer.append("Политические взгляды: {}".format(pol[vk_answer['personal']['political']]))
        if 'religion' in vk_answer['personal']:
            social_answer.append("Религиозные взгляды: {}".format(vk_answer['personal']['religion']))
        if 'langs' in vk_answer['personal']:
            for lang in vk_answer['personal']['langs']:
                social_answer.append("Указан язык: {}".format(lang))


    if 'relatives' in vk_answer:
        for rel in vk_answer['relatives']:
            social_answer.append("Родной {}: vk.com/id{}".format(rel['type'], rel['id']))
        pass

    if 'relation' in vk_answer:
        rel = {1: "не женат/не замужем", 2: "есть друг/есть подруга", 3: "помолвлен/помолвлена", 4: "женат/замужем", 5: "всё сложно", 6: "в активном поиске", 7: "влюблён/влюблена", 8: "в гражданском браке", 0: "не указано"}
        social_answer.append("Семейное положение: {}".format(rel[vk_answer['relation']]))

    if 'schools' in vk_answer:
        for sch in vk_answer['schools']:
            social_answer.append("Учился в {}".format(sch['name']))
        pass

    if 'sex' in vk_answer:
        if vk_answer['sex'] == 1:
            social_answer.append("Пол: женский")
        elif vk_answer['sex'] == 2:
            social_answer.append("Пол: мужской")
        elif vk_answer['sex'] == 0:
            social_answer.append("Пол: не указан")

    if 'universities' in vk_answer:
        for uni in vk_answer['universities']:
            if ('faculty_name' in uni) and ('education_status' in uni):
                social_answer.append("Высшее образование - {} в {}, {}".format(uni['education_status'], uni['name'], uni['faculty_name']))
            else:
                social_answer.append("Высшее образование - {}".format(uni['name']))
        pass

    if 'facebook' in vk_answer:
        social_answer.append("Facebook: facebook.com/{}".format(vk_answer['facebook']))
        pass
    if 'twitter' in vk_answer:
        social_answer.append("Twitter: twitter.com/{}".format(vk_answer['twitter']))
        pass
    if 'instagram' in vk_answer:
        social_answer.append("Instagram: instagram.com/{}".format(vk_answer['instagram']))
        pass


    return social_answer


