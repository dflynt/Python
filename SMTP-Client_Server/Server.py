'''
Author: Daniel flynt
Last edited: October 24, 2:01PM
Description: This is an SMTP server that formats email files 
according to the RFC 822 standard.
'''
mail_var = "MAIL"
from_var = "FROM:"
space = " "
rcpt_var = "RCPT"
to_var = "TO:"
data_var = "DATA"
def check_RCPT(rcpt_var, str):
	"This checks the validity of the RCPT command"
	if str[0:4] != rcpt_var:
		print str
		print "500 Syntax error: command unrecognized"
		return -1
	elif str[4] != space:
		print str
		print "500 Syntax error: command unrecognized"
		return -1
	i = 4
	while str[i] != "T":
		i += 1
		if i == len(str):
			print str
			print "500 Syntax error: command unrecognized"
			return -1
	if str[i:i+3] != to_var:
		print str
		print "500 Syntax error: command unrecognized"
		return -1
	else:
		return i+2	
def check_Data(data_var, str):
	"This checks the validity of the DATA command"
	if str[0:4] != data_var:
		print "500 Syntax error: command unrecognized"
		return -1
	else:
		#print "DATA"
		return 1
def check_MailFrom(mail_var, from_var, str):
	"This checks the validity of the SMTP command"
	if str[0:4] != mail_var:
		print str
		print "500 syntax error: command unrecognized"
		return -1
	elif str[4] != space and  str[4] != "\t":
		print str
		print "500 Syntax error: command unrecognized"
		return -1

	#finds where the word 'FROM:' starts in the string
	i = 0
	while str[i] != "F":
		i = i + 1
		if i == len(str):
			print str
			print "500 Syntax error: command unrecognized"
			return -1
	if str[i:i+5] != from_var:
		print str
		print "500 Syntax error: command unrecognized"
 		return -1
	elif str[i+5:] == "":
		print str
		print "501 Syntax error in parameters or arguments"
		return -1
	else:
		return i + 5	
def check_Domain(str):
	foundPeriod = False
	foundNumberCount = 0
	if str[:len(str)-1] == ">" or str[:len(str)-1] == "" or str[:len(str)-1] == " " or str[:len(str)-1] == "\t":
		return False
	i = 0

	if ord(str[i]) >= 48 and ord(str[i]) <= 57:
		return False
	#check for any invalid characters. - 1 for >	
	for i in range(len(str) - 2):	
		if ord(str[i]) >= 65 and  ord(str[i]) <= 90 or \
		ord(str[i]) >= 97 and  ord(str[i]) <= 122 or \
		ord(str[i]) >= 48 and ord(str[i]) <= 57 or str[i] == ".":
			if ord(str[i]) >= 65 and  ord(str[i]) <= 90 or \
			ord(str[i]) >= 97 and  ord(str[i]) <= 122:
				foundPeriod = False
				continue
			if str[i] == ".":
				if foundPeriod == True:
					return False
				foundPeriod = True
				continue
			if ord(str[i]) >= 48 and  ord(str[i]) <= 57:
				if foundPeriod:
					return False
				else:
					continue
			else:
				foundPeriod = False
		#else not in specified range return false		
		else:
			return False
def check_Path(mail_var, from_var, str, index):
	i = index	
	while str[i] != "<":
		i += 1
		#if it hasn't been found in the string, print error
		if i == len(str):
			print "501 Syntax error in parameters or arguments"
			return -1
	if str[i-1] != ":" and str[i-1] != " " and str[i-1] != "\t":
		print str
		print "501 Syntax error in parameters or arguments"
		return -1
	index = index + 1
	#increment past < character and start reading the email address
	atCounter = 0
	for k in range(len(str)):
		if str[k] == "@":
			atCounter += 1
	if atCounter !=  1:
		print str
		print "501 Syntax error in parameters or arguments"
		return -1
	#while loop to search for the mailbox in the string
	i += 1
	count = i
	foundLetter = False
	while str[i] != "@":
		if ord(str[i]) >= 65 and  ord(str[i]) <= 90 or \
		ord(str[i]) >= 94 and ord(str[i]) <= 126 or \
		ord(str[i]) >= 48 and ord(str[i]) <= 57 or \
		ord(str[i]) == 63 or ord(str[i]) == 61 or \
		ord(str[i]) == 47 or ord(str[i]) >= 42 and ord(str[i]) <= 43 or \
		ord(str[i]) >= 35 and ord(str[i]) <= 38 or ord(str[i])== 33:
			foundLetter = True
			i += 1	
		elif i == len(str):
			print str
			print "501 Syntax error in parameters or arguments"
			return -1
		else:
			print str
			#character not in specified ascii range
			print "501 Syntax error in parameters or arguments"
			return -1
	address = str[count:i]
	if " " in address or "\t" in address:
		print str
		print "501 Syntax error in parameters or arguments"
		return -1
	domainStart = i+1
	if address == "":
		print str
		print "501 Syntax error in parameters or arguments"
		return -1
	pathCloserIndex = 0
	#check if there are spaces after mailbox@
	while i < len(str):
		if str[i] == ">":
			pathCloserIndex = i
		if str[i] == " ":
			print str
			print "501 Syntax error in parameters or arguments"
			return -1	
		else:
			i += 1
	#> character before end of domain	
	if pathCloserIndex < len(str) - 2:
		print str
		print "501 Syntax error in parameters or arguments"
		return -1
	#start parsing the domain
	if check_Domain(str[domainStart:]) == False:	
		print str
		print "501 Syntax error in parameters or arguments"
		return -1
	#if the program has made it down this far, sender is ok
	emailAddress = str[count:len(str)-1]
	emailAddress = emailAddress + " " + str[domainStart:len(str)-1] 
	return emailAddress
import socket
import sys
import os
sender = ""
receiver = ""
emailAddressList = [];
fileToWriteList = [];
port = sys.argv[1]
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("",int( port)))
server.listen(0)
while True:
	sender = ""
	receiver = ""
	del emailAddressList[:]
	del fileToWriteList[:]
	clientSocket, addr = server.accept()
	greeting = "220 Welcome to " + socket.gethostname()
	clientSocket.send(greeting.encode())
	#receive HELO command
	helo = clientSocket.recv(1024).decode()
	helo = "250 " + helo + " pleased to meet you."
	clientSocket.send(helo.encode())
	while True:
		input = clientSocket.recv(1024).decode()
		if input is False and sender == "":
			print "501 Syntax error in parameters or arguments"
			break
		if input[0] == 'M':
			i = check_MailFrom(mail_var, from_var, input)
			if i != -1:
				mailfrom = check_Path(mail_var, from_var, input, i)
				if mailfrom != -1:
					if sender != "":
						clientSocket.send("503".encode())
						clientSocket.close()
						break
					else:
						sender = mailfrom.split(" ")	
						clientSocket.send("250".encode())
						continue
				else:
					clientSocket.send("501 Syntax error in parameters".encode())
					clientSocket.close()
					break
			if i == -1:
				clientSocket.send("500/501 Syntax Error in parameters or arguments".encode())
				clientsocket.close()
				break
		elif input[0] == 'R': 
			i = check_RCPT(rcpt_var, input)
			if i != -1:
				receiver = check_Path(mail_var, from_var, input, i)
				if receiver != -1:
					if sender == "":
						clientSocket.send("503".encode())
						clientSocket.close()
						break
					else: 
						receiver = receiver.split(" ")
						clientSocket.send("250".encode())
						emailAddressList.append(receiver)
						continue
				else:
					clientSocket.send("501 Syntax error in parameters or arguments".encode())
					clientSocket.close()
					break
			if i == -1:
				clientSocket.send("500/501 Syntax error in paramters or arguments".encode())
				clientSocket.close()
				break
		elif input[0] == 'D':
			if sender == "" or receiver == "":
				clientSocket.send("503".encode())
				clientSocket.close()
				#bad input so take in another line and
				#reiterate through the loop to parse what was just typed
				break
			i = check_Data(data_var, input)
			if i != -1:
				if sender == "" or receiver == "":
					clientSocket.send("503".encode())
					clientSocket.close()
					#bad input so take in another line and
					#reiterate through the loop to parse what was just typed
					break
				else:
					#file creation
					for f in range(len(emailAddressList)):
						fileName = emailAddressList[f][1]
						if os.path.isfile(fileName):
							file = open(fileName, 'a')
							isInList = False
							#check if domain is already in the 'fileToWriteList'
							for f in range(len(fileToWriteList)):
								if file.name ==fileToWriteList[f].name:
									isInList = True
							if isInList == False:
								fileToWriteList.append(file)
						else:
							file = open(fileName, 'w')
							fileToWriteList.append(file)
							#add file object to 'mailing list'
			elif i == -1:
				clientSocket.send("500".encode())
				clientSocket.close()
				break
			for f in range(len(fileToWriteList)):
				fileToWriteList[f].write("From: " + sender[0] + "\n")
				for emailAdd in range(len(emailAddressList)):
					fileToWriteList[f].write("To: " + emailAddressList[emailAdd][0] + "\n")
			message = clientSocket.recv(1024).decode() + "\n"
			while message != ".":
				for f in range(len(fileToWriteList)):
					fileToWriteList[f].write(message + '\n')
					fileToWriteList[f].flush()
				message = clientSocket.recv(1024).decode()
			#break to while loop that listens for connections		
			#Once the program breaks out of while loop
			#reset all variables to have a new sender and receivers.
			sender = ""
			receiver = ""
			for fi in range(len(fileToWriteList)):
				fileToWriteList[fi].close()
			del emailAddressList[:]
			del fileToWriteList[:]
			clientSocket.close()	
			break	
		else:
			clientSocket.close()
			break
