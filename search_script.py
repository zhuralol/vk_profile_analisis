#from main.py import api
#from main import api


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
    fullfields = ["first_name", "last_name", "is_closed", "bdate", "user_image", "about", "activities", "career", "city", "connections", "contacts", "education", "exports", "interests", "last_seen", "military", "personal", "relatives", "relation", "schools", "sex", "universities"]
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
