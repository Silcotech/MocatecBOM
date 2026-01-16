import streamlit as st
import pandas as pd
import io

# Configurar página
st.set_page_config(layout="wide", page_title="BOM Máquina 2", initial_sidebar_state="expanded")
st.title("🔩 Gestor BOM - Máquina 2 MAQ")
st.markdown("---")

# Dados iniciais da vossa BOM (baseados no ficheiro Excel)
@st.cache_data
def load_bom_data():
    data = {
        "Part_Number": ["701357018", "801357017", "501319004", "701357030", "501357007"],
        "Description": [
            "CALIBRE POSICIONAMENTO", 
            "ESTRUTURA MAQUINA", 
            "PERFIL ALUMNIO 45X90MM x 2260 mm", 
            "LATERAL INTERIOR CHAPA ZINCADA", 
            "TAPETE XP COM 304.8mm Largura 6 Mts"
        ],
        "QTY": [1, 1, 2, 2, 1],
        "Material": ["AW-5083", "Estrutural", "Aluminio 45x90", "CHAPA ZINCADA", "S235JR"],
        "Tratamento": ["sim", "sim", "", "Laser", ""]
    }
    return pd.DataFrame(data)

# Carregar dados
df = load_bom_data()

# Sidebar - Filtros
st.sidebar.header("🔍 Filtros")
material_filter = st.sidebar.multiselect(
    "Material", 
    options=df['Material'].unique(), 
    default=df['Material'].unique()
)
tratamento_filter = st.sidebar.multiselect(
    "Tratamento", 
    options=df['Tratamento'].unique()
)

# Aplicar filtros
df_filtered = df[
    df['Material'].isin(material_filter) & 
    (df['Tratamento'].isin(tratamento_filter) | tratamento_filter == [])
]

# Métricas principais
col1, col2, col3, col4 = st.columns(4)
col1.metric("📦 Total Peças", len(df_filtered))
col2.metric("🔢 Total QTY", int(df_filtered['QTY'].sum()))
col3.metric("🏭 Materiais", df['Material'].nunique())
col4.metric("⚙️ Com Tratamento", len(df[df['Tratamento'] != '']))

# Tabela principal
st.subheader("📋 Lista Completa BOM")
st.dataframe(df_filtered, use_container_width=True, height=400)

# Formulário para adicionar itens
st.subheader("➕ Adicionar Novo Item")
with st.form("add_item", clear_on_submit=True):
    col_a, col_b = st.columns(2)
    
    with col_a:
        part_num = st.text_input("**Part Number**", placeholder="ex: 701357018")
        desc = st.text_area("**Descrição**", placeholder="Descreva a peça", height=80)
    
    with col_b:
        qty = st.number_input("**Quantidade**", min_value=1, step=1, value=1)
        material = st.selectbox("**Material**", 
                               ["AW-5083", "Aluminio", "S235JR", "Inox A2", "CHAPA ZINCADA", "Nylon 66", "Outros"])
        tratamento = st.multiselect("**Tratamento**", 
                                   ["Oxicorte", "Torno", "Maquinao", "Laser", "Waterjet", "sim"])
    
    col_btn1, col_btn2 = st.columns([3,1])
    with col_btn1:
        add_button = st.form_submit_button("✅ **ADICIONAR ITEM**", use_container_width=True)
    with col_btn2:
        if st.form_submit_button("🗑️ Limpar Tudo"):
            df = load_bom_data()
            st.success("BOM resetada!")
            st.rerun()
    
    if add_button and part_num:
        new_row = pd.DataFrame({
            "Part_Number": [part_num], 
            "Description": [desc],
            "QTY": [qty], 
            "Material": [material], 
            "Tratamento": [", ".join(tratamento) if tratamento else ""]
        })
        df = pd.concat([df, new_row], ignore_index=True)
        st.success(f"✅ **{part_num}** adicionado com sucesso!")
        st.balloons()
        st.rerun()

# Estatísticas por material
st.subheader("📊 Resumo por Material")
if not df_filtered.empty:
    resumo = df.groupby('Material')['QTY'].sum().sort_values(ascending=False)
    st.bar_chart(resumo)

# Download
st.subheader("💾 Exportar BOM")
csv_data = df.to_csv(index=False).encode('utf-8')
st.download_button(
    "📥 Download CSV Completo",
    csv_data,
    "BOM_MAQ_completa.csv",
    "csv"
)

# Info equipa
st.markdown("---")
st.markdown("""
**👥 Para a Equipa:**
- **Adicionar**: Use o formulário acima
- **Filtrar**: Sidebar à esquerda  
- **Download**: Botão CSV sempre atualizado
- **Acesso**: Partilhe esta URL com todos
""")
