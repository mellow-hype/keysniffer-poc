# README
A simple PoC keysniffer for Linux using the technique discussed in [this article](http://theinvisiblethings.blogspot.com/2011/04/linux-security-circus-on-gui-isolation.html). Not meant to be anything super dangerous or useful at the moment, but we'll see where it goes.


**Depends on `xinput` and `xmodmap`. Written in Python 3.**

## Details
The lack of isolation between GUI objects in the X display server allows any process, privileged or unprivileged, to see what other processes are doing in the context of the GUI. This makes it trivial to sniff keystrokes, take screenshots of other windows, etc. This is a fundamental flaw in the design of the X server architecture, though it is not unique to it.

This PoC keysniffer shows how an unprivileged user could run such a script and capture admin credentials or other private data on a shared system. As an experiment, one can run the script in one terminal window while using `su` to elevate privileges in another, for example. The script will capture all keystrokes, including the credentials used to elevate privileges.

## Usage
```
python3 poc.py
```
To stop the script, Control-C or send a keyboard interrupt to terminal where this is running.

The script will write the collected keys to a file 'rekt.txt' upon receiving a keyboard interrupt. Modifications can be done directly in the code which shouldn't be too difficult.
