# -*- coding: utf-8 -*-
"""
Created on Sun May 28 11:03:55 2023

@author: Jose Giner
"""

import pandas as pd
import locale
from pyuca import Collator
import streamlit as st
import plotly.express as px

st.set_page_config(page_title="Estadísticas de las categorias", page_icon="📊")

locale.setlocale(locale.LC_ALL, 'es_ES.UTF-8')
# Crea un objeto Unicode Collation Algorithm (UCA)
collator = Collator()


def display_prov_filter(df):
    return st.sidebar.selectbox('Provincia', prov_list)

def display_metric_filter(df):
    metric_list = ['Unidades vendidas','Ingresos','Beneficios']
    metric = st.sidebar.radio('Indicador', metric_list)
    return metric

def display_barchart(df,prov_name,metric):
    if prov_name != 'todas las provincias':
        df = df[df['provincia'] == prov_name]
    if metric == 'Unidades vendidas':
        df_cat = df.groupby('analytic_category',as_index = False).qty_ordered.sum().sort_values(by = 'qty_ordered', ascending = False)
        fig = px.bar(df_cat, x='analytic_category', y='qty_ordered', 
                     height=400)
        fig.update_layout(xaxis_title="Categoría", yaxis_title="Unidades vendidas")
        fig.update_traces(marker_color='blue', hovertemplate= "<b>Unidades vendidas: </b> %{y:.0f}")
        st.plotly_chart(fig, theme="streamlit", use_container_width=True)
    
    if metric == 'Ingresos':
        df_cat = df.groupby('analytic_category',as_index = False).revenue.sum().sort_values(by = 'revenue', ascending = False)
        fig = px.bar(df_cat, x='analytic_category', y='revenue', 
                     height=400)
        fig.update_layout(xaxis_title="Categoría", yaxis_title="Ingresos (€)")
        fig.update_traces(marker_color='blue', hovertemplate= "<b>Ingresos: </b> %{y:.2f} €")
        st.plotly_chart(fig, theme="streamlit", use_container_width=True)
    
    if metric == 'Beneficios':
        df_cat = df.groupby('analytic_category',as_index = False).profit.sum().round(2).sort_values(by = 'profit', ascending = False)
        fig = px.bar(df_cat, x='analytic_category', y='profit', 
                     height=400)
        fig.update_layout(xaxis_title="Categoría", yaxis_title="Beneficio (€)")
        fig.update_traces(marker_color='blue', hovertemplate= "<b>Beneficio: </b> %{y:.2f} €")
        st.plotly_chart(fig, theme="streamlit", use_container_width=True)
        
def display_piechart(df,prov_name,metric):
    if prov_name != 'todas las provincias':
        df = df[df['provincia'] == prov_name]
    if metric == 'Unidades vendidas':
        df_cat = df.groupby('analytic_category',as_index = False).qty_ordered.sum().sort_values(by = 'qty_ordered', ascending = False)
        fig = px.pie(df_cat, names='analytic_category', values='qty_ordered')
        fig.update_traces(hovertemplate= "<b>%{label}<br>Unidades vendidas: %{value}</b>")
        st.plotly_chart(fig, theme="streamlit", use_container_width=True)
    
    if metric == 'Ingresos':
        df_cat = df.groupby('analytic_category',as_index = False).revenue.sum().sort_values(by = 'revenue', ascending = False)
        fig = px.pie(df_cat, names='analytic_category', values='revenue')
        fig.update_traces(hovertemplate= "<b>%{label}<br>Ingresos: %{value} €</b>")
        st.plotly_chart(fig, theme="streamlit", use_container_width=True)
    
    if metric == 'Beneficios':
        df_cat = df.groupby('analytic_category',as_index = False).profit.sum().round(2).sort_values(by = 'profit', ascending = False)
        fig = px.pie(df_cat, names='analytic_category', values='profit')
        fig.update_traces(hovertemplate= "<b>%{label}<br>Beneficio: %{value} €</b>")
        st.plotly_chart(fig, theme="streamlit", use_container_width=True)
    

def display_lineplot(df,prov_name,metric):
    if prov_name != 'todas las provincias':
        df = df[df['provincia'] == prov_name]
    df['month_and_year'] = pd.to_datetime(df["created_at"]).dt.to_period('M').astype(str)
    if metric == 'Unidades vendidas':
        df_cat = df.groupby(['analytic_category','month_and_year'],as_index = False).qty_ordered.sum()
        df_cat.columns = ['Categoría','Fecha','Unidades vendidas']
        fig = px.line(df_cat, x="Fecha", y="Unidades vendidas", color="Categoría")
        fig.update_layout(hovermode="x unified")
        st.plotly_chart(fig, theme="streamlit", use_container_width=True)
    
    if metric == 'Ingresos':
        df_cat = df.groupby(['analytic_category','month_and_year'],as_index = False).revenue.sum()
        df_cat.columns = ['Categoría','Fecha','Ingresos (€)']
        fig = px.line(df_cat, x="Fecha", y="Ingresos (€)", color="Categoría")
        fig.update_layout(hovermode="x unified")
        st.plotly_chart(fig, theme="streamlit", use_container_width=True)
    
    if metric == 'Beneficios':
        df_cat = df.groupby(['analytic_category','month_and_year'],as_index = False).profit.sum()
        df_cat.columns = ['Categoría','Fecha','Beneficios (€)']
        fig = px.line(df_cat, x="Fecha", y="Beneficios (€)", color="Categoría")
        fig.update_layout(hovermode="x unified")
        st.plotly_chart(fig, theme="streamlit", use_container_width=True)
    

@st.cache_data
def read_datos():
    ventas = 'pages/ventas_final.csv'
    ventas = pd.read_csv(ventas, encoding='utf-8')
    return ventas

ventas = read_datos()
prov_list = list(ventas['provincia'][ventas['provincia'] != 'UNK'].unique())
prov_list = sorted(prov_list, key=collator.sort_key) + ['todas las provincias']

prov_name = display_prov_filter(ventas)
metric = display_metric_filter(ventas)

st.header('Estadísticas de las categorías analíticas según la provincia' )

st.subheader(f'Ventas en {prov_name}')   
display_barchart(ventas, prov_name, metric)

st.subheader(f'Distribución de {metric.lower()} en {prov_name}')  
display_piechart(ventas,prov_name,metric)

st.subheader(f'{metric} mensuales en {prov_name}')  
display_lineplot(ventas,prov_name,metric)

