import os, sys, time
import pigpio

key1_pin = 25
key2_pin = 23

def reset_wifi():
    os.system("sudo rm /etc/Hiwonder/* -rf > /dev/null 2>&1")
    os.system("sudo systemctl restart hw_wifi.service > /dev/null 2>&1")

if __name__ == "__main__":
    os.system('sudo pigpiod')
    
    time.sleep(1)
    pi = pigpio.pi()
    pi.set_mode(key1_pin, pigpio.INPUT)
    pi.set_mode(key2_pin, pigpio.INPUT)
    pi.set_pull_up_down(key1_pin, pigpio.PUD_UP)
    pi.set_pull_up_down(key2_pin, pigpio.PUD_UP)
    
    

    key1_pressed = False
    key2_pressed = False
    count = 0
    while True:
        if pi.read(key1_pin) == 0:
            time.sleep(0.05)
            if pi.read(key1_pin) == 0:
                if key1_pressed == False:
                    key1_pressed = True
                    count = 0
                else:
                    count += 1
                    if count == 20:
                        count = 0
                        key1_pressed = False
                        print('restart wifi')
                        reset_wifi()
            else:
                count = 0
                key1_pressed = False
                continue
        elif pi.read(key2_pin) == 0:
            time.sleep(0.05)
            if pi.read(key2_pin) == 0:
                if key2_pressed == False:
                    key2_pressed = True
                    count = 0
                else:
                    count += 1
                    if count == 20:
                        count = 0
                        key2_pressed = False
                        print('halt')
                        os.system('sudo halt')

                        pi.write(21, 1)
                        time.sleep(0.05)
                        pi.write(21, 0)
            else:
                count = 0
                key2_pressed = False
                continue
        else:
            count = 0
            key1_pressed = False
            key2_pressed = False
            time.sleep(0.05)
