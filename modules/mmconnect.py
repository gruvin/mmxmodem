import sys
import serial
from time import time, sleep
import logging

log = logging.getLogger()

SOH='\x01'
STX='\x02'
ACK='\x06'
NAK='\x15'
CAN='\x18'

log.debug('opening serial port')
def mmconnect(sp):
    try:
        s = serial.Serial(
        port=sp, 
        baudrate=115200, 
        bytesize=8, 
        parity='N',
        stopbits=1,
        timeout=3,
        rtscts=1,
#    dsrdtr=1
        )
    except:
      print 'ERROR: Could not access serial port ' + sp + '\n'
      quit()

    found = 0
    for a in range(1, 6):
        log.debug('Waiting for "... Maximite ..." [%d]', a)
        hello = ''
        timeout = time() + 2.0
        while (1):
            log.debug('time: %f', time())
            if time() > timeout: 
                log.debug('TIMEOUT');
                break
            if s.inWaiting():
                c = s.read()
                # sys.stdout.write(c)
                if c == NAK or c == ACK or c == STX or c == SOH:
                    log.debug('Detected xmodem session. Attempting to cancel it ...')
                    for i in range(1, 5): 
                        s.write(CAN)
                        sleep(0.1)
                    sleep(1.0)
                    s.readline()
                    hello=''
                    break
            
                elif c == '\r':
                    break

                else:
                    hello += c

        if hello.find('Maximite') != -1: 
            found = 1
            break
        
        s.write(NAK)
        s.flushInput()
        s.close()
        log.debug('closing serial port')
        sleep(1.0) 
        log.debug('re-opening serial port')
        s.open()

    if found == 0:
        print 'Expected "... Maximite ..." but got "' + hello + '"\nAborting.\n\n'
        quit()

    log.info('Maximite connected. Checking for command prompt ...')

# now ensure that we are at a cmd prompt
    found = 0
    for n in range(1, 2):
        s.write('\003');
        sleep(0.2)
        s.flushInput();
        s.write('print "m""m""x"\r')
        sleep(0.2)
        s.readline()
        hello = s.readline()
        log.debug('prompt? %s', hello)
        if hello.find('mmx') != -1: 
            found = 1
            break
        sleep(1.0)
        s.flushInput()

    if found == 0:
        print 'Cannot seem to get to a command prompt :-(\nAborting\n\n'
        quit()

    sleep(0.2)
    return s
