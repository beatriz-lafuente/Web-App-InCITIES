import pandas as pd
from sklearn.impute import KNNImputer
from sklearn.preprocessing import MinMaxScaler
import streamlit as st
import plotly.express as px
from scipy.stats import bartlett
from factor_analyzer import calculate_kmo
from sklearn.decomposition import PCA
import numpy as np
from streamlit_echarts import st_echarts
import warnings

warnings.filterwarnings("ignore", message="The inverse of the variance-covariance matrix was calculated using the Moore-Penrose generalized matrix inversion")


def replace_NaN_values(df):
    
    knn_imputer = KNNImputer(n_neighbors=3)
    
    for column in df.columns:
        for geo, group in df.groupby(level='geo'):
            
            column_data = group[[column]].values
            imputed_column = knn_imputer.fit_transform(column_data)
            df.loc[(geo, slice(None)), column] = imputed_column
    
    df_imputed = df
    
    return df_imputed

def normalize_data(df):

    scaler = MinMaxScaler()
    
    df_scaled = pd.DataFrame(
        scaler.fit_transform(df),
        columns=df.columns,
        index=df.index
    )
    
    return df_scaled


def corr_matrix_plot(correlation_matrix):
    
    fig = px.imshow(
        correlation_matrix, 
        text_auto=True, 
        color_continuous_scale='RdBu_r',
        aspect="auto", 
        labels={'color': 'Correlation'} 
    )
    fig.update_layout(
        title='Correlation Matrix',
        title_x=0.5,
        width=800, 
        height=600 
    )

    st.plotly_chart(fig, use_container_width=True)


def test_of_sphericity(df):

    chi_square_value, p_value = bartlett(*[df[col] for col in df.columns])
    
    result = {
    "Statistic": ["Chi-Square Value", "P-Value"],
    "Value": [chi_square_value, p_value]
    }
    result_df = pd.DataFrame(result)

    st.table(result_df)
    

def KMO_measure(df):
    
    correlation_matrix = df.corr()

    kmo_all, kmo_model = calculate_kmo(correlation_matrix)
    
    st.write(f"Overall KMO: {kmo_model:.4f}")

    kmo_indicators = pd.Series(kmo_all, index=df.columns)
    kmo_df = pd.DataFrame(kmo_indicators, columns=['KMO']).reset_index()
    kmo_df.columns = ['Indicator', 'KMO']
    
    st.write("KMO for each indicator:")
    st.table(kmo_df)
    

def principal_component_analysis(df):
    
    pca = PCA()
    pca.fit(df)

    eigenvalues = pca.explained_variance_
    explained_variance_ratio = pca.explained_variance_ratio_

    num_components = len(eigenvalues)
    
    results_df = pd.DataFrame({
        'Component': [f'PC{i+1}' for i in range(num_components)],
        'Eigenvalue': eigenvalues,
        'Proportion': explained_variance_ratio * 100,
    })
    results_df['Difference'] = results_df['Eigenvalue'].diff().fillna(0)
    results_df['Cumulative'] = results_df['Proportion'].cumsum()
    total_variance = np.sum(eigenvalues)
    results_df['PCw (%)'] = (results_df['Eigenvalue'] / total_variance) * 100
    results_df = results_df[['Component', 'Eigenvalue', 'Difference', 'Proportion', 'Cumulative', 'PCw (%)']]
    
    return results_df


def get_final_ranking(df, pca_result_df):
    
    pca = PCA()
    pca.fit(df)
    
    eigenvalues = pca.explained_variance_
    
    num_components = len(eigenvalues)
    
    factor_scores = np.dot(df.values, pca.components_.T)
    factor_scores_df = pd.DataFrame(factor_scores, index=df.index, columns=[f'PC{i+1}' for i in range(num_components)])

    weights = pca_result_df['PCw (%)'].values[:num_components] / 100
    final_scores = np.dot(factor_scores_df.values, weights)
    final_scores_df = pd.DataFrame(final_scores, index=df.index, columns=['Final Score'])

    final_scores_df['region'] = final_scores_df.index.get_level_values('geo')
    final_scores_df['year'] = final_scores_df.index.get_level_values('time')

    region_ranks = final_scores_df.groupby('region')['Final Score'].mean().reset_index()
    region_ranks['Rank'] = region_ranks['Final Score'].rank(ascending=False)
    region_ranks = region_ranks.sort_values('Rank')
    
    geo_name = {
        "DEA2": "Cologne",
        "FI1B": "Helsinki",
        "SK03": "Zilina",
        "PT17": "Lisbon",
        "FR10": "Paris"
    }
    region_ranks['region'] = region_ranks['region'].replace(geo_name)
    
    color_mapping = {
        "Cologne": "#6272A4",
        "Helsinki": "#8BE9FD",
        "Zilina": "#FFB86C",
        "Lisbon": "#FF79C6",
        "Paris": "#BD93F9"
    }
    
    xaxis_list = region_ranks['region'].tolist() 
    yaxis_list = region_ranks['Final Score'].tolist()
    colors = [color_mapping[region] for region in xaxis_list] 

    series_data = [{"value": y, "itemStyle": {"color": c}} for y, c in zip(yaxis_list, colors)]
    
    option = {
        "title": {"text": "Inclusive, Sustainable and Resilient Cities", "subtext": "Ranking"},
        "grid": {'top': '15%', 'right': '5%', 'bottom': '5%', 'left': '5%', 'containLabel': 'true'},
        "tooltip": {},
        "xAxis": {
            "type": 'category',
            "data": xaxis_list,
        },
        "yAxis": {
            "type": 'value'
        },
        "series": [
            {
                "data": series_data,
                "type": 'bar'
            }
        ]
    }
    
    st_echarts(options=option, height="500px")