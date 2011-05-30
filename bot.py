#!/usr/bin/env python
 
import sys, time
import socket
import string
import argparse
from daemon import Daemon

#args = ""

def cmd():
	parser = argparse.ArgumentParser()

# IRC
	parser.add_argument('-s', action='store', dest='server', help='Set IRC server')
	parser.add_argument('-p', action='store', dest='port', help='Set IRC port')
	parser.add_argument('-n', action='store', dest='nick', help='Set IRC nick')
	parser.add_argument('-i', action='store', dest='ident', help='Set IRC ident')
	parser.add_argument('-r', action='store', dest='real', help='Set IRC real name')
	parser.add_argument('-c', action='store', dest='channel', help='Set IRC channel')
# daemon
	parser.add_argument('-D', action='store_true', default=False, dest='deactivate_deamon', help='Deactivate deamon')
	
	return parser.parse_args()

def bot():
	global args
# -s
	HOST="irc.freenode.net"
	if (args.server):
		HOST=args.server
# -p
	PORT=6667
	if (args.port):
		PORT=args.port
# -n
	NICK="IRC_Bot"
	if (args.nick):
		NICK=args.nick
# -i
	IDENT="bot"
	if (args.ident):
		IDENT=args.ident
# -r
	REALNAME="IRC Bot"
	if (args.real):
		REALNAME=args.real
# -c
	CHANNEL="irclib"
	if (args.channel):
		CHANNEL=args.channel
	
	#server connect 
	IRCsocket=socket.socket()
	IRCsocket.connect((HOST, PORT))
	IRCsocket.send("NICK %s\r\n" % NICK)
	IRCsocket.send("USER %s %s bla :%s\r\n" % (IDENT, HOST, REALNAME))
	IRCsocket.send("JOIN #%s\r\n" % CHANNEL)
	
	buffer = ""
	online = set()
	while 1:
		buffer=buffer + IRCsocket.recv(1024)
		irc=string.split(buffer, "\n")
		buffer=irc.pop()
		
		for msg in irc:
			msg=string.rstrip(msg)
			msg=string.split(msg)
			
			print msg
			
			if(msg[0]=="PING"):
				IRCsocket.send("PONG %s\r\n" % msg[1])
			
			elif ((msg[1] == "PRIVMSG") & (msg[2] == NICK)):
				"add msg to db"
				
				if (msg[3][1:] == "mail"):
					if len(msg) > 3:
						print "send email"
				
				elif (msg[3][1:] == "when"):
					if len(msg) > 3:
						print "seen"
			elif (msg[1] == "JOIN"):
				print "join"
				online.add(msg[0].split("!")[0][1:])
				
			elif (msg[1] == "PART"):
				print "part"
				online.discard(msg[0].split("!")[0][1:])
				
			elif ((msg[2] == NICK) & (len(msg)>3)):
				if ((msg[3] == "=") & (len(msg)>4)):
					if ((msg[4] == ("#" + CHANNEL)) & (len(msg)>5)):
						online.add(msg[5][1:])
						if len(msg) > 6:
							for person in msg[6:]:
								online.add(person)

class MyDaemon(Daemon):
		def run(self):
			bot()

if __name__ == "__main__":
	daemon = MyDaemon('/tmp/daemon-example.pid')
	global args 
	args = cmd()

	if not args.deactivate_deamon:
		daemon.start()
	else:
		bot()
	sys.exit(0)