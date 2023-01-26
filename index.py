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
kppn = st.sidebar.radio(
    "Pilih KPPN: ",
    options = options_filter('kppn'),
)
satker = st.sidebar.multiselect(
    "Pilih Satker: ",
    options = df["namasatker"].unique()
)
# options_base_bank = df["bank"].unique()
# options_base_bank = np.insert(options_base_bank,0,"ALL")
bank = st.sidebar.radio(
    "Pilih bank: ",
    options = options_filter('bank'), 
)
tahun = st.sidebar.radio(
    "pilih tahun:  ",
    options = options_filter('tahun'),
)

df_kppn = df.query ('kppn == @kppn')
df_namasatker = df.query('namasatker == @satker')
df_bank = df.query('bank == @bank')

df_selection = df.query('kppn == @kppn or namasatker == @satker or bank == @bank')


#--MAINPAGE---
st.title(':bar_chart: Dashboard Digipay')
st.markdown('##')
#TOPKPI

total_nilai_transaksi = int(find_value(kppn).sum())
jumlah_transaksi = int(find_value(kppn).count())
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



st.dataframe(all_or_classified(kppn))


# nominal_per_kppn = (
#     df_selection.groupby(by=["kppn"]).sum()[["nilai"]].sort_values(by="nilai")
# )
# fig_nominal_kppn = px.bar(
#     nominal_per_kppn,
#     x="nilai",
#     y=nominal_per_kppn,
#     orientation="h",
#     title = "<b>Nominal per KPPN</b>",
#     color_discrete_sequence=["#0083B8"] * len(nominal_per_kppn),
#     template = "plotly_white",
    
# )




hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

