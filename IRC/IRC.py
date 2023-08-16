# WipedLife + GPT3.5 authors. 
# License ....
# 2023 (c)
import asyncio
import socket,re,sys,time,threading

from threading import Thread
from .commands import commands

DEF_COMMAND_CHAR = '!'
DoPingTimer=5.0

class IRC:
  
  async def channel_msg_handler(self, user_part, to, msg):
    msg = msg[1:]
    print("do user_msg_handler")
    await self.user_msg_handler(user_part, to, msg)

  async def user_msg_handler(self, user_part, to, msg):
    print('user_part is ' + user_part)
    parts = msg.replace("\r","").split(" ")
    print("parts is")
   
    if parts[0] in commands.both_cmnds:
      print("Command is found in both cmnds")
      await commands.both_cmnds[parts[0]](self, user_part, to, msg)
    else:
      print(parts[0] + " " + " not in " )
      print(commands.both_cmnds)
    print(msg)
    print("от %s" % (user_part))

  # Check if socks exists and opened (not clossed. TODO: add check to closed socket) (null returns from server though socket)
  def assert_sock(self):
    if self.sock is None: assert()

  async def doRead(self, s = 1024):
    tmp = self.sock.recv(s)
    if len(tmp) == 0:
      print("Connection was broken")
      sys.exit(1)
    return tmp.decode(self.encode)

  async def doSend(self, msg):
    msg = (msg + "\r\n").encode(self.encode)
    print("DO Send ~%s~" % (msg) )
    self.sock.send(msg)

  async def joinToChannel(self, chName):
    msg = ("JOIN #%s\r\n" % chName).encode(self.encode)
    self.sock.send(msg)

  async def read_loop(self):
    while True:
      if self.connected == True: return False
      msg = await self.doRead()
      lines = msg.split("\n")
      print(lines)
      pingRegex = re.compile("PING :\\w{8}")
      privmsgRegex = re.compile( ":\\w+!\\w+@(\\w+)?.(\\w+)?.(\\w+) PRIVMSG \\#?\\w+ :([а-яА-Яa-zA-Z!0-9] ?)+" )
      for line in lines:
        if pingRegex.match(line):
          await self.ping_pong(line)
        elif privmsgRegex.match(line):
          parts = line.split(" ", 3)
          if len(parts) != 4:
            print("Is broken PRIVMSG. warning.")
            continue
          print("PrivMSG parts is: " + str(parts) )
          user_part = parts[0]
          msg = parts[3]
          msg = msg[1:]
          print("For now msg is %s" % msg)
          if  not "#" in line:
              to = user_part.split("!")[0][1:]
              await self.user_msg_handler(user_part, to, msg)
          else:
            if msg[0] == DEF_COMMAND_CHAR:
                to = parts[2]
                await self.channel_msg_handler(user_part, to, msg)
        else:
          if msg == 'ping':
              self.sock.send(b"PING\r\n")
              pass
          pass
        pass

  async def wMsg(self, to, msg):
    await self.doSend("PRIVMSG %s :%s" % (to,msg))

  async def ping_pong(self, l):
    print("Do Ping")
    l = l.split(" ")
    if len(l) != 2:
      print("Broken PING. Exit")
      sys.exit(0)
    n_msg = ("PONG %s\r\n" % l[1]).encode(self.encode)
    self.sock.send(n_msg)
    await self.joinToChannel("testbot")
    #
    await self.wMsg("#testbot", "hewwo world")
    print("Ping is done. bot will be joined to channel")
    pass

  def doPing(self):
      #   tmstmp = int(time.time())
    #while True:
     # if int(time.time()) - tmstmp > 15:
     #   #print("need write PING")
     #   tmstmp = int(time.time())
     #   self.sock.send(b"PING\r\n")
     #   pass
     #print("вызвано")
     self.sock.send(b"PONG\r\n")
     threading.Timer(DoPingTimer, self.doPing).start()

  async def doConnection(self, nick = b"AntebeotBot", username = b"Antebeot"):
    self.assert_sock()
    if self.connected == True: return False
    self.sock.sendall(b"NICK %s\n" % (nick) )
    self.sock.sendall(b"USER %s 8 * * 8\n" % (username) )

    # Threading do to
    threading.Timer(DoPingTimer, self.doPing).start()
    await self.read_loop()

  def __init__(self, addr = "localhost", port = 1919,  encode= "utf-8"):
    n_addr = (addr, port)
    self.connected = False
    self.encode = encode
    self.sock = socket.create_connection( n_addr )
    self.sock.setblocking(True)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(self.doConnection())
    loop.close()

if __name__ == '__main__':
  irc = IRC()
