'''
Author: Daniel Flynt
Last edited: October 3, 2016 11:38AM
Description: Parsing program that reads an email file
and outputs the proper SMTP commands until the EOF
'''
import sys
def main():
	#fileName = raw_input()
	fileName = sys.argv[1]
	f = open(fileName, 'r')
	sender = ""
	receivers = ""
	dataSequence = False
	hasSender = False
	for line in f:
		if line[0:5] == "From:":
			if dataSequence == True:
				#if we get a From: line while dataSequence is True
				#that must mean that a new message is starting
				#set variable to False and begin parsing new message
				dataSequence = False
				print "."
				input = raw_input()
				if input[0:3] == "250":
					print >> sys.stderr, input
				else:
					print >> sys.stderr, input
					print "QUIT"
					return
			if dataSequence == False and hasSender == True:	
			#if a message is blank. This was the best I could come up with 
				input = raw_input()
				if input[0:3] == "354":
					print >> sys.stderr, input
					print >> sys.stderr, "."
					input = raw_input()
					if input[0:3] == "250":
						print >> sys.stderr, input
					else:
						print >> sys.stderr, input
						print "QUIT"
						return
			sender = line[5:len(line)-1]
			print "MAIL FROM:" + sender
			input = raw_input()
			if input[0:3] == "250":
				print >> sys.stderr, input
				continue
			else:
				print >> sys.stderr, input
				print "QUIT"
				return
		elif line[0:3] == "To:":
			#no need to check order of From: and To:
			#because these are 'well-formed' messages
			receiver = line[3:len(line)-1]
			print "RCPT TO:" + receiver
			input = raw_input()
			if input[0:3] == "250":
				print >> sys.stderr, input
				print >> sys.stderr, "DATA"
				hasSender = True
				continue
			else:
				print >> sys.stderr, input
				print "QUIT"
				return
		else:
			#if block for the first line of actual message
			if dataSequence == False:
				dataSequence = True
				hasSender = False
				input = raw_input()
				if input[0:3] == "354":
					print >> sys.stderr, input
					print line[:len(line)-1]
					continue
				else:
					print >> sys.stderr, input
					print "QUIT"
					return
			else:
				print line[:len(line)-1]	
	print >> sys.stderr, "."
	input = raw_input()
	print >> sys.stderr, input
	print "QUIT"
main()
