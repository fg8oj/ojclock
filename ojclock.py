#!/usr/bin/python
# Version 3
# coding: utf-8

import ntplib
import ctypes
import ctypes.util
import time
from datetime import datetime, date,time,timezone,timedelta

def _linux_set_time(dt):
    import ctypes
    import ctypes.util
    import time

    # /usr/include/linux/time.h:
    #
    # define CLOCK_REALTIME                     0
    CLOCK_REALTIME = 0
    CLOCK_PROCESS_CPUTIME_ID=0
    CLOCK_THREAD_CPUTIME_ID=0
    # /usr/include/time.h
    #
    # struct timespec
    #  {
    #    __time_t tv_sec;            /* Seconds.  */
    #    long int tv_nsec;           /* Nanoseconds.  */
    #  };
    class timespec(ctypes.Structure):
        _fields_ = [("tv_sec", ctypes.c_long),
                    ("tv_nsec", ctypes.c_long)]

    librt = ctypes.CDLL(ctypes.util.find_library("rt"))

    ts = timespec()
    ts.tv_sec = int( time.mktime( dt.timetuple() ) )
    ts.tv_nsec =dt.microsecond * 1000 # microsecond to nanosecond
    # http://linux.die.net/man/3/clock_settime
    ret=librt.clock_settime(CLOCK_REALTIME, ctypes.byref(ts))
    print(ret)


ms = input("Enter a delay in milliseconds [0] : ")
delay=0
try:
	if float(ms)!=0:
	 print(float(ms))
	 delay=int(float(ms))
except ValueError:
	delay=0

ntpserver= 'us.pool.ntp.org'
client = ntplib.NTPClient()
response = client.request(ntpserver, version=3)
print(f"client time of request: {datetime.fromtimestamp(response.orig_time, timezone.utc)}")
print(f"server responded with: {datetime.fromtimestamp(response.tx_time, timezone.utc)}")
print(f"delay:{response.delay}")

dt=datetime.fromtimestamp(response.tx_time, timezone.utc)
pause=timedelta(milliseconds=delay)
current_time = (dt+pause)
_linux_set_time(current_time)
print("Current Time =", current_time)

now = datetime.now()
current_time = now.strftime( "%Y-%m-%d %H:%M:%S.%f")
print("Current Time =", current_time)
