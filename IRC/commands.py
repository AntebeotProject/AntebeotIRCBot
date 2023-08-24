import requests, hashlib, json
from AntebeotCli_py import client as AntebeotClient

uCookiesSessions = {} # user_part : req.cookies
REST_API_WEB='https://antebeot.world/'
CAPTCHA_PATH='/var/www/html/captchas'
CAPTCHA_WEBSITE='byyesxdjlrywth252dcplh46ypyvurpbjudr5koswiu27ywecz3q.b32.i2p/captchas/'

###
#TODO: this global var is not nice
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
          if len(parts) != 7:
#        def output_money(self,login, password, output_address, count_of_money, coin_name, captcha_data, ulang = "ru_RU"):
           await irc.wMsg(to, "withdraw %login% %pass% %output_addr% %amount% %coinname% %captchaData (getCaptcha)%")
           return False
          uApi = aClient.getAPIForUser(user_part, ignoreNotSession = False)
          res = uApi.output_money(parts[1], parts[2], parts[3], parts[4], parts[5], parts[6])
          await irc.wMsg( to,  "Результат: {} ".format( res ) )
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
  @staticmethod
  async def uGetNotify(irc, user_part, to, msg):
      uApi = aClient.getAPIForUser(user_part, ignoreNotSession = False)
      notifications = uApi.notify_data({})
      print( notifications )
      id_ = 1
      for notif in notifications:
          #m = "{} - {} ({})".format( notif['owner'], notif['msg'], notif['time'])
          m = "{}){}({})".format(id_, notif['msg'], notif['time'])
          id_=id_+1
          await irc.wMsg(to, m)
  @staticmethod
  async def uGetUInfo(irc, user_part, to, msg):
      
      parts = msg.split(" ")
      if len(parts) != 2:
          await irc.wMsg(to, "getBalance %coinname%")
          return False

      uApi = aClient.getAPIForUser(user_part, ignoreNotSession = False)
      uInfo = uApi.get_user_info()
  #    uInfo = json.loads(uInfo)
   #   print( uInfo )
      fCrypto = "Not found"
      try: 
       fCrypto = uInfo['Balances'][ parts[1] ]['balance']
      except KeyError as _:
          pass
      await irc.wMsg(to, str( fCrypto ))
  @staticmethod
  async def uUpdateSession(irc, user_part, to, msg):
      uApi = aClient.getAPIForUser(user_part, ignoreNotSession = False)
      uApi.update_session()
      await irc.wMsg(to, "Session was update")
  @staticmethod
  async def uCOrder(irc, user_part, to, msg):
#              def add_order_to_sell_coin2coin(self,sell_namecoin, buy_namecoin, price, volume_start, volume_max):
      parts = msg.split(" ")
      if len ( parts ) < 5:
          await irc.wMsg(to, "cOrder %sellNameCoin% %buyNameCoin% %price% %vStart% %vMax%")
          return False
      sell_name_coin = parts[1]
      buy_name_coin = parts[2]
      price = parts[3]
      vStart = parts[4]
      vMax = parts[5]
      # https://github.com/AntebeotProject/VapsePool/blob/main/HTTPServer/ru/templates/exchange.html
      uApi = aClient.getAPIForUser(user_part, ignoreNotSession = False)
      res = uApi.add_order_to_sell_coin2coin(sell_name_coin, buy_name_coin, price, vStart, vMax)
      await irc.wMsg(to, str( res ) )
  @staticmethod
  async def uGOwnOrders(irc, user_part, to, msg):
      uApi = aClient.getAPIForUser(user_part, ignoreNotSession = False)
      res = uApi.get_own_orders()
      await irc.wMsg(to, str( res ) )
      pass
  @staticmethod
  async def uROrder(irc, user_part, to, msg):
      parts = msg.split( " " )
      if len(parts) != 2:
          await irc.wMsg(to, "rOrder %key_order%")
          return False
      uApi = aClient.getAPIForUser(user_part, ignoreNotSession = False)
      res = uApi.rem_order(parts[1])
      await irc.wMsg(to, str( res ) )
  @staticmethod 
  async def uCActiveOrder(irc, user_part, to, msg):
      parts = msg.split( " " )
      if len(parts) != 3:
          await irc.wMsg(to, "cActiveOrder %key_order% %true/false%")
          return False
      if parts[2] != "false" and parts[2] != "true":
       await irc.wMsg(to, "true or false will be")
       return False
      uApi = aClient.getAPIForUser(user_part, ignoreNotSession = False)
      r = True if parts[2] == "true" else False
      print(r)
      res = uApi.change_active_order(parts[1], r)
      await irc.wMsg(to, str( res ) )
      pass
  @staticmethod
  async def uDoTrade(irc, user_part, to, msg):
      parts = msg.split( " " )
      if len(parts) != 3:
          await irc.wMsg(to, "doTrade %key_order% %count%")
          return False
      uApi = aClient.getAPIForUser(user_part, ignoreNotSession = False)
      res = uApi.do_trade(parts[1], parts[2])
      await irc.wMsg( to, str(res) )
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
    'getCoinList': uGetAllowCoins,
    'getNotify': uGetNotify,
    'getBalance': uGetUInfo,
    'uSession': uUpdateSession,
    #
    'cOrder': uCOrder,
    'gOwnOrders': uGOwnOrders,
    'rOrder': uROrder,
    'cActiveOrder': uCActiveOrder,
    'doTrade': uDoTrade
  }
  
