# alarm_clock.py

# Description: A simple Python program to make the computer act
# like an alarm clock. Start it running from the command line
# with a command line argument specifying the duration in minutes
# after which to sound the alarm. It will sleep for that long,
# and then beep a few times. Use a duration of 0 to test the
# alarm immediiately, e.g. for checking that the volume is okay.


import sys
import time
from pygame import mixer

mixer.init()
mixer.music.load('alarm.mp3')

ctime = time.localtime()
sa = sys.argv
lsa = len(sys.argv)
if lsa != 2:
    print("Usage: [ python ] alarm_clock.py duration_in_minutes")
    print("Example: [ python ] alarm_clock.py 10")
    print("Use a value of 0 minutes for testing the alarm immediately.")
    print("Beeps a few times after the duration is over.")
    print("Press Ctrl-C to terminate the alarm clock early.")
    sys.exit(1)

itime = sa[1]
timelist = itime.split(':')

hour = abs(int(timelist[0]) - ctime.tm_hour)
print('hour in minutes ', hour)

min = int(timelist[1]) - ctime.tm_min
print('minute(s)', min)

time_in_min = (hour * 60) + min
print('total time in minutes', time_in_min)

try:
    minutes = time_in_min
except ValueError:
    print("Invalid numeric value (%s) for minutes" % sa[1])
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
    for i in range(5):
        print(chr(7))
        mixer.music.play()
        time.sleep(1)
        mixer.music.stop()
except KeyboardInterrupt:
    print("Interrupted by user")
    sys.exit(1)
# EOF
