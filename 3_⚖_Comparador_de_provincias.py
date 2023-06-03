# -*- coding: utf-8 -*-
"""
Created on Mon May 29 11:37:49 2023

@author: Jose Giner
"""
import pandas as pd
import locale
from pyuca import Collator
import streamlit as st
import plotly.express as px

st.set_page_config(page_title="Comparador de provincias", page_icon="⚖")

locale.setlocale(locale.LC_ALL, 'es_ES.UTF-8')
# Crea un objeto Unicode Collation Algorithm (UCA)
collator = Collator()

def display_number_input():
    return st.number_input('Provincias a comparar (max 5)', min_value = 2, max_value=5)

def display_prov_filter(k, n):
    return st.sidebar.selectbox(f'Provincia {n}', prov_list, key=k, index=k)

def display_evol_sells(df, selected_provs):
    df_prov = df[df['provincia'].isin(selected_provs)]
    df_prov = df_prov.groupby(['provincia','month_and_year'],as_index = False).qty_ordered.sum()
    df_prov.columns = ['Provincia','Fecha','Unidades vendidas']
    fig = px.line(df_prov, x="Fecha", y="Unidades vendidas", color="Provincia")
    st.plotly_chart(fig, theme="streamlit", use_container_width=True)
    
def display_bar_sells(df, selected_provs):
    df_prov = df[df['provincia'].isin(selected_provs)]
    sales_by_prov = df_prov.groupby(['provincia','analytic_category'], as_index = False).qty_ordered.sum().sort_values(by = 'qty_ordered', ascending = False)
    sales_by_prov.columns = ['Provincia','Categoría','Unidades vendidas']
    
    fig = px.bar(sales_by_prov, x='Unidades vendidas', y='Provincia', color = 'Categoría', height=400)
    fig.update_layout(yaxis=dict(autorange="reversed"))
    fig.update_traces(hovertemplate= "<b>Unidades vendidas: </b> %{x:.0f}")
    st.plotly_chart(fig, theme="streamlit", use_container_width=True)

def display_evol_revenue(df, selected_provs):
    df_prov = df[df['provincia'].isin(selected_provs)]
    df_prov = df_prov.groupby(['provincia','month_and_year'],as_index = False).revenue.sum()
    df_prov.columns = ['Provincia','Fecha','Ingresos']
    fig = px.line(df_prov, x="Fecha", y="Ingresos", color="Provincia")
    fig.update_layout(yaxis_title="Ingresos (€)")
    st.plotly_chart(fig, theme="streamlit", use_container_width=True)
    
def display_bar_revenue(df, selected_provs):
    df_prov = df[df['provincia'].isin(selected_provs)]
    sales_by_prov = df_prov.groupby(['provincia','analytic_category'], as_index = False).revenue.sum().sort_values(by = 'revenue', ascending = False)
    sales_by_prov.columns = ['Provincia','Categoría','Ingresos']
    
    fig = px.bar(sales_by_prov, x='Ingresos', y='Provincia', color = 'Categoría', height=400)
    fig.update_layout(xaxis_title="Ingresos (€)", yaxis=dict(autorange="reversed"))
    fig.update_traces(hovertemplate= "<b>Ingresos: </b> %{x:.0f} €")
    st.plotly_chart(fig, theme="streamlit", use_container_width=True)


@st.cache_data
def read_datos():
    ventas = 'pages\\ventas_final.csv'
    ventas = pd.read_csv(ventas, encoding='utf-8')
    ventas['month_and_year'] = pd.to_datetime(ventas["created_at"]).dt.to_period('M').astype(str)
    return ventas

ventas = read_datos()
prov_list = list(ventas['provincia'][ventas['provincia'] != 'UNK'].unique())
prov_list = sorted(prov_list, key=collator.sort_key)

n = display_number_input()
k = 0
selected_provs = []
for i in range(n):
    prov_name = display_prov_filter(k, i+1)
    selected_provs.append(prov_name)
    k += 1

st.subheader('Productos vendidos') 
display_evol_sells(ventas, selected_provs)
display_bar_sells(ventas, selected_provs)

st.subheader('Ingresos generados') 
display_evol_revenue(ventas, selected_provs)
display_bar_revenue(ventas, selected_provs)
    
    
