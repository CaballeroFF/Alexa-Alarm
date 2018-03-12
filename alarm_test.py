import sys
import time
from pygame import mixer
#import alarm_leds as led
import threading

'''#for getting dates right from Alexa
days_dictionary = {'Today':int(time.localtime().tm_wday),
					'Tomorrow':int((time.localtime().tm_wday))+1,
					'two days from now':int((time.localtime().tm_wday))+2,
					'Monday':0,
					'Tuesday':1,
					'Wednesday':2,
					'Thursday':3,
					'Friday':4,
					'Saturday':5,
					'Sunday':6}
for now ignore this
'''
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


def set_alarm(sa,days):
	#mixer.init()
	#mixer.music.load('alarm.mp3')

	ctime = time.localtime()
	print(ctime)

	itime = sa
	timelist = itime.split(':')

	hour = int(timelist[0]) - ctime.tm_hour
	print('hours ', hour)

	minute = int(timelist[1]) - ctime.tm_min
	print('minute(s)', minute)

	time_in_min = (hour * 60) + minute
	print('total time in minutes', time_in_min)
	
	day_set = days_dictionary(days)
	
	try:
		days_until = day_set - int(time.localtime().tm_wday)
	except ValueError:
		print("Invalid numeric value (%s) for days" % days_until)
		print("Should be an integer >= 0")
		sys.exit(1)
		
	days_until_m = days_until*24*60

	try:
		minutes = time_in_min
	except ValueError:
		print("Invalid numeric value (%s) for minutes" % sa)
		print("Should be an integer >= 0")
		sys.exit(1)

	seconds = minutes * 60

	if minutes == 1:
		unit_word = " minute"
	else:
		unit_word = " minutes"

	try:
		while minutes != 0:
			print("Sleeping for " + str(minutes) + unit_word)
			time.sleep(1)
			ctime = time.localtime()
			h = int(timelist[0]) - ctime.tm_hour
			m = int(timelist[1]) - ctime.tm_min
			t = (h * 60) + m
			minutes = t
			print(timelist[0], timelist[1], ctime.tm_hour, ctime.tm_min )
		print("Wake up")
		
		#t1_stop= threading.Event()
		#threading.Thread(target=lights, args=(1, t1_stop)).start()
		
		for i in range(5):
			print(chr(7), i)
			#mixer.music.play(start=0)
			time.sleep(1.5)
			#mixer.music.rewind()
		#mixer.music.stop()
		#t1_stop.set()
			
	except KeyboardInterrupt:
		print("Interrupted by user")
		sys.exit(1)


#def lights(arg1, stop_event):
	#while not stop_event.is_set():
		#led.pwm_led(SLEEP=.005)
		#time.sleep(.5)
# EOF
set_alarm('10:20')
