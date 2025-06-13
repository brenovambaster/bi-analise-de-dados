import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

# Configuração da página
st.set_page_config(
    page_title="Dashboard E-commerce Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)


st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #1e3c72 0%, #2a5298 100%);
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        text-align: center;
        color: white;
    }
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        border-left: 4px solid #2a5298;
        margin-bottom: 1rem;
    }
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #f8f9fa 0%, #e9ecef 100%);
    }
    .stSelectbox > div > div {
        background-color: #f8f9fa;
    }
</style>
""", unsafe_allow_html=True)

# Função para carregar dados
@st.cache_data
def load_data():
    return pd.read_csv('dados_final.csv')

# Carregar dados
df = load_data()

# Header principal
st.markdown("""
<div class="main-header">
    <h1>📊 Dashboard E-commerce Analytics</h1>
    <p>Análise Completa de Performance de Vendas e Marketing</p>
</div>
""", unsafe_allow_html=True)

# Sidebar para filtros
st.sidebar.markdown("## 🔍 Filtros")
canal_filter = st.sidebar.multiselect(
    "Selecione os Canais:",
    options=df['canal_origem'].unique(),
    default=df['canal_origem'].unique()
)

categoria_filter = st.sidebar.multiselect(
    "Selecione as Categorias:",
    options=df['categoria_interesse'].unique(),
    default=df['categoria_interesse'].unique()
)

# Filtrar dados
df_filtered = df[
    (df['canal_origem'].isin(canal_filter)) &
    (df['categoria_interesse'].isin(categoria_filter))
]

# KPIs principais
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class="metric-card">
        <h3 style="color: #2a5298; margin: 0;">Taxa de Conversão</h3>
        <h2 style="margin: 0.5rem 0;">{:.1f}%</h2>
        <p style="color: #666; margin: 0;">Total de conversões</p>
    </div>
    """.format(df_filtered['realizou_compra'].mean() * 100), unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="metric-card">
        <h3 style="color: #2a5298; margin: 0;">Receita Total</h3>
        <h2 style="margin: 0.5rem 0;">R$ {:.0f}</h2>
        <p style="color: #666; margin: 0;">Valor total em vendas</p>
    </div>
    """.format(df_filtered['valor_compra'].sum()), unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="metric-card">
        <h3 style="color: #2a5298; margin: 0;">AOV Médio</h3>
        <h2 style="margin: 0.5rem 0;">R$ {:.0f}</h2>
        <p style="color: #666; margin: 0;">Ticket médio</p>
    </div>
    """.format(df_filtered[df_filtered['realizou_compra'] == 1]['valor_compra'].mean()), unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="metric-card">
        <h3 style="color: #2a5298; margin: 0;">Taxa de Abandono</h3>
        <h2 style="margin: 0.5rem 0;">{:.1f}%</h2>
        <p style="color: #666; margin: 0;">Carrinho abandonado</p>
    </div>
    """.format(df_filtered['abandonou_carrinho'].mean() * 100), unsafe_allow_html=True)

# Gráficos principais
st.markdown("---")

# 1. Taxa de Conclusão vs. Abandono por Canal de Marketing
col1, col2 = st.columns(2)

with col1:
    st.markdown("### 📈 Taxa de Conclusão vs. Abandono por Canal")
    
    # Lógica corrigida: Taxa de Conversão + Taxa de Não Conversão = 100%
    canal_stats = df_filtered.groupby('canal_origem').agg({
        'realizou_compra': ['sum', 'count']
    }).round(2)
    
    canal_stats.columns = ['Compras', 'Total']
    canal_stats['Taxa_Conversao'] = (canal_stats['Compras'] / canal_stats['Total'] * 100).round(1)
    canal_stats['Taxa_Nao_Conversao'] = (100 - canal_stats['Taxa_Conversao']).round(1)
    
    fig1 = go.Figure()
    fig1.add_trace(go.Bar(
        name='Taxa de Conversão',
        x=canal_stats.index,
        y=canal_stats['Taxa_Conversao'],
        marker_color='#2a5298',
        text=canal_stats['Taxa_Conversao'].astype(str) + '%',
        textposition='outside'
    ))
    fig1.add_trace(go.Bar(
        name='Taxa de Não Conversão',
        x=canal_stats.index,
        y=canal_stats['Taxa_Nao_Conversao'],
        marker_color='#e74c3c',
        text=canal_stats['Taxa_Nao_Conversao'].astype(str) + '%',
        textposition='outside'
    ))
    fig1.update_layout(
        barmode='group',
        height=400,
        showlegend=True,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        title="Conversão vs Não Conversão (Total = 100%)"
    )
    st.plotly_chart(fig1, use_container_width=True)


# 2. Receita Total por Canal de Marketing
with col2:
    st.markdown("### 💰 Receita Total por Canal")
    receita_canal = df_filtered.groupby('canal_origem')['valor_compra'].sum().sort_values(ascending=False)
    
    fig2 = px.bar(
        x=receita_canal.values,
        y=receita_canal.index,
        orientation='h',
        color=receita_canal.values,
        color_continuous_scale=['#b7e4c7', '#1b4332'],
        text=receita_canal.values.round(0)
    )
    fig2.update_traces(texttemplate='R$ %{text:.0f}', textposition='outside')
    fig2.update_layout(
        height=400,
        showlegend=False,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        coloraxis_showscale=False,
        xaxis_title="Receita (R$)",
        yaxis_title="Canal de Origem"
    )
    st.plotly_chart(fig2, use_container_width=True)

# Segunda linha de gráficos
col3, col4 = st.columns(2)

with col3:
    # 3. AOV por Canal de Origem
    st.markdown("### 🎯 AOV por Canal de Origem")
    aov_canal = df_filtered[df_filtered['realizou_compra'] == 1].groupby('canal_origem')['valor_compra'].mean().sort_values(ascending=False)
    
    fig3 = px.scatter(
        x=aov_canal.index,
        y=aov_canal.values,
        size=aov_canal.values,
        color=aov_canal.values,
        color_continuous_scale='Viridis',
        size_max=30
    )
    fig3.update_traces(
        text=aov_canal.values.round(0),
        textposition='top center'
    )
    fig3.update_layout(
        height=400,
        showlegend=False,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        coloraxis_showscale=False,
        xaxis_title="Canal de Origem",
        yaxis_title="Aov (R$)"
    )
    st.plotly_chart(fig3, use_container_width=True)

with col4:
    # 4. Distribuição de Clientes por Faixa de Valor
    st.markdown("### 📊 Distribuição por Faixa de Valor")
    faixa_dist = df_filtered[df_filtered['Faixa de Valor'] != 'N/A']['Faixa de Valor'].value_counts()
    
    fig4 = px.pie(
        values=faixa_dist.values,
        names=faixa_dist.index,
        color_discrete_sequence=['#2a5298', '#3498db', '#85c1e9']
    )
    fig4.update_traces(textposition='inside', textinfo='percent+label')
    fig4.update_layout(
        height=400,
        showlegend=True,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    st.plotly_chart(fig4, use_container_width=True)

# Terceira linha de gráficos
col5, col6 = st.columns(2)

with col5:
    # 5. Abandono de Carrinho por Categoria - Taxa Percentual
    st.markdown("### 🛒 Taxa de Abandono por Categoria")
    abandono_cat = df_filtered.groupby('categoria_interesse').agg({
        'abandonou_carrinho': ['sum', 'count']
    })
    abandono_cat.columns = ['Abandonos', 'Total']
    abandono_cat['Taxa_Abandono'] = (abandono_cat['Abandonos'] / abandono_cat['Total'] * 100).round(1)
    
    fig5 = px.bar(
        x=abandono_cat.index,
        y=abandono_cat['Taxa_Abandono'],
        color=abandono_cat['Taxa_Abandono'],
        color_continuous_scale='Reds',
        text=abandono_cat['Taxa_Abandono'].astype(str) + '%'
    )
    fig5.update_traces(textposition='outside')
    fig5.update_layout(
        height=400,
        showlegend=False,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        coloraxis_showscale=False,
        xaxis_title="Categoria de Interesse",
        yaxis_title="Taxa de Abandono (%)"
    )
    st.plotly_chart(fig5, use_container_width=True)

with col6:
    # 6. Gráfico adicional: Engajamento por Canal (Email)
    st.markdown("### 📧 Taxa de Engajamento por Canal")
    engagement = df_filtered.groupby('canal_origem').agg({
        'abriu_email': 'mean',
        'clicou_em_link': 'mean'
    }) * 100
    
    fig6 = go.Figure()
    fig6.add_trace(go.Scatter(
        x=engagement['abriu_email'],
        y=engagement['clicou_em_link'],
        mode='markers+text',
        marker=dict(size=15, color='#2a5298'),
        text=engagement.index,
        textposition='top center'
    ))
    fig6.update_layout(
        xaxis_title='Taxa de Abertura de Email (%)',
        yaxis_title='Taxa de Clique em Link (%)',
        height=400,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    st.plotly_chart(fig6, use_container_width=True)

# # Gráfico adicional 7: Análise Temporal (simulada)
# st.markdown("### 📅 Análise de Performance Temporal")
# dates = pd.date_range(start='2024-01-01', end='2024-12-31', freq='M')
# monthly_revenue = np.random.lognormal(10, 0.3, len(dates))
# monthly_conversions = np.random.poisson(50, len(dates))

# fig7 = make_subplots(specs=[[{"secondary_y": True}]])
# fig7.add_trace(
#     go.Scatter(x=dates, y=monthly_revenue, name="Receita Mensal", line=dict(color='#2a5298')),
#     secondary_y=False,
# )
# fig7.add_trace(
#     go.Scatter(x=dates, y=monthly_conversions, name="Conversões", line=dict(color='#e74c3c')),
#     secondary_y=True,
# )
# fig7.update_xaxes(title_text="Período")
# fig7.update_yaxes(title_text="Receita (R$)", secondary_y=False)
# fig7.update_yaxes(title_text="Número de Conversões", secondary_y=True)
# fig7.update_layout(
#     height=400,
#     plot_bgcolor='rgba(0,0,0,0)',
#     paper_bgcolor='rgba(0,0,0,0)'
# )
# st.plotly_chart(fig7, use_container_width=True)

# Tabela de dados
st.markdown("---")
st.markdown("### 📋 Dados Detalhados")
st.dataframe(
    df_filtered[['nome', 'canal_origem', 'categoria_interesse', 'Status da Compra', 'valor_compra', 'Faixa de Valor']],
    use_container_width=True,
    height=300
)

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #666;'>"
    "Dashboard desenvolvido para análise de performance de e-commerce | "
    "Dados atualizados automaticamente"
    "</div>",
    unsafe_allow_html=True
)