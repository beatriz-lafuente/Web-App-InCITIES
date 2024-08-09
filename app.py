import streamlit as st
from utils import *
from streamlit_option_menu import option_menu

st.set_page_config(layout="wide")

selected = option_menu(
  menu_title="InCITIES Dashboard",
  options=["Ranking", "Cities", "Inclusion", "Sustainability", "Resilience"],
  icons=["bar-chart", "buildings", "people", "globe-europe-africa", "hammer"],
  menu_icon="cast",
  orientation="horizontal",
)



if selected == "Inclusion":
  
  kpi_name = st.selectbox("Select KPI:", list(inclusion_kpis.keys()))
  dataset_code = inclusion_kpis[kpi_name]
  
  col1, col2 = st.columns(2)
  with col1:
    echarts_option('dash1_line_chart', dataset_code)
  with col2:
    echarts_option('dash1_bar_chart_ranking', dataset_code)
  
  with col1:
    scatter_plot_gini_vs_poverty()
  with col2:
    lev_limit_list = {'Severe': 'SEV', 'Some': 'SOME'}
    lev_limit_name = st.selectbox("Select activity limitation level:", list(lev_limit_list.keys()))
    lev_limit = lev_limit_list[lev_limit_name]
    echarts_option_kpi('disability_employment_gap_by_sex', 'tepsr_sp200', 'lev_limit', lev_limit)
  


col1, col2, col3 = st.columns(3)
with col1:
  domain = st.selectbox("Select domain:", domains_list)
with col2:
  if domain == "Inclusion":
    chart = st.selectbox("Select type of chart:", chart_list)
  elif domain == "Sustainability":
    sub_domain = st.selectbox("Select sub-domain:", sustainability_list)
  else:
    sub_domain = st.selectbox("Select sub-domain:", resilience_list)
with col3:
  if domain == "Inclusion":
    kpi_name = st.selectbox("Select KPI:", list(dash1_social_kpis.keys()))
    dataset_code = dash1_social_kpis[kpi_name]
  if domain == "Sustainability":
    if sub_domain == "Air Quality":
      kpi_name = st.selectbox("Select KPI:", list(dash2_air_quality_kpis.keys()))
      dataset_code = dash2_air_quality_kpis[kpi_name]      
    if sub_domain == "Energy":
      kpi_name = st.selectbox("Select KPI:", list(dash2_energy_kpis.keys()))
      dataset_code = dash2_energy_kpis[kpi_name]
  if domain == "Resilience":
    if sub_domain == "Social":
      kpi_name = st.selectbox("Select KPI:", list(dash3_social_kpis.keys()))
      dataset_code = dash3_social_kpis[kpi_name]



col1, col2 = st.columns(2)

if domain == "Inclusion":
  col1, col2, col3 = st.columns([2, 6, 2])
  with col2:
    if chart == "Line":
      chart_1 = echarts_option('dash1_inclusion_q11', dataset_code)
    else:
      chart_2 = echarts_option('dash1_inclusion_q12', dataset_code)

if domain == "Sustainability":
  if sub_domain == "Air Quality":
    with col1:
      echarts_option_dash2_q11('dash2_q11', dataset_code)
    with col2:
      echarts_option_dash2_q12('dash2_q12', dataset_code)
  
  if sub_domain == "Clean City":
    col1, col2, col3 = st.columns([2, 6, 2])
    with col1:
      cities_dict = {
        "Helsinki": "FI001C", 
        "Lisbon": "PT001C", 
        "Paris": "FR001C",
      }
      cities_name = st.selectbox('Filter by city:', list(cities_dict.keys()))
      city = cities_dict[cities_name]
    with col2:
      echarts_option_city('dash2_q21', 'urb_percep', city)
    
  if sub_domain == "Energy":
    with col1:
      echarts_option_kpi('dash2_q22', 'sdg_07_40', 'nrg_bal', dataset_code)
    with col2:
      echarts_option_dash2_q31('dash2_q31', dataset_code)
 
if domain == "Resilience":
  if sub_domain == "Social":
    with col1:
      echarts_option_dash3_chart_1(dataset_code)
    with col2:
      echarts_option_dash3_chart2()
      
