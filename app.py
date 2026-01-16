import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, date
import numpy as np

# Configuração página
st.set_page_config(
    layout="wide", 
    page_title="BOM Máquina 2", 
    page_icon="🔩",
    initial_sidebar_state="expanded"
)

# Persistência dados
@st.cache_data
def init_data():
    bom_data = {
        "Part_Number": ["701357018", "801357017", "501319004", "701357030", "501357007"],
        "Descrição": [
            "CALIBRE POSICIONAMENTO AW-5083", 
            "ESTRUTURA PRINCIPAL MAQUINA", 
            "PERFIL ALUMINIO 45X90 x 2260mm",
            "LATERAL CHAPA ZINCADA", 
            "TAPETE XP 304.8mm x 6M"
        ],
        "QTY": [1, 1, 2, 2, 1],
        "Material": ["AW-5083", "Estrutural", "Aluminio", "Chapa Zincada", "S235JR"],
        "Tratamento": ["sim", "sim", "", "Laser", ""],
        "Stock": ["OK", "OK", "Baixo", "OK", "OK"],
        "Custo": [150.50, 2500.00, 120.00, 85.75, 450.00]
    }
    
    tarefas_data = {
        "ID": [1, 2, 3],
        "Funcionário": ["João Silva", "Maria Santos", "Pedro Costa"],
        "Tarefa": ["Cortar perfis alumínio", "Usinar calibres", "Montar estrutura base"],
        "Status": ["Em Progresso", "Pendente", "Concluída"],
        "Prazo": ["20/01/2026", "18/01/2026", "15/01/2026"],
        "Prioridade": ["Alta", "Média", "Alta"]
    }
    
    return pd.DataFrame(bom_data), pd.DataFrame(tarefas_data)

# Carregar dados
if 'bom_df' not in st.session_state:
    st.session_state.bom_df, st.session_state.tarefas_df = init_data()

# SIDEBAR COM MENU
st.sidebar.title("🔩 **Menu Principal**")
page = st.sidebar.selectbox(
    "Navegação:",
    ["🏠 Dashboard", "📦 BOM Materiais", "✅ Tarefas", "👥 Funcionários"]
)

# ============ PÁGINA INICIAL - DASHBOARD ============
if page == "🏠 Dashboard":
    st.title("🔩 **DASHBOARD MÁQUINA 2**")
    st.markdown("### 📊 Visão Geral da Produção")
    
    # MÉTRICAS PRINCIPAIS
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        total_pecas = len(st.session_state.bom_df)
        st.metric("📦 Total Peças", total_pecas)
    with col2:
        total_qtd = st.session_state.bom_df['QTY'].sum()
        st.metric("🔢 Qtd Total", total_qtd)
    with col3:
        custo_total = st.session_state.bom_df['Custo'].sum()
        st.metric("💰 Custo Total", f"€{custo_total:,.2f}")
    with col4:
        pendentes = len(st.session_state.tarefas_df[st.session_state.tarefas_df['Status']=='Pendente'])
        st.metric("⏳ Tarefas Pendentes", pendentes)
    
    # GRÁFICOS
    col_g1, col_g2 = st.columns(2)
    with col_g1:
        # GRÁFICO MATERIAL
        resumo_material = st.session_state.bom_df.groupby('Material')['QTY'].sum().reset_index()
        fig1 = px.bar(resumo_material, x='Material', y='QTY', title="Distribuição Materiais")
        st.plotly_chart(fig1, use_container_width=True)
    
    with col_g2:
        # GRÁFICO STATUS TAREFAS
        status_tarefas = st.session_state.tarefas_df['Status'].value_counts().reset_index()
        fig2 = px.pie(status_tarefas, names='Status', values='count', title="Status Tarefas")
        st.plotly_chart(fig2, use_container_width=True)
    
    # TABELAS RESUMO
    col_t1, col_t2 = st.columns(2)
    with col_t1:
        st.subheader("🔍 TOP 5 Materiais (Valor)")
        top_materiais = st.session_state.bom_df.groupby('Material')['Custo'].sum().sort_values(ascending=False).head()
        st.dataframe(top_materiais, use_container_width=True)
    
    with col_t2:
        st.subheader("⚠️ Stock Crítico")
        stock_critico = st.session_state.bom_df[st.session_state.bom_df['Stock']=='Baixo']
        st.dataframe(stock_critico[['Part_Number', 'Descrição', 'QTY']], use_container_width=True)

# ============ PÁGINA BOM ============
elif page == "📦 BOM Materiais":
    st.header("📦 **LISTA DE MATERIAIS BOM**")
    
    # FILTROS
    col_f1, col_f2, col_f3 = st.columns(3)
    with col_f1:
        material_filter = st.multiselect("Material", st.session_state.bom_df['Material'].uniqu
