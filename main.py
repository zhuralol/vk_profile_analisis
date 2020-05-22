# coding=utf-8
import search_script
import auth
import sys
import vk
import requests
import time
import vk_requests
from datetime import datetime

# flask stuff:
from flask import Flask, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask import render_template

# mysqlite

# creating application and bootstrapping it
app = Flask(__name__)
bootstrap = Bootstrap(app)

# turn off on production!
app.config['DEBUG'] = True

# create API to use
# TODO - поменять scope
# TODO - решить проблему количества запросов в секунду и парралельной работы пользователей
api = vk_requests.create_api(app_id=auth.APP_ID, login=auth.APP_LOGIN, password=auth.APP_PASSWORD,
                             phone_number=auth.APP_LOGIN,
                             scope=['offline'])

# some variable to use with VK API
USER_ID = "12708191"

first_name = "First Name"
last_name = "Last Name"
is_closed = "Is account closed"


# удалить дубликаты словарей в списке словарей
def dictcleaner(keyname, lst):
    s = set()
    out = list()
    for item in lst:
        if item[keyname] not in s:
            s.add(item[keyname])
            out.append(item)
    return out


# test page
@app.route('/test')
def test():
    user = {'username': 'Miguel'}
    userdict = {}
    return render_template("index2.html", userdict=userdict)


question_fields = ['id', 'first_name', 'last_name', 'is_closed', 'bdate', 'counters', 'photo_max', 'about',
                   'activities', 'career',
                   'city', 'connections', 'contacts', 'education', 'exports', 'interests', 'last_seen', 'military',
                   'personal', 'relatives', 'relation', 'schools', 'sex', 'universities']

answer_fields = ['id', 'first_name', 'last_name', 'is_closed', 'bdate', 'photo_max', 'about', 'activities', 'career',
                 'city', 'education', 'exports', 'home_phone', 'interests', 'last_seen', 'military', 'mobile_phone',
                 'personal', 'relatives', 'relation', 'schools', 'sex', 'universities',
                 'facebook', 'facebook_name', 'twitter', 'instagram', 'livejournal']


# test page
@app.route('/')
def index():
    userdict = {"id": "none"}
    profile_friends = []
    user_interests = []
    graph_data = [
        [{"id": 1, "shape": "circularImage", "label": "Sample"}, {"id": 2, "shape": "circularImage", "label": "graph"},
         {"id": 1, "shape": "circularImage", "label": "data"}], [{"from": 1, "to": 2}, {"from": 3, "to": 2}]]
    #    return render_template("test.html")
    return render_template("index2.html", userdict=userdict, graph_data=graph_data, profile_friends=profile_friends,
                           user_interests=user_interests)


@app.route('/about')
def about():
    userdict = {}
    return render_template("about.html")


@app.route('/pricing')
def pricing():
    userdict = {}
    return render_template("pricing.html")


@app.route('/graph')
def friend_graph():
    return render_template("graph.html")


# test sending
@app.route('/send', methods=['GET', 'POST'])
def send():
    if request.method == 'POST':
        profile_friends = []
        graph_data = [[], []]

        # запрос userid из формы
        user_ids = request.form['user_ids']

        # userinfo = api.users.get(user_ids=age, fields=['bdate', 'city', 'photo_max'])
        # userinfo = api.users.get(user_ids=age, fields=['id', 'first_name', 'last_name', 'is_closed', 'bdate',
        # 'photo_max', 'about', 'activities', 'career', 'city', 'connections', 'contacts', 'education', 'exports',
        # 'interests', 'last_seen', 'military', 'personal', 'relatives', 'relation', 'schools', 'sex', 'universities'])

        # запрос к VK API
        # TODO - определить версию API
        userinfo = api.users.get(user_ids=user_ids, fields=question_fields)
        print("userinfo is:")
        print(str(userinfo))

        # вытаскиваем словарь с данными из ответа, т.к. рассчитано на несколько userid, берем нулевой
        # TODO - поставить проверку одного id в поле
        userdict = {}
        user_interests = []
        userdict.update(userinfo[0])
        # userdict.update(userinfo2[0])
        print(userdict)

        # построение графа
        # graph_get_data(userdict['id'])

        # переводим данные в человеческий вид
        nicedata = search_script.social_to_human(userdict)

        # отрисовка графа
        profile_friends = get_friends(userdict['id'])
        graph_data = gen_graph(userdict['id'], profile_friends)
        graph_data[1].append({"id": userdict['id'], "shape": "circularImage", "image": userdict['photo_max'],
                              "label": userdict['first_name'] + userdict['last_name']})

        #list_counter = 0
        # for everything in profile_friends['items']:
        #     graph_data = graph_friend_draw(profile_friends, graph_data, list_counter)
        #     list_counter = list_counter + 1

        # ngd = (graph_data[0],dictcleaner("id",graph_data[1]))
        # graph_data=ngd

        # filter to remove some unused data - 'track_code': '\S*'

        # взять данные для графа
        '''
        with open(str(userdict['id'])+'graphdata.txt', 'w', encoding='utf-8') as g:
            g.write(str(profile_friends['items']))


            for everything in profile_friends['items']:
                try:
                    time.sleep(0.3)
                    t = get_friends(everything['id'])
                    print(t)
                    k = t['items']
                    for item in k:
                        item['origin'] = everything['id']
                        item.pop("track_code", None)
                    g.write(str(k))
                except Exception as e:
                    print(str(e))
            pass
        pass
        '''

        # анализ подписок
        user_groups = get_groups(userdict['id'])
        print(user_groups)
        user_interests = get_group_activities(user_groups)
        print(user_interests)
        # рендерим шаблон, внутри него словарь отрендерится сам
        # return render_template('index2.html', userdict=userdict)
        return render_template('index2.html', userdict=userdict, nicedata=nicedata, graph_data=graph_data,
                               user_interests=user_interests, profile_friends=profile_friends)

    return render_template('index2html')


def get_friends(id):
    friends = []
    try:
        friends = api.friends.get(user_id=id, order="hints", count=5000, offset=0,
                                  fields=["photo_100", "city", "education"], name_case="nom")
        # print(friends)
        if friends['count'] > 5000:
            sfriends = api.friends.get(user_id=id, order="hints", count=5000, offset=5000,
                                       fields=["photo_100", "city", "education"], name_case="nom")
            friends['items'].append(sfriends['items'])
            friends['count'] = friends['count'] + sfriends['count']

    except Exception as e:
        print(e)

    return friends
    pass


def get_groups(user_id):
    result = []
    try:
        result = api.groups.get(user_id=user_id, fields=["activity"], count=1000, extended=True)
    except Exception as e:
        print(e)
        result = []
    return result
    pass


def get_group_activities(grouplist):
    result = {}

    try:
        for pub in grouplist['items']:
            print(pub)
            try:
                act = pub['activity']

                try:
                    result[act] = result[act] + 1
                except Exception as e:
                    result[act] = 1
                    print(e)
                print(result)

            except Exception as e:
                print("act = pub['activity'] ERROR")
                print(e)

        try:
            endresult = sorted(result.items(), key=lambda x: x[1], reverse=True)
            print(endresult[:15][0][0])
            print(endresult[:15][1][0])
            print(endresult[:15])
            return endresult[:15]
        except Exception as e:

            print(e)
            return []
    except Exception as e:
        print(str(e))
        return []

    # print(result)
    # print(endresult)

    pass


def gen_graph(userid, friends):
    edges = []
    nodes = []

    try:
        for friend in friends['items']:
            friend_dict = {}
            friend_dict['id'] = friend['id']
            friend_dict['label'] = friend['first_name'] + " " + friend['last_name']
            friend_dict['image'] = friend['photo_100']
            friend_dict['shape'] = "image"
            # print(id['id'])
            edges.append({"from": userid, "to": friend['id']})
            nodes.append(friend_dict)
            pass
    except Exception as e:
        print(str(e))

    return (edges, nodes)


# result = gen_graph(userid,d)
# edges = result[0]
# edges = graph_data[0]
# nodes = graph_data[1]
# nodes = result[1]
# print(edges)
# print(nodes)


def graph_friend_draw(profile_friends, graph_data, num):
    friend_friends = get_friends(profile_friends['items'][num]['id'])
    friend_data = gen_graph(profile_friends['items'][num]['id'], friend_friends)

    print(friend_friends)
    print(friend_data[0][0])
    print(friend_data[1][0])
    print(graph_data[1])
    for k in friend_data[1]:
        # print(k)
        graph_data[1].append(k)
    print(graph_data[1])
    for l in friend_data[0]:
        print(l)
        graph_data[0].append(l)
    print(graph_data[0])
    return (graph_data)
    pass


if __name__ == '__main__':
    print("Main script is loaded")
    # print(get_friends(12437923))
    # print(api.users.get(user_ids=1))
    app.run(debug=True)
    pass
