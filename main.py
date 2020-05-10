import search_script
import auth
import sys
import vk
import requests
import vk_requests
import search_script

# flask stuff:
from flask import Flask, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask import render_template


# creating application and bootstrapping it
app = Flask(__name__)
Bootstrap(app)

# turn off on production!
app.config['DEBUG'] = True


# create API to use
api = vk_requests.create_api(app_id=auth.APP_ID, login=auth.APP_LOGIN, password=auth.APP_PASSWORD,
                             phone_number=auth.APP_LOGIN,
                             scope=['offline', 'messages'])

# some variable to use with VK API
USER_ID = "12708191"

first_name = "First Name"
last_name = "Last Name"
is_closed = "Is account closed"

# index page
@app.route('/test')
def index():
    user = {'username': 'Miguel'}
    return render_template("index.html", user=user)


# debug


# test page
@app.route('/')
def test():
    return render_template("test.html")

# test sending
@app.route('/send', methods=['GET', 'POST'])
def send():
    if request.method == 'POST':
        # запрос userid из формы
        user_ids = request.form['user_ids']
        # список полей для запроса и отображения
        fields = ['id', 'first_name', 'last_name', 'is_closed', 'bdate', 'photo_400', 'about', 'activities', 'career',
                  'city', 'connections', 'contacts', 'education', 'exports', 'interests', 'last_seen', 'military',
                  'personal', 'relatives', 'relation', 'schools', 'sex', 'universities']
        # userinfo = api.users.get(user_ids=age, fields=['bdate', 'city', 'photo_400'])
        # userinfo = api.users.get(user_ids=age, fields=['id', 'first_name', 'last_name', 'is_closed', 'bdate',
        # 'photo_400', 'about', 'activities', 'career', 'city', 'connections', 'contacts', 'education', 'exports',
        # 'interests', 'last_seen', 'military', 'personal', 'relatives', 'relation', 'schools', 'sex', 'universities'])

        # запрос к VK API
        # TODO - определить версию API
        userinfo = api.users.get(user_ids=user_ids, fields=fields)
        print("userinfo is:")
        print(str(userinfo))
        # вытаскиваем словарь с данными из ответа, т.к. рассчитано на несколько userid, берем нулевой
        # TODO - поставить проверку одного id в поле
        userdict = {}
        userdict.update(userinfo[0])
        # userdict.update(userinfo2[0])
        print(userdict)

        # итерируем все элементы списка fields и используя их как ключи, берем выданные данные из словаря userdict
        # если нет совпадения, пишем "не указано"

        for f in fields:
            try:
                print(userdict[f])
            except Exception as e:
                print("произошло исключение!")
                print(e)
                userdict[f] = "Unknown"



        try:
            id = userdict['id']
            first_name = userdict['first_name']
            last_name = userdict['last_name']
            is_closed = str(userdict['is_closed'])
            bdate = str(userdict['bdate'])
            user_image = (userdict['photo_400'])
            # 'about', 'activities', 'career', 'city', 'connections', 'contacts', 'education', 'exports', 'interests'
            about = str(userdict['about'])
            activities = str(userdict['activities'])
            career = str(userdict['career'])
            city = str(userdict['city'])
            connections = str(userdict['connections'])
            # 'facebook': '501012028', 'facebook_name': 'Pavel Durov', 'twitter': 'durov', 'instagram': 'durov'
            contacts = str(userdict['contacts'])
            # 'mobile_phone': '12345 mobile', 'home_phone': '12345 additional'
            education = str(userdict['education'])
            exports = str(userdict['exports'])
            interests = str(userdict['interests'])
            # 'last_seen', 'military', 'personal', 'relatives', 'relation', 'schools', 'sex', 'universities'
            last_seen = str(userdict['last_seen'])
            military = str(userdict['military'])
            personal = str(userdict['personal'])
            relatives = str(userdict['relatives'])
            relation = str(userdict['relation'])
            schools = str(userdict['schools'])
            sex = str(userdict['sex'])
            universities = str(userdict['universities'])
            print(str(sex))
            print(str(universities))
            return render_template('test.html', ** locals())
            # return render_template('test.html', first_name=first_name, last_name=last_name,
            # is_closed=is_closed, bdate=bdate,user_image=user_image)
        except Exception as e:
            # Just print(e) is cleaner and more likely what you want,
            # but if you insist on printing message specifically whenever possible...
            first_name = "User is"
            last_name = str(e)
            is_closed = "str(e.message)"
            if hasattr(e, 'message'):
                print(e)
                print(e.message)
            else:
                print(e)
            return render_template('test.html', first_name=first_name, last_name=last_name, is_closed=is_closed)

    return render_template('test.html')


if __name__ == '__main__':
    print("Main script is loaded")
    print(api.users.get(user_ids=1))
    app.run(debug=True)
    pass
