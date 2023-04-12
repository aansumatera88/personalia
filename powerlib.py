#import mysql.connector
from streamlit_custom_notification_box import custom_notification_box as scnb


import psycopg2



LIVE_ = False
#LIVE_ = True
if LIVE_:
    myhost = "newprojectgallery.com"
    myport = "3306"
    myuser = "u1719453_personalia"               # Metro Komputer
    mypass = "@Psn123123"
    mydbna = "u1719453_personalia"
else:
    myhost = "localhost"
    myport = "3306"
    myuser = "admin"               # Metro Komputer
    mypass = "8088"
    mydbna = "personalia"
    
def dbConnection():
    
    try:
        connLink = psycopg2.connect( host=myhost, user=myuser, password=mypass, database=mydbna )
        connStatus = True
    except:
        connLink = None
        connStatus = False
    return connLink, connStatus
        
def dbConnection2():
    #conn = mysql.connector.connect(user=myuser, password=mypass, host=myhost, database=mydbna)
    try:
        connLink = mysql.connector.connect(
            user=myuser, password=mypass, host=myhost, database=mydbna)
        connStatus = True
    except:
        pesan = "No Connection Database !"
        #print(pesan)
        connLink = None
        connStatus = False
    return connLink, connStatus

def sqlSelect(pConn, sqlText):
    '''
    if pConn.is_connected() != True:
        pConn, pStatus = dbConnection()  
    else:
        pStatus = True
    if not pStatus:
        return {}, 0
    '''
    pCursor = pConn.cursor()   
    pCursor.execute(sqlText)
    tableRec = pCursor.fetchall()
    tableNum = pCursor.rowcount
    #print(tableRec)
    return tableRec, tableNum

def sqlUpdate(pConn, sqlText):
    #try:
    pCursor = pConn.cursor()   
    pCursor.execute(sqlText)
    pConn.commit()
    return True
    #except:
    #    return False
    
#3896de
def pesan(wht_msg):
    styles = {'material-icons':{'color': '#faebd7'},
            'text-icon-link-close-container': {'box-shadow': '#faebd7 3px 8px'},
            'notification-text': {'':''},
            'close-button':{'':''},
            'link':{'':''}}

    scnb(icon='', 
        textDisplay=wht_msg, 
        externalLink='', 
        url='#', 
        styles=styles, 
        key="foo")

def convertNumToStr(myNum, decCount):
    if decCount > 0:
        myString = str(myNum)
    else:
        try:
            myString = str(int(myNum))
        except:
            myString = ""
    return myString


def convertNumToStrFormat(myNum, decCount, lenVar):
    myDecimal = ""
    if decCount > 0:
        # print(myNum)
        tempString = str(myNum)
        mLEN = len(tempString)
        # print(len(myString))
        mPOS = tempString.find('.')
        if mPOS >= 0:
            myString = tempString[0:mPOS]
        else:
            myString = ""
        myDecimal = tempString[mPOS+1:mPOS+3]
        if len(myDecimal) == 0:
            myDecimal = "00"
        if len(myDecimal) == 1:
            myDecimal = myDecimal + "0"

        # print(myString)
        # print(myDecimal)
    else:
        try:
            myString = str(int(myNum))
        except:
            myString = ""

    mLEN = len(myString)

    if mLEN > 3:
        myString = myString[:mLEN-3] + "," + myString[mLEN-3:]
        mLEN = mLEN + 1
        if mLEN > 7:
            myString = myString[:mLEN-7] + "," + myString[mLEN-7:]
            mLEN = mLEN + 1
            if mLEN > 11:
                myString = myString[:mLEN-11] + "," + myString[mLEN-11:]

    if decCount > 0:
        myString = myString + "." + myDecimal

    nLEN = lenVar + int((lenVar-1)/3)
    mLEN = len(myString)
    if nLEN > mLEN:
        myString = (nLEN - mLEN) * " " + myString

    if myNum == 0 and decCount == -1:
        myString = " " * lenVar

    return myString


def convertStrToNum(myString, decCount):
    if myString == "":
        myNum = 0
    else:
        if decCount > 0:
            myNum = float(myString)
        else:
            if myString.find(".0") != -1:
                try:
                    myNum = float(myString)
                    myNum = int(myNum)
                except:
                    myNum = 0
            else:
                try:
                    myNum = int(myString)
                except:
                    myNum = 0

    return myNum


def convertStrToStrFormat(myNum, decCount, lenVar):
    myString = myNum

    mLEN = len(myString)

    if mLEN > 3:
        myString = myString[:mLEN-3] + "," + myString[mLEN-3:]
        mLEN = mLEN + 1
        if mLEN > 7:
            myString = myString[:mLEN-7] + "," + myString[mLEN-7:]
            mLEN = mLEN + 1
            if mLEN > 11:
                myString = myString[:mLEN-11] + "," + myString[mLEN-11:]

    nLEN = lenVar + int((lenVar-1)/3)
    mLEN = len(myString)
    if nLEN > mLEN:
        myString = (nLEN - mLEN) * " " + myString

    return myString


def convertStrFormatToNum(myString, decCount):
    if myString == "":
        myNum = 0
    else:
        myString = myString.replace(",", "", 3)
        if decCount > 0:
            try:
                myNum = float(myString)
                # print("F1")
            except:
                myNum = int(myString)
                # print("F2")
        else:
            try:
                myNum = int(myString)
                # print("I1")
            except:
                myNum = float(myString)
                # print("I2")
    return myNum
