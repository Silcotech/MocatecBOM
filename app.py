import streamlit as st
import pandas as pd
from datetime import datetime, date

st.set_page_config(layout="wide", page_title="BOM + Tarefas")
st.title("🔩👷 **BOM Máquina 2 + Gestão Tarefas**")
st.markdown("---")

# SESSION STATE para persistir dados
if 'bom_df' not in st.session_state:
    st.session_state.bom_df = pd.DataFrame({
        "Part_Number": ["701357018", "801357017", "501319004"],
        "Descrição": ["CALIBRE POSICIONAMENTO", "ESTRUTURA MAQUINA", "PERFIL ALUMNIO"],
        "QTY": [1, 1, 2],
        "Material": ["AW-5083", "Estrutural", "Aluminio"],
        "Tratamento": ["sim", "sim", ""]
    })

if 'tarefas_df' not in st.session_state:
    st.session_state.tarefas_df = pd.DataFrame(columns=["Funcionario", "Tarefa", "Status", "Data"])

df_bom = st.session_state.bom_df
df_tarefas = st.session_state.tarefas_df

# TABS
tab1, tab2 = st.tabs(["📋 BOM", "✅ Tarefas Funcionários"])

# TAB 1 - BOM
with tab1:
    st.subheader("📦 Lista BOM")
    
    # Filtros BOM
    col1, col2 = st.columns(2)
    with col1:
        material_filter = st.multiselect("Material", df_bom['Material'].unique())
    with col2:
        tratamento_filter = st.multiselect("Tratamento", df_bom['Tratamento'].unique())
    
    df_bom_filtered = df_bom
    if material_filter:
        df_bom_filtered = df_bom_filtered[df_bom_filtered['Material'].isin(material_filter)]
    if tratamento_filter:
        df_bom_filtered = df_bom_filtered[df_bom_filtered['Tratamento'].isin(tratamento_filter)]
    
    st.dataframe(df_bom_filtered, use_container_width=True)
    
    # Adicionar BOM
    with st.expander("➕ Adicionar Peça BOM"):
        col_a, col_b = st.columns(2)
        with col_a:
            part = st.text_input("Part Number")
            desc = st.text_input("Descrição")
        with col_b:
            qty = st.number_input("QTY", min_value=1)
            material = st.selectbox("Material", ["AW-5083", "Aluminio", "S235JR", "Inox"])
        
        if st.button("✅ Adicionar Peça", key="add_bom"):
            new_row = pd.DataFrame({
                "Part_Number": [part], "Descrição": [desc], "QTY": [qty],
                "Material": [material], "Tratamento": [""]
            })
            st.session_state.bom_df = pd.concat([st.session_state.bom_df, new_row], ignore_index=True)
            st.success("✅ Peça adicionada!")
            st.rerun()

# TAB 2 - TAREFAS POR FUNCIONÁRIO
with tab2:
    st.subheader("✅ **Gestão Tarefas por Funcionário**")
    
    # Lista funcionários (pode expandir)
    funcionarios = ["João Silva", "Maria Santos", "Pedro Costa", "Ana Oliveira", "Carlos Mendes"]
    
    # Sidebar seleção funcionário
    st.sidebar.header("👤 Selecione Funcionário")
    selected_funcionario = st.sidebar.selectbox("Funcionário", funcionarios + ["TODOS"])
    
    # Mostrar tarefas
    if selected_funcionario == "TODOS":
        tarefas_display = df_tarefas
    else:
        tarefas_display = df_tarefas[df_tarefas['Funcionario'] == selected_funcionario]
    
    st.dataframe(tarefas_display, use_container_width=True)
    
    # ADICIONAR TAREFA
    st.subheader("➕ **Nova Tarefa**")
    with st.form("nova_tarefa"):
        col1, col2, col3 = st.columns(3)
        with col1:
            func = st.selectbox("Para:", funcionarios)
        with col2:
            tarefa = st.text_area("Tarefa:", placeholder="Ex: Cortar perfil alumínio 45x90")
        with col3:
            status = st.selectbox("Status:", ["Pendente", "Em Progresso", "Concluída"])
        
        data_criacao = datetime.now().strftime("%d/%m/%Y %H:%M")
        
        if st.form_submit_button("✅ Atribuir Tarefa"):
            new_tarefa = pd.DataFrame({
                "Funcionario": [func], "Tarefa": [tarefa], 
                "Status": [status], "Data": [data_criacao]
            })
            st.session_state.tarefas_df = pd.concat([st.session_state.tarefas_df, new_tarefa], ignore_index=True)
            st.success(f"✅ Tarefa atribuída para **{func}**!")
            st.rerun()
    
    # ATUALIZAR STATUS TAREFA
    st.subheader("🔄 **Atualizar Status**")
    if not tarefas_display.empty:
        tarefa_id = st.selectbox("Selecione tarefa:", tarefas_display.index.tolist())
        novo_status = st.selectbox("Novo Status:", ["Pendente", "Em Progresso", "Concluída"])
        
        if st.button("🔄 Atualizar"):
            st.session_state.tarefas_df.loc[tarefa_id, 'Status'] = novo_status
            st.success("✅ Status atualizado!")
            st.rerun()
    
    # ESTATÍSTICAS TAREFAS
    col1, col2, col3 = st.columns(3)
    col1.metric("📊 Total Tarefas", len(df_tarefas))
    col2.metric("✅ Concluídas", len(df_tarefas[df_tarefas['Status']=='Concluída']))
    col3.metric("⏳ Pendentes", len(df_tarefas[df_tarefas['Status']=='Pendente']))

# DOWNLOADS
st.subheader("💾 **Exportar Dados**")
col1, col2 = st.columns(2)
with col1:
    csv_bom = df_bom.to_csv(index=False, encoding='utf-8').encode()
    st.download_button("📦 BOM CSV", csv_bom, "BOM_MAQ.csv")
with col2:
    csv_tarefas = df_tarefas.to_csv(index=False, encoding='utf-8').encode()
    st.download_button("✅ Tarefas CSV", csv_tarefas, "TAREFAS_FUNCIONARIOS.csv")

# INFO FINAL
st.info("""
👥 **COMO USAR:**
• **BOM**: Adicione peças, filtre por material
• **Tarefas**: Sidebar → Selecione funcionário → Atribua tarefas
• **Status**: Atualize progresso das tarefas
• 📱 **Mobile OK** - funciona em telemóvel!
""")
