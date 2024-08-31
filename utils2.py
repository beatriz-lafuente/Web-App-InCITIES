import requests
import streamlit as st
import plotly.io as pio
from streamlit_echarts import st_echarts


# Define domains
domain_list = ["Inclusion", "Sustainability", "Resilience"]

# Define sub-domains
sub_domain_inclusion = ["Social", "Economic", "Gender"]

sub_domain_sustainability = ["Environmental", "Social", "Economic"]

sub_domain_resilience = ["Social", "Economic", "Infrastructure", "Institutional", "Hazard"]

# Define regions
nat_dict = {
    "Finland": "FI",
    "Portugal": "PT",
    "Slovakia": "SK", 
    "France": "FR", 
    "Germany": "DE"
}

# Define sub-domain KPIs
inclusion_kpis = {
    "Gini coefficient": "tessi190", 
    "Poverty Rate": "ilc_li41",
    "Persons employed in productive age": "tgs00007",
    "Youth Unemployment": "edat_lfse_22", 
    "Slum Household": "ilc_lvhl21n", 
    "Disability employment gap": "tepsr_sp200", 
    "Voter turnout": "",
    "Gender employment gap": "tepsr_lm220", 
    "Equitable School Enrolment": "educ_uoe_enra11"
}

sustainability_topics = ["Air Quality", "Energy", "Biodiversity", "Waste Management"]

air_quality_kpis = {
    "Concentration of NO2 (µg/m³)": "no2", 
    "Concentration of PM10 (µg/m³)": "pm10",
    "Concentration of PM2.5 (µg/m³)": "pm25",
}

energy_kpis = {
    "Renewable energy sources in transport": "REN_TRA",
    "Renewable energy sources in electricity": "REN_ELC",
    "Renewable energy sources in heating and cooling": "REN_HEAT_CL",
}

resilience_kpis = [""]

# Functions to display data visualizations
def echarts_option(echarts_function, key_name, kpi):
    
    response = requests.get(f'http://localhost:8000/data_charts/{echarts_function}/?{key_name}={kpi}')
    chart_option = response.json()
    st_echarts(options=chart_option, height="500px")


def echarts_option_without_kpi(echarts_function):
    
    response = requests.get(f'http://localhost:8000/data_charts/{echarts_function}/')
    chart_option = response.json()
    st_echarts(options=chart_option, height="500px")
    

def echarts_option_kpi(echarts_function, dataset_code, col_kpi, kpi):
    response = requests.get(f"http://localhost:8000/data_charts/{echarts_function}/?dataset_code={dataset_code}&{col_kpi}={kpi}")
    chart_option = response.json()
    st_echarts(options=chart_option, height="500px")


def plotly_chart(plotly_chart, key_name, kpi):
    
    response = requests.get(f'http://localhost:8000/data_charts/{plotly_chart}/?{key_name}={kpi}')
    fig_json = response.json()
    fig = pio.from_json(fig_json)
    st.plotly_chart(fig)


def plotly_chart_without_kpi(plotly_chart):
    
    response = requests.get(f'http://localhost:8000/data_charts/{plotly_chart}/')
    fig_json = response.json()
    fig = pio.from_json(fig_json)
    st.plotly_chart(fig)
    
    
def plotly_chart_cards(plotly_chart, key_name, kpi):

    response = requests.get(f'http://localhost:8000/data_charts/{plotly_chart}/?{key_name}={kpi}')
    figures_json = response.json()
    figures = [pio.from_json(fig_json) for fig_json in figures_json]
    return figures