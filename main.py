from IRC.IRC import IRC as IRC
import configparser
def WriteDefConfig():
 config = configparser.ConfigParser()
 config['irc'] = {}
 config['irc']['port'] = '6668'
 config['irc']['addr'] = 'localhost'
 with open('settings.ini', 'w') as configfile:
     config.write(configfile)

def main():
  try:
   c = configparser.ConfigParser()
   c.read('settings.ini')
   # TODO: config
   m_irc = IRC( addr = c['irc']['addr'], port = int(c['irc']['port']) )
  except KeyError as _:
   WriteDefConfig()
   print("Configure your settings.ini firstly")

main()
