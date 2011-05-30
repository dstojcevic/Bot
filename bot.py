import sys, time
import socket
import string
import argparse

def cmd():
	parser = argparse.ArgumentParser()

# IRC
	parser.add_argument('-s', action='store', dest='server',
						help='Set IRC server')
	parser.add_argument('-p', action='store', dest='port',
						help='Set IRC port')
	parser.add_argument('-n', action='store', dest='nick',
						help='Set IRC nick')
	parser.add_argument('-i', action='store', dest='ident',
						help='Set IRC ident')
	parser.add_argument('-r', action='store', dest='real',
						help='Set IRC real name')
# daemon
	parser.add_argument('-D', action='store_false', default=True,
						dest='deactivate_daemon',
						help='Deactivate deamon')
	
	return parser.parse_args()

def bot(args):
# -s
	HOST="irc.freenode.net"
	if (args.server):
		HOST=args.server
# -p
	PORT=6667
	if (args.port):
		PORT=args.port
# -n
	NICK="Bot"
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
	
	print args
	print HOST
	#server connect 
	IRCsocket=socket.socket()
	IRCsocket.connect((HOST, PORT))
	IRCsocket.send("NICK %s\r\n" % NICK)
	IRCsocket.send("USER %s %s bla :%s\r\n" % (IDENT, HOST, REALNAME))
	IRCsocket.send("JOIN #irclib\r\n")
	IRCsocket.send("QUIT\r\n")
	
if __name__ == "__main__":
	args = cmd()
	bot(args)