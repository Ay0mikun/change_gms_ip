import paramiko, threading

class Ssh_tool:

    def __init__(self, ip_address, username, password):
        print("Connecting to server...")
        #New SSH client
        self.client = paramiko.client.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.client.AutoAddPolicy())
        # Make the connection
        self.client.connect(ip_address, username=username,
                            password=password, look_for_keys=False)
        self.transport = paramiko.Transport((ip_address, 22))
        self.transport.connect(username=username, password=password)
        
        thread = threading.Thread(target=self.process)
        thread.daemon = True
        thread.start()

    def closeConnection(self):
        if(self.client != None):
            self.client.close()
            self.transport.close()

    def openShell(self):
        self.shell = self.client.invoke_shell()

    def sendShell(self, command):
        if(self.shell):
            self.shell.send(command + "\n")
        else:
            print("Shell not opened.")

    def process(self):
        global connection
        while True:
            # Print data when available
            if self.shell != None and self.shell.recv_ready():
                alldata = self.shell.recv(1024)
                while self.shell.recv_ready():
                    alldata += self.shell.recv(1024)
                strdata = str(alldata, "utf8")
                strdata.replace('\r', '')
                print(strdata, end="")
                if(strdata.endswith("$ ")):
                    print("\n$ ", end="")


ssh_username = "root"
ssh_password = "sonicssh"
ssh_server = "10.61.242.96"


connection = Ssh_tool(ssh_server, ssh_username, ssh_password)
connection.openShell()
while True:
    command = input('$ ')
    if command.startswith(" "):
        command = command[1:]
    connection.sendShell(command)
