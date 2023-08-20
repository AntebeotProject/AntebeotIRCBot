import requests, hashlib, json
from AntebeotCli_py import client as AntebeotClient

uCookiesSessions = {} # user_part : req.cookies
REST_API_WEB='https://antebeot.world/'
CAPTCHA_PATH='/var/www/html/captchas'
CAPTCHA_WEBSITE='byyesxdjlrywth252dcplh46ypyvurpbjudr5koswiu27ywecz3q.b32.i2p/captchas/'

###
aClient = AntebeotClient.AntebeotClient()
def uCookiesSessionsExists(user_part,what):
 try:
  if uCookiesSessions[user_part] is None or  uCookiesSessions[user_part][what] is None: return False
  return True
 except Exception:
  return False
class commands:
  #commands that allows in PM also in channel
  # type to method is will be (irc, user_part, to, msg)
  @staticmethod 
  async def uTestCaptcha(irc, user_part, to, msg):
   global aClient
   (captchaFileName, captcha_id) = aClient.getCaptcha(user_part)
   await irc.wMsg(to, "path to your file: %s/%s.png" % (aClient.captchaWebsitePath ,captchaFileName))
   pass
     
  # there is example how to use cookie
  
  #def dropNewLine(msg): return msg.replace("\r", "").replace("\n","")
  @staticmethod
  async def uTestCaptcha_(irc, user_part, to, msg):
   global aClient
   answ = msg.split(" ", 2)[1].replace("\n", "").replace("\r", "")
   err, ret = aClient.checkCaptcha(user_part, answ)
   if err == False:
    await irc.wMsg(to, str(ret) )
   else:
     # print error message
     await irc.wMsg(to, ret)
   #
  @staticmethod
  async def uPing(irc, user_part, to, msg):
   await irc.wMsg(to, "pong")
   pass
  @staticmethod
  async def uRegister(irc, user_part, to, msg):
   await irc.wMsg(to, "Not implemented yet")
   pass
  @staticmethod
  async def uDashboard(irc, user_part, to, msg):
   await irc.wMsg(to, aClient.getDashboard())
   pass
  @staticmethod
  async def uHelp(irc, user_part, to, msg):
      await irc.wMsg(to, "use a instruction from ...")
      pass
  # Auth/Reg parts
  @staticmethod
  async def uAuth(irc, user_part, to,msg):
      parts = msg.split(" ")
      if len(parts) != 4:
          await irc.wMsg(to, "auth login password captcha(get from getCaptcha)")
          return False
      global aClient
      res = aClient.do_auth (user_part, parts[1], parts[2], parts[3])
      #print(res)
      if not type(res) is str and res["result"] == True:
          await irc.wMsg(to, "Авторизировано")
      else:
         await irc.wMsg(to, "Ошибка {}". format( str(res) ) )
  @staticmethod
  async def uRegister(irc, user_part, to, msg):
      parts = msg.split(" ")
      if len(parts) != 5:
          await irc.wMsg(to, "register login password password2 captcha(get from getCaptcha)")
          return False
      global aClient
      if parts[2] != parts[3]:
          await irc.wMsg(to, "not correct password2")
          return False
      #parts[4] = self.dropNewLine(parts[4])

      res = aClient.do_registration(user_part, parts[1], parts[2], parts[3], parts[4])
      if not type(res) is str and res["result"] == True:
          await irc.wMsg(to, "Зарегестрировано")
      else:
         await irc.wMsg(to, "Ошибка {}". format( str(res) ) )
      #await irc.wMsg( to, str(res) )
  # end of auth/reg parts

  @staticmethod
  async def uGetAllowCoins(irc, user_part, to, msg):
      try:
          uApi = aClient.getAPIForUser(user_part, ignoreNotSession = False)
          coins = uApi.get_allow_coins()
          await irc.wMsg( to,  "Криптовалюты, поддерживаемые: {} ".format( ",".join(coins) ) )
      except Exception as e:
          print(e)
          await irc.wMsg(to, "залогиньтесь: " + str(e) )
      pass
     
  @staticmethod
  async def uOutputMoney(irc, user_part, to, msg):
      # TODO
      try:
          parts = msg.split(" ")
          if len(parts) != 2:
           await irc.wMsg(to, "getOwnInput %cryptocurrency%")
           return False
          uApi = aClient.getAPIForUser(user_part, ignoreNotSession = False)
          inputAddr = uApi.get_own_input()
          await irc.wMsg( to,  "Входящий адрес: {} ".format( inputAddr ) )
      except Exception as e:
          print(e)
          await irc.wMsg(to, "залогиньтесь: " + str(e) )
  @staticmethod
  async def uGetOwnInput(irc, user_part, to, msg):
      try:
          parts = msg.split(" ")
          if len(parts) != 2:
           await irc.wMsg(to, "getOwnInput %cryptocurrency%")
           return False
          uApi = aClient.getAPIForUser(user_part, ignoreNotSession = False)
          inputAddr = uApi.get_own_input(parts[1])
          if inputAddr == None:
           await irc.wMsg(to, "У вас отсутсвовал входящий адрес, сгенерировали новый")
           inputAddr = uApi.gen_new_address(parts[1])
           pass
          await irc.wMsg( to,  "Входящий адрес: {} ".format( str(inputAddr) ) )
      except Exception as e:
          print(e)
          await irc.wMsg(to, "залогиньтесь: " + str(e) )
      pass
  # both_cmnds for a privmsg to PM and channel
  both_cmnds = {
    'ping' : uPing,
    'register': uRegister,
    'dashboard': uDashboard,
    'getCaptcha': uTestCaptcha,
    'testCaptcha': uTestCaptcha_,
    'help': uHelp,
    'register': uRegister,
    'auth': uAuth,
    #
    'getOwnInput': uGetOwnInput,
    'withdraw': uOutputMoney,
    'getCoinList': uGetAllowCoins
  }
  
