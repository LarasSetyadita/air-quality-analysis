import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import datetime

# caching untuk mempersingkat waktu
@st.cache_data
def load_data(url): #fungsi untuk load dataframe
    dataFrame = pd.read_csv(url) #membaca dataframe
    return dataFrame 

# create daily temp index
def create_pm25_index_per_hour(df, date, station):
    pm25_index_per_hour = df[['hour', 'date', 'PM2.5', 'station']] 
    pm25_index_per_hour['date'] = pd.to_datetime(pm25_index_per_hour['date'])
    pm25_index_per_hour = pm25_index_per_hour.loc[
         (pm25_index_per_hour['date'] == date)&(pm25_index_per_hour['station'] == station)
    ]
    
    return pm25_index_per_hour

def create_temp_per_hour(df, date, station):
    temp_per_hour = df[['hour', 'date', 'TEMP', 'station']]
    temp_per_hour.date = pd.to_datetime(temp_per_hour.date)
    temp_per_hour = temp_per_hour.loc[(temp_per_hour['date'] == date) & (temp_per_hour['station'] == station)]

    return temp_per_hour

# import data
data = './dashboard/data_kualitas_udara.csv'
result_df = load_data(data)


st.title('Periksa Kualitas Udara dan Suhu ')
st.write('Silahkan masukkan tanggal kualitas udara yang ingin anda lihat')
    
station_list = st.selectbox(
    label = "pilih stasiun yang anda cari",
    options=('Aotizhongxin', 
            'Changping', 
            'Dingling', 
            'Dongsi', 
            'Guanyuan', 
            'Gucheng', 
            'Huairou', 
            'Nongzhangguan', 
            'Shunyi', 
            'Tiantan', 
            'Wanliu')
)

date_input = st.date_input(
    label='Masukkan tanggal', 
    min_value = datetime.date(2013, 3, 1), 
    max_value=datetime.date(2017, 2, 28)
)

st.subheader('Kualitas Udara Berdasarkan Index PM2.5')
date_input = pd.to_datetime(date_input)

pm25_index = create_pm25_index_per_hour(result_df, date_input, station_list)
    

col1, col2 = st.columns(2)
pm25_mean = pm25_index['PM2.5'].mean()
pm25_mean = round(pm25_mean, 2)

with col1:
    if pm25_mean < 21.1:
        st.metric('kategori', value="Baik")
    elif  pm25_mean < 35.5:
        st.metric('kategori', value="Sedang")
    elif pm25_mean < 55.5:
        st.metric('kategori', value="Sedikit Tidak Sehat")
    elif pm25_mean < 55.5:
        st.metric('kategori', value="Tidak Sehat")
    elif pm25_mean < 105.5:
        st.metric('kategori', value="Sangat Tidak Sehat")
    elif pm25_mean < 205.5:
        st.metric('kategori', value="Berbahaya")
    else:
        st.metric('kategori', value="Baik")

with col2 : 
    st.metric('indeks rata-rata', value=pm25_mean)

fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    pm25_index["hour"],
    pm25_index["PM2.5"],
    marker='o', 
    linewidth=2,
    color="#90CAF9"
)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)
plt.xlabel('Waktu (Jam)', fontsize=25)
plt.ylabel('Kadar PM2.5', fontsize=25)
st.pyplot(fig)   

st.subheader('Suhu')
temp_per_hour = create_temp_per_hour(result_df, date_input, station_list)

temp_mean = temp_per_hour['TEMP'].mean()
temp_mean = round(temp_mean, 2)

st.metric('Suhu Rata-rata harian', value=temp_mean)

fig, ax = plt.subplots(figsize=(16,8))
ax.plot(
    temp_per_hour["hour"],
    temp_per_hour["TEMP"],
    marker='o',
    linewidth=2,
    color="#90CAF9"
)

ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)
plt.xlabel('Waktu (Jam)', fontsize=25)
plt.ylabel('Suhu', fontsize=25)
st.pyplot(fig) 



