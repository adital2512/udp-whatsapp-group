import socket
import sys


class User:
    def __init__(self, name, address):
        self.name = name
        self.address = address
        self.unread = ""

    def addMessage(self, msg):
        if self.unread != "":
            self.unread += "\n"
        self.unread += msg

    def getUnreadMessages(self):
        unreadM = self.unread
        self.unread = ""  # clear
        return unreadM

    def getName(self):
        return self.name

    def setName(self, name):
        self.name = name

    def getAddress(self):
        return self.address
    def changeName(self, newName):
        self.name = newName


class UserBank:
    def __init__(self):
        self.users = []

    def addUser(self, usr):
        flag = False
        for u in self.users:
            if u.getName() == usr.getName():
                return False  # fail
        if flag == False:
            self.users.append(usr)
            return True  # success

    def list(self):
        return self.users

    def nameByAddress(self, address):
        for usr in self.users:
            if str(usr.getAddress()) == str(address):
                return usr.getName()
        return None

    def msgAll(self, msg, name):
        for usr in self.users:
            if usr.getName() != name:
                usr.addMessage(name + ": "+msg)

    def getUnreadMessages(self, name):
        for usr in self.users:
            if usr.getName() == name:
                return usr.getUnreadMessages()
    def isUser(self, address):
        for usr in self.users:
            if usr.getAddress() == address:
                return True
        return False
    def changeName(self, newName, oldName):
        for usr in self.users:
            if usr.getName() == oldName:
                usr.changeName(newName)
            else:
                usr.addMessage(oldName + " changed his name to " + newName)

    def leaveChat(self, name):
        i = 0
        userIndex = 0
        for usr in self.users:
            if usr.getName() == name:
                userIndex = i
            else:
                usr.addMessage(name + " has left the group")
            i += 1
        self.users.pop(userIndex)

    def welcome(self, name):
        msg = name + " has joined"
        listNames = ""
        for i in range(len(self.users) - 2, -1, -1):
            if self.users[i].getName() != name:
                if listNames != "":
                    listNames += "\n"
                listNames += (self.users[i].getName())
                self.users[i].addMessage(msg)
        (self.users[-1]).addMessage(listNames)




s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
if sys.argv[1] > 65536 or sys.argv[1] < 1:
    sys.exit()
socket = sys.argv[1]
s.bind(('', int(socket)))
users = UserBank()
while True:
    data, addr = s.recvfrom(1024)
    strData = data.decode('ascii')
    if ((strData[0] != '1') and strData[0] != '4' and (users.isUser(addr) is False)) or \
            (len(strData) > 1 and (strData[1] != " ")) or len(strData) == 2:
        #if someone tried to do an action without joining the group, itws illegal.
        #if a message is only 2 chars it means there is no message in there, maybe number.
        msg = "illegal request"
        s.sendto(msg.encode('ascii'), addr)
    elif strData[0] == '1':
        name = strData[2:]
        flag = users.addUser(User(name, addr))
        if flag:
            users.welcome(name)
            msg = users.getUnreadMessages(name)
        else:
            msg = "illegal request"
        s.sendto(msg.encode('ascii'), addr)
    elif strData[0] == '2':
        message = strData[2:]
        name = users.nameByAddress(addr)
        users.msgAll(message, name)
        msg = users.getUnreadMessages(name)
        s.sendto(msg.encode('ascii'), addr)
    elif strData[0] == '3':
        newName = str(strData[2:])
        oldName = users.nameByAddress(addr)
        users.changeName(newName, oldName)
        msg = users.getUnreadMessages(newName)
        s.sendto(msg.encode('ascii'), addr)
    elif strData[0] == '4':
        if users.isUser(addr):
            name = users.nameByAddress(addr)
            users.leaveChat(name)
            msg = "disconnect"
        else:
            msg = "illegal request"
        s.sendto(msg.encode('ascii'), addr)
    elif strData[0] == '5':
        name = users.nameByAddress(addr)
        msg = users.getUnreadMessages(name)
        s.sendto(msg.encode('ascii'), addr)
    else:
        msg = "illegal request"
        s.sendto(msg.encode('ascii'), addr)