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
        material_filter = st.multiselect("Material", st.session_state.bom_df['Material'].unique())
    with col_f2:
        stock_filter = st.multiselect("Stock", st.session_state.bom_df['Stock'].unique())
    with col_f3:
        tratamento_filter = st.multiselect("Tratamento", st.session_state.bom_df['Tratamento'].unique())
    
    # APLICAR FILTROS
    df_bom = st.session_state.bom_df.copy()
    if material_filter: df_bom = df_bom[df_bom['Material'].isin(material_filter)]
    if stock_filter: df_bom = df_bom[df_bom['Stock'].isin(stock_filter)]
    if tratamento_filter: df_bom = df_bom[df_bom['Tratamento'].isin(tratamento_filter)]
    
    # TABELA PRINCIPAL
    st.dataframe(df_bom, use_container_width=True, height=500)
    
    # ADICIONAR NOVA PEÇA
    st.subheader("➕ **Nova Peça**")
    with st.form("nova_peca"):
        col1, col2 = st.columns(2)
        with col1:
            part_num = st.text_input("Part Number")
            desc = st.text_area("Descrição", height=60)
            material = st.selectbox("Material", ["Aluminio", "AW-5083", "S235JR", "Inox", "Chapa"])
        with col2:
            qty = st.number_input("Quantidade", min_value=1)
            custo = st.number_input("Custo Unit. (€)", min_value=0.0, format="%.2f")
            stock = st.selectbox("Stock", ["OK", "Baixo", "Esgotado"])
            tratamento = st.multiselect("Tratamento", ["sim", "Laser", "Torno", "Oxicorte"])
        
        if st.form_submit_button("✅ Adicionar Peça"):
            new_row = pd.DataFrame({
                "Part_Number": [part_num], "Descrição": [desc], "QTY": [qty],
                "Material": [material], "Tratamento": [", ".join(tratamento)],
                "Stock": [stock], "Custo": [custo]
            })
            st.session_state.bom_df = pd.concat([st.session_state.bom_df, new_row], ignore_index=True)
            st.success("✅ Peça adicionada!")
            st.balloons()
            st.rerun()

# ============ PÁGINA TAREFAS ============
elif page == "✅ Tarefas":
    st.header("✅ **GESTÃO DE TAREFAS**")
    
    # Sidebar funcionário
    funcionarios = ["TODOS", "João Silva", "Maria Santos", "Pedro Costa", "Ana Oliveira"]
    selected_func = st.sidebar.selectbox("👤 Funcionário:", funcionarios)
    
    # FILTRAR TAREFAS
    df_tarefas = st.session_state.tarefas_df.copy()
    if selected_func != "TODOS":
        df_tarefas = df_tarefas[df_tarefas['Funcionário'] == selected_func]
    
    # TABELA TAREFAS
    st.dataframe(df_tarefas, use_container_width=True, height=400)
    
    # NOVA TAREFA
    st.subheader("➕ **Nova Tarefa**")
    with st.form("nova_tarefa"):
        col1, col2, col3 = st.columns(3)
        with col1:
            func = st.selectbox("Funcionário", ["João Silva", "Maria Santos", "Pedro Costa", "Ana Oliveira"])
            prioridade = st.selectbox("Prioridade", ["Alta", "Média", "Baixa"])
        with col2:
            tarefa = st.text_area("Descrição", height=80)
        with col3:
            status = st.selectbox("Status", ["Pendente", "Em Progresso", "Concluída"])
            prazo = st.date_input("Prazo", value=date(2026, 1, 25))
        
        if st.form_submit_button("✅ Criar Tarefa"):
            new_id = len(st.session_state.tarefas_df) + 1
            new_row = pd.DataFrame({
                "ID": [new_id], "Funcionário": [func], "Tarefa": [tarefa],
                "Status": [status], "Prazo": [prazo.strftime("%d/%m/%Y")],
                "Prioridade": [prioridade]
            })
            st.session_state.tarefas_df = pd.concat([st.session_state.tarefas_df, new_row], ignore_index=True)
            st.success("✅ Tarefa criada!")
            st.rerun()
    
    # ATUALIZAR STATUS
    if not df_tarefas.empty:
        st.subheader("🔄 **Atualizar Tarefa**")
        tarefa_id = st.selectbox("Tarefa:", df_tarefas['ID'].tolist())
        novo_status = st.selectbox("Status:", ["Pendente", "Em Progresso", "Concluída"])
        if st.button("🔄 Atualizar"):
            st.session_state.tarefas_df.loc[
                st.session_state.tarefas_df['ID'] == tarefa_id, 'Status'
            ] = novo_status
            st.success("✅ Atualizado!")
            st.rerun()

# ============ PÁGINA FUNCIONÁRIOS ============
elif page == "👥 Funcionários":
    st.header("👥 **PANEL FUNCIONÁRIOS**")
    
    # ESTATÍSTICAS POR FUNCIONÁRIO
    resumo_func = st.session_state.tarefas_df.groupby('Funcionário').agg({
        'ID': 'count',
        'Status': lambda x: (x=='Concluída').sum()
    }).round(0).astype(int)
    resumo_func.columns = ['Total Tarefas', 'Concluídas']
    resumo_func['% Concluídas'] = (resumo_func['Concluídas'] / resumo_func['Total Tarefas'] * 100).round(1)
    
    st.dataframe(resumo_func, use_container_width=True)
    
    # GRÁFICO PRODUTIVIDADE
    fig_func = px.bar(resumo_func.reset_index(), x='Funcionário', y='% Concluídas',
                     title="Produtividade por Funcionário (%)")
    st.plotly_chart(fig_func, use_container_width=True)

# DOWNLOADS GLOBAIS
st.sidebar.markdown("---")
col_d1, col_d2 = st.sidebar.columns(2)
with col_d1:
    csv_bom = st.session_state.bom_df.to_csv(index=False, encoding='utf-8').encode('utf-8')
    st.sidebar.download_button("📦 BOM", csv_bom, "BOM_COMPLETA.csv")
with col_d2:
    csv_tarefas = st.session_state.tarefas_df.to_csv(index=False, encoding='utf-8').encode('utf-8')
    st.sidebar.download_button("✅ Tarefas", csv_tarefas, "TAREFAS.csv")

# FOOTER
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; font-size: 12px'>
🔩 **BOM Máquina 2** - Sistema de Gestão Industrial • Online 24/7
</div>
""")

