import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")
st.title("🔩 BOM Máquina 2 - FUNCIONANDO!")

# Dados base da BOM (do seu Excel)
data = {
    "Part_Number": ["701357018", "801357017", "501319004", "701357030", "501357007"],
    "Descrição": [
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
df = pd.DataFrame(data)

# CORRIGIDO: Filtros simples e seguros
st.sidebar.header("🔍 Filtros")
material_filter = st.sidebar.multiselect("Material", df['Material'].unique(), default=df['Material'].unique())
tratamento_filter = st.sidebar.multiselect("Tratamento", ["sim", "Laser", "Oxicorte", "Torno"])

# FILTRO CORRIGIDO - SEM ERRO
if material_filter or not tratamento_filter:
    df_filtered = df[df['Material'].isin(material_filter)]
    if tratamento_filter:
        df_filtered = df_filtered[df_filtered['Tratamento'].isin(tratamento_filter)]
else:
    df_filtered = df

# Métricas
col1, col2, col3 = st.columns(3)
col1.metric("📦 Total Peças", len(df_filtered))
col2.metric("🔢 Total QTY", int(df_filtered['QTY'].sum()))
col3.metric("🏭 Materiais", len(df_filtered['Material'].unique()))

# Tabela principal
st.subheader("📋 Lista BOM")
st.dataframe(df_filtered, use_container_width=True, height=400)

# Form adicionar item
st.subheader("➕ Adicionar Peça")
with st.form("add_item", clear_on_submit=True):
    col1, col2 = st.columns(2)
    with col1:
        part = st.text_input("Part Number", placeholder="ex: 701357018")
        desc = st.text_input("Descrição", placeholder="Descreva a peça")
    with col2:
        qty = st.number_input("Quantidade", min_value=1, value=1)
        material = st.selectbox("Material", df['Material'].unique().tolist() + ["Novo"])
    
    submitted = st.form_submit_button("✅ ADICIONAR", use_container_width=True)
    if submitted and part:
        new_row = pd.DataFrame({
            "Part_Number": [part], 
            "Descrição": [desc], 
            "QTY": [qty], 
            "Material": [material],
            "Tratamento": [""]
        })
        df = pd.concat([df, new_row], ignore_index=True)
        st.success("✅ Peça adicionada!")
        st.balloons()
        st.rerun()

# Download
st.subheader("💾 Exportar")
csv = df.to_csv(index=False, encoding='utf-8')
st.download_button("📥 Download CSV", csv, "BOM_MAQ.csv", "csv")
st.info("👥 **Partilhe esta URL com a equipa!**")


