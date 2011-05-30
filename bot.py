import sys, time
import socket
import string

def bot():
	HOST="irc.freenode.net"
	PORT=6667
	NICK="Bot"
	IDENT="bot"
	REALNAME="IRC Bot"
	
	#server connect 
	IRCsocket=socket.socket()
	IRCsocket.connect((HOST, PORT))
	IRCsocket.send("NICK %s\r\n" % NICK)
	IRCsocket.send("USER %s %s bla :%s\r\n" % (IDENT, HOST, REALNAME))
	IRCsocket.send("JOIN #irclib\r\n")
	IRCsocket.send("QUIT\r\n")
	
if __name__ == "__main__":
	bot()