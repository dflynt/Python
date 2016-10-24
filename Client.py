'''
Author: Daniel Flynt
Last edited: October 24, 2:01PM
Description: Email client that connects to an SMTP server.
'''
import sys
import socket
def main():
	serverName = sys.argv[1]
	port = sys.argv[2]
	try:
		clientSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		clientSock.connect((serverName, int(port)))
	except socket.error:
		print "Socket in use or server unavailable"
		return
	greeting = clientSock.recv(1024).decode()
	#print greeting
	helo = "HELO " + socket.gethostname()
	#print helo
	clientSock.send(helo.encode())
	response = clientSock.recv(1024).decode()
	#print response
	if "250" not in response:
		return
	while True:
		print "From: ",
		line = raw_input()
		if line == "QUIT":
			return
		elif line is False:
			print "No valid sender address"
			clientSock.close()
			return
		elif "," in line:
			print "Can only have one sender"
			clientSock.close()
			return
		fromCommand =  "MAIL FROM: <" + line + ">"
		clientSock.send(fromCommand.encode())
		smtpResponse = clientSock.recv(1024).decode()
		if "250" not in smtpResponse:
			print "QUIT" + smtpResponse
			return
		print "To: ",
		line = raw_input()
		if line == "QUIT":
			clientSock.close()
			return
		elif line is False:
			print "No valid recipient address"
			clientSock.close()
			return
		if ", " in line:
			receivers = line.split(", ")
			for i in receivers:
				i = "RCPT TO: <" + i + ">"
				clientSock.send(i.encode())
				smtpResponse = clientSock.recv(1024).decode()
				if "250" not in smtpResponse:
					print smtpResponse
					print "QUIT"
					return
		else:
			rcptToCommand = "RCPT TO: <" + line + ">"
			clientSock.send(rcptToCommand.encode())
			smtpResponse = clientSock.recv(1024).decode()
			if "250" not in smtpResponse:
				print smtpResponse
				print "QUIT"
				clientSock.close()
				return
		clientSock.send(("DATA").encode())
		print "Subject:",
		if line == "QUIT":
			clientsock.close()
			return
		subject = raw_input()
		clientSock.send(("Subject: " + subject).encode())
		print "Message:",
		input = raw_input()
		while input != ".":
			clientSock.send(input.encode())
			input = raw_input()
		clientSock.send(input.encode())
		#response = clientSock.recv(1024).decode()
		#print response
		#clientSock.send(("QUIT").encode())
		#response = clientSock.recv(1024).decode()
		#print response
		clientSock.close()
		return
main()
