import imapclient
import logging
import pyzmail
import pyperclip
import sys
import smtplib
import json

#Reaading mail with Subject COUPON CouponType

imapObj = imapclient.IMAPClient('imap.gmail.com', ssl=True)
print("Enter password: ")
passwd = input()
imapObj.login('sender@gmail.com ', passwd)
imapObj.select_folder('INBOX', readonly=True)

dct={}
UIDs = imapObj.search(['SUBJECT COUPON','UNSEEN'])
for item in range(len(UIDs)):
	print("I AM IN UID LOOP		"+str(UIDs[item]))
	rawMessages = imapObj.fetch([UIDs[item]], ['BODY[]', 'FLAGS'])
	
	message = pyzmail.PyzMessage.factory(rawMessages[int(UIDs[item])][b'BODY[]'])#['BODY[COUPON]']
	
	lst = message.get_addresses('from')
	for a,b in lst:
		dct["from"]=b

	lst1 = message.get_addresses('to')
	for c,d in lst1:
		dct["to"]=d
		
	dct["sub"]=message.get_subject()
	
imapObj.logout()

#Sending Mail With Coupon Deatils of CouponType

name=[]
for k,v in dct.items():
	if  k=='from':
		name.append(v)
	if k == 'sub':
		fn = v
		print(fn)
		fileName = fn.replace("COUPON ","")


logging.info("Type of Coupon Selected is "+ fileName)

smtpObj = ""

line = 0
st = ""
# Read the File Present in Folder by using fileName
for i in open(fileName):
	line +=1
	st +=i
	if line==18:
		break

logging.info(st)

try:
	smtpObj = smtplib.SMTP('smtp.gmail.com', 587)
except :
	smtpObj = smtplib.SMTP_SSL('smtp.gmail.com', 465)

smtpObj.ehlo()
smtpObj.starttls()
smtpObj.login('sender@gmail.com',passwd)
for item in range(len(name)):
	logging.info("Mail Send to "+name[item]+ " for Coupon Type "+ fileName)
	smtpObj.sendmail('sender@gmail.com',name[item], 'Subject: Your Coupon for '+fileName+'.\n\n\nDear , Please check the latest '+fileName+' coupon Details'+st+',\n\n\nRegards XYZRAJ')
{}
	

smtpObj.quit()

