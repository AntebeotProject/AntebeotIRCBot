import requests

uCookiesSessions = {} # user_part : req.cookies
REST_API_WEB='https://antebeot.world/'
CAPTCHA_PATH='/var/www/html/captchas'
CAPTCHA_WEBSITE='byyesxdjlrywth252dcplh46ypyvurpbjudr5koswiu27ywecz3q.b32.i2p/captchas/'

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
   global uCookiesSessions
   captcha_req = requests.get(REST_API_WEB+'restapi/captcha?w=get')
   cData = captcha_req.content
   if not captcha_req.cookies['captcha_id'] is None: 
    # drop files in the dir though cron/... 
    with open("%s/%s.png" % (CAPTCHA_PATH, captcha_req.cookies['captcha_id']) , "wb" ) as f:
     f.write(cData)
     f.close()
     await irc.wMsg(to, "path to your file: %s/%s.png" % (CAPTCHA_WEBSITE,captcha_req.cookies['captcha_id']))
     try: 
      if uCookiesSessions[user_part] is None: uCookiesSessions[user_part] = {}   #captcha_req.cookies # add cookies. not rewrite it! todo:!
     except Exception as e:  uCookiesSessions[user_part] = {}
     uCookiesSessions[user_part]['captcha_id'] = captcha_req.cookies['captcha_id']
     print("uCookieSession now is")
     print(uCookiesSessions[user_part])
     pass
     
  # there is example how to use cookie
  
  
  @staticmethod
  async def uTestCaptcha_(irc, user_part, to, msg):
   global uCookiesSessions
   print("uCookieSession now is (#2)")
   print(uCookiesSessions[user_part])
   try: 
       if uCookiesSessions[user_part] is None or  uCookiesSessions[user_part]['captcha_id'] is None:
        await irc.wMsg(to, "You are not ask captcha before! (#1)")
        return False
       answ = msg.split(" ", 2)[1].replace("\n", "").replace("\r", "")
       print("answ")
       print(answ)
       captcha_answ = requests.get( '%s/restapi/captcha?w=answerTest&a=%s' % (REST_API_WEB,answ), cookies={ 'captcha_id': uCookiesSessions[user_part]['captcha_id'] } )
       await irc.wMsg(to, captcha_answ.content)
   except Exception as e: 
        await irc.wMsg(to, "You are not ask captcha before! (#2) : " + str(e))
        return False
   #
  @staticmethod
  async def uPing(irc, user_part, to, msg):
   print("Answer to ping")
   await irc.wMsg(to, "pong")
   pass
  @staticmethod
  async def uRegister(irc, user_part, to, msg):
   await irc.wMsg(to, "Not implemented yet")
   pass
  @staticmethod
  async def uDashboard(irc, user_part, to, msg):
   r = requests.get('%s/restapi/dashboard' % REST_API_WEB)
   decoded = r.content.decode("utf-8")
   await irc.wMsg(to, decoded)
   pass
  both_cmnds = {
    'ping' : uPing,
    'register': uRegister,
    'dashboard': uDashboard,
    'getCaptcha': uTestCaptcha,
    'testCaptcha': uTestCaptcha_
  }
  
