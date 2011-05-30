#!/usr/bin/env python
 
import sys, time
import socket
import string
import argparse
from daemon import Daemon
import os
from os.path import isfile
import smtplib
import imp
from email import Encoders
from email.MIMEBase import MIMEBase
from email.MIMEMultipart import MIMEMultipart
from email.Utils import formatdate

def use_plugin(name, path, globals=None, locals=None, fromlist=None):
# source: http://technogeek.org/python-module.html
	try:
		return sys.modules[name]
	except KeyError:
		pass

	fp, pathname, description = imp.find_module(name, [path])
	
	try:
		return imp.load_module(name, fp, pathname, description)
	finally:
		if fp:
			fp.close()

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
# mail
	parser.add_argument('-address', action='store', dest='m_address', help='Mail address')
	parser.add_argument('-server', action='store', dest='m_server', help='Mail server')
	parser.add_argument('-username', action='store', dest='m_username', help='Mail username')
	parser.add_argument('-password', action='store', dest='m_password', help='Mail password')
#plugin
	parser.add_argument('-plugin', action='store', dest='plugin', help='used logging plugin', default="bot_sqlite")
	
	return parser.parse_args()

def bot():
	global args
	global base_path
	
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
	
	
	database = os.path.dirname(base_path) + "log.db"
	db = use_plugin(args.plugin, os.path.dirname(base_path))
	
	if not isfile(database):
		db.create(database)
		
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
				db.add(database, msg[1], msg[0].split("!")[0][1:], " ".join(msg[3:]))
				
				if (msg[3][1:] == "mail"):
					if (args.m_address & args.m_server):
						if len(msg) > 3:
							mail = MIMEMultipart()
							mail["From"] = args.m_address
							mail["To"] = msg[4]
							mail["Subject"] = "IRC Log"
							mail['Date'] = formatdate(localtime=True)
						 
							part = MIMEBase('application', "octet-stream")
							part.set_payload( open(database,"rb").read() )
							Encoders.encode_base64(part)
							part.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(database))
							mail.attach(part)
						 
							server = smtplib.SMTP(args.m_server)
							if (args.m_username & args.m_password):
								server.login(args.m_username, args.m_password)

							try:
								failed = server.sendmail(args.m_address, msg[4], mail.as_string())
								server.close()
							except Exception, e:
								errorMsg = "Unable to send email. Error: %s" % str(e)
				
				elif (msg[3][1:] == "when"):
					if len(msg) > 3:
						if msg[4] in online:
							IRCsocket.send("PRIVMSG %s :%s is now online\r\n" % (msg[0].split("!")[0][1:], msg[4]))
						else:
							IRCsocket.send("PRIVMSG %s :%s was last seen %s\r\n" % (msg[0].split("!")[0][1:], msg[4], db.seen(database, msg[4])))
						
			elif (msg[1] == "JOIN"):
				db.add(database, msg[1], msg[0].split("!")[0][1:], msg[2])
				online.add(msg[0].split("!")[0][1:])
			elif (msg[1] == "PART"):
				db.add(database, msg[1], msg[0].split("!")[0][1:], msg[2])
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
	global base_path
	base_path = sys.argv[0]
	
	if not args.deactivate_deamon:
		daemon.start()
	else:
		bot()
	sys.exit(0)