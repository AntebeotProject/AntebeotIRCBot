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
  # both_cmnds for a privmsg to PM and channel
  both_cmnds = {
    'ping' : uPing,
    'register': uRegister,
    'dashboard': uDashboard,
    'getCaptcha': uTestCaptcha,
    'testCaptcha': uTestCaptcha_
  }
  
