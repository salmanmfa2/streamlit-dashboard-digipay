import pandas as pd
import plotly.express as px
import streamlit as st
import numpy as np

st.set_page_config(page_title="Dashboard Digipay",
page_icon=":bar_chart:",
layout ="wide",
initial_sidebar_state="expanded")

df = pd.read_excel(
    io='Digipay_transaksi.xlsx',
    engine='openpyxl',
    sheet_name='Sheet3',
    skiprows=0,
    nrows=5000
)
# Functions
def all_or_classified(input):
    if input == 'ALL':
        return df
    else:
        return df_selection

def find_value(input):
    if input == 'ALL':
        return df['nilai']
    else:
        return df_selection["nilai"]

def options_filter(input):
    if input =='tahun':
        return df['tahun'].unique()
    else:
        options_base = df[input].unique()
        options_base = np.insert(options_base,0,"ALL")
        return options_base




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
    options = options_filter('tahun'),
)
tahun_query = ['2020','2021','2022'] if tahun == 'ALL' else tahun

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
@st.cache
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode('utf-8')

csv = convert_df(df_selection)

st.download_button(
    label="Download data as XLSX",
    data=csv,
    file_name='digipay.xlsx',
    mime='application/vnd.ms-excel',
)

hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

