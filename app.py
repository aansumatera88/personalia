
import streamlit as st
from PIL import Image
import requests
import base64
from streamlit_option_menu import option_menu
import powerlib


st.formNew_ = "New"
st.formEdit_ = "Edit"
st.formQuery_ = "Query"

st.formDraft_ = "Draft"
st.formPrinted_ = "Printed"
st.formPosted_ = "Posted"

st.LIVE_ = False
#st.LIVE_ = True

# Page setting
st.set_page_config(page_title="HRD Apps", page_icon="mylogo.jpg", layout="wide")

if "myConnLink" not in st.session_state:
    st.session_state.myConnLink, st.session_state.myConnStatus = powerlib.dbConnection()

if not st.session_state.myConnStatus:
    st.warning("Server Connection not Available !")
    st.stop()

if "selected" not in st.session_state:
    st.session_state.selected = ""
     
if "loginApp" not in st.session_state:
    st.session_state.loginApp = False
    st.session_state.SecuCode_ = ""
    st.session_state.SecuCod2_ = ""
    st.session_state.SecuCod3_ = ""
    
def loginCallback():
    st.compcode = st.session_state.CompCode_
    st.compcode = st.compcode.strip()
    st.compcode = st.compcode.upper()
    st.username = st.session_state.UserName_.upper()
    st.username = st.username.strip()
    st.username = st.username.upper()
    st.password = st.session_state.Password_
    st.session_state.SecuCode_ = ""
    st.session_state.SecuCod2_ = ""
    st.session_state.SecuCod3_ = ""
    
    sqlString = "SELECT u.usrco,u.usrna,c.secco,c.secc2,c.secc3 FROM usrmas u JOIN commbr c "
    sqlString = sqlString + "ON u.resta=c.resta  AND u.usrco=c.usrco "
    sqlString = sqlString + "WHERE u.resta = 'A' AND upper(c.comco)='%s' AND upper(u.usrco)='%s' AND u.paswd='%s'"
    sqlString = sqlString%(st.compcode, st.username, st.password)
    recUSRMAS, numUSRMAS = powerlib.sqlSelect(st.session_state.myConnLink, sqlString)
    if numUSRMAS > 0:
        st.session_state.SecuCode_ = recUSRMAS[0][2]
        st.session_state.SecuCod2_ = recUSRMAS[0][3]
        st.session_state.SecuCod3_ = recUSRMAS[0][4]
        st.session_state.loginApp = True
        st.placeholder1.empty()
        st.placeholder2.empty()
        st.placeholder3.empty()
        
        st.success("Welcome " + recUSRMAS[0][1] + " ...")
        #st.balloons()
    else:
        st.error("Invalid credentials")     
        
def logoutCallback():
    st.session_state.loginApp = False
    

def loginPro():
    st.header("Login")
    loginColumn1, loginColumn2 = st.columns([1,2])
    with loginColumn1:
        st.placeholder1 = st.empty()
        st.placeholder2 = st.empty()
        st.placeholder3 = st.empty()
        st.placeholder4 = st.empty()
        compcode = st.placeholder1.text_input("Company Code", key="CompCode_")
        username = st.placeholder2.text_input("User Account", key="UserName_")
        password = st.placeholder3.text_input("Password", key="Password_", type="password")
        if st.placeholder4.button("Login", key="loginButton", on_click=loginCallback):
            if st.session_state.loginApp:
                st.placeholder1.empty()
                st.placeholder2.empty()
                st.placeholder3.empty()
                st.placeholder4.empty()
                
def logoutPro():
    st.header("Welcome")
    placeholder5 = st.empty()
    logoutColumn1, logoutColumn2 = st.columns([1,2])
    with logoutColumn1:
        if st.button("Logout", key="logoutButton", on_click=logoutCallback):
            placeholder5.empty()


# Sidebar
with st.sidebar:
    # Logo
    logo = Image.open('MetroLogo2.jpg')
    #st.image(logo, use_column_width=True)
    st.image(logo, use_column_width='auto')

    st.session_state.selected = option_menu (None, ["Dashboard", "Master", 'Transaction', 'Billing Generator', 'Reporting', 'Utility System'],
    icons= ["house-fill", "folder-fill", "folder-symlink-fill", "bank", "book-fill", "gear-fill"] , default_index=0)
                
            
if(st.session_state.selected == 'Dashboard'):
    if not st.session_state.loginApp:
        if st.LIVE_:
            loginPro()
        else:
            st.session_state.UserName_ = "USER@GMAIL.COM"
            st.session_state.SecuCode_ = "ADMINISTRATOR"
            st.session_state.SecuCod2_ = "SUPERVISOR"
            st.session_state.SecuCod3_ = ""
            st.session_state.loginApp = True
            st.success("Welcome " + st.session_state.SecuCode_  + " ...")            
    else:
        logoutPro()
        

if(st.session_state.selected == 'Master'):
    if not st.session_state.loginApp:
        st.warning("Please Login ... ")
        st.stop()
    
    if st.session_state.SecuCode_ == "ADMINISTRATOR":
        sqlString = "SELECT prgco, prgna FROM prgmas WHERE resta = 'A' AND prgrp='MASTER'"
    else:
        sqlString = "SELECT p.prgco, p.prgna FROM prgmas p JOIN secacc s ON p.resta=s.resta AND p.prgco=s.prgco "
        sqlString = sqlString  + "AND (s.secco='%s' "
        if st.session_state.SecuCod2_ != "":
            sqlString = sqlString  + "OR s.secco='%s' "
        if st.session_state.SecuCod3_ != "":
            sqlString = sqlString  + "OR s.secco='%s' "
        sqlString = sqlString  + ") "
        sqlString = sqlString  + "WHERE p.resta = 'A' AND p.prgrp='MASTER'"
        if st.session_state.SecuCod3_ != "":
            sqlString = sqlString%(st.session_state.SecuCode_, st.session_state.SecuCod2_, st.session_state.SecuCod3_)
        elif st.session_state.SecuCod2_ != "":
            sqlString = sqlString%(st.session_state.SecuCode_, st.session_state.SecuCod2_)
        else:
            sqlString = sqlString%(st.session_state.SecuCode_)
        
    prgmasRec, prgmasNum = powerlib.sqlSelect(st.session_state.myConnLink, sqlString)
    print(sqlString)
    print(prgmasRec)
    st.menuName = []
    st.menuCode = []
    st.menuTabs = []
    if prgmasNum > 0:
        tabString = ""
        for data in range(prgmasNum):
            st.menuCode.append(prgmasRec[data][0])
            st.menuName.append(prgmasRec[data][1])
            #st.menuTabs.append("master"+str(data))
            
            if data > 0:
                tabString = tabString + ","
            tabString = tabString + "master"+str(data)
            
        tabString = tabString + " = st.tabs(["
        for data in range(prgmasNum):
            if data > 0:
                tabString = tabString + ","
            tabString = tabString + "'" + st.menuName[data] + "'"
        tabString = tabString + "])"  
       
        exec(tabString)
     
        
        for data2 in range(prgmasNum):
            myProgram = st.menuCode[data2]
            myProgram = myProgram.lower()
            myString1 = "import " + myProgram
            myString2 = myProgram + "." + myProgram.title() + "()"
            with eval('master'+str(data2)):
                exec(myString1)
                exec(myString2)
    
if(st.session_state.selected == 'Transaction'):
    if not st.session_state.loginApp:
        st.warning("Please Login ... ")
        st.stop()
    
    import trd110
    trd110.Trd110()