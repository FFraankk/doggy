import os
import sys
import time
import logging
import threading
import pywifi
import yaml
from copy import deepcopy
import led_ctl
from subprocess import Popen, PIPE
from hw_find import get_cpu_serial_number

DEFAULT_CONFIG_PATH = "wifi.yaml"
USER_CONFIG_PATH = "/boot/Hiwonder/wifi.yaml"
SYS_CONFIG_PATH = "/etc/Hiwonder/wifi.yaml"
INTERFACE_PATH = "/tmp/hiwonder_interfaces"

wifi_config = {
    "mode": "ap",
    "flash_led": True,
    "reset": False,
    "ap_mode": {
        "ssid": "Hiwonder",
        "password": "",
        "country": "US",
        "channel": 149,  # 149 153  157 161
        "band": 5,
        "gateway": "192.168.149.1"
    },
    "client_mode": {
        "ssid": "AGFW",
        "password": "lyp123456789",
        "akm_type": "AKM_TYPE_WPA2PSK",
        "cipher_type": "CIPHER_TYPE_CCMP",
        "timeout": 30
    }
}
default_wifi_conf = deepcopy(wifi_config)


def check_dependents(logger):
    exit_ = False
    dep = ("hostapd", "ip", "dnsmasq", "iw", "create_ap", "haveged")
    for d in dep:
        if os.system("which " + d + " > /dev/null 2>&1") != 0:
            logger.error(d + " not installed")
            exit_ = True
    if exit_ is True:
        sys.exit(-1)


def update_config_from_file(path):
    with open(path) as f:
        new_conf = yaml.safe_load(f.read())
        if not new_conf:
            return
        for k, v in new_conf.items():
            if not isinstance(v, dict):
                wifi_config[k] = v
        if 'ap_mode' in new_conf:
            for k, v in new_conf['ap_mode'].items():
                wifi_config['ap_mode'][k] = v
        if 'client_mode' in new_conf:
            for k, v in new_conf['client_mode'].items():
                wifi_config['client_mode'][k] = v


def kill_all():
    os.system("pkill wpa_supplicant")
    os.system("pkill create_ap > /dev/null 2>&1")
    os.system("pkill hostapd > /dev/null 2>&1")
    os.system("pkill ifup > /dev/null 2>&1")
    os.system("pkill ifdown > /dev/null 2>&1")
    os.system("pkill dhclient > /dev/null 2>&1")
    if os.path.exists(INTERFACE_PATH):
        os.system("ifdown -i " + INTERFACE_PATH + " wlan0")


def ap_mode(config):
    kill_all()
    led_ctl.set_period(500, 500)
    time.sleep(1)
    cmd = "create_ap" + \
          " -n wlan0" + \
          " --no-virt" + \
          " --country " + config['country'] + \
          " -g " + config['gateway'] + \
          " --freq-band " + str(config['band']) + \
          " " + config['ssid'] + \
          " " + config['password']
    # " --ieee80211ac" + \
            #" -c " + str(config['channel']) + \
    os.system(cmd)


def client_mode(config):
    kill_all()

    led_ctl.set_period(50, 50)
    logger.info("Connecting to " + config["ssid"])
    with open(INTERFACE_PATH, 'w') as f:
        f.write("auto wlan0\n")
        f.write("iface wlan0 inet dhcp\n")
        f.write("\twpa-ssid " + config['ssid'] + "\n")
        f.write("\twpa-psk " + config['password'] + "\n")

    cmd = "ifup -i " + INTERFACE_PATH + " wlan0"
    p = Popen(cmd, stdout=PIPE, shell=True)
    cmd = "wpa_cli -i wlan0 status|grep ip_address"
    time.sleep(1)
    timeout = time.time() + config['timeout']
    while os.system(cmd) != 0:
        if timeout < time.time():
            raise OSError("Can not connect to " + config['ssid'])
    logger.info("Connected to " + config['ssid'])
    led_ctl.set_period(100, 0)
    while True:
        time.sleep(0.1)


if __name__ == "__main__":
    kill_all()
    sn = get_cpu_serial_number()  # get cpu serial number
    wifi_config["ap_mode"]["ssid"] = "".join(["HW-", sn[:8]])
    led_ctl.start()
    led_ctl.set_period(0, 100)
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger("Hiwonder_WiFi")
    check_dependents(logger)  # check dependents

    # read config file
    if os.path.exists(DEFAULT_CONFIG_PATH):
        update_config_from_file(DEFAULT_CONFIG_PATH)
    if os.path.exists(SYS_CONFIG_PATH):
        update_config_from_file(SYS_CONFIG_PATH)
    if os.path.exists(USER_CONFIG_PATH):
        update_config_from_file(USER_CONFIG_PATH)
    if wifi_config["reset"]:
        os.remove(DEFAULT_CONFIG_PATH)
        os.remove(SYS_CONFIG_PATH)
    if wifi_config['mode'] == 'client':
        if not os.path.exists(INTERFACE_PATH):
            cmd = "create_ap -n wlan0 --no-virt --country US --freq-band 5 -c 149 --hidden hiwonder hiwonder" 
            threading.Thread(target=lambda:os.system(cmd), daemon=True).start()
            time.sleep(15)
            with open(INTERFACE_PATH, 'w') as f:
                f.write("")

    while True:
        if wifi_config['mode'] == 'ap':
            try:
                with open(INTERFACE_PATH, 'w') as f:
                    f.write("")
                ap_mode(wifi_config['ap_mode'])
            except Exception as e:
                print(e)
            
            sys.exit(-2)
        elif wifi_config['mode'] == 'client':
            try:
                client_mode(wifi_config["client_mode"])
            except Exception as e:
                print(e)
                wifi_config['mode'] = 'ap'
