import requests
uCookiesSessions = {} # user_part : req.cookies
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
  def uTestCaptcha(irc, user_part, to, msg):
   global uCookiesSessions
   captcha_req = requests.get('https://antebeot.ru/restapi/captcha?w=get')
   cData = captcha_req.content
   if not captcha_req.cookies['captcha_id'] is None: 
    # drop files in the dir though cron/... 
    with open("C:\\poolserver\\ver3\\HTTPServer\\temporarly\\%s.png" % (captcha_req.cookies['captcha_id']) , "wb" ) as f:
     f.write(cData)
     f.close()
     irc.wMsg(to, "path to your file: https://antebeot.ru/restapi/temporarly/%s.png" % (captcha_req.cookies['captcha_id']))
     try: 
      if uCookiesSessions[user_part] is None: uCookiesSessions[user_part] = {}   #captcha_req.cookies # add cookies. not rewrite it! todo:!
     except Exception as e:  uCookiesSessions[user_part] = {}
     uCookiesSessions[user_part]['captcha_id'] = captcha_req.cookies['captcha_id']
     print("uCookieSession now is")
     print(uCookiesSessions[user_part])
     pass
     
  # there is example how to use cookie
  
  
  @staticmethod
  def uTestCaptcha_(irc, user_part, to, msg):
   global uCookiesSessions
   print("uCookieSession now is (#2)")
   print(uCookiesSessions[user_part])
   try: 
       if uCookiesSessions[user_part] is None or  uCookiesSessions[user_part]['captcha_id'] is None:
        irc.wMsg(to, "You are not ask captcha before! (#1)")
        return False
       answ = msg.split(" ", 2)[1].replace("\n", "").replace("\r", "")
       print("answ")
       print(answ)
       captcha_answ = requests.get( 'https://antebeot.ru/restapi/captcha?w=answerTest&a=%s' % answ, cookies={ 'captcha_id': uCookiesSessions[user_part]['captcha_id'] } )
       irc.wMsg(to, captcha_answ.content)
   except Exception as e: 
        irc.wMsg(to, "You are not ask captcha before! (#2) : " + str(e))
        return False
   #
  @staticmethod
  def uPing(irc, user_part, to, msg):
   print("Answer to ping")
   irc.wMsg(to, "pong")
   pass
  @staticmethod
  def uRegister(irc, user_part, to, msg):
   irc.wMsg(to, "Not implemented yet")
   pass
  @staticmethod
  def uDashboard(irc, user_part, to, msg):
   r = requests.get('https://antebeot.ru/restapi/dashboard')
   decoded = r.content.decode("utf-8")
   irc.wMsg(to, decoded)
   pass
  both_cmnds = {
    'ping' : uPing,
    'register': uRegister,
    'dashboard': uDashboard,
    'getCaptcha': uTestCaptcha,
    'testCaptcha': uTestCaptcha_
  }
  