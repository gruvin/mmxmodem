# mmsend/mmrecv
## Easily transfer files to/from a Maximite over USB serial Mac/Linux/Windows
#### Requires Python and the xmodem python module

### DOCUMENTATION DRAFT

### Prelude

I enjoy messing about with Geoff's cool little <a href="http://geoffg.net/mini-maximite.html">Maximite mini</a> micro-computer, based on a PIC32 chip. Call me quaint if you will. But I've built several of them and find them a joy to use, when I feel like a change from Raspberry Pi's and Arduinos and Sparkcores, etc.

By default, the 'mini doesn't have an SD-Card. So to transfer files back and forth, Geoff implemented the (simple) XMODEM protocol as a built-in feature of MM-BASIC.

### So why these scripts, specifically?

Under Windows, one may use TeraTerm to emulate a VT100 terminal (for which MM-Basic is designed) as serial console. Files can be easily transferred using MM-BASIC's _XMODEM SEND/RECEIVE_ commands and TeraTerm's corresponding built-in Xmodem file transfer features of TeraTerm. But who in the world wants to use Windows? :-P

I generally prefer to use either Mac OS X or Ubuntu Linux, along with Xterm and ```screen```. (See below for some specifics about that.)

So what? Well, you may think that transferring a file to my little Maximite mini would be as simple as initiating the transfer on the 'mini, with ```xmodem receive "test.bas"<CR>```, then simply using ```sx /dev/ttyACM0 test.bas < /dev/ttyACM0 > /dev/ttyACM0```. But there's a catch.

It turns out that the Maximite always sends something like, "Maximite BASIC Version 4.5 ...", whenever a new USB serial connection is made. This upsets ```sx``` considerably, resulting in the proverbial, _"Close ... but no cigar"_.

So, I wrote ```mmsend``` and ```mmrecv``` -- Python scripts that take care of those problems, using the Python XMODEM module (author unknown) and some other tricks.

    Usage: mmsend <serial-port> <filename> [<dest-filename>]

and

    Usage: mmrecv <serial-port> <source-filename> [<local-filename>]

Example: ```mmsend /dev/ttyACM0 foo.bas wahoo.bas```

Sample session:

    % ./mmsend /dev/ttyACM0 foo.bas wahoo.bas
    MM-BASIC connected. Setting up XMODEM transfer ...
    Sending  foo.bas as wahoo.bas ...
    Done!

Sample session -- Windows Command Prompt:

    C:\Users\Gruvin\mmxmodem> mmsend com3 foo.bas wahoo.bas
    MM-BASIC connected. Setting up XMODEM transfer ...
    Sending  foo.bas as wahoo.bas ...
    Done!

### Notes

* All files are transferred in binary mode. No CR/LF translation is attempted for text files. But MMBasic hadnles that OK.
* Wildcards (multiple files) are NOT handled (on either end). Thus, ```mmrecv /dev/tty/ACM0 *.BAS``` will *not* work.
* Received files often have trailing null characters on the end. I believe this is a bug at the Maximite end -- possibly related to the "A:" drive internal block size or something. (I'm really just guessing.) In any case, I can't really strip them off, because a non-".BAS" file may well have appended null chars intentionally. Any ideas Geoff?

### Wait! What magic is this?

In case it wasn't made clear above ...

#### You do NOT need to initiate XMODEM on the Maximite. Just quit your terminal and go.

You do have to quit your terminal (or at least tell it to disconnect) because these scripts require sole access to the USB serial port.

The scripts take care of initialising the ```xmodem send/receive``` at the Maximite end. When you're done transferring files, simply re-launch your terminal to carry on with the Maximite, where you left off.


## Xterm configuration

To get Xterm working well with MM-BASIC, I have the following in my ```~/.Xresources``` file ...

    xterm*VT100.geometry:     80x36
    xterm*faceName:           Terminus:style=Regular:size=10
    !xterm*font:              -*-dina-large-r-*-*-16-*-*-*-*-*-*-*
    xterm*dynamicColors:      true
    xterm*utf8:               2
    xterm*backarrowKey:       true
    xterm*backarrowKeyIsErase: false
    xterm*oldXtermFKeys:      true
    xterm*reverseVideo:       true

Then I launch ```xterm``` and ```screen``` (to connect to the Maximite) within that in one line, as follows ...

    % xterm -e screen -S minimite /dev/ttyACM0 115200

... though in fact, you only really need ...

    % xterm -e screen /dev/ttyACM0

I created a launcher for Ubuntu for this, as follows ...

In ```~/.local/share/applications/``` ...

File: ```minimite.desktop```

    [Desktop Entry]
    Name=Maximite Mini
    Comment=
    Path=/home/bryan
    Exec=/usr/bin/xterm -e screen -S minimite -c /home/bryan/.scn_minimiterc /dev/ttyACM0 115200
    Type=Application
    Icon=xterm-color
    Terminal=false

(The file ``` /home/bryan/.scn_minimiterc``` contains the single line, ```autodetach off```, which causes ```screen``` to completely die when I close the Xterm window -- otherwise it merely detaches, leaving the serial port tied up.)

With that in place, your can use the Search feature on the desktop, "Maxi" and if you like, drag the icon to the launch bar (is that what it's called, on the left of the desktop?) for quick access.


