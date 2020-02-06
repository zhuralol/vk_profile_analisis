import search_script
import auth
import sys
import vk
import requests
import vk_requests
import search_script

# flask stuff:
from flask import Flask, redirect, url_for, request
app = Flask(__name__)
from flask import render_template


# create API to use
api = vk_requests.create_api(app_id=auth.APP_ID, login=auth.APP_LOGIN, password=auth.APP_PASSWORD,
                             phone_number=auth.APP_LOGIN,
                             scope=['offline', 'messages'])
name = api.users.get(user_ids=1)[0]['first_name']
surname = api.users.get(user_ids=1)[0]['last_name']


@app.route('/')
def hello_world():
    return 'Hello, Worldd2!'


print(name)
print(surname)


@app.route('/index')
def index():
    username = name + " " + surname
    return render_template("index.html", user=username)

# if __name__ == '__main__':
#     print("Main script is loaded")
#     print(api.users.get(user_ids=1))
#     pass
