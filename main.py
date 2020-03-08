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
@app.route('/')
def index():
    user = {'username': 'Miguel'}
    return render_template("index.html", user=user)


# debug


# test page
@app.route('/test')
def test():
    return render_template("test.html")

# test sending
@app.route('/send', methods=['GET', 'POST'])
def send():
    if request.method == 'POST':
        age = request.form['age']
        userinfo = api.users.get(user_ids=age, fields=['bdate', 'city', 'photo_400'])
        print(userinfo)

        try:

            first_name = userinfo[0]['first_name']
            last_name = userinfo[0]['last_name']
            is_closed = str(userinfo[0]['is_closed'])
            bdate = str(userinfo[0]['bdate'])
            user_image = (userinfo[0]['photo_400'])
            return render_template('test.html', first_name=first_name, last_name=last_name, is_closed=is_closed, bdate=bdate,user_image=user_image)
        except Exception:
            first_name = "User is"
            last_name = "deleted"
            is_closed = "none"
            return render_template('test.html', first_name=first_name, last_name=last_name, is_closed=is_closed)
    return render_template('test.html')


if __name__ == '__main__':
    print("Main script is loaded")
    print(api.users.get(user_ids=1))
    app.run(debug=True)
    pass
