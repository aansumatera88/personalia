# File Code  : trd020.py
# File Name  : Grup Pegawai

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
import trd020p

def loadEGRMAS(sqlString):
    df = []
    list = []  
    list.append({
        'egrco': "",
        'egrna': ""
    })
    egrmasRec, egrmasNum = powerlib.sqlSelect(st.session_state.myConnLink, sqlString)
    if egrmasNum > 0:   
        for data in range(egrmasNum):
            list.append({
                'egrco': egrmasRec[data][0],
                'egrna': egrmasRec[data][1]
            })
        df = pd.DataFrame(list)
    return df

def callback0():
    st.session_state.trd020_button1Disabled = True
    st.session_state.trd020_button2Disabled = True  
    st.session_state.trd020_button3Disabled = False  
    
def callback1():
    st.session_state.trd020_button1Disabled = True
    st.session_state.trd020_button2Disabled = False  
    st.session_state.trd020_button3Disabled = False  
    
def callback2():
    if st.session_state.trd020_ScreenMode == 2:
        st.session_state.trd020_button1Disabled = False
        st.session_state.trd020_button2Disabled = True 
        st.session_state.trd020_button3Disabled = True  
        
def callback3():
    st.mEGRCO = st.session_state.trd020_sEGRCO 
    st.mEGRNA = st.session_state.trd020_sEGRNA
    st.mEGRCO = st.mEGRCO.strip()
    st.mEGRCO = st.mEGRCO.upper()
    if st.session_state.trd020_ScreenMode == 1:
        if st.mEGRCO == "":
            st.warning("Kode Grup Pegawai Harus diisi !")
            return       
        else:
            sqlString = "SELECT egrna FROM egrmas WHERE resta='A' AND egrco='%s'"%(st.mEGRCO)
            egrmasdRec, egrmasdNum = powerlib.sqlSelect(st.session_state.myConnLink, sqlString)
            if egrmasdNum > 0:
                st.warning("Kode Grup Pegawai sudah terdaftar !")     
                return     
    if st.mEGRNA == "":
        st.warning("Nama Grup Pegawai Harus diisi !")
        return
    
    st.session_state.trd020_button1Disabled = False
    st.session_state.trd020_button2Disabled = True 
    st.session_state.trd020_button3Disabled = True  
    
def callback4():
    st.session_state.trd020_button1Disabled = False
    st.session_state.trd020_button2Disabled = True 
    st.session_state.trd020_button3Disabled = True  
    
def callback5():
    if st.session_state.trd020_ShowPDF:
        st.session_state.trd020_ShowPDF = False
        html("""<script>
            var frame = document.getElementById("myframe");
            frame.parentNode.removeChild(frame);
            </script>""")
    else:
        st.session_state.trd020_ShowPDF = True
        trd020p.Trd020p()
    

def Trd020():
    if "myConnLink" not in st.session_state:
        st.session_state.myConnLink, st.session_state.myConnStatus = powerlib.dbConnection()
        
    if not st.session_state.myConnStatus:
        st.warning("Server Connection not Available !")
        st.stop()
    
    if "trd020_ScreenMode" not in st.session_state:
        st.session_state.selectEGRNA = 0
        st.session_state.trd020_ScreenMode = 1   # Add Mode
        st.session_state.trd020_FindDisabled = True
        st.session_state.trd020_KeyVarDisabled = False
        st.session_state.trd020_DatVarDisabled = False
        st.session_state.trd020_ButtonNumber = 0
        st.session_state.trd020_ShowPDF = False

        st.session_state.trd020_button1Disabled = False
        st.session_state.trd020_button2Disabled = True
        st.session_state.trd020_button3Disabled = True
        
        st.session_state.trd020_mFORMS = st.formNew_
        
        st.mEGRCO = ""
        st.mEGRNA = ""
        st.mEGRST = True
        
        st.session_state.trd020_lEGRCO = ""
        st.session_state.trd020_lEGRNA = ""
        st.session_state.trd020_lEGRST = True
        
        sqlString = "SELECT egrco,egrna,egrst FROM egrmas WHERE resta = 'A' ORDER BY egrna LIMIT 1"
        egrmasdRec, egrmasdNum = powerlib.sqlSelect(st.session_state.myConnLink, sqlString)
        if egrmasdNum > 0:
            st.session_state.trd020_ScreenMode= 0   # Query Mode
            st.session_state.trd020_mFORMS = st.formQuery_
            for data in range(egrmasdNum):
                st.mEGRCO = egrmasdRec[data][0]
                st.mEGRNA = egrmasdRec[data][1]
                if egrmasdRec[data][2] == 1:
                    st.mEGRST = True
                else:
                    st.mEGRST = False
                    
                st.session_state.trd020_lEGRCO = egrmasdRec[data][0]
                st.session_state.trd020_lEGRNA = egrmasdRec[data][1]
                if egrmasdRec[data][2] == 1:
                    st.session_state.trd020_lEGRST = True
                else:
                    st.session_state.trd020_lEGRST = False
                    
            st.session_state.trd020_FindDisabled = False
            st.session_state.trd020_KeyVarDisabled = True
            st.session_state.trd020_DatVarDisabled = True
        else:
            st.session_state.trd020_button1Disabled = True
            st.session_state.trd020_button2Disabled = True  
            st.session_state.trd020_button3Disabled = False  
      
    ### Button Section ###
    with st.container():
        headerColumn1, headerColumn2, headerColumn3 = st.columns([1,3,1])
        with headerColumn1:
            st.subheader(":blue[Grup Pegawai]")
            #st.header('A header with _italics_ :blue[colors] and emojis :sunglasses:')
             
        with headerColumn2:
            buttonColumn1, buttonColumn2, buttonColumn3, buttonColumn4, buttonColumn5, buttonColumn6, buttonColumn7 = st.columns(7)
            with buttonColumn1:
                if st.button("New", key= "trd020_buttonNew", on_click=callback0, disabled=st.session_state.trd020_button1Disabled):
                    clickButton(0)
            with buttonColumn2:
                if st.button("Edit", key= "trd020_buttonEdit", on_click=callback1, disabled=st.session_state.trd020_button1Disabled):
                    clickButton(1)
            with buttonColumn3:                
                if st.button("Delete", key= "trd020_buttonDelete", on_click=callback2, disabled=st.session_state.trd020_button2Disabled):
                    clickButton(2)
            with buttonColumn4:
                if st.button("Save", key= "trd020_buttonSave", on_click=callback3, disabled=st.session_state.trd020_button3Disabled):
                    clickButton(3)
            with buttonColumn5:
                if st.button("Undo", key= "trd020_buttonUndo", on_click=callback4, disabled=st.session_state.trd020_button3Disabled):
                    clickButton(4)
            with buttonColumn6:
                if st.button("Print", key= "trd020_buttonPrint", on_click=callback5, disabled=st.session_state.trd020_button1Disabled):
                    clickButton(5)
            with buttonColumn7:
                st.write(" ")

        with headerColumn3:
            st.trd020_FORMS = st.text_input("Status", value=st.session_state.trd020_mFORMS, key="trd020Form", disabled=True, label_visibility="collapsed")
        
    ### Search Section ###
    with st.container():
        searchColumn1, searchColumn2, searchColumn3 = st.columns([2,1,2])
        with searchColumn2:
            strSearch = "SELECT egrco, egrna FROM egrmas WHERE resta='A' ORDER BY egrna"
            st.listEGRMAS = loadEGRMAS(strSearch)
            try:
                st.selected_egrna = st.selectbox("Pilih Nama Grup Pegawai", st.listEGRMAS.egrna, st.session_state.selectEGRNA, key="trd020Search",  disabled= st.session_state.trd020_FindDisabled )
                st.EGRCO = st.listEGRMAS.loc[st.listEGRMAS.egrna == st.selected_egrna]["egrco"].iloc[0]
                queryVar(st.EGRCO)   
            except:
                pass
            
    ### Data Section ###               
    with st.container():
        detailColumn1, detailColumn2 = st.columns([1,2])
        with detailColumn1:
            st.trd020_EGRCO = st.text_input("Kode Grup Pegawai", value=st.mEGRCO,  max_chars=5, key="trd020_sEGRCO", disabled=st.session_state.trd020_KeyVarDisabled)
            st.trd020_EGRNA = st.text_input("Nama Grup Pegawai", value=st.mEGRNA,  max_chars=35, key="trd020_sEGRNA", disabled=st.session_state.trd020_DatVarDisabled)
            st.trd020_EGRST = st.checkbox("Status Grup Pegawai", value=st.mEGRST, key="trd020_sEGRST", disabled=st.session_state.trd020_DatVarDisabled)
                  
def clickButton(pNumber):
    if pNumber == 0 and st.session_state.trd020_ScreenMode== 0 :           
        ## New Data  ##
        st.session_state.trd020_ScreenMode = 1
        st.session_state.trd020_mFORMS = st.formNew_
        st.session_state.trd020_ButtonNumber == 0
        lastVarValue()
        setVarMode()
        setVarValue()
   
    elif pNumber == 1 and st.session_state.trd020_ScreenMode== 0 :         
        ## Edit Data ##
        st.session_state.trd020_button1Disabled = True
        st.session_state.trd020_button2Disabled = False        
        
        st.session_state.trd020_ScreenMode= 2
        st.session_state.trd020_mFORMS = st.formEdit_
        st.session_state.trd020_ButtonNumber == 0
        lastVarValue()
        setVarMode()

    elif pNumber== 2 and st.session_state.trd020_ScreenMode == 2:                                 
        ## Delete Data ##
        st.mEGRCO = st.session_state.trd020_sEGRCO 
    
        if st.session_state.trd020_ScreenMode == 2 :
            mDATEN = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            strData = "UPDATE egrmas SET resta='D', ladup='%s', upusr='%s' WHERE resta='A' AND egrco='%s' "
            strData = strData%(mDATEN, st.session_state.UserName_, st.mEGRCO)
            powerlib.sqlUpdate(st.session_state.myConnLink, strData)
            
            st.session_state.trd020_ScreenMode = 1
            sqlString = "SELECT egrco FROM egrmas WHERE resta = 'A' LIMIT 1"
            egrmasdRec, egrmasdNum = powerlib.sqlSelect(st.session_state.myConnLink, sqlString)
            if egrmasdNum > 0:
                st.session_state.trd020_ScreenMode = 0
                for data in range(egrmasdNum):
                    st.session_state.trd020_sEGRCO = egrmasdRec[data][0]
            
            st.session_state.trd020_ScreenMode= 0
            st.session_state.trd020_mFORMS = st.formQuery_
            setVarValue()
            setVarMode()
                 
    elif pNumber == 3 and st.session_state.trd020_ScreenMode != 0:                                 
        ## Save Data ##
        st.session_state.trd020_ButtonNumber == 0
        st.mEGRCO = st.session_state.trd020_sEGRCO 
        st.mEGRNA = st.session_state.trd020_sEGRNA
        if st.session_state.trd020_sEGRST:
            st.mEGRST = 1
        else:
            st.mEGRST = 0
        st.mEGRCO = st.mEGRCO.strip()
        st.mEGRCO = st.mEGRCO.upper()
        
        if st.mEGRCO == "":
            return 
               
        if st.mEGRNA == "":
            return

        mDATEN = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        if st.session_state.trd020_ScreenMode== 1:
            strData = "INSERT INTO egrmas(daten,enusr,resta,egrco,egrna,egrst) VALUES('%s','%s','%s','%s','%s','%s')"
            strData = strData%(mDATEN, st.session_state.UserName_, 'A', st.mEGRCO, st.mEGRNA, st.mEGRST)
        else:
            strData = "UPDATE egrmas SET ladup='%s', enusr='%s', egrna='%s', egrst='%s' WHERE resta='A' AND egrco='%s' "
            strData = strData%(mDATEN, st.session_state.UserName_, st.mEGRNA, st.mEGRST, st.mEGRCO)
        powerlib.sqlUpdate(st.session_state.myConnLink, strData)
        
        st.session_state.trd020_ScreenMode= 0
        st.session_state.trd020_mFORMS = st.formQuery_
        st.session_state.trd020_button1Disabled = False
        st.session_state.trd020_button2Disabled = True  
        setVarMode()
        
        #powerlib.pesan("Data tersebut Berhasil di simpan !")
        
        
    elif pNumber == 4 and st.session_state.trd020_ScreenMode != 0:                                 
        ## Undo Process ##
        st.session_state.trd020_ButtonNumber == 0
        st.session_state.trd020_sEGRCO = st.session_state.trd020_lEGRCO
        st.session_state.trd020_sEGRNA = st.session_state.trd020_lEGRNA
        st.session_state.trd020_sEGRST = st.session_state.trd020_lEGRST

        st.session_state.trd020_ScreenMode= 0
        st.session_state.trd020_mFORMS = st.formQuery_        
        st.session_state.trd020_button1Disabled = False
        st.session_state.trd020_button2Disabled = True  
        setVarMode()
    
def lastVarValue():
    try:
        st.session_state.trd020_lEGRCO = st.session_state.trd020_sEGRCO
        st.session_state.trd020_lEGRNA = st.session_state.trd020_sEGRNA
        st.session_state.trd020_lEGRST = st.session_state.trd020_sEGRST
    except:
        pass
    
def queryVar(pEGRCO):
    if pEGRCO == "":
        return
    st.session_state.trd020_sEGRCO = pEGRCO
    st.session_state.trd020_ScreenMode == 0
    setVarValue()
    st.session_state.selectEGRNA = 0
    
def setVarValue():
    if st.session_state.trd020_ScreenMode == 1:
        st.session_state.trd020_sEGRCO = ""
        st.session_state.trd020_sEGRNA = ""
        st.session_state.trd020_sEGRST = True 
          
    elif st.session_state.trd020_ScreenMode == 0:
        st.mEGRCO = st.session_state.trd020_sEGRCO
        sqlString = "SELECT egrna,egrst FROM egrmas WHERE resta = 'A' AND egrco='%s' LIMIT 1"%(st.mEGRCO)
        egrmasdRec, egrmasdNum = powerlib.sqlSelect(st.session_state.myConnLink, sqlString)
        if egrmasdNum > 0:
            for data in range(egrmasdNum):
                st.mEGRNA = egrmasdRec[data][0]
                if egrmasdRec[data][1] == 1:
                    st.session_state["trd020_sEGRST"] = True
                else:
                    st.session_state["trd020_sEGRST"] = False
        
def setVarMode():
    if st.session_state.trd020_mFORMS == st.formNew_:               # Add Mode
        st.session_state.trd020_FindDisabled = True
        st.session_state.trd020_KeyVarDisabled = False
        st.session_state.trd020_DatVarDisabled = False

          
    elif st.session_state.trd020_mFORMS == st.formEdit_:            # Edit Mode
        st.session_state.trd020_FindDisabled = True
        st.session_state.trd020_KeyVarDisabled = True
        st.session_state.trd020_DatVarDisabled = False

    else:                                                           # Query Mode
        st.session_state.trd020_FindDisabled = False
        st.session_state.trd020_KeyVarDisabled = True
        st.session_state.trd020_DatVarDisabled = True