import requests
import streamlit as st
from streamlit_echarts import st_echarts


# Domain list
domains_list = ["Inclusion", "Sustainability", "Resilience"]

# Sub domain list
inclusion_list = ["Social"]
sustainability_list = ["Air Quality", "Clean City", "Energy"]
resilience_list = ["Social", "Economic & Infrastructure"]

# KPIs
# --> Inclusion
dash1_social_kpis = {
  "Gini coefficient": "tessi190",
  "Disability employment gap": "tepsr_sp200",
  "People at risk of poverty": "tepsr_lm410",
  "Gender employment gap": "tepsr_lm220"
}
# --> Sustainability
dash2_air_quality_kpis = {
  "Greenhouse gases emissions": "cei_gsr011",
  "Average CO2 emissions": "sdg_12_30",
  'Annual average concentration of NO2': "EN2026V",
  'Annual average concentration of PM10': "EN2027V",
  'Accumulated ozone concentration': "EN2025V"
}
dash2_energy_kpis = {
    "Renewable energy sources": "REN",
    "Renewable energy sources in transport": "REN_TRA",
    "Renewable energy sources in electricity": "REN_ELC",
    "Renewable energy sources in heating and cooling": "REN_HEAT_CL",
}
# --> Resilience
dash3_social_kpis = {
    "Total Population on 1 January": "Total",
    "Proportion of population aged over 65": "Aged",
    "Tertiary educational attainment": "tgs00109",
    "Low work intensity households": "tgs00108"
}

# National dictionary
geo_dict = {
        "Finland": "FI",
        "Portugal": "PT",
        "Slovakia": "SK", 
        "France": "FR", 
        "Germany": "DE"
      }

# Nuts3 dictionary
cities_dict = {
      "Helsinki": "FI001C", 
      "Lisbon": "PT001C", 
      "Paris": "FR001C",
      "Köln": "DE004C",
      "Zilina": "SK006C"
    }

# Years list
year_list = [2023, 2022, 2021, 2020, 2019, 2018, 2017, 2016, 2015, 2014]

# Chart List
chart_list = ["Line", "Heatmap"]


# Functions to display echarts visualizations

# --> General chart functions
def echarts_option(echarts_function, kpi):
    response = requests.get(f'http://localhost:8000/data_charts/{echarts_function}/?dataset_code={kpi}')
    chart_option = response.json()
    st_echarts(options=chart_option, height="400px", width="800px")


def echarts_option_city(echarts_function, kpi, city):
    response = requests.get(f'http://localhost:8000/data_charts/{echarts_function}/?dataset_code={kpi}&city={city}')
    chart_option = response.json()
    st_echarts(options=chart_option, height="500px")


def echarts_option_kpi(echarts_function, dataset_code, col_kpi, kpi):
    response = requests.get(f"http://localhost:8000/data_charts/{echarts_function}/?dataset_code={dataset_code}&{col_kpi}={kpi}")
    chart_option = response.json()
    st_echarts(options=chart_option, height="500px")


# --> Specific chart functions
def echarts_option_dash2_q11(echarts_function, kpi): 
    year_filter_list = [5, 10, 15]
    year_filter = st.selectbox('Filter by years to display:', year_filter_list)
    
    if kpi in ["cei_gsr011", "sdg_12_30"]:
        response = requests.get(f'http://localhost:8000/data_charts/{echarts_function}/?dataset_code={kpi}&year_filter={year_filter}')
    if kpi in ["EN2026V", "EN2027V", "EN2025V"]:
        response = requests.get(f'http://localhost:8000/data_charts/{echarts_function}/?dataset_code=urb_cenv&indic_ur={kpi}&year_filter={year_filter}')

    chart_option = response.json()
    st_echarts(options=chart_option, height="400px", width="700px")


def echarts_option_dash2_q12(echarts_function, kpi):
    if kpi in ["cei_gsr011", "sdg_12_30"]:
        get_years = requests.get(f"http://localhost:8000/data_charts/get_available_years/?dataset_code={kpi}&geo=nat")
        years_list = get_years.json()
    if kpi in ["EN2026V", "EN2027V", "EN2025V"]:
        get_years = requests.get(f"http://localhost:8000/data_charts/get_available_years/?dataset_code=urb_cenv&indic_ur={kpi}&geo=nuts3")
        years_list = get_years.json()
     
    col1, col2 = st.columns(2)
    with col1:
        year1 = st.selectbox('Select year 1:', years_list)
    with col2:
        year2 = st.selectbox('Select year 2:', years_list)
    
    if kpi in ["cei_gsr011", "sdg_12_30"]:  
        response = requests.get(f'http://localhost:8000/data_charts/{echarts_function}/?dataset_code={kpi}&year1={year1}&year2={year2}')
    if kpi in ["EN2026V", "EN2027V", "EN2025V"]:
        response = requests.get(f'http://localhost:8000/data_charts/{echarts_function}/?dataset_code=urb_cenv&indic_ur={kpi}&year1={year1}&year2={year2}')

    chart_option = response.json()
    st_echarts(options=chart_option, height="400px", width="700px")
    
    
def echarts_option_dash2_q31(echarts_function, kpi):
    get_years = requests.get(f"http://localhost:8000/data_charts/get_available_years/?dataset_code=sdg_07_40&indic_ur={kpi}&geo=nat")
    years_list = get_years.json()
    
    col1, col2 = st.columns(2)
    with col1:
        geo_name = st.selectbox('Filter by geo:', list(geo_dict.keys()))
        geo = geo_dict[geo_name]
    with col2:
        year = st.selectbox('Filter by year:', years_list)
    
    response = requests.get(f"http://localhost:8000/data_charts/{echarts_function}/?dataset_code=sdg_07_40&nrg_bal={kpi}&geo={geo}&year={year}")
    chart_option = response.json()
    st_echarts(options=chart_option, height="500px")


def echarts_option_dash3_chart_1(kpi):
    
    if kpi in ["tgs00109", "tgs00108"]:
        response = requests.get(f"http://localhost:8000/data_charts/dash3_chart_1/?dataset_code={kpi}")
        chart_option = response.json()
    if kpi in ["Total", "Aged"]:
        response = requests.get(f"http://localhost:8000/data_charts/dash3_chart_1/?dataset_code=demo_r_pjangrp3&ind={kpi}")
        chart_option = response.json()
        
    st_echarts(options=chart_option, height="500px")
    

def echarts_option_dash3_chart2():
    
    get_years = requests.get(f"http://localhost:8000/data_charts/get_available_years/?dataset_code=demo_r_pjangrp3&geo=nuts2_1")
    years_list = get_years.json()
    
    year = st.selectbox('Filter by year:', years_list)
    
    response = requests.get(f"http://localhost:8000/data_charts/dash3_chart_2/?dataset_code=demo_r_pjangrp3&year={year}")
    chart_option = response.json()
    st_echarts(options=chart_option, height="500px")