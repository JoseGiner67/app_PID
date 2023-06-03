# -*- coding: utf-8 -*-
"""
Created on Mon May 29 09:35:55 2023

@author: Jose Giner
"""

import streamlit as st

st.set_page_config(
    page_title="Bienvenida",
    page_icon="👋",
)

st.write("# Atida Mifarma - Visualización")

st.sidebar.success("Elige la ventana a visualizar.")

st.markdown(
    """
    Atida | Mifarma es el ecommerce líder en España y Portugal en la venta de productos de parafarmacia y farmacia. 
    Con sede en Albacete y Madrid, más de 10 años de experiencia en el sector y un equipo de más de 120 profesionales, 
    ofrece una experiencia confiable y personalizada antes, durante y después de todo el proceso de compra. 
    La compañía ofrece un amplio catálogo de productos para el cuidado y bienestar a través de un servicio rápido 
    y personalizado respaldado por expertos farmacéuticos.

    En el año 2019 Mifarma se unió a Atida con el objetivo de convertirse en la mayor plataforma de salud holística online en Europa. 
    De este modo, trabajan día a día para construir un ecosistema online cuyo objetivo es transformar el panorama de salud y bienestar, 
    convirtiéndose en la farmacia online más grande de Europa y un lugar de referencia al que acudir en busca de información y consejo profesional.
    
    Esta aplicación contiene diversos gráficos exploratorios sobre los datos limpiados y anonimizados con la información de negocio del periodo transcurrido entre el 01/01/2017 y el 31/12/2018.
    
    ### Pestañas a visualizar
    - **Ventas por provincia**: Se ilustra un mapa de coropletas con la cantidad de productos vendidos por cada provincia en
    un periodo y categoría de producto seleccionado. Se muestran las unidades vendidas, ingresos y beneficios generados en la provincia seleccionada, 
    además de las marcas, productos y categorías secundarias más vendidas.  
    
    - **Estadísticas de categorías**: Se ilustran varios gráficos exploratorios con las ventas según las principales categorías de productos para una provincia
    a seleccionar (o todas ellas). También se puede cambiar el indicador a visualizar. 
    
    - **Comparador de provincias**: Se comparan los registros de hasta un máximo de 5 provincias.
    
    """
)