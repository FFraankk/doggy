import time
import threading
import RPi.GPIO as GPIO

_led1 = 16
_led2 = 26
_period = 0
_lock = threading.Lock()

time_on = 1000  # ms
time_off = 1000  # ms

leds = [_led1, _led2]


def start(p1=16, p2=26):
    global _led1, _led2
    _led1 = p1
    _led2 = p2
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(_led1, GPIO.OUT)
    GPIO.output(_led1, 1)
    GPIO.setup(_led2, GPIO.OUT)
    GPIO.output(_led2, 0)
    threading.Thread(target=_task, daemon=True).start()

def set_led(i, n):
    GPIO.output(leds[i -1], n)

def set_period(t_on, t_off):
    global time_on, time_off, _period
    with _lock:
        time_on = t_on
        time_off = t_off
        _period = t_off + t_on


def _task():
    global time_on, time_off, _period
    count = 0
    while True:
        with _lock:
            if count < time_on:
                GPIO.output(_led1, 0)
                count += 10
            elif count < _period:
                GPIO.output(_led1, 1)
                count += 10
            else:
                count = 0
        time.sleep(0.01)
