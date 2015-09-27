import requests,os,bs4
import webbrowser
import sys
import json
import logging
import datetime
import time
import threading

site = "http://www.qwqwqwqwqw.com/"
fileName = ""
couponTypeDict ={1: 'foodpanda', 2: 'paytm', 3:'food', 4: 'olacabs', 5:'flipkart', 6:'uber', 7:'zoomcar',8:'swiggy',9: 'snapdeal', 10:'freecharge', 11:'travel', 12:'electronics', 13:'recharge', 14:'fashion', 15:'furniture'}

vendor={"FOODPANDA": 'foodpanda', "PAYTM": 'paytm', "FOOD":'food', "OLA": 'olacabs', "FLIPKART":'flipkart', "UBER":'uber', "ZOOMCAR":'zoomcar',"SWIGGY":'swiggy',"SNAPDEAL": 'snapdeal', "FREECHARGE":'freecharge', "TRAVEL":'travel', "ELECTRONICS":'electronics', "RECHARGE":'recharge', "FASHION":'fashion', "FURNITURE":'furniture'}


logging.basicConfig(filename="CouponLog.txt", level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def Intialization():
	for k,v in couponTypeDict.items():
		print(k,v)
	print("Do Enter Index for Coupons::")
	logging.info("Do Enter Index for Coupons::")
	index = input()
	return index

def CreateUrl(index,strMore="Nothing"):
	print("you have selected "+couponTypeDict[int(index)]+ "  Coupons.")
	logging.info("you have selected "+couponTypeDict[int(index)]+ "  Coupons.")
	url = site+couponTypeDict[int(index)]+"-coupons/"
	return url


def GetSoup(url):
	logging.info("IN GETSOUP "+url)
	res = requests.get(url)
	res.raise_for_status()
	return bs4.BeautifulSoup(res.text)


def GetRequest(soup,choice="No"):
	#Not Used If and elif Conditions
	if choice == "Dialogue":
		comicElem = soup.select('#showCouponPopup')
	elif choice == "Site":
		comicElem = soup.select('.page-coupons')
	else:
		comicElem = soup.select('.page-body .row .page-coupons')
	return comicElem

def FileRename(FullFileName,Subscript):
	name,ext = os.path.splitext(FullFileName)
	newName = name+Subscript+ext
	os.rename(FullFileName,name+Subscript+ext)
	return newName

def ReadFromFile(FullFileName,no):
	print("ReadFromFile")
	fo = open(FullFileName,"r+")
	position = fo.seek(0, 0);
	str = fo.read(no);
	print(str)

os.makedirs('JSON', exist_ok=True)
def FileCheckUtil(fileName):
	str = os.getcwd()+"\\JSON\\"+fileName
	print(str)
	name = ""
	st = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
	#if os.path.exists(str):
	#IF File is present then just rename the current present file with Current TimeStamp
	if os.path.isfile(str):
		print("Yes Present")
		logging.info("----------------------------Yes Present------------------")
		name = FileRename(str,st)
	#else:
	#	print("Not Present")
	#	logging.info("----------------------NOT Present------------------------")
		#name,ext = os.path.splitext(fileName)
		#print(name+"--"+ext)
	name = str #fileName
	return name

dict={}

def GoTo(Url,Index):
	index = 0
	global fileName
	logging.info("Start GOTO 		"+Url)
	soup = GetSoup(Url)
	comicElem = GetRequest(soup)
	logging.info("PAGE_BODY PAGE_COUPONS 		"+str(len(comicElem)))
	
	#Creating File Name
	fl = couponTypeDict[int(Index)]+".json"
	print(fl)
	logging.info(fl)
	fl = FileCheckUtil(fl)
	logging.info(fl+"----FileName------")

	try:
		for i in range(len(comicElem)):
			try:
				summary = comicElem[i].select('li[class^=coupon-list-item]')
				logging.info("I AM IN GOTO COUPON_LIST_ITEM						"+ str(len(summary)))

				for item in range(len(summary)):
						index +=1
						logging.info(("---------"+str(index)+"---------------"))

						try:
							code = summary[item].select('.coupon-click small')
							print("\n\n"+code[0].getText())
							logging.info(code[0].getText())
							dict["code"]=code[0].getText()
						except IndexError:
							print("\n\nNO CODE")
							logging.debug("No Coupon Code")
						
						try:
							link = summary[item].select('.coupon-click a[href^=?go]')
							logging.info(link[0].get('href'))
							dict["link"]=link[0].get('href')
						except IndexError:
							logging.debug("No Coupon Link")

						info = summary[item].select('div.coupon-info b')
						print(str(info[0].getText().encode('utf-8'))+"\n")
						logging.info(info[0].getText())
						dict["info"]=str(info[0].getText().encode('utf-8'))

						details = summary[item].select('div.coupon-info p')
						print((details[0].getText()).encode('utf-8'))
						logging.info((details[0].getText()).encode('utf-8'))
						dict["details"]=str((details[0].getText()).encode('utf-8'))

						#save					
						out_file = open(fl,"a")
						json.dump(dict,out_file, indent=4)                           
						out_file.close()


			except IndexError:
				print("*********???Check Out ur Application--INNER***************")
				logging.debug("*********???Check Out ur Application--INNER***************")
	except IndexError:
		print("*********???Check Out ur Application--OUTER***************")
		logging.debug("*********???Check Out ur Application--OUTER***************")


def Start(index):
	#index = Intialization()
	#fileName = couponTypeDict[int(index)]
	print(str(index)+"I AM IN START                  ")
	url = CreateUrl(int(index))
	GoTo(url,index)



if __name__ == "__main__":
	print(str(len(couponTypeDict)))
	#Start(0)
	downloadThreads = []             # a list of all the Thread objects
	for index in range(len(couponTypeDict)):    # loops 14 times, creates 14 threads
	    #Start(index+1)		
	    downloadThread = threading.Thread(target=Start, args=(index+1,))
	    downloadThreads.append(downloadThread)
	    downloadThread.start()
	for downloadThread in downloadThreads:
	    downloadThread.join()
	print('Done.')
	



