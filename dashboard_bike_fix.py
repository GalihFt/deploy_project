# -*- coding: utf-8 -*-
"""
Created on Mon Mar  4 23:29:10 2024

@author: USER
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
sns.set()
sns.set(style='dark')


#import data
day_df = pd.read_csv("day.csv", sep=";")
hour_df = pd.read_csv("hour.csv", sep=";")

#mengubah kategori
category = ["season","mnth","yr", "holiday", "weekday", "workingday", "weathersit"]
for categ in category:
    day_df[categ] = day_df[categ].astype('category')
    hour_df[categ] = hour_df[categ].astype('category')

day_df["dteday"] = pd.to_datetime(day_df["dteday"], format='%d/%m/%Y')
hour_df["dteday"] = pd.to_datetime(hour_df["dteday"], format='%d/%m/%Y')

#mengubah value kategori
day_df.season.replace((1,2,3,4), ("Springer","Summer","Fall","Winter"), inplace=True)
day_df.yr.replace((0,1), (2011,2012), inplace=True)
day_df.mnth.replace((1,2,3,4,5,6,7,8,9,10,11,12),('Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'), inplace=True)
day_df.holiday.replace((0,1),("No", "Yes"), inplace=True)
day_df.weekday.replace((0,1,2,3,4,5,6), ('Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday'), inplace=True)
day_df.workingday.replace((0,1), ('No', 'Yes'), inplace=True)
day_df.weathersit.replace((1,2,3,4), ('Clear','Misty/Cloudy','Light Snow/Rain','Heavy Rain'), inplace=True)
hour_df.season.replace((1,2,3,4), ("Spring","Summer","Fall","Winter"), inplace=True)
hour_df.yr.replace((0,1), (2011,2012), inplace=True)
hour_df.mnth.replace((1,2,3,4,5,6,7,8,9,10,11,12),('Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'), inplace=True)
hour_df.holiday.replace((0,1),("No", "Yes"), inplace=True)
hour_df.weekday.replace((0,1,2,3,4,5,6), ('Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday'), inplace=True)
hour_df.workingday.replace((0,1), ('No', 'Yes'), inplace=True)
hour_df.weathersit.replace((1,2,3,4), ('Clear','Misty/Cloudy','Light Snow/Rain','Heavy Rain'), inplace=True)

#Melakukan Unstandarized day_df
day_df['temp'] = day_df['temp']*41
day_df['atemp'] = day_df['atemp']*50
day_df['hum'] = day_df['hum']*100
day_df['windspeed'] = day_df['windspeed']*67

#Melakukan Unstandarized hour_df
hour_df['temp'] = hour_df['temp']*41
hour_df['atemp'] = hour_df['atemp']*50
hour_df['hum'] = hour_df['hum']*100
hour_df['windspeed'] = hour_df['windspeed']*67




# Filter
min_date = day_df["dteday"].min()
max_date = day_df["dteday"].max()

#membuat sidebar
with st.sidebar:
    # Menambahkan logo 
    st.image("https://github.com/GalihFt/Coba/blob/main/Untitled%20design.png?raw=true")
    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )
    

main_df_day = day_df[(day_df["dteday"] >= str(start_date)) & 
                (day_df["dteday"] <= str(end_date))]
main_df_hour = hour_df[(hour_df["dteday"] >= str(start_date)) & 
                (hour_df["dteday"] <= str(end_date))]



#Title
st.markdown("<h1 style='color: #8080ff; font-size: 100px; text-align: center;'>BIKE SHARING</h1>", unsafe_allow_html=True)
st.markdown("<h2 style='color: #ff3333; font-size: 100px; text-align: center;'>DASHBOARD</h2>", unsafe_allow_html=True)
st.markdown("<div style='width: 730px; height: 100px;text-align: justify'>Sistem Bike Sharing adalah inovasi penyewaan sepeda modern yang memungkinkan pengguna untuk menyewa dan mengembalikan sepeda secara otomatis. Ada lebih dari 500 program berbagi sepeda di seluruh dunia dengan lebih dari 500 ribu sepeda. Sistem ini penting dalam masalah lalu lintas, lingkungan, dan kesehatan.</div>", unsafe_allow_html=True)
st.markdown("<h4 style='color: black; font-size: 20px; text-align: center;'>Periode Waktu {} s.d {} </h4>".format(start_date,end_date), unsafe_allow_html=True)

st.markdown("<h4 style='color: black; font-size: 30px; text-align: center;'>Perkembangan Jumlah Sewa Sepeda</h4>", unsafe_allow_html=True) 

#Matriks teratas
col1, col2, col3 = st.columns(3)
with col1:
    total_casual = main_df_day.casual.sum()
    st.metric("Casual User", value="{:,}".format(total_casual))  # Applying formatting

# Total registered users
with col2:
    total_registered = main_df_day.registered.sum()
    st.metric("Registered User", value="{:,}".format(total_registered))  # Applying formatting

# Total users
with col3:
    total_user = main_df_day.registered.sum() + main_df_day.casual.sum()
    st.metric("Total User", value="{:,}".format(total_user))  # Applying formatting


#Line Chart Waktu ke Waktu
fig,ax=plt.subplots(figsize=(15, 6))
sns.lineplot(data=main_df_day, x='dteday', y='cnt', color='green', marker='o', markersize=10)
sns.lineplot(data=main_df_day, x='dteday', y='registered', color='blue', marker='o', markersize=10)
sns.lineplot(data=main_df_day, x='dteday', y='casual', color='red', marker='o', markersize=10)

green_patch = plt.Rectangle((0,0),1,1,fc="green", edgecolor = 'none')
blue_patch = plt.Rectangle((0,0),1,1,fc="blue", edgecolor = 'none')
red_patch = plt.Rectangle((0,0),1,1,fc="red", edgecolor = 'none')
plt.legend([green_patch,blue_patch, red_patch], ['Total','Registered', 'Casual'], loc="upper left")

plt.title('Time Series Chart: Perkembangan Jumlah Sepeda yang Disewa', fontsize=20, fontweight='bold')
plt.xlabel('Date')
plt.ylabel('Value')

plt.tight_layout()
st.pyplot(fig)


#Important Plot
st.markdown("<h4 style='color: black; font-size: 30px; text-align: center;'>Visualisasi Jumlah Sewa Sepeda Berdasarkan Waktu</h4>", unsafe_allow_html=True) 
data = [main_df_day['registered'].sum(), main_df_day['casual'].sum()]
keys = ["Registered Customers", "Casual Customers"]

fig, axes = plt.subplots(2, 2, figsize=(12, 10), dpi=200)
pie = axes[0, 0].pie(data, autopct="%.0f%%", colors=("#8080ff", "#ff3333"))
axes[0, 0].set_title('Pie Chart: Tipe User', fontsize=20, fontweight='bold')
axes[0, 0].legend(pie[0], keys, loc="upper left", bbox_to_anchor=(1, 1))

# Barchart
sns.barplot(data=main_df_day, x="workingday", y="cnt", palette=("#ff3333", "#8080ff"), ax=axes[0, 1])
axes[0, 1].set_xticklabels(labels=["Non-Working Day", "Working Day"], rotation=45)
axes[0, 1].set_title('Barchart: Perbandingan Rata-Rata Jumlah Sewa pada\n Hari Bekerja dan Tidak Bekerja', fontsize=15, fontweight='bold')
axes[0, 1].set_xlabel('Date')
axes[0, 1].set_ylabel('Value')

sns.barplot(data=main_df_day, x="weathersit", y="cnt", color="#ff3333", ax=axes[1, 0],)
axes[1, 0].set_xticklabels(labels=day_df["weathersit"].unique(), rotation=45)
axes[1, 0].set_title('Barchart: Perbandingan Rata-Rata Jumlah Sewa \n pada Setiap Tipe Cuaca', fontsize=15, fontweight='bold')
axes[1, 0].set_xlabel('Weather Situation')
axes[1, 0].set_ylabel('Value')

sns.barplot(data=main_df_day, x="weekday", y="cnt", color="#ff3333", ax=axes[1, 1])
axes[1, 1].set_xticklabels(labels=["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"], rotation=45)
axes[1, 1].set_title('Barchar: Perbandingan Rata-Rata Jumlah Sewa \n pada Setiap Hari', fontsize=15, fontweight='bold')
axes[1, 1].set_xlabel('Weekday')
axes[1, 1].set_ylabel('Value')

plt.tight_layout()
plt.show()
st.pyplot(fig)


#Barchart per Jam
st.markdown("<h4 style='color: black; font-size: 30px; text-align: center;'>Detail Rata-Rata Penyewaan Sepeda per Jam</h4>", unsafe_allow_html=True)
# Buat objek gambar Matplotlib
fig, ax = plt.subplots()
sns.barplot(data=main_df_hour, x="hr", y="registered", color="#8080ff")
sns.barplot(data=main_df_hour, x="hr", y="casual", color="#ff3333")
blue_patch = plt.Rectangle((0,0),1,1,fc="#8080ff", edgecolor = 'none')
red_patch = plt.Rectangle((0,0),1,1,fc="#ff3333", edgecolor = 'none')
plt.legend([blue_patch, red_patch], ['Registered', 'Casual'])
ax.set_xlabel('Jam')
ax.set_ylabel('Jumlah Penyewa')
st.pyplot(fig)

st.caption('Copyright (c) Galih Fitriatmo 2024')
