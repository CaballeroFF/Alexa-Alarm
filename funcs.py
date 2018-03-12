from flask import Flask
from flask_ask import Ask, statement, session, question
from datetime import datetime
import time
from datetime import date

import delighted_clock as dl
import threading

app = Flask(__name__)
ask = Ask(app, "/skill")


def set_alarm(tstr,dstr):
    dl.set_alarm(tstr,dstr)


@app.route('/')
def homepage():
    return "Hi there, how is it going."


@ask.launch
def satart_skill():
    welcome_msg = 'Hey you, do you want me to set your alarm?'
    return question(welcome_msg)


@ask.intent("YesIntent", default={'atime': '9:20', 'adate': date.today()})
def yes_intent(atime,adate):
	threading.Thread(target=set_alarm, args=(atime,adate,)).start()
	d = datetime.strptime(atime, '%H:%M')
	print(d.strftime("%I:%M %p"))
	headline_msg = 'Your alarm is set to {} {}'.format(d.strftime("%I:%M %p"),adate)
	return statement(headline_msg)


@ask.intent("NoIntent")
def no_intent():
    bye_msg = 'Okay but if you need me holla'
    return statement(bye_msg)


if __name__ == "__main__":
    app.run(debug=True)
