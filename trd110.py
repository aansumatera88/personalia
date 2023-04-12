# File Code  : trd110.py
# File Name  : Pendataan Absensi

import base64
import requests
import streamlit as st
from PIL import Image
from streamlit_option_menu import option_menu
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder, JsCode
from streamlit.components.v1 import html
from st_aggrid import AgGrid
import pandas as pd
import datetime

import powerlib
from datetime import datetime
import trd110p

def loadAremas(sqlString):
    df = []
    list = []  
    list.append({
        'areco': "",
        'arena': ""
    })
    aremasRec, aremasNum = powerlib.sqlSelect(st.session_state.myConnLink, sqlString)
    if aremasNum > 0:   
        for data in range(aremasNum):
            list.append({
                'areco': aremasRec[data][0],
                'arena': aremasRec[data][1]
            })
        df = pd.DataFrame(list)
    return df

def callback0():
    st.session_state.trd110_button1Disabled = True
    st.session_state.trd110_button2Disabled = True  
    st.session_state.trd110_button3Disabled = False  
    
def callback1():
    st.session_state.trd110_button1Disabled = True
    st.session_state.trd110_button2Disabled = False  
    st.session_state.trd110_button3Disabled = False  
    
def callback2():
    if st.session_state.trd110_ScreenMode == 2:
        st.session_state.trd110_button1Disabled = False
        st.session_state.trd110_button2Disabled = True 
        st.session_state.trd110_button3Disabled = True  
        
def callback3():
    st.mATTNO = st.session_state.trd110_sATTNO 
    st.mATTDA = st.session_state.trd110_sATTDA
    st.mATTNO = st.mATTNO.strip()
    st.mATTNO = st.mATTNO.upper()
    if st.session_state.trd110_ScreenMode == 1:
        if st.mATTNO == "":
            st.warning("No. Kehadiran Harus diisi !")
            return       
        else:
            
            sqlString = "SELECT arena FROM aremas WHERE resta='A' AND areco='%s'"%(st.mATTNO)
            aremasdRec, aremasdNum = powerlib.sqlSelect(st.session_state.myConnLink, sqlString)
            if aremasdNum > 0:
                st.warning("No. Kehadiran sudah terdaftar !")     
                return     
    if st.mATTDA == "":
        st.warning("Tgl. Kehadiran Harus diisi !")
        return
    
    st.session_state.trd110_button1Disabled = False
    st.session_state.trd110_button2Disabled = True 
    st.session_state.trd110_button3Disabled = True  
    
def callback4():
    st.session_state.trd110_button1Disabled = False
    st.session_state.trd110_button2Disabled = True 
    st.session_state.trd110_button3Disabled = True  
    
def callback5():
    if st.session_state.trd110_ShowPDF:
        st.session_state.trd110_ShowPDF = False
        html("""<script>
            var frame = document.getElementById("myframe");
            frame.parentNode.removeChild(frame);
            </script>""")
    else:
        st.session_state.trd110_ShowPDF = True
        trd110p.Trd110p()
    

def Trd110():
    if "myConnLink" not in st.session_state:
        st.session_state.myConnLink, st.session_state.myConnStatus = powerlib.dbConnection()
        
    #if not st.session_state.myConnStatus:
    #    st.warning("Server Connection not Available !")
    #    st.stop()
    
    if "trd110_ScreenMode" not in st.session_state:
        st.session_state.selectArena = 0
        st.session_state.trd110_ScreenMode = 1   # Add Mode
        st.session_state.trd110_FindDisabled = True
        st.session_state.trd110_KeyVarDisabled = False
        st.session_state.trd110_DatVarDisabled = False
        st.session_state.trd110_ButtonNumber = 0
        st.session_state.trd110_ShowPDF = False

        st.session_state.trd110_button1Disabled = False
        st.session_state.trd110_button2Disabled = True
        st.session_state.trd110_button3Disabled = True
        
        st.session_state.trd110_mFORMS = st.formNew_
        
        st.mATTNO = ""
        st.mATTDA = datetime.now()
        st.mATTTY = True
        
        st.session_state.trd110_lATTNO = ""
        st.session_state.trd110_lATTDA = ""
        st.session_state.trd110_lATTTY = True
        
        st.mATTNO = "AT.YYYYMM.99999"
        st.mATTDA = datetime.now()
        
        st.mATTTY = True
        st.session_state.trd110_button1Disabled = True
        st.session_state.trd110_button2Disabled = True  
        st.session_state.trd110_button3Disabled = False  
      
    ### Button Section ###
    with st.container():
        headerColumn1, headerColumn2, headerColumn3 = st.columns([1,3,1])
        with headerColumn1:
            st.subheader(":blue[Pendataan Absensi]")
            #st.header('A header with _italics_ :blue[colors] and emojis :sunglasses:')
             
        with headerColumn2:
            buttonColumn1, buttonColumn2, buttonColumn3, buttonColumn4, buttonColumn5, buttonColumn6, buttonColumn7 = st.columns(7)
            with buttonColumn1:
                if st.button("New", key= "trd110_buttonNew", on_click=callback0, disabled=st.session_state.trd110_button1Disabled):
                    clickButton(0)
            with buttonColumn2:
                if st.button("Edit", key= "trd110_buttonEdit", on_click=callback1, disabled=st.session_state.trd110_button1Disabled):
                    clickButton(1)
            with buttonColumn3:                
                if st.button("Delete", key= "trd110_buttonDelete", on_click=callback2, disabled=st.session_state.trd110_button2Disabled):
                    clickButton(2)
            with buttonColumn4:
                if st.button("Save", key= "trd110_buttonSave", on_click=callback3, disabled=st.session_state.trd110_button3Disabled):
                    clickButton(3)
            with buttonColumn5:
                if st.button("Undo", key= "trd110_buttonUndo", on_click=callback4, disabled=st.session_state.trd110_button3Disabled):
                    clickButton(4)
            with buttonColumn6:
                if st.button("Print", key= "trd110_buttonPrint", on_click=callback5, disabled=st.session_state.trd110_button1Disabled):
                    clickButton(5)
            with buttonColumn7:
                st.write(" ")

        with headerColumn3:
            st.trd110_FORMS = st.text_input("Status", value=st.session_state.trd110_mFORMS, key="trd110Form", disabled=True, label_visibility="collapsed")
        
    ### Search Section ###
    with st.container():
        searchColumn1, searchColumn2, searchColumn3 = st.columns([2,1,2])
        with searchColumn2:
            strSearch = "SELECT areco, arena FROM aremas WHERE resta='A' ORDER BY arena"
            st.listAREMAS = loadAremas(strSearch)
            try:
                st.selected_arena = st.selectbox("Choose a Area Name", st.listAREMAS.arena, st.session_state.selectArena, key="trd110Search", disabled= st.session_state.trd110_FindDisabled )
                st.areco = st.listAREMAS.loc[st.listAREMAS.arena == st.selected_arena]["areco"].iloc[0]
                queryVar(st.areco)   
            except:
                pass
            
    ### Data Section ###               
    with st.container():
        detailColumn1, detailColumn2 = st.columns([1,2])
        with detailColumn1:
            st.trd110_ATTNO = st.text_input("No. Kehadiran", value=st.mATTNO,  max_chars=5, key="trd110_sATTNO", disabled=st.session_state.trd110_KeyVarDisabled)
            st.trd110_ATTDA = st.date_input("Tgl. Kehadiran", value=st.mATTDA, key="trd110_sATTDA", disabled=st.session_state.trd110_DatVarDisabled)
            st.trd110_ATTTY = st.radio("Jenis Kehadiran", ("Regular", "Assignment", "Project"), disabled=st.session_state.trd110_DatVarDisabled)
                  
def clickButton(pNumber):
    if pNumber == 0 and st.session_state.trd110_ScreenMode== 0 :           
        ## New Data  ##
        st.session_state.trd110_ScreenMode = 1
        st.session_state.trd110_mFORMS = st.formNew_
        st.session_state.trd110_ButtonNumber == 0
        lastVarValue()
        setVarMode()
        setVarValue()
   
    elif pNumber == 1 and st.session_state.trd110_ScreenMode== 0 :         
        ## Edit Data ##
        st.session_state.trd110_button1Disabled = True
        st.session_state.trd110_button2Disabled = False        
        
        st.session_state.trd110_ScreenMode= 2
        st.session_state.trd110_mFORMS = st.formEdit_
        st.session_state.trd110_ButtonNumber == 0
        lastVarValue()
        setVarMode()

    elif pNumber== 2 and st.session_state.trd110_ScreenMode == 2:                                 
        ## Delete Data ##
        st.mATTNO = st.session_state.trd110_sATTNO 
    
        if st.session_state.trd110_ScreenMode == 2 :
            mDATEN = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            strData = "UPDATE aremas SET resta='D', ladup='%s', upusr='%s' WHERE resta='A' AND areco='%s' "
            strData = strData%(mDATEN, st.session_state.UserName_, st.mATTNO)
            powerlib.sqlUpdate(st.session_state.myConnLink, strData)
            
            st.session_state.trd110_ScreenMode = 1
            sqlString = "SELECT areco FROM aremas WHERE resta = 'A' LIMIT 1"
            aremasdRec, aremasdNum = powerlib.sqlSelect(st.session_state.myConnLink, sqlString)
            if aremasdNum > 0:
                st.session_state.trd110_ScreenMode = 0
                for data in range(aremasdNum):
                    st.session_state.trd110_sATTNO = aremasdRec[data][0]
            
            st.session_state.trd110_ScreenMode= 0
            st.session_state.trd110_mFORMS = st.formQuery_
            setVarValue()
            setVarMode()
                 
    elif pNumber == 3 and st.session_state.trd110_ScreenMode != 0:                                 
        ## Save Data ##
        st.session_state.trd110_ButtonNumber == 0
        st.mATTNO = st.session_state.trd110_sATTNO 
        st.mATTDA = st.session_state.trd110_sATTDA
        if st.session_state.trd110_sATTTY:
            st.mATTTY = 1
        else:
            st.mATTTY = 0
        st.mATTNO = st.mATTNO.strip()
        st.mATTNO = st.mATTNO.upper()
        
        if st.mATTNO == "":
            return 
               
        if st.mATTDA == "":
            return

        mDATEN = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        if st.session_state.trd110_ScreenMode== 1:
            strData = "INSERT INTO aremas(daten,enusr,resta,areco,arena,arest) VALUES('%s','%s','%s','%s','%s','%s')"
            strData = strData%(mDATEN, st.session_state.UserName_, 'A', st.mATTNO, st.mATTDA, st.mATTTY)
        else:
            strData = "UPDATE aremas SET ladup='%s', upusr='%s', arena='%s', arest='%s' WHERE resta='A' AND areco='%s' "
            strData = strData%(mDATEN, st.session_state.UserName_, st.mATTDA, st.mATTTY, st.mATTNO)
        powerlib.sqlUpdate(st.session_state.myConnLink, strData)
        
        st.session_state.trd110_ScreenMode= 0
        st.session_state.trd110_mFORMS = st.formQuery_
        st.session_state.trd110_button1Disabled = False
        st.session_state.trd110_button2Disabled = True  
        setVarMode()
        
        #powerlib.pesan("Data tersebut Berhasil di simpan !")
        
        
    elif pNumber == 4 and st.session_state.trd110_ScreenMode != 0:                                 
        ## Undo Process ##
        st.session_state.trd110_ButtonNumber == 0
        st.session_state.trd110_sATTNO = st.session_state.trd110_lATTNO
        st.session_state.trd110_sATTDA = st.session_state.trd110_lATTDA
        st.session_state.trd110_sATTTY = st.session_state.trd110_lATTTY

        st.session_state.trd110_ScreenMode= 0
        st.session_state.trd110_mFORMS = st.formQuery_        
        st.session_state.trd110_button1Disabled = False
        st.session_state.trd110_button2Disabled = True  
        setVarMode()
    
def lastVarValue():
    try:
        st.session_state.trd110_lATTNO = st.session_state.trd110_sATTNO
        st.session_state.trd110_lATTDA = st.session_state.trd110_sATTDA
        st.session_state.trd110_lATTTY = st.session_state.trd110_sATTTY
    except:
        pass
    
def queryVar(pATTNO):
    if pATTNO == "":
        return
    st.session_state.trd110_sATTNO = pATTNO
    st.session_state.trd110_ScreenMode == 0
    setVarValue()
    st.session_state.selectArena = 0
    
def setVarValue():
    if st.session_state.trd110_ScreenMode == 1:
        st.session_state.trd110_sATTNO = ""
        st.session_state.trd110_sATTDA = ""
        st.session_state.trd110_sATTTY = True 
          
    elif st.session_state.trd110_ScreenMode == 0:
        st.mATTNO = st.session_state.trd110_sATTNO
        sqlString = "SELECT arena,arest FROM aremas WHERE resta = 'A' AND areco='%s' LIMIT 1"%(st.mATTNO)
        aremasdRec, aremasdNum = powerlib.sqlSelect(st.session_state.myConnLink, sqlString)
        if aremasdNum > 0:
            for data in range(aremasdNum):
                st.mATTDA = aremasdRec[data][0]
                if aremasdRec[data][1] == 1:
                    st.session_state["trd110_sATTTY"] = True
                else:
                    st.session_state["trd110_sATTTY"] = False
        
def setVarMode():
    if st.session_state.trd110_mFORMS == st.formNew_:               # Add Mode
        st.session_state.trd110_FindDisabled = True
        st.session_state.trd110_KeyVarDisabled = False
        st.session_state.trd110_DatVarDisabled = False

          
    elif st.session_state.trd110_mFORMS == st.formEdit_:            # Edit Mode
        st.session_state.trd110_FindDisabled = True
        st.session_state.trd110_KeyVarDisabled = True
        st.session_state.trd110_DatVarDisabled = False

    else:                                                           # Query Mode
        st.session_state.trd110_FindDisabled = False
        st.session_state.trd110_KeyVarDisabled = True
        st.session_state.trd110_DatVarDisabled = True