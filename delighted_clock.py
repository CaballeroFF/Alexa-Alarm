import sys
import time
from pygame import mixer
import alarm_leds as led
import threading
import RPi.GPIO as GPIO
#added for date function
from datetime import date


ir = 16

GPIO.setmode(GPIO.BCM) 

#defining the pins as output/inputs
GPIO.setup(ir, GPIO.IN)

def ampm():
    ctime = time.localtime()
    if int(ctime.tm_hour) < 12:
        return ' AM'
    return ' PM'


def in_a_minute(alarm=False):
    ctime = time.localtime()
    minute = ctime.tm_min + 1
    if int(minute) < 10:
        minute = '0' + str(minute)
    timestr = str(ctime.tm_hour) + ':' + str(minute)
    print(ctime.tm_hour, ':', ctime.tm_min)
    print(timestr)
    if alarm:
        set_alarm(timestr)
    return timestr

#sa = set alarm //// sd = set date
def set_alarm(salarm, sdate):
	mixer.init()
	mixer.music.load('alarm.mp3')

	ctime = time.localtime()

	idate = sdate
	if sdate == 'today':
		idate = str(ctime.tm_year) + '-' + str(ctime.tm_mon) + '-' + str(ctime.tm_mday)
	print('default', idate)

	itime = salarm
	timelist = itime.split(':')
	datelist = idate.split('-')

	hour = abs(int(timelist[0]) - ctime.tm_hour)
	print('hours ', hour)

	minute = int(timelist[1]) - ctime.tm_min
	print('minute(s)', minute)

	time_in_min = (hour * 60) + minute
	print('total time in minutes', time_in_min)

	try:
		minutes = time_in_min
	except ValueError:
		print("Invalid numeric value (%s) for minutes" % salarm)
		print("Should be an integer >= 0")
		sys.exit(1)

	if minutes < 0:
		print("Invalid value for minutes, should be >= 0")
		sys.exit(1)

	change = minutes

	if minutes == 1:
		unit_word = " minute"
	else:
		unit_word = " minutes"

	try:
		print("Sleeping for " + str(minutes) + unit_word)
		while not (ctime.tm_hour == int(timelist[0]) and ctime.tm_min == int(timelist[1]) and ctime.tm_mday == int(datelist[2])):
			if change != minutes:
				change = minutes
				print("Sleeping for " + str(minutes) + unit_word)
				print(ctime.tm_hour, ctime.tm_min)
			time.sleep(1)

			ctime = time.localtime()
			hour = abs(int(timelist[0]) - ctime.tm_hour)
			minute = int(timelist[1]) - ctime.tm_min
			time_in_min = (hour * 60) + minute
			minutes = time_in_min
			if minutes < 0:
				minutes = minutes + 1440
		
		print("Wake up")
		
		t1_stop= threading.Event()
		threading.Thread(target=lights, args=(1, t1_stop)).start()
		
		while(GPIO.input(ir)==1):
		#for i in range(12):
			print(chr(7))
			mixer.music.play(start=0)
			time.sleep(1.5)
			mixer.music.rewind()
			print(GPIO.input(ir))
		print("we out")
		mixer.music.stop()
		t1_stop.set()
			
	except KeyboardInterrupt:
		print("Interrupted by user")
		mixer.music.stop()
		t1_stop.set()
		sys.exit(1)


def lights(arg1, stop_event):
	i = 0
	while not stop_event.is_set():
		print("we in")
		time.sleep(.3)
		while(i < 100):
			led.pwm_led(SLEEP=.20,dc=i)
			time.sleep(.01)
			i = i +1
			print(i)
			break
# EOF
#set_alarm('15:03','2018-03-12')

#debug
#set_alarm(str(time.localtime().tm_hour) + ':' + str(time.localtime().tm_min),'2018-03-12')
