#!/opt/local/bin/python
import sys
from os import remove, rename, unlink
from os.path import isfile, dirname, realpath
from time import sleep
import logging
import serial

real_path = dirname(realpath(__file__))
sys.path.insert(0, real_path + '/modules')
from mmxmodem import XMODEM
from mmconnect import mmconnect

if len(sys.argv) < 3:
  print 'Usage: ' + sys.argv[0] + ' <serial-port> <filename> [<dest-filename>]\n'
  quit()

sp = sys.argv[1]
fn = sys.argv[2]
dfn = fn
if len(sys.argv) == 4: dfn = sys.argv[3]

try:
    stream = file(fn, 'rb')
except:
    print 'Oops! Could not open local file %s\n' % (fn)
    quit()
    
def getc(size, timeout=1):
  data = s.read(size)
  return data or None
def putc(data, timeout=1):
  sent = s.write(data)
  s.flush()
  return sent or None
xmodem = XMODEM(getc, putc)

log = logging.getLogger()
log.setLevel(logging.WARNING)
ch = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter('%(asctime)s - %(levelname)s: %(message)s')
ch.setFormatter(formatter)
log.addHandler(ch)

s = mmconnect(sp)

print "Maximite connected. Setting up XMODEM transfer ..."

s.write('xmodem receive "' + dfn + '"\r')
sleep(0.2)
s.flushInput()

print 'Sending  ' + fn + ' as ' + dfn + ' ...'

status = xmodem.send(stream, quiet=0, retry=8)
if (status):
    print "Done!"
else:
    print "There could be a problem :-("

stream.close()
s.close()

