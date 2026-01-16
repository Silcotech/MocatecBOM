import streamlit as st
import pandas as pd
from datetime import datetime, date

# Configuração
st.set_page_config(layout="wide", page_title="BOM Máquina 2", page_icon="🔩")

# Inicializar dados
@st.cache_data
def init_data():
    bom_data = {
        "Part_Number": ["701357018", "801357017", "501319004", "701357030", "501357007"],
        "Descrição": ["CALIBRE POSICIONAMENTO", "ESTRUTURA MAQUINA", "PERFIL ALUMINIO 45X90", "CHAPA ZINCADA", "TAPETE XP 6M"],
        "QTY": [1, 1, 2, 2, 1],
        "Material": ["AW-5083", "Estrutural", "Aluminio", "Chapa", "S235JR"],
        "Tratamento": ["sim", "sim", "", "Laser", ""],
        "Stock": ["OK", "OK", "Baixo", "OK", "OK"],
        "Custo": [150.50, 2500.00, 120.00, 85.75, 450.00]
    }
    
    tarefas_data = {
        "ID": [1, 2, 3, 4],
        "Funcionário": ["João Silva", "Maria Santos", "Pedro Costa", "Ana Oliveira"],
        "Tarefa": ["Cortar perfis alumínio", "Usinar calibres", "Montar estrutura", "Comprar chapas"],
        "Status": ["Em Progresso", "Pendente", "Concluída", "Pendente"],
        "Prazo": ["20/01/2026", "18/01/2026", "15/01/2026", "22/01/2026"],
        "Prioridade": ["Alta", "Média", "Alta", "Alta"]
    }
    return pd.DataFrame(bom_data), pd.DataFrame(tarefas_data)

if 'bom_df' not in st.session_state:
    st.session_state.bom_df, st.session_state.tarefas_df = init_data()

# MENU LATERAL
st.sidebar.title("🔩 **BOM MÁQUINA 2**")
page = st.sidebar.selectbox("📂 Navegar:", ["🏠 Dashboard", "📦 BOM", "✅ Tarefas", "👥 Equipa"])

# ============ DASHBOARD ============
if page == "🏠 Dashboard":
    st.title("🏠 **DASHBOARD PRINCIPAL**")
    
    # MÉTRICAS
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("📦 Peças Totais", len(st.session_state.bom_df), 2)
    col2.metric("🔢 Quantidade", st.session_state.bom_df['QTY'].sum())
    col3.metric("💰 Custo Total", f"€{st.session_state.bom_df['Custo'].sum():.2f}")
    col4.metric("⏳ Tarefas Pendentes", len(st.session_state.tarefas_df[st.session_state.tarefas_df['Status']=='Pendente']))
    
    # RESUMOS
    col_r1, col_r2 = st.columns(2)
    with col_r1:
        st.subheader("📊 Materiais por QTY")
        resumo_mat = st.session_state.bom_df.groupby('Material')['QTY'].sum().sort_values(ascending=False)
        st.dataframe(resumo_mat, use_container_width=True)
    
    with col_r2:
        st.subheader("📈 Status Tarefas")
        status_count = st.session_state.tarefas_df['Status'].value_counts()
        st.dataframe(status_count.reset_index(), use_container_width=True)
    
    # ALERTAS
    st.subheader("⚠️ **ALERTAS**")
    stock_baixo = st.session_state.bom_df[st.session_state.bom_df['Stock']=='Baixo']
    if not stock_baixo.empty:
        st.error(f"🟡 **{len(stock_baixo)} itens com stock baixo:**")
        st.dataframe(stock_baixo[['Part_Number', 'Descrição']], use_container_width=True)
    else:
        st.success("✅ Todos os stocks OK!")

# ============ BOM ============
elif page == "📦 BOM":
    st.title("📦 **BOM MATERIAIS**")
    
    # FILTROS
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        material_f = st.multiselect("Material:", st.session_state.bom_df['Material'].unique())
    with col_f2:
        stock_f = st.multiselect("Stock:", st.session_state.bom_df['Stock'].unique())
    
    df_show = st.session_state.bom_df.copy()
    if material_f: df_show = df_show[df_show['Material'].isin(material_f)]
    if stock_f: df_show = df_show[df_show['Stock'].isin(stock_f)]
    
    st.dataframe(df_show, use_container_width=True, height=500)
    
    # NOVA PEÇA
    with st.expander("➕ **Adicionar Peça**"):
        with st.form("add_peca"):
            col1, col2 = st.columns(2)
            with col1:
                part_num = st.text_input("Part Number:")
                desc = st.text_input("Descrição:")
                material = st.selectbox("Material", ["Aluminio", "AW-5083", "S235JR", "Chapa", "Inox"])
            with col2:
                qty = st.number_i
