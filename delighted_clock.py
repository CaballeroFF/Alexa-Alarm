import sys
import time
from pygame import mixer
import alarm_leds as led
import threading
#added for date function
from datetime import date


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
def set_alarm(sa,sd):
	mixer.init()
	mixer.music.load('alarm.mp3')

	ctime = time.localtime()

	itime = sa
	timelist = itime.split(':')
	
#for day function added by Carlos
	currmonth = date.today().month
	
	idate = sd
	newadate = idate.split('-')
	
	month = int(newadate[2])
	monthrem = abs(int(month-currmonth))
	print('month(s)',monthrem)
	
	currday = date.today().day	
	day = int(newadate[1])
	dayrem = abs(int(day-currday))
	print('day(s)',dayrem)

	hour = abs(int(timelist[0]) - ctime.tm_hour)
	print('hours ', hour)

	minute = int(timelist[1]) - ctime.tm_min
	print('minute(s)', minute)

#approx because using 30 days in month
	time_in_min = (monthrem*30*24*60)+(dayrem*24*60)+(hour * 60) + minute
	print('approx. total time in minutes', time_in_min)
	
#for debug
	print('approx. time in hours',time_in_min/60)

	try:
		minutes = time_in_min
	except ValueError:
		print("Invalid numeric value (%s) for minutes" % sa)
		print("Should be an integer >= 0")
		sys.exit(1)

	if minutes < 0:
		print("Invalid value for minutes, should be >= 0")
		sys.exit(1)

	seconds = minutes * 60

	if minutes == 1:
		unit_word = " minute"
	else:
		unit_word = " minutes"

	try:
		if minutes > 0:
			print("Sleeping for " + str(minutes) + unit_word)
			time.sleep(seconds)
		print("Wake up")
		
		t1_stop= threading.Event()
		threading.Thread(target=lights, args=(1, t1_stop)).start()
		
		for i in range(10):
			print(chr(7), i)
			mixer.music.play(start=0)
			time.sleep(1.5)
			mixer.music.rewind()
		mixer.music.stop()
		t1_stop.set()
			
	except KeyboardInterrupt:
		print("Interrupted by user")
		mixer.music.stop()
		t1_stop.set()
		sys.exit(1)


def lights(arg1, stop_event):
	while not stop_event.is_set():
		led.pwm_led(SLEEP=.005)
		time.sleep(.5)
# EOF
#set_alarm('20:37','2018-15-03')
