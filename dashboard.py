#!/usr/bin/env python
# coding: utf-8

# In[94]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency

sns.set(style='dark')

# Helper function yang dibutuhkan untuk menyiapkan berbagai dataframe

def create_penyewaan_harian_df(df):
    penyewaan_harian_df = day_df.resample(rule='D', on='tanggal').agg({
        "total": "sum"
    }).reset_index()
    
    return penyewaan_harian_df

def create_musim_df(df):
    musim_df = day_df.groupby(by="musim").total.sum().reset_index()
    return musim_df

def create_cuaca_df(df):
    cuaca_df = hour_df.groupby(by="cuaca").total.sum().sort_values(ascending=False).reset_index()
    return cuaca_df

def create_bulan_df(df):
    bulan_df = day_df.groupby(by="bulan").total.sum().reset_index()
    return bulan_df

def create_jam_df(df):
    jam_df = hour_df.groupby(by="jam").total.sum().reset_index()
    return jam_df

def create_pelanggan_df(df):
    pelanggan_df = day_df.groupby(by="bulan").agg({
        "pelanggan_biasa": "sum",
        "pelanggan_terdaftar": "sum"
    }).reset_index()

    return pelanggan_df

# Load cleaned data
hour_df = pd.read_csv("hour_data.csv")
day_df = pd.read_csv("day_data.csv")

day_df["tanggal"] = pd.to_datetime(day_df["tanggal"])

# Filter data
min_date = day_df["tanggal"].min()
max_date = day_df["tanggal"].max()

with st.sidebar:
    # Menambahkan logo
    st.image("bike.png")
    
    # Mengambil start_date & end_date dari tanggal
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = day_df[(day_df["tanggal"] >= str(start_date)) &
                 (day_df["tanggal"] <= str(end_date))]

# Menyiapkan berbagai dataframe
penyewaan_harian_df = create_penyewaan_harian_df(main_df)
musim_df = create_musim_df(day_df)
cuaca_df = create_cuaca_df(day_df)
bulan_df = create_bulan_df(day_df)
jam_df = create_jam_df(hour_df)
pelanggan_df = create_pelanggan_df(day_df)

# Plot total sewa harian
st.header('Bike Sharing Dashboard :bicyclist:')
st.subheader('Penyewaan Harian')

total_sewa = penyewaan_harian_df.total.sum()
st.metric("Total sewa", value=total_sewa)

fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    penyewaan_harian_df["tanggal"],
    penyewaan_harian_df["total"],
    marker='o', 
    linewidth=2,
    color="#90CAF9"
)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)

st.pyplot(fig)

# Plot total sewa berdasarkan kriteria tertentu
st.subheader("Penyewaan Sepeda Berdasarkan Kriteria Khusus")

# Plot berdasarkan musim dan cuaca
col1, col2 = st.columns(2)

with col1:
    fig, ax = plt.subplots(figsize=(20, 10))
    
    colors = ["#90CAF9", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
    
    sns.barplot(
        y="total", 
        x="musim",
        data=musim_df.sort_values(by="total", ascending=False),
        palette=colors,
        ax=ax
    )
    ax.set_title("Total Penyewaan Berdasarkan Musim", loc="center", fontsize=50)
    ax.set_ylabel(None)
    ax.set_xlabel(None)
    ax.tick_params(axis='x', labelsize=35)
    ax.tick_params(axis='y', labelsize=30)
    st.pyplot(fig)

with col2:
    fig, ax = plt.subplots(figsize=(20, 10))
    
    colors = ["#90CAF9", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
    
    sns.barplot(
        y="total", 
        x="cuaca",
        data=cuaca_df.sort_values(by="total", ascending=False),
        palette=colors,
        ax=ax
    )
    ax.set_title("Total Penyewaan Berdasarkan Cuaca", loc="center", fontsize=50)
    ax.set_ylabel(None)
    ax.set_xlabel(None)
    ax.tick_params(axis='x', labelsize=35)
    ax.tick_params(axis='y', labelsize=30)
    st.pyplot(fig)

# Plot berdasarkan bulan dan jam
col1, col2 = st.columns(2)

with col1:
    fig, ax = plt.subplots(figsize=(20, 10))
    
    ax.plot(
        bulan_df['bulan'],
        bulan_df['total'],
        marker='o',
        linewidth=2,
        color="#90CAF9"
    )
    plt.title("Trend penyewaan sepeda berdasarkan bulan", fontsize=50)
    ax.tick_params(axis='x', labelsize=35)
    ax.tick_params(axis='y', labelsize=30)
    st.pyplot(fig)

with col2:
    fig, ax = plt.subplots(figsize=(20, 10))
    
    ax.plot(
        jam_df['jam'],
        jam_df['total'],
        marker='o',
        linewidth=3,
        color="#90CAF9"
    )
    plt.title("Trend penyewaan sepeda berdasarkan jam", fontsize=50)
    ax.tick_params(axis='x', labelsize=35)
    ax.tick_params(axis='y', labelsize=30)
    plt.xticks(np.arange(min(jam_df['jam']), max(jam_df['jam'])+1, 2.0))
    st.pyplot(fig)

# Demografi pelanggan
st.subheader('Demografi Pelanggan')

fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    pelanggan_df["bulan"], pelanggan_df["pelanggan_terdaftar"], marker='o', linewidth=2, color="#90CAF9"
)
ax.plot(
    pelanggan_df["bulan"], pelanggan_df["pelanggan_biasa"], marker='o', linewidth=2, color="#D3D3D3"
)
ax.legend(["pelanggan_terdaftar","pelanggan_biasa"], loc="upper left")
plt.title("Profil pelanggan penyewaan sepeda", fontsize=50)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)

st.pyplot(fig)

st.caption('Made by dwiHadi')

