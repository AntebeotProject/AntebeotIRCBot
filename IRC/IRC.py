import socket
import re, sys, time
from threading import Thread
DEF_COMMAND_CHAR = '!'
from .commands import commands

class IRC:  
 # we would to use instead normal method for channel and PM handler. but for not is okey.
 # so. double of code in the part of our code is ok. fine.
 def channel_msg_handler(self, user_part, to, msg):
  msg = msg[1:]
  self.user_msg_handler(user_part, to, msg) #
 def user_msg_handler(self, user_part, to, msg): 
  parts = msg.replace("\r","").split(" ")
  print("parts is")
  print(parts)
  if parts[0] in commands.both_cmnds:
   print("Command is found in both cmnds")
   commands.both_cmnds[parts[0]](self, user_part, to, msg)
   pass
  else:
   print(parts[0] + " " + " not in " )
   print(commands.both_cmnds)
  print(msg)
  print("от %s" % (user_part))
  # macro was be good but is python
  pass

  
 # Check if socks exists and opened (not clossed. TODO: add check to closed socket) (null returns from server though socket)
 def assert_sock(self):
  if self.sock is None: assert()
 def doRead(self, s = 1024):
  tmp = self.sock.recv(s)
  if len(tmp) == 0:
   print("Connection was broken")
   sys.exit(1)
  return tmp.decode(self.encode)
 def doSend(self, msg):
  msg = (msg + "\r\n").encode(self.encode)
  print("DO Send ~%s~" % (msg) )
  self.sock.send(msg) # 
 def joinToChannel(self, chName):
  msg = ("JOIN #%s\r\n" % chName).encode(self.encode) # is outdated. use self.doSend #  insted
  self.sock.send(msg) #  
 def doPing(self):
  tmstmp = int(time.time())
  while True:
   if int(time.time()) - tmstmp > 15:
     #print("need write PING")
     tmstmp = int(time.time())
     self.sock.send(b"PING\r\n") 
     #time.sleep(5)
     pass 
 def read_loop(self):

  while True: 
   if self.connected == True: return False
   msg = self.doRead()
   lines = msg.split("\n")
   pingRegex = re.compile("PING :\\w{8}")
   # :oruge!oruge@j4wduidqa6rqy3banpvs6em2yeatovx5ws3g22jo3zoqihkzy2xq.b32.i2p PRIVMSG #testbot :test
   privmsgRegex = re.compile( ":\\w+!\\w+@(\\w+)?.(\\w+)?.(\\w+) PRIVMSG \\#?\\w+ :([а-яА-Яa-zA-Z!0-9] ?)+" )
   #Start FOR
   for line in lines:
    if pingRegex.match(line):
      self.ping_pong(line)
    elif privmsgRegex.match(line):
       parts = line.split(" ", 3) # PRIVMSG 
       if len(parts) != 4: 
        print("Is broken PRIVMSG. warning.")
        continue
       user_part = parts[0]
       to = parts[2]
       msg = parts[3]
       msg = msg[1:]
       print("For now msg is %s" % msg)
       #
       #print(parts)
       if  not "#" in line: self.user_msg_handler(user_part, to, msg)
       else:
         if msg[0] == DEF_COMMAND_CHAR: self.channel_msg_handler(user_part, to, msg)
          
    # FOR end
    else:
     #print("this Line is not regex on any bull...")
     #print(line)
     pass
    # for not get timeout
    # We would use async code or another thread
    
        
    pass
   
 # 
 def wMsg(self, to, msg):
  self.doSend("PRIVMSG %s :%s" % (to,msg)) # 
  
 def ping_pong(self, l):
   # PING ....
   # split ... if exists PING phrase else is will be MOTD. then skip it yet.
   print("Do Ping")
   l = l.split(" ")
   if len(l) != 2: 
    print("Broken PING. Exit")
    sys.exit(0)
   n_msg = ("PONG %s\r\n" % l[1]).encode(self.encode)
   self.sock.send(n_msg)
   self.joinToChannel("testbot") # testbot
   # PRIVMSG #testbot :pizda
   self.wMsg("#testbot", "hewwo world")
   print("Ping is done. bot will be joined to channel")
   tmstmp_thread = Thread(target=IRC.doPing, args=(self,))
   tmstmp_thread.start()
   pass
# Do IRC connection (Ping/Pong also Nick and USER parts)
 def doConnection(self, nick = b"AntebeotBot", username = b"Antebeot"): 
  self.assert_sock()
  if self.connected == True: return False
  self.sock.sendall(b"NICK %s\n" % (nick) )
  self.sock.sendall(b"USER %s 8 * * 8\n" % (username) )
  
  self.read_loop()
# Init Socket And call doConnection
 def __init__(self, addr = "localhost", port = 1919,  encode= "utf-8"):
   n_addr = (addr, port)
   self.connected = False
   self.encode = encode
   self.sock = socket.create_connection( n_addr )
   self.doConnection()
   pass
   