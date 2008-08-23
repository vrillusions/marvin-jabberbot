#!/usr/bin/python

##  --------------------------------------------------------
##  imports 
##  --------------------------------------------------------

import sys, os, re
import urllib2


##  --------------------------------------------------------
##  constants
##  --------------------------------------------------------

YubicoAuthSrvURLprefix = 'http://api.yubico.com/wsapi/verify?id='
AuthSrvRespRegex = re.compile('^status=(?P<rc>\w{2})')


##  --------------------------------------------------------
##  function definitions
##  --------------------------------------------------------

def usage():
  print "\n\nUsage :  " + os.path.basename(sys.argv[0]) + "  clientID  oneTimePasscode\n\n\n"

def verify(clientId,otp):
  YubicoAuthSrvURL = YubicoAuthSrvURLprefix + clientId + "&otp=" + otp
  fh = urllib2.urlopen(YubicoAuthSrvURL)   # URL response assigned to a file handle/object

  for line in fh:
    AuthSrvRespMatch = AuthSrvRespRegex.search(line.strip('\n'))

    if AuthSrvRespMatch:
      if AuthSrvRespMatch.group('rc') == 'OK': return True 
      else: return False

      break 


##  --------------------------------------------------------
##  main program
##  --------------------------------------------------------

if __name__ == '__main__':
  if len(sys.argv) == 3:
    res = verify(sys.argv[1], sys.argv[2])
    if res == True:
      print "\nOTP verification ok\n"
    else:
      print "\nOTP verification failed\n"
  else:
    usage()

 
