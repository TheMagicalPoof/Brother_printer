import RPi.GPIO as GPIO
import time
import requests

GPIO.setwarnings(False)

def main():
    """Configuration"""
    check_time = 3
    bad_req_num = 3
    req_timeout = 3
    restarting_sleep_time = 20
    Wakeup_pin = 21
    """Script"""
    bad_try_count = 0
    while True:
        if bad_try_count != bad_req_num:
            try:
                requests.get("http://google.con", timeout=req_timeout)
                print("Have connection")
                time.sleep(check_time)
                bad_try_count = 0
            except:
                bad_try_count += 1
                time.sleep(check_time)
                print("No connection")
        else:
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(Wakeup_pin, GPIO.OUT)
            GPIO.output(Wakeup_pin, GPIO.LOW)
            GPIO.output(Wakeup_pin, GPIO.HIGH)
            time.sleep(5)
            GPIO.output(Wakeup_pin, GPIO.LOW)
            time.sleep(1)
            GPIO.output(Wakeup_pin, GPIO.HIGH)
            time.sleep(5)
            GPIO.output(Wakeup_pin, GPIO.LOW)
            GPIO.cleanup()
            time.sleep(restarting_sleep_time)

if __name__ == '__main__':
    main()