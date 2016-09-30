'''
Author: Daniel Flynt
Last edited: September 30, 2016 6:00PM
Description: Parsing program that reads an email file
and outputs the proper SMTP commands until the EOF
'''
import sys
def main():
	fileName = raw_input()
	f = open(fileName, 'r')
	sender = ""
	receivers = ""
	dataSequence = False
	for line in f:
		if line[0:5] == "From:":
			if dataSequence == True:
				#if we get a From: line while dataSequence is true
				#that must mean that a new message is starting
				#reset all variable and begin parsing new message
				dataSequence = False
				print "."
				input = raw_input()
				if input[0:3] == "250":
					print >> sys.stderr, input
				else:
					print input
					print "QUIT"
					return

			sender = line[5:len(line)-1]
			print "MAIL FROM:" + sender
			input = raw_input()
			if input[0:3] == "250":
				print >> sys.stderr, input
				continue
			else:
				print input
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
				continue
			else:
				print input
				print "QUIT"
				return
		else:
			#if block for the first line of actual message
			if dataSequence == False:
				dataSequence = True
				print "DATA"	
				input = raw_input()
				if input[0:3] == "354":
					print >> sys.stderr, input
					print line[:len(line)-1]
					continue
				else:
					print input
					print "QUIT"
					return
			else:
				print line[:len(line)-1]	
	print "."
	input = raw_input()
	print >> sys.stderr, input
	print "QUIT"
main()