import search_script
import auth
import sys
import vk
import requests
import vk_requests
import search_script

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
api = vk_requests.create_api(app_id=auth.APP_ID, login=auth.APP_LOGIN, password=auth.APP_PASSWORD,
                             phone_number=auth.APP_LOGIN,
                             scope=['offline', 'messages'])

# some variable to use with VK API
USER_ID = "12708191"

first_name = "First Name"
last_name = "Last Name"
is_closed = "Is account closed"

# test page
@app.route('/test')
def test():
    user = {'username': 'Miguel'}
    userdict = {}
    return render_template("index2.html", userdict=userdict)

question_fields = ['id', 'first_name', 'last_name', 'is_closed', 'bdate', 'counters', 'photo_400', 'about', 'activities', 'career',
                  'city', 'connections', 'contacts', 'education', 'exports', 'interests', 'last_seen', 'military',
                  'personal', 'relatives', 'relation', 'schools', 'sex', 'universities']

answer_fields = ['id', 'first_name', 'last_name', 'is_closed', 'bdate', 'photo_400', 'about', 'activities', 'career',
              'city', 'education', 'exports', 'home_phone', 'interests', 'last_seen', 'military', 'mobile_phone',
              'personal', 'relatives', 'relation', 'schools', 'sex', 'universities',
              'facebook', 'facebook_name', 'twitter', 'instagram', 'livejournal']

# test page
@app.route('/')
def index():
    userdict = {}
#    return render_template("test.html")
    return render_template("index2.html", userdict=userdict)

@app.route('/about')
def about():
    userdict = {}
    return render_template("about.html")

@app.route('/pricing')
def pricing():
    userdict = {}
    return render_template("pricing.html")



# test sending
@app.route('/send', methods=['GET', 'POST'])
def send():
    if request.method == 'POST':
        # запрос userid из формы
        user_ids = request.form['user_ids']

        # userinfo = api.users.get(user_ids=age, fields=['bdate', 'city', 'photo_400'])
        # userinfo = api.users.get(user_ids=age, fields=['id', 'first_name', 'last_name', 'is_closed', 'bdate',
        # 'photo_400', 'about', 'activities', 'career', 'city', 'connections', 'contacts', 'education', 'exports',
        # 'interests', 'last_seen', 'military', 'personal', 'relatives', 'relation', 'schools', 'sex', 'universities'])

        # запрос к VK API
        # TODO - определить версию API
        userinfo = api.users.get(user_ids=user_ids, fields=question_fields)
        print("userinfo is:")
        print(str(userinfo))
        # вытаскиваем словарь с данными из ответа, т.к. рассчитано на несколько userid, берем нулевой
        # TODO - поставить проверку одного id в поле
        userdict = {}
        userdict.update(userinfo[0])
        # userdict.update(userinfo2[0])
        print(userdict)

        # чиним данные из ВК, подставляя unknown там, где нет значений
        # а это и не надо, так как берем для рендера те данные, где значения есть!
        #userdict = search_script.repair_social_data(userdict, answer_fields)

        # переводим данные в человеческий вид
        nicedata = search_script.social_to_human(userdict)

        # рендерим шаблон, внутри него словарь отрендерится сам
        # return render_template('index2.html', userdict=userdict)
        return render_template('index2.html', userdict=userdict, nicedata=nicedata)

    return render_template('index2html')


if __name__ == '__main__':
    print("Main script is loaded")
    print(api.users.get(user_ids=1))
    app.run(debug=True)
    pass
