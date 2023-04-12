# File Code  : trd010.py
# File Name  : Master Area

import base64
import requests
import streamlit as st
from PIL import Image
from streamlit_option_menu import option_menu
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder, JsCode
from streamlit.components.v1 import html

import powerlib
from datetime import datetime
import trd010p

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
    st.session_state.trd010_button1Disabled = True
    st.session_state.trd010_button2Disabled = True  
    st.session_state.trd010_button3Disabled = False  
    
def callback1():
    st.session_state.trd010_button1Disabled = True
    st.session_state.trd010_button2Disabled = False  
    st.session_state.trd010_button3Disabled = False  
    
def callback2():
    if st.session_state.trd010_ScreenMode == 2:
        st.session_state.trd010_button1Disabled = False
        st.session_state.trd010_button2Disabled = True 
        st.session_state.trd010_button3Disabled = True  
        
def callback3():
    st.mARECO = st.session_state.trd010_sARECO 
    st.mARENA = st.session_state.trd010_sARENA
    st.mARECO = st.mARECO.strip()
    st.mARECO = st.mARECO.upper()
    if st.session_state.trd010_ScreenMode == 1:
        if st.mARECO == "":
            st.warning("Kode Area Harus diisi !")
            return       
        else:
            
            sqlString = "SELECT arena FROM aremas WHERE resta='A' AND areco='%s'"%(st.mARECO)
            aremasdRec, aremasdNum = powerlib.sqlSelect(st.session_state.myConnLink, sqlString)
            if aremasdNum > 0:
                st.warning("Kode Area sudah terdaftar !")     
                return     
    if st.mARENA == "":
        st.warning("Nama Area Harus diisi !")
        return
    
    st.session_state.trd010_button1Disabled = False
    st.session_state.trd010_button2Disabled = True 
    st.session_state.trd010_button3Disabled = True  
    
def callback4():
    st.session_state.trd010_button1Disabled = False
    st.session_state.trd010_button2Disabled = True 
    st.session_state.trd010_button3Disabled = True  
    
def callback5():
    if st.session_state.trd010_ShowPDF:
        st.session_state.trd010_ShowPDF = False
        html("""<script>
            var frame = document.getElementById("myframe");
            frame.parentNode.removeChild(frame);
            </script>""")
    else:
        st.session_state.trd010_ShowPDF = True
        trd010p.Trd010p()
    

def Trd010():
    if "myConnLink" not in st.session_state:
        st.session_state.myConnLink, st.session_state.myConnStatus = powerlib.dbConnection()
        
    #if not st.session_state.myConnStatus:
    #    st.warning("Server Connection not Available !")
    #    st.stop()
    
    if "trd010_ScreenMode" not in st.session_state:
        st.session_state.selectArena = 0
        st.session_state.trd010_ScreenMode = 1   # Add Mode
        st.session_state.trd010_FindDisabled = True
        st.session_state.trd010_KeyVarDisabled = False
        st.session_state.trd010_DatVarDisabled = False
        st.session_state.trd010_ButtonNumber = 0
        st.session_state.trd010_ShowPDF = False

        st.session_state.trd010_button1Disabled = False
        st.session_state.trd010_button2Disabled = True
        st.session_state.trd010_button3Disabled = True
        
        st.session_state.trd010_mFORMS = st.formNew_
        
        st.mARECO = ""
        st.mARENA = ""
        st.mAREST = True
        
        st.session_state.trd010_lARECO = ""
        st.session_state.trd010_lARENA = ""
        st.session_state.trd010_lAREST = True
        
        sqlString = "SELECT areco,arena,arest FROM aremas WHERE resta = 'A' ORDER BY arena LIMIT 1"
        aremasdRec, aremasdNum = powerlib.sqlSelect(st.session_state.myConnLink, sqlString)
        if aremasdNum > 0:
            st.session_state.trd010_ScreenMode= 0   # Query Mode
            st.session_state.trd010_mFORMS = st.formQuery_
            for data in range(aremasdNum):
                st.mARECO = aremasdRec[data][0]
                st.mARENA = aremasdRec[data][1]
                if aremasdRec[data][2] == 1:
                    st.mAREST = True
                else:
                    st.mAREST = False
                    
                st.session_state.trd010_lARECO = aremasdRec[data][0]
                st.session_state.trd010_lARENA = aremasdRec[data][1]
                if aremasdRec[data][2] == 1:
                    st.session_state.trd010_lAREST = True
                else:
                    st.session_state.trd010_lAREST = False
                    
            st.session_state.trd010_FindDisabled = False
            st.session_state.trd010_KeyVarDisabled = True
            st.session_state.trd010_DatVarDisabled = True
        else:
            st.session_state.trd010_button1Disabled = True
            st.session_state.trd010_button2Disabled = True  
            st.session_state.trd010_button3Disabled = False  
      
    ### Button Section ###
    with st.container():
        headerColumn1, headerColumn2, headerColumn3 = st.columns([1,3,1])
        with headerColumn1:
            st.subheader(":blue[Area Master]")
            #st.header('A header with _italics_ :blue[colors] and emojis :sunglasses:')
             
        with headerColumn2:
            buttonColumn1, buttonColumn2, buttonColumn3, buttonColumn4, buttonColumn5, buttonColumn6, buttonColumn7 = st.columns(7)
            with buttonColumn1:
                if st.button("New", key= "trd010_buttonNew", on_click=callback0, disabled=st.session_state.trd010_button1Disabled):
                    clickButton(0)
            with buttonColumn2:
                if st.button("Edit", key= "trd010_buttonEdit", on_click=callback1, disabled=st.session_state.trd010_button1Disabled):
                    clickButton(1)
            with buttonColumn3:                
                if st.button("Delete", key= "trd010_buttonDelete", on_click=callback2, disabled=st.session_state.trd010_button2Disabled):
                    clickButton(2)
            with buttonColumn4:
                if st.button("Save", key= "trd010_buttonSave", on_click=callback3, disabled=st.session_state.trd010_button3Disabled):
                    clickButton(3)
            with buttonColumn5:
                if st.button("Undo", key= "trd010_buttonUndo", on_click=callback4, disabled=st.session_state.trd010_button3Disabled):
                    clickButton(4)
            with buttonColumn6:
                if st.button("Print", key= "trd010_buttonPrint", on_click=callback5, disabled=st.session_state.trd010_button1Disabled):
                    clickButton(5)
            with buttonColumn7:
                st.write(" ")

        with headerColumn3:
            st.trd010_FORMS = st.text_input("Status", value=st.session_state.trd010_mFORMS, key="trd010Form", disabled=True, label_visibility="collapsed")
        
    ### Search Section ###
    with st.container():
        searchColumn1, searchColumn2, searchColumn3 = st.columns([2,1,2])
        with searchColumn2:
            strSearch = "SELECT areco, arena FROM aremas WHERE resta='A' ORDER BY arena"
            st.listAREMAS = loadAremas(strSearch)
            try:
                st.selected_arena = st.selectbox("Choose a Area Name", st.listAREMAS.arena, st.session_state.selectArena, key="trd010Search", disabled= st.session_state.trd010_FindDisabled )
                st.areco = st.listAREMAS.loc[st.listAREMAS.arena == st.selected_arena]["areco"].iloc[0]
                queryVar(st.areco)   
            except:
                pass
            
    ### Data Section ###               
    with st.container():
        detailColumn1, detailColumn2 = st.columns([1,2])
        with detailColumn1:
            st.trd010_ARECO = st.text_input("Kode Area", value=st.mARECO,  max_chars=5, key="trd010_sARECO", disabled=st.session_state.trd010_KeyVarDisabled)
            st.trd010_ARENA = st.text_input("Nama Area", value=st.mARENA,  max_chars=35, key="trd010_sARENA", disabled=st.session_state.trd010_DatVarDisabled)
            st.trd010_AREST = st.checkbox("Status Area", value=st.mAREST, key="trd010_sAREST", disabled=st.session_state.trd010_DatVarDisabled)
                  
def clickButton(pNumber):
    if pNumber == 0 and st.session_state.trd010_ScreenMode== 0 :           
        ## New Data  ##
        st.session_state.trd010_ScreenMode = 1
        st.session_state.trd010_mFORMS = st.formNew_
        st.session_state.trd010_ButtonNumber == 0
        lastVarValue()
        setVarMode()
        setVarValue()
   
    elif pNumber == 1 and st.session_state.trd010_ScreenMode== 0 :         
        ## Edit Data ##
        st.session_state.trd010_button1Disabled = True
        st.session_state.trd010_button2Disabled = False        
        
        st.session_state.trd010_ScreenMode= 2
        st.session_state.trd010_mFORMS = st.formEdit_
        st.session_state.trd010_ButtonNumber == 0
        lastVarValue()
        setVarMode()

    elif pNumber== 2 and st.session_state.trd010_ScreenMode == 2:                                 
        ## Delete Data ##
        st.mARECO = st.session_state.trd010_sARECO 
    
        if st.session_state.trd010_ScreenMode == 2 :
            mDATEN = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            strData = "UPDATE aremas SET resta='D', ladup='%s', upusr='%s' WHERE resta='A' AND areco='%s' "
            strData = strData%(mDATEN, st.session_state.UserName_, st.mARECO)
            powerlib.sqlUpdate(st.session_state.myConnLink, strData)
            
            st.session_state.trd010_ScreenMode = 1
            sqlString = "SELECT areco FROM aremas WHERE resta = 'A' LIMIT 1"
            aremasdRec, aremasdNum = powerlib.sqlSelect(st.session_state.myConnLink, sqlString)
            if aremasdNum > 0:
                st.session_state.trd010_ScreenMode = 0
                for data in range(aremasdNum):
                    st.session_state.trd010_sARECO = aremasdRec[data][0]
            
            st.session_state.trd010_ScreenMode= 0
            st.session_state.trd010_mFORMS = st.formQuery_
            setVarValue()
            setVarMode()
                 
    elif pNumber == 3 and st.session_state.trd010_ScreenMode != 0:                                 
        ## Save Data ##
        st.session_state.trd010_ButtonNumber == 0
        st.mARECO = st.session_state.trd010_sARECO 
        st.mARENA = st.session_state.trd010_sARENA
        if st.session_state.trd010_sAREST:
            st.mAREST = 1
        else:
            st.mAREST = 0
        st.mARECO = st.mARECO.strip()
        st.mARECO = st.mARECO.upper()
        
        if st.mARECO == "":
            return 
               
        if st.mARENA == "":
            return

        mDATEN = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        if st.session_state.trd010_ScreenMode== 1:
            strData = "INSERT INTO aremas(daten,enusr,resta,areco,arena,arest) VALUES('%s','%s','%s','%s','%s','%s')"
            strData = strData%(mDATEN, st.session_state.UserName_, 'A', st.mARECO, st.mARENA, st.mAREST)
        else:
            strData = "UPDATE aremas SET ladup='%s', upusr='%s', arena='%s', arest='%s' WHERE resta='A' AND areco='%s' "
            strData = strData%(mDATEN, st.session_state.UserName_, st.mARENA, st.mAREST, st.mARECO)
        powerlib.sqlUpdate(st.session_state.myConnLink, strData)
        
        st.session_state.trd010_ScreenMode= 0
        st.session_state.trd010_mFORMS = st.formQuery_
        st.session_state.trd010_button1Disabled = False
        st.session_state.trd010_button2Disabled = True  
        setVarMode()
        
        #powerlib.pesan("Data tersebut Berhasil di simpan !")
        
        
    elif pNumber == 4 and st.session_state.trd010_ScreenMode != 0:                                 
        ## Undo Process ##
        st.session_state.trd010_ButtonNumber == 0
        st.session_state.trd010_sARECO = st.session_state.trd010_lARECO
        st.session_state.trd010_sARENA = st.session_state.trd010_lARENA
        st.session_state.trd010_sAREST = st.session_state.trd010_lAREST

        st.session_state.trd010_ScreenMode= 0
        st.session_state.trd010_mFORMS = st.formQuery_        
        st.session_state.trd010_button1Disabled = False
        st.session_state.trd010_button2Disabled = True  
        setVarMode()
    
def lastVarValue():
    try:
        st.session_state.trd010_lARECO = st.session_state.trd010_sARECO
        st.session_state.trd010_lARENA = st.session_state.trd010_sARENA
        st.session_state.trd010_lAREST = st.session_state.trd010_sAREST
    except:
        pass
    
def queryVar(pARECO):
    if pARECO == "":
        return
    st.session_state.trd010_sARECO = pARECO
    st.session_state.trd010_ScreenMode == 0
    setVarValue()
    st.session_state.selectArena = 0
    
def setVarValue():
    if st.session_state.trd010_ScreenMode == 1:
        st.session_state.trd010_sARECO = ""
        st.session_state.trd010_sARENA = ""
        st.session_state.trd010_sAREST = True 
          
    elif st.session_state.trd010_ScreenMode == 0:
        st.mARECO = st.session_state.trd010_sARECO
        sqlString = "SELECT arena,arest FROM aremas WHERE resta = 'A' AND areco='%s' LIMIT 1"%(st.mARECO)
        aremasdRec, aremasdNum = powerlib.sqlSelect(st.session_state.myConnLink, sqlString)
        if aremasdNum > 0:
            for data in range(aremasdNum):
                st.mARENA = aremasdRec[data][0]
                if aremasdRec[data][1] == 1:
                    st.session_state["trd010_sAREST"] = True
                else:
                    st.session_state["trd010_sAREST"] = False
        
def setVarMode():
    if st.session_state.trd010_mFORMS == st.formNew_:               # Add Mode
        st.session_state.trd010_FindDisabled = True
        st.session_state.trd010_KeyVarDisabled = False
        st.session_state.trd010_DatVarDisabled = False

          
    elif st.session_state.trd010_mFORMS == st.formEdit_:            # Edit Mode
        st.session_state.trd010_FindDisabled = True
        st.session_state.trd010_KeyVarDisabled = True
        st.session_state.trd010_DatVarDisabled = False

    else:                                                           # Query Mode
        st.session_state.trd010_FindDisabled = False
        st.session_state.trd010_KeyVarDisabled = True
        st.session_state.trd010_DatVarDisabled = True