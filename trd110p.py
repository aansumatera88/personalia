from fpdf import FPDF
import streamlit as st
import base64, urllib
import powerlib

if "myConnLink" not in st.session_state:
    st.session_state.myConnLink, st.session_state.myConnStatus = powerlib.dbConnection()

def create_download_link(val, filename):
    b64 = base64.b64encode(val)  # val looks like b'...'
    #return f'<a href="data:application/octet-stream;base64,{b64.decode()}" download="{filename}.pdf">Download file</a>'
    return f'<a href="data:application/octet-stream;base64,{b64.decode()}" download="{filename}.pdf">Download file</a>'


class PDF(FPDF):
    def header(self):
        # Logo
        self.image('MetroLogo.png', 10, 8, 33)
        # Arial bold 15
        self.set_font('Arial', 'B', 15)
        # Move to the right
        self.cell(80)
        # Title
        self.cell(30, 10, 'Daftar Area', 0, 0, 'C')
        # Line break
        self.ln(20)
        self.line(10,35,200,35)
        self.set_font('Courier', 'B', 12)
        myRecLine = 98 * " "
        myRecLine = myRecLine[:0] + "No."           + myRecLine[3:]
        myRecLine = myRecLine[:8] + "Kode Area"     + myRecLine[17:]
        myRecLine = myRecLine[:22] + "Nama Area"    + myRecLine[31:]
        myRecLine = myRecLine[:55] + "Status"       + myRecLine[61:]
        self.cell(0, 20, myRecLine, 0, 1)
        self.line(10,45,200,45)
        #self.ln(10)

    # Page footer
    def footer(self):
        # Position at 1.5 cm from bottom
        self.set_y(-15)
        # Arial italic 8
        self.set_font('Courier', 'I', 8)
        # Page number
        self.cell(0, 10, 'Page ' + str(self.page_no()) + '/{nb}', 0, 0, 'C')
        
#export_as_pdf = st.button("Export Report")

def show_pdf(file_path):
    with open(file_path,"rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="800" height="800" type="application/pdf" target="_blank"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)
    #st.write(st.session_state)
   
    
def Trd110p():
# Instantiation of inherited class
    pdf = PDF()
    pdf.alias_nb_pages()
    pdf.add_page()
    pdf.set_font('Courier', '', 12)


    sqlString = "SELECT areco,arena,arest FROM aremas WHERE resta = 'A' AND arest = 1"
    aremasdRec, aremasdNum = powerlib.sqlSelect(st.session_state.myConnLink, sqlString)
    if aremasdNum > 0:
        mLINNO = 0
        for data in range(aremasdNum):
            mARECO = aremasdRec[data][0]
            mARENA = aremasdRec[data][1]
            if aremasdRec[data][2] == 1:
                mAREST = "Aktif"
            else:
                mAREST = "Tidak Aktif"
                
            lenARECO = len(mARECO)
            lenARENA = len(mARENA)
            lenAREST = len(mAREST)
            mLINNO = mLINNO + 1
            myRecLine = 98 * " "
            myRecLine = myRecLine[:0] + \
                powerlib.convertNumToStrFormat(mLINNO, 0, 3) + myRecLine[4:]
            myRecLine = myRecLine[:8] + mARECO + myRecLine[8+lenARECO:]
            myRecLine = myRecLine[:22] + mARENA + myRecLine[22+lenARENA:]
            myRecLine = myRecLine[:55] + mAREST + myRecLine[55+lenAREST:]
            pdf.cell(0, 10, myRecLine, 0, 1)
    pdf.output("trd110p.pdf")  
       
    #show_pdf("trd110p.pdf")
    
    pdf_data = open("trd110p.pdf", "rb").read()
    b64 = base64.b64encode(pdf_data).decode('utf-8')
    pdf_url = f"data:application/pdf;base64,{b64}"

    iframe = f'<iframe src="{pdf_url}" width="100%" height="500px"></iframe>'
    st.markdown(f'<a href="{pdf_url}" target="_blank">{iframe}</a>', unsafe_allow_html=True)
    
    
    #html = create_download_link(pdf.output(dest="S").encode("latin-1"), "trd110p")
    #st.markdown(html, unsafe_allow_html=True)