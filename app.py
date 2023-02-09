import pandas as pd
import plotly.express as px
import streamlit as st
import numpy as np
from io import BytesIO

st.set_page_config(page_title="Dashboard Digipay",
page_icon=":bar_chart:",
layout ="wide",
initial_sidebar_state="expanded")

df = pd.read_excel(
    io='.\Assets\Digipay_transaksi.xlsx',
    engine='openpyxl',
    sheet_name='Sheet3',
    skiprows=0,
    nrows=5000
)
# Functions
@st.cache
def options_filter(input):
    if input =='tahun':
        return df['tahun'].unique()
    else:
        options_base = df[input].unique()
        options_base = np.insert(options_base,0,"ALL")
        return options_base

def to_excel(df):
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, index=False, sheet_name='Sheet1')
    workbook = writer.book
    worksheet = writer.sheets['Sheet1']
    format1 = workbook.add_format({'num_format': '0.00'}) 
    worksheet.set_column('A:A', None, format1)  
    writer.save()
    processed_data = output.getvalue()
    return processed_data

def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode('utf-8')


#--Sidebar Filter

st.sidebar.header("Filter Data:")

# options_base = df["kppn"].unique()
# options_base = np.insert(options_base,0,"ALL")
st.sidebar.button('Reset Filter', key=None, help=None, on_click=None,)
kppn = st.sidebar.radio(
    "Pilih KPPN: ",
    options = options_filter('kppn'),
)
kppn_query = ['Kendari','Kolaka','Baubau','Raha'] if kppn == 'ALL' else kppn

# options_base_bank = df["bank"].unique()
# options_base_bank = np.insert(options_base_bank,0,"ALL")
bank = st.sidebar.radio(
    "Pilih bank: ",
    options = options_filter('bank'), 
)
bank_query = ['BRI','MDRI','BNI'] if bank == 'ALL' else bank
tahun = st.sidebar.radio(
    "pilih tahun:  ",
    options = [2020,2021,2022,2023,'ALL'],
)
tahun_query = [2020,2021,2022,2023] if tahun == 'ALL' else tahun

df_selection = df.query('kppn == @kppn_query and bank == @bank_query and @tahun_query == tahun' )


#--MAINPAGE---
st.title(':bar_chart: Dashboard Digipay')
st.markdown('##')
#TOPKPI

total_nilai_transaksi = int(df_selection['nilai'].sum())
jumlah_transaksi = int(df_selection['nilai'].count())
accounting_format_nominal = "{:,.2f}".format(total_nilai_transaksi)
accounting_format_jumlah = "{:,}".format(jumlah_transaksi)
kolom1 , kolom2 = st.columns(2)
with kolom1:
    st.subheader("Nilai Transaksi :")
    st.subheader("Rp. "+ str(accounting_format_nominal))
with kolom2:
    st.subheader ("Jumlah Transaksi :")
    st.subheader(str(accounting_format_jumlah) + " Transaksi")
st.markdown('---')

st.dataframe(df_selection)

st.markdown("""
<style>
.big-font {
    font-size:300px !important;
}
</style>
""", unsafe_allow_html=True)
st.subheader('Unduh File: ')
df_xlsx = to_excel(df_selection)
df_csv = convert_df(df_selection)

kolom1, kolom2, kolom3, kolom4, kolom5,kolom6,kolom7,kolom8,kolom9 = st.columns(9, gap = "large")
with kolom1:
    st.download_button(label='Xlsx',
                                data=df_xlsx ,
                                file_name= 'download.xlsx')
with kolom2:
    st.download_button(
    label="CSV",
    data=df_csv,
    file_name='download.csv',
    mime='text/csv',)

with kolom3:
    st.download_button(label="Generate Laporan (Pdf)",
    data = df_csv,
     file_name='laporan.pdf',
     mime='text/pdf')







hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

