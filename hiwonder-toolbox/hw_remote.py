import os, sys
import socketserver
import json
import yaml

wifi_config = {
    "mode": "client",
    "client_mode": {
    }
}


class TCPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        print("CCCC")
        global wifi_config
        self.request.settimeout(2)
        data = None
        while True:
            try:
                if data is None:
                    data = self.request.recv(1024)
                else:
                    data += self.request.recv(1024)
                if not data:
                    print("nod")
                    pass
                else:
                    msg = str(data, encoding='utf-8')
                    try:
                        key_dict = json.loads(msg)
                    except:
                        continue
                    print('key_dict', key_dict)
                    if 'setwifi' in key_dict:
                        key_dict = key_dict['setwifi']
                        if 'ssid' in key_dict and 'passwd' in key_dict:
                            wifi_config['client_mode']['ssid'] = key_dict['ssid']
                            wifi_config['client_mode']['password'] = key_dict['passwd']
                            buf = yaml.dump(wifi_config)
                            with open("/etc/Hiwonder/wifi.yaml", "w") as fp:
                                fp.write(buf)
                            print('buf', buf)
                            os.system("sudo systemctl restart hw_wifi.service")
                    break
            except:
                break
        self.request.close()


class PhoneServer(socketserver.TCPServer):
    timeout = 2
    daemon_threads = True
    allow_reuse_address = True

    def __init__(self, server_address, RequestHandlerClass):
        socketserver.TCPServer.__init__(self, server_address, RequestHandlerClass)
        print("INIT")

    def handle_timeout(self):
        print('Timeout')


if __name__ == "__main__":
    if not os.path.exists("/etc/Hiwonder"):
        os.system("mkdir /etc/Hiwonder")
    server = PhoneServer(('0.0.0.0', 9026), TCPHandler)
    server.serve_forever()
