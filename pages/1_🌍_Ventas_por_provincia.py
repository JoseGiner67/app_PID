# -*- coding: utf-8 -*-
"""
Created on Thu May 25 12:41:38 2023

@author: Jose Giner
"""
import pandas as pd
import streamlit as st
import numpy as np
import folium
from streamlit_folium import st_folium
import locale
from pyuca import Collator
import plotly.express as px

st.set_page_config(page_title="Ventas por provincia", page_icon="🌍")

# Establece la configuración regional para el español
locale.setlocale(locale.LC_ALL, 'es_ES.UTF-8')
# Crea un objeto Unicode Collation Algorithm (UCA)
collator = Collator()


def display_time_filters(df):
    year_list = list(df['year'].unique())
    year_list.sort()
    year = st.sidebar.radio('Año', year_list + ['todos'])
    month_list = ['enero','febrero','marzo','abril','mayo','junio','julio','agosto','septiembre','octubre','noviembre','diciembre','todos los meses']
    month = st.sidebar.selectbox('Mes', month_list)
    return year, month

def display_cat_filter(df):
    category_list = list(df['analytic_category'][df['analytic_category'].notnull()].unique())
    category_list = sorted(category_list, key=collator.sort_key)
    category = st.sidebar.selectbox('Categoría de producto', category_list)
    return category

def display_prov_filter(df):
    return st.sidebar.selectbox('Provincia', prov_list)

def display_map(df, year, month, cat):
    if month != 'todos los meses' and year != 'todos':
        ventas_por_prov = df[(df['year'] == year) & (df['month'] == month) & (df['analytic_category'] == cat)].groupby(['cod_provincia'], as_index = False).qty_ordered.sum()
    
    elif month != 'todos los meses' and year == 'todos':
        ventas_por_prov = df[(df['month'] == month) & (df['analytic_category'] == cat)].groupby(['cod_provincia'], as_index = False).qty_ordered.sum()
     
    elif month == 'todos los meses' and year != 'todos':
        ventas_por_prov = df[(df['year'] == year) & (df['analytic_category'] == cat)].groupby(['cod_provincia'], as_index = False).qty_ordered.sum()
    
    else:
        ventas_por_prov = df[df['analytic_category'] == cat].groupby(['cod_provincia'], as_index = False).qty_ordered.sum()
    ventas_por_prov.columns = ['cod_provincia','qty_ordered']
    m = folium.Map(location=[40.42,  -3.7], zoom_start=5, min_zoom = 4, max_zoom = 10, min_lat= 30, max_lat = 50, min_lon= -10, max_lon=10)
    coropletas = folium.Choropleth(geo_data=prov_geo,name="choropleth",data=ventas_por_prov,columns=["cod_provincia", "qty_ordered"],key_on="properties.codigo", fill_color='YlGnBu',fill_opacity=0.7,line_opacity=1.0,legend_name="Unidades vendidas")
    coropletas.add_to(m)
    for feature in coropletas.geojson.data['features']:
       code = feature['properties']['codigo']
       feature['properties']['Provincia'] = prov_dict[code]
    
    coropletas.geojson.add_child(folium.features.GeoJsonTooltip(['Provincia'], labels=False)) 
    return st_folium(m, width=700, height=450)
    

def display_datos_ventas(df, year, month, cat, prov_name, metric):
    if month != 'todos los meses' and year != 'todos':
        df = df[(df['year'] == year) & (df['month'] == month) & (df['analytic_category'] == cat) & (df['provincia'] == prov_name)]    
    
    elif month != 'todos los meses' and year == 'todos':
        df = df[(df['month'] == month) & (df['analytic_category'] == cat) & (df['provincia'] == prov_name)]
    
    elif month == 'todos los meses' and year != 'todos':
        df = df[(df['year'] == year) & (df['analytic_category'] == cat) & (df['provincia'] == prov_name)]
    
    else:
        df = df[(df['analytic_category'] == cat) & (df['provincia'] == prov_name)]
        
    if metric == 'Unidades vendidas':
        st.metric(metric, str(round(df.qty_ordered.sum())))
    
    if metric == 'Ingresos':
        st.metric(metric, str(round(df.revenue.sum(),2)) + ' €')
    
    if metric == 'Beneficio':
        st.metric(metric, str(round(df.profit.sum(),2)) + ' €')
        
def display_bars_brand(df, year, month, prov_name, cat):
    if month != 'todos los meses' and year != 'todos':
        df = df[(df['year'] == year) & (df['month'] == month) & (df['analytic_category'] == cat) & (df['provincia'] == prov_name)]    
    
    elif month != 'todos los meses' and year == 'todos':
        df = df[(df['month'] == month) & (df['analytic_category'] == cat) & (df['provincia'] == prov_name)]
    
    elif month == 'todos los meses' and year != 'todos':
        df = df[(df['year'] == year) & (df['analytic_category'] == cat) & (df['provincia'] == prov_name)]
    
    else:
        df = df[(df['analytic_category'] == cat) & (df['provincia'] == prov_name)]
        
    sales_by_brand = df.groupby('marca_value', as_index = False).qty_ordered.sum().sort_values(by = 'qty_ordered', ascending = False)
    sales_by_brand.columns = ['Marca','Unidades vendidas']
    top_sales = sales_by_brand[:10]
    
    fig = px.bar(top_sales, x='Unidades vendidas', y='Marca', 
                 height=400)
    fig.update_layout(yaxis=dict(autorange="reversed"))
    fig.update_traces(marker_color='blue', hovertemplate= "<b>Unidades vendidas: </b> %{x}")
    st.plotly_chart(fig, theme="streamlit", use_container_width=True)


def display_bars_prodname(df, year, month, prov_name, cat):
    if month != 'todos los meses' and year != 'todos':
        df = df[(df['year'] == year) & (df['month'] == month) & (df['analytic_category'] == cat) & (df['provincia'] == prov_name)]    
    
    elif month != 'todos los meses' and year == 'todos':
        df = df[(df['month'] == month) & (df['analytic_category'] == cat) & (df['provincia'] == prov_name)]
    
    elif month == 'todos los meses' and year != 'todos':
        df = df[(df['year'] == year) & (df['analytic_category'] == cat) & (df['provincia'] == prov_name)]
    
    else:
        df = df[(df['analytic_category'] == cat) & (df['provincia'] == prov_name)]
    
    sales_by_productname = df.groupby('name', as_index = False).qty_ordered.sum().sort_values(by = 'qty_ordered', ascending = False)
    sales_by_productname.columns = ['Producto','Unidades vendidas']
    top_sales = sales_by_productname[:10]
    
    fig = px.bar(top_sales, x='Unidades vendidas', y='Producto', 
                 height=400)
    fig.update_layout(yaxis=dict(autorange="reversed"))
    fig.update_traces(marker_color='blue', hovertemplate= "<b>Unidades vendidas: </b> %{x}")
    st.plotly_chart(fig, theme="streamlit", use_container_width=True)
    
    
def display_bars_secondary_category(df, year, month, prov_name, cat):
    if month != 'todos los meses' and year != 'todos':
        df = df[(df['year'] == year) & (df['month'] == month) & (df['analytic_category'] == cat) & (df['provincia'] == prov_name)]    
    
    elif month != 'todos los meses' and year == 'todos':
        df = df[(df['month'] == month) & (df['analytic_category'] == cat) & (df['provincia'] == prov_name)]
    
    elif month == 'todos los meses' and year != 'todos':
        df = df[(df['year'] == year) & (df['analytic_category'] == cat) & (df['provincia'] == prov_name)]
    
    else:
        df = df[(df['analytic_category'] == cat) & (df['provincia'] == prov_name)]
        
    sales_by_secondarycat = df.groupby('cat2', as_index = False).qty_ordered.sum().sort_values(by = 'qty_ordered', ascending = False)
    sales_by_secondarycat.columns = ['Categoría secundaria','Unidades vendidas']
    top_sales = sales_by_secondarycat[:10]
    
    fig = px.bar(top_sales, x='Unidades vendidas', y='Categoría secundaria', 
                 height=400)
    fig.update_layout(yaxis=dict(autorange="reversed"))
    fig.update_traces(marker_color='blue', hovertemplate= "<b>Unidades vendidas: </b> %{x}")
    st.plotly_chart(fig, theme="streamlit", use_container_width=True)
    

@st.cache_data
def read_datos():
    ventas = 'pages/ventas_final.csv'
    ventas = pd.read_csv(ventas, encoding='utf-8')
    return ventas
    

prov_geo = 'pages/provincias.geojson'
ventas = read_datos()
ventas['cod_provincia'] = ventas['cod_provincia'].astype(str)

prov_list = list(ventas['provincia'][ventas['provincia'] != 'UNK'].unique())
prov_list = sorted(prov_list, key=collator.sort_key)

prov_dict = pd.Series(ventas.provincia.values,index=ventas.cod_provincia).to_dict()

cat = display_cat_filter(ventas)
year, month = display_time_filters(ventas)
prov_name = display_prov_filter(ventas)

if month != 'todos los meses' and year != 'todos':
    st.header(f'Ventas de productos de {cat} en {month} de {year}' )
elif month != 'todos los meses' and year == 'todos':
    st.header(f'Ventas de productos de {cat} en {month}' )
elif month == 'todos los meses' and year != 'todos':
    st.header(f'Ventas de productos de {cat} en {year}' )
else:
    st.header(f'Ventas de productos de {cat}' )
    

display_map(ventas, year, month, cat)
  
st.subheader(f'Datos de ventas en {prov_name}')    

col1, col2, col3 = st.columns(3)
with col1:
    display_datos_ventas(ventas, year, month, cat, prov_name, 'Unidades vendidas')
with col2:
    display_datos_ventas(ventas, year, month, cat, prov_name, 'Ingresos')
with col3:
    display_datos_ventas(ventas, year, month, cat, prov_name, 'Beneficio')

st.subheader(f'Marcas más vendidas: {prov_name}')   
display_bars_brand(ventas, year, month, prov_name, cat)

st.subheader(f'Productos más vendidos: {prov_name}')   
display_bars_prodname(ventas, year, month, prov_name, cat)

st.subheader(f'Categorías secundarias más vendidas: {prov_name}')   
display_bars_secondary_category(ventas, year, month, prov_name, cat)


