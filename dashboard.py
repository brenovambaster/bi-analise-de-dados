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

def formatar_moeda_br(valor):
    return f"R$ {valor:,.0f}".replace(',', '.')


# CSS personalizado para cards e layout com maior contraste
st.markdown("""
<style>
    /* Força o fundo da aplicação */
    .stApp {
        background: #f0f2f6 !important;
    }
    
    .main-header {
        background: linear-gradient(90deg, #257685 0%, #19c3cc 100%) !important;
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        text-align: center;
        color: white;
        box-shadow: 0 8px 32px rgba(42, 82, 152, 0.3) !important;
        border: 2px solid rgba(255, 255, 255, 0.1);
    }
    
    .metric-card {
        background: #ffffff !important;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 8px 25px rgba(0,0,0,0.15) !important;
        border: 2px solid #e3e8ef !important;
        margin-bottom: 1rem;
        transition: all 0.3s ease;
        position: relative;
        border: 1.5px solid #d1d5db !important; /* Borda bem fina em cinza claro */
            
    }
    
    .metric-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 12px 35px rgba(42, 82, 152, 0.2) !important;
        border-color: #257685 !important;
    }
        
    /* Estiliza todos os containers de gráficos */
    .element-container:has(.stPlotlyChart) {
        background: #ffffff !important;
        padding: 1.5rem !important;
        border-radius: 12px !important;
        box-shadow: 0 8px 25px rgba(0,0,0,0.15) !important;
        border: 1.5px solid #d1d5db !important; /* Borda bem fina em cinza claro */
        margin-bottom: 1.5rem !important;
        transition: all 0.3s ease !important;
    }
    .element-container:has(.stPlotlyChart):hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 12px 35px rgba(42, 82, 152, 0.15) !important;
        border-color: #a8c0e0 !important;
    }
    
    /* Estiliza os containers que têm dataframe */
    .element-container:has(.stDataFrame) {
        background: #ffffff !important;
        padding: 1.5rem !important;
        border-radius: 12px !important;
        box-shadow: 0 8px 25px rgba(0,0,0,0.15) !important;
        border: 2px solid #e3e8ef !important;
        margin-top: 2rem !important;
        border: 1.5px solid #d1d5db !important; /* Borda bem fina em cinza claro */
    }
    
    /* Estiliza títulos dos gráficos - REMOVIDA A LINHA AZUL */
    .chart-title {
        font-size: 1.2rem !important;
        font-weight: 600 !important;
        color: #0A4D68 !important;
        margin-bottom: 1rem !important;
        padding-bottom: 0.5rem !important;
        background: linear-gradient(90deg, rgba(42, 82, 152, 0.05) 0%, transparent 100%) !important;
        padding-left: 0.5rem !important;
        margin-left: -0.5rem !important;
        margin-right: -0.5rem !important;
        border-radius: 6px 6px 0 0 !important;
    }
    
    /* Força o container principal */
    .block-container {
        padding-top: 2rem;
        background: transparent;
    }
    
    /* Remove fundo dos gráficos */
    .stPlotlyChart {
        background: transparent !important;
    }
    
    /* Estiliza a sidebar */
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #ffffff 0%, #f8f9fa 100%) !important;
        border-right: 2px solid #e3e8ef !important;
    }
    
    /* Melhora os inputs da sidebar */
    .stSelectbox > div > div {
        background-color: #f8f9fa !important;
        border: 1px solid #dee2e6 !important;
        border-radius: 8px;
    }
    
    /* Força visibilidade das bordas em dataframes */
    .stDataFrame {
        border: 1px solid #dee2e6 !important;
        border-radius: 8px;
        overflow: hidden;
    }
    
    /* Remove margin de alguns elementos para melhor encaixe */
    .element-container div[data-testid="stMarkdownContainer"] p {
        margin-bottom: 0 !important;
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
    <h1>E-commerce Analytics</h1>
    <p>Análise da Performance de Vendas e Marketing</p>
</div>
""", unsafe_allow_html=True)

# Sidebar para filtros
canal_filter = st.sidebar.multiselect(
    "Canais:",
    options=df['canal_origem'].unique(),
    default=df['canal_origem'].unique()
)

categoria_filter = st.sidebar.multiselect(
    "Categorias:",
    options=df['categoria_interesse'].unique(),
    default=df['categoria_interesse'].unique()
)

# Filtrar dados
df_filtered = df[
    (df['canal_origem'].isin(canal_filter)) &
    (df['categoria_interesse'].isin(categoria_filter))
]

# KPIs principais em cards
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class="metric-card">
        <h3 style="color: #257685; margin: 0; font-size: 1rem;">Taxa de Conversão</h3>
        <h2 style="text-align: center;margin: 0.5rem 0; color: #176B87;">{:.1f}%</h2>
        <p style="color: #7f8c8d; margin: 0; font-size: 0.9rem;">Total de conversões</p>
    </div>
    """.format(df_filtered['realizou_compra'].mean() * 100), unsafe_allow_html=True)

with col2:
    valor_total_em_vendas = df_filtered['valor_compra'].sum()
    st.markdown(f"""
    <div class="metric-card">
        <h3 style="color: #257685; margin: 0; font-size: 1rem;">Receita Total</h3>
        <h2 style="text-align: center;margin: 0.5rem 0; color: #176B87;">{formatar_moeda_br(valor_total_em_vendas)}</h2>
        <p style="color: #7f8c8d; margin: 0; font-size: 0.9rem;">Valor total em vendas</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    valor_aov = df_filtered[df_filtered['realizou_compra'] == 1]['valor_compra'].mean()
    st.markdown(f"""
        <div class="metric-card">
            <h3 style="color: #257685; margin: 0; font-size: 1rem;">AOV Médio</h3>
            <h2 style="text-align: center;margin: 0.5rem 0; color: #176B87;">{formatar_moeda_br(valor_aov)}</h2>
            <p style="color: #7f8c8d; margin: 0; font-size: 0.9rem;">Ticket médio</p>
        </div>
        """, unsafe_allow_html=True)
with col4:
    st.markdown("""
    <div class="metric-card">
        <h3 style="color: #257685; margin: 0; font-size: 1rem;">Taxa de Abandono</h3>
        <h2 style="text-align: center;margin: 0.5rem 0; color: #176B87;">{:.1f}%</h2>
        <p style="color: #7f8c8d; margin: 0; font-size: 0.9rem;">Carrinhos abandonados</p>
    </div>
    """.format(df_filtered['abandonou_carrinho'].mean() * 100), unsafe_allow_html=True)

# Primeira linha de gráficos em cards
col1, col2 = st.columns(2)

with col1:
    st.markdown("<br></br>", unsafe_allow_html=True)
    st.markdown('<p class="chart-title" style="text-align: center;">Taxa de Conclusão vs. Abandono por Canal</p>', unsafe_allow_html=True)
    
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
        marker_color='#3091a2',
        text=canal_stats['Taxa_Conversao'].astype(str) + '%',
        textposition='outside'
    ))
    fig1.add_trace(go.Bar(
        name='Taxa de Não Conversão',
        x=canal_stats.index,
        y=canal_stats['Taxa_Nao_Conversao'],
        marker_color='#19c3cc',
        text=canal_stats['Taxa_Nao_Conversao'].astype(str) + '%',
        textposition='outside'
    ))
    fig1.update_layout(
        barmode='group',
        height=350,
        showlegend=True,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=0, r=0, t=20, b=0),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        yaxis=dict(
            gridcolor="#cfd4db"  
        )
        
    )
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.markdown("<br></br>", unsafe_allow_html=True)
    st.markdown('<p class="chart-title" style="text-align: center;">Taxa de Abandono por Categoria</p>', unsafe_allow_html=True)
    
    abandono_cat = df_filtered.groupby('categoria_interesse').agg({
        'abandonou_carrinho': ['sum', 'count']
    })
    abandono_cat.columns = ['Abandonos', 'Total']
    abandono_cat['Taxa_Abandono'] = (abandono_cat['Abandonos'] / abandono_cat['Total'] * 100).round(1)
    
    fig5 = px.bar(
        x=abandono_cat.index,
        y=abandono_cat['Taxa_Abandono'],
        color=abandono_cat['Taxa_Abandono'],
        # color_continuous_scale='Reds',
        color_continuous_scale=['#19c3cc', "#257685"],
        text=abandono_cat['Taxa_Abandono'].astype(str) + '%'
    )
    fig5.update_traces(textposition='outside')
    fig5.update_layout(
        height=350,
        showlegend=False,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        coloraxis_showscale=False,
        xaxis_title="Categoria de Interesse",
        yaxis_title="Taxa de Abandono (%)",
        margin=dict(l=0, r=0, t=20, b=0),
        yaxis=dict(
            gridcolor="#d5d9df"  
        )
    )
    st.plotly_chart(fig5, use_container_width=True)

# Segunda linha de gráficos em cards
col3, col4 = st.columns(2)

with col3:
    st.markdown("<br></br>", unsafe_allow_html=True)
    st.markdown('<p class="chart-title" style="text-align: center;">Receita Total por Canal</p>', unsafe_allow_html=True)   

    # Calcular a receita por canal
    receita_canal = df_filtered.groupby('canal_origem')['valor_compra'].sum().sort_values(ascending=False)

    # Criar o gráfico de barras horizontais
    fig2 = px.bar(
        x=receita_canal.values,
        y=receita_canal.index,
        orientation='h',
        color=receita_canal.values,
        color_continuous_scale=['#19c3cc', "#287e8d"],
        text=receita_canal.values.round(0)

    )

    # Ajustar o texto
    fig2.update_traces(texttemplate='R$ %{text:.0f}', textposition='outside')

    # Ajustar o layout do gráfico
    fig2.update_layout(
        height=350,
        showlegend=False,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        coloraxis_showscale=False,
        xaxis_title="Receita (R$)",
        yaxis_title="Canal de Origem",
        margin=dict(l=0, r=10, t=20, b=30),  # Ajustar o espaço da margem direita e inferior
        xaxis=dict(
            range=[0, receita_canal.max() * 1.1],  # Limitar o eixo X para evitar que as barras saiam do gráfico
        ),
    )

    # Exibir o gráfico
    st.plotly_chart(fig2, use_container_width=True)
with col4:
    st.markdown("<br></br>", unsafe_allow_html=True)
    st.markdown('<p class="chart-title" style="text-align: center;">Distribuição por Faixa de Valor</p>', unsafe_allow_html=True)
    
    faixa_dist = df_filtered[df_filtered['Faixa de Valor'] != 'N/A']['Faixa de Valor'].value_counts()
    
    fig4 = px.pie(
        values=faixa_dist.values,
        names=faixa_dist.index,
        color_discrete_sequence=["#146775", '#25aab7', '#19c3cc']
    )
    fig4.update_traces(textposition='inside', textinfo='percent+label')
    fig4.update_layout(
        height=350,
        showlegend=True,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=0, r=0, t=20, b=0)
    )
    st.plotly_chart(fig4, use_container_width=True)

# Terceira linha de gráficos em cards
col5, col6 = st.columns(2)

with col5:
    
    st.markdown("<br></br>", unsafe_allow_html=True)
    st.markdown('<p class="chart-title" style="text-align: center;">AOV por Canal de Origem</p>', unsafe_allow_html=True)
    
    aov_canal = df_filtered[df_filtered['realizou_compra'] == 1].groupby('canal_origem')['valor_compra'].mean().sort_values(ascending=False)
    
    fig3 = px.scatter(
        x=aov_canal.index,
        y=aov_canal.values,
        size=aov_canal.values,
        color=aov_canal.values,
        color_continuous_scale=['#185D61', "#0B4447"],
        size_max=10,
        
    )
    fig3.update_traces(
        text=aov_canal.values.round(0),
        textposition='top center'
    )
    fig3.update_layout(
        height=350,
        showlegend=False,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        coloraxis_showscale=False,
        xaxis_title="Canal de Origem",
        yaxis_title="AOV (R$)",
        margin=dict(l=0, r=0, t=20, b=0),
        yaxis=dict(
            gridcolor="#cfd4db"  
        )
    )
    st.plotly_chart(fig3, use_container_width=True)


with col6:
    st.markdown("<br></br>", unsafe_allow_html=True)
    st.markdown('<p class="chart-title" style="text-align: center;">Taxa de Engajamento por Canal</p>', unsafe_allow_html=True)
    
    engagement = df_filtered.groupby('canal_origem').agg({
        'abriu_email': 'mean',
        'clicou_em_link': 'mean'
    }) * 100
    
    fig6 = go.Figure()
    fig6.add_trace(go.Scatter(
        x=engagement['abriu_email'],
        y=engagement['clicou_em_link'],
        mode='markers+text',
        marker=dict(size=15, color='#3091a2'),
        text=engagement.index,
        textposition='top center'
    ))
    fig6.update_layout(
        xaxis_title='Taxa de Abertura de Email (%)',
        yaxis_title='Taxa de Clique em Link (%)',
        height=350,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=0, r=0, t=20, b=0),
        yaxis=dict(
            gridcolor="#d1d5db"  
        )
    )
    st.plotly_chart(fig6, use_container_width=True)

st.markdown("<br></br>", unsafe_allow_html=True)

# Tabela de dados em card
st.markdown('<p class="chart-title" style="text-align: center;">Dados Detalhados</p>', unsafe_allow_html=True)

st.dataframe(
    df_filtered[['nome', 'canal_origem', 'categoria_interesse', 'Status da Compra', 'valor_compra', 'Faixa de Valor']],
    use_container_width=True,
    height=300
)

# Footer
# st.markdown(
#     "<div style='text-align: center; color: #7f8c8d; margin-top: 3rem; padding: 2rem;'>"
#     "Dashboard desenvolvido para análise de performance de e-commerce | "
#     "Dados atualizados automaticamente"
#     "</div>",
#     unsafe_allow_html=True
# )