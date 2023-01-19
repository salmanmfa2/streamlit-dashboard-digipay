import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Dashboard Digipay",
page_icon=":bar_chart:",
layout ="wide",
initial_sidebar_state="expanded")

df = pd.read_excel(
    io='E:\Laboratory\Experiment Room 2\Streamlit\DataSource\Digipay_transaksi.xlsx',
    engine='openpyxl',
    sheet_name='Sheet1',
    skiprows=0,
    usecols='C:M',
    nrows=2000
)


#--Sidebar Filter

st.sidebar.header("Filter Data:")

eselonSatu = st.sidebar.multiselect(
    "Pilih Eselon I: ",
    options = df["NAMA_ESI"].unique(),
)
kppn = st.sidebar.multiselect(
    "Pilih KPPN: ",
    options = df["NAMA_KPPN"].unique(),
)
satker = st.sidebar.multiselect(
    "Pilih Satker: ",
    options = df["NAMA_SATKER"].unique()
)

bank = st.sidebar.multiselect(
    "Pilih bank: ",
    options = df["BANK"].unique() 
)
aplikasi_digipay = {'list Bank':{'BRI':'Digipay002', 'MDRI':'Digipay008','BNI':'Digipay009'}}
df_selection = df.query('NAMA_ESI == @eselonSatu or NAMA_KPPN == @kppn or NAMA_SATKER == @satker or  BANK == @bank')

#--MAINPAGE---
st.title(':bar_chart: Dashboard Digipay')
st.markdown('##')
#TOPKPI
total_nilai_transaksi = int(df_selection["NILAI"].sum())
jumlah_transaksi = int(df_selection["NILAI"].count())
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

# nominal_per_kppn = (
#     df_selection.groupby(by=["KPPN"]).sum()[["NILAI"]].sort_values(by="NILAI")
# )
# fig_nominal_kppn = px.bar(
#     nominal_per_kppn,
#     x="Nilai",
#     y=nominal_per_kppn,
    
# )




hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

