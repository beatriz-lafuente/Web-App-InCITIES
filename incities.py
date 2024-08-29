import streamlit as st
from streamlit_option_menu import option_menu
from utils2 import *
import plotly.express as px
import pandas as pd
import os
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(page_title="InCITIES Dashboard", page_icon=":cityscape:", layout="wide")

st.title(":cityscape: InCITIES Dashboard")
st.markdown('<style>div.block-container{padding-top:1rem;}</style>',unsafe_allow_html=True)

# Create Menu side bar
with st.sidebar:
    menu = option_menu(
    menu_title="Menu",
    options=["Data Visualizations", "Cities Ranking", "Indicators Check List"],
    icons=["bar-chart", "buildings", "list-check"],
    menu_icon="cast"
    )

if menu == "Data Visualizations":
    st.sidebar.header("Choose your filter")
    # Create filter by Domain
    domain = st.sidebar.selectbox("Select domain:", domain_list)

    # Create filter by KPI
    if domain == "Inclusion": 
        sub_domain = st.sidebar.selectbox("Select sub-domain:", sub_domain_inclusion)
        if sub_domain == "Economic":
            kpi = st.sidebar.selectbox("Select KPI:", list(economic_inclusion_kpis.keys()))
            dataset_code = economic_inclusion_kpis[kpi]
            
        elif sub_domain == "Social":
            kpi = st.sidebar.selectbox("Select KPI:", list(social_inclusion_kpis.keys()))
            dataset_code = social_inclusion_kpis[kpi]
        else:
            kpi = st.sidebar.selectbox("Select KPI:", list(gender_inclusion_kpis.keys()))
            dataset_code = gender_inclusion_kpis[kpi]
    
    elif domain == "Sustainability":
        kpi = st.sidebar.selectbox("Select KPI:", sustainability_kpis)
    else:
        kpi = st.sidebar.selectbox("Select KPI:", resilience_kpis)

# Add visualizations by KPI
if domain == "Inclusion":
    col1, col2, col3 = st.columns(3)
    with col1:
        chart_list = ["Line Chart", "Map", "Bar Chart"]
        chart = st.selectbox("Choose type of chart:", chart_list)
    if chart == "Line Chart":
        echarts_option('line_chart_inclusion_kpis', dataset_code)
    if chart == "Map":
        plotly_chart('cloropleth_map_inclusion', dataset_code)