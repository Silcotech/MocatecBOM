import streamlit as st
import pandas as pd
from datetime import date

st.set_page_config(layout="wide", page_title="BOM Máquina 2", page_icon="🔩")

# DADOS EXATOS da sua BOM colorida [file:118]
@st.cache_data
def load_bom_real():
    data = {
        "Imagem": ["🟨", "🟨", "🟨", "🟨", "🟨", "🟥"],
        "Part_Number": ["BOM-2-MAQ", "701357018", "801357017", "501319004", "701357030", "801357030"],
        "Descrição": [
            "ESTRUTURA MAQUINA 2", 
            "CALIBRE POSICIONAMENTO", 
            "ESTRUTURA PRINCIPAL", 
            "PERFIL ALUMINIO 45X90MM", 
            "LATERAL CHAPA ZINCADA", 
            "SUPORTE FINAL"
        ],
        "QTY": [1, 1, 1, 4, 2, 1],
        "Material": ["ESTRUTURAL", "AW-5083", "Estrutural", "Aluminio 45x90", "Chapa Zincada", "Aço S235"],
        "Tratamento": ["sim", "sim", "sim", "", "Laser", "Torno"]
    }
    return pd.DataFrame(data)

if 'bom_df' not in st.session_state:
    st.session_state.bom_df = load_bom_real()
    st.session_state.tarefas_df = pd.DataFrame({
        "ID": [], "Funcionário": [], "Tarefa": [], "Status": [], "Prazo": [], "Prioridade": []
    })

# MENU PRINCIPAL
st.sidebar.title("🔩 **BOM MÁQUINA 2**")
page = st.sidebar.selectbox("📂 Páginas:", ["🏠 Dashboard", "📦 BOM Colorida", "✅ Tarefas", "👥 Equipa"])

# ============ DASHBOARD ============
if page == "🏠 Dashboard":
    st.title("🏠 **DASHBOARD BOM MÁQUINA 2**")
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("📦 Total Peças", len(st.session_state.bom_df))
    col2.metric("🔢 Total QTY", st.session_state.bom_df['QTY'].sum())
    col3.metric("🟨 Itens Amarelos", len(st.session_state.bom_df[st.session_state.bom_df['Imagem']=='🟨']))
    col4.metric("🟥 Itens Vermelhos", len(st.session_state.bom_df[st.session_state.bom_df['Imagem']=='🟥']))

# ============ BOM COLORIDA (EXATA) ============
elif page == "📦 BOM Colorida":
    st.title("📦 **BOM MÁQUINA 2 - COM CÓDIGOS DE COR**")
    
    # FILTROS BOM
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        cor_filter = st.multiselect("Cor:", ["🟨 Amarelo", "🟥 Vermelho"], default=["🟨 Amarelo", "🟥 Vermelho"])
    with col_f2:
        material_filter = st.multiselect("Material:", st.session_state.bom_df['Material'].unique())
    
    df_bom = st.session_state.bom_df.copy()
    if "🟨 Amarelo" not in cor_filter: 
        df_bom = df_bom[df_bom['Imagem'] != '🟨']
    if "🟥 Vermelho" not in cor_filter: 
        df_bom = df_bom[df_bom['Imagem'] != '🟥']
    if material_filter:
        df_bom = df_bom[df_bom['Material'].isin(material_filter)]
    
    # TABELA COLORIDA EXATA [file:118]
    st.subheader("📋 **BOM COMPLETA**")
    
    # CSS para cores da sua macro
    st.markdown("""
    <style>
    .status-amarelo { background-color: #FFF200; font-weight: bold; }
    .status-vermelho { background-color: #FF0000; color: white; font-weight: bold; }
    .status-cabecalho { background-color: #FFD700; font-weight: bold; font-size: 14px; }
    </style>
    """, unsafe_allow_html=True)
    
    # MOSTRAR TABELA COM CORES
    for idx, row in df_bom.iterrows():
        cor_class = "status-amarelo" if row['Imagem'] == '🟨' else "status-vermelho"
        st.markdown(f"""
        <div style='border: 2px solid #000; margin: 5px 0; padding: 10px;'>
            <table style='width: 100%; border-collapse: collapse;'>
                <tr class='status-cabecalho'>
                    <td style='width: 5%; padding: 8px;'>{row['Imagem']}</td>
                    <td style='width: 15%; padding: 8px; font-weight: bold;'>{row['Part_Number']}</td>
                    <td style='width: 50%; padding: 8px;'>{row['Descrição']}</td>
                    <td style='width: 10%; padding: 8px; text-align: center;'>{row['QTY']}</td>
                    <td style='width: 20%; padding: 8px;'>{row['Material']}</td>
                    <td style='width: 15%; padding: 8px;'>{row['Tratamento']}</td>
                </tr>
            </table>
        </div>
        """, unsafe_allow_html=True)
    
    # ADICIONAR NOVA PEÇA
    st.subheader("➕ **Nova Peça**")
    with st.form("add_peca"):
        col1, col2, col3 = st.columns(3)
        with col1:
            part_num = st.text_input("Part Number:")
            cor = st.selectbox("Cor:", ["🟨 Amarelo", "🟥 Vermelho"])
        with col2:
            desc = st.text_input("Descrição:")
            qty = st.number_input("QTY:", 1)
        with col3:
            material = st.selectbox("Material:", ["Aluminio", "AW-5083", "S235JR", "Chapa"])
            tratamento = st.multiselect("Tratamento:", ["sim", "Laser", "Torno"])
        
        if st.form_submit_button("✅ ADICIONAR"):
            new_row = pd.DataFrame({
                "Imagem": [cor[0]], "Part_Number": [part_num], "Descrição": [desc],
                "QTY": [qty], "Material": [material], "Tratamento": [", ".join(tratamento)]
            })
            st.session_state.bom_df = pd.concat([st.session_state.bom_df, new_row], ignore_index=True)
            st.success("✅ Peça adicionada com cor!")
            st.rerun()

# ============ TAREFAS ============
elif page == "✅ Tarefas":
    st.title("✅ **TAREFAS POR FUNCIONÁRIO**")
    
    funcs = ["TODOS", "João Silva", "Maria Santos", "Pedro Costa", "Ana Oliveira"]
    func_sel = st.sidebar.selectbox("👤:", funcs)
    
    df_tarefas = st.session_state.tarefas_df.copy()
    if func_sel != "TODOS":
        df_tarefas = df_tarefas[df_tarefas['Funcionário'] == func_sel]
    
    st.dataframe(df_tarefas, use_container_width=True)
    
    # NOVA TAREFA
    with st.expander("➕ Nova Tarefa"):
        with st.form("tarefa"):
            col1, col2 = st.columns(2)
            with col1:
                func = st.selectbox("Para:", ["João Silva", "Maria Santos", "Pedro Costa"])
                prio = st.selectbox("Prioridade:", ["Alta", "Média", "Baixa"])
            with col2:
                tarefa = st.text_area("Descrição:")
                prazo = st.date_input("Prazo:")
            
            if st.form_submit_button("✅ Criar"):
                new_id = len(st.session_state.tarefas_df) + 1
                st.session_state.tarefas_df = pd.concat([st.session_state.tarefas_df, pd.DataFrame({
                    "ID": [new_id], "Funcionário": [func], "Tarefa": [tarefa],
                    "Status": ["Pendente"], "Prazo": [prazo.strftime("%d/%m/%Y")],
                    "Prioridade": [prio]
                })], ignore_index=True)
                st.rerun()

# ============ EQUIPE ============
elif page == "👥 Equipa":
    st.title("👥 **PRODUTIVIDADE EQUIPE**")
    resumo = st.session_state.tarefas_df.groupby('Funcionário')['ID'].count().to_frame('Total')
    st.dataframe(resumo, use_container_width=True)

# DOWNLOADS
st.sidebar.markdown("---")
csv_bom = st.session_state.bom_df.to_csv(index=False).encode('utf-8')
st.sidebar.download_button("📦 BOM.csv", csv_bom, "BOM.csv")
if not st.session_state.tarefas_df.empty:
    csv_tarefas = st.session_state.tarefas_df.to_csv(index=False).encode('utf-8')
    st.sidebar.download_button("✅ Tarefas.csv", csv_tarefas, "TAREFAS.csv")

st.markdown("---")
st.success("✅ **BOM EXATA com as suas cores amarelo/vermelho + Dashboard + Tarefas!**")
