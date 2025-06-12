import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Título
st.title("Dashboard de Desempenho de Vendas e Marketing")

# Carregar dados
@st.cache_data
def carregar_dados():
    return pd.read_csv("dados_final.csv")

df = carregar_dados()

# Seção: Filtros
st.sidebar.header("Filtros")
categoria = st.sidebar.multiselect("Categoria de Interesse", options=df['categoria_interesse'].unique(), default=df['categoria_interesse'].unique())
canal = st.sidebar.multiselect("Canal de Origem", options=df['canal_origem'].unique(), default=df['canal_origem'].unique())

# Aplicar filtros
df_filtrado = df[(df['categoria_interesse'].isin(categoria)) & (df['canal_origem'].isin(canal))]

# AOV por canal
st.subheader("Valor Médio de Pedido (AOV) por Canal")
df_compras = df_filtrado[df_filtrado['realizou_compra'] == 1]
aov_canal = df_compras.groupby('canal_origem')['valor_compra'].mean().reset_index()

fig1, ax1 = plt.subplots()
ax1.bar(aov_canal['canal_origem'], aov_canal['valor_compra'])
ax1.set_xlabel("Canal")
ax1.set_ylabel("AOV")
ax1.set_title("AOV por Canal de Origem")
st.pyplot(fig1)

# Abandono de carrinho por categoria
st.subheader("Abandono de Carrinho por Categoria")
abandono_categoria = df_filtrado.groupby('categoria_interesse')['abandonou_carrinho'].sum().reset_index()

fig2, ax2 = plt.subplots()
ax2.bar(abandono_categoria['categoria_interesse'], abandono_categoria['abandonou_carrinho'])
ax2.set_xlabel("Categoria")
ax2.set_ylabel("Abandonos")
ax2.set_title("Abandonos por Categoria de Interesse")
st.pyplot(fig2)

# Curva de Pareto
st.subheader("Curva de Pareto de Receita por Cliente")
df_pareto = df_compras[['nome', 'valor_compra']].groupby('nome').sum().sort_values(by='valor_compra', ascending=False).reset_index()
df_pareto['acumulado'] = df_pareto['valor_compra'].cumsum()
df_pareto['percentual'] = 100 * df_pareto['acumulado'] / df_pareto['valor_compra'].sum()

fig3, ax3 = plt.subplots()
ax3.plot(df_pareto.index + 1, df_pareto['percentual'])
ax3.axhline(80, color='red', linestyle='--')
ax3.set_xlabel("Clientes (ordenados)")
ax3.set_ylabel("% Receita Acumulada")
ax3.set_title("Curva de Pareto")
st.pyplot(fig3)
