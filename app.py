import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(layout="wide", page_title="BOM Máquina 2")
st.title("🔩👷 **Gestor BOM - Máquina 2 MAQ**")
st.markdown("---")

# ÍCONE DA MÁQUINA (EMOJI como imagem)
st.markdown("![Máquina](https://img.shields.io/badge/Máquina-2_MAQ-brightgreen)")

# Dados COMPLETOS da vossa BOM (do Excel)
@st.cache_data
def load_bom():
    data = {
        "Part_Number": ["701357018", "801357017", "501319004", "701357030", "501357007", "701325025"],
        "Descrição": [
            "CALIBRE POSICIONAMENTO 3.3547 AW-5083",
            "ESTRUTURA MAQUINA Componentes Estruturais", 
            "PERFIL ALUMNIO 45X90MM x 2260 mm",
            "LATERAL INTERIOR CHAPA ZINCADA", 
            "TAPETE XP 304.8mm x 6M S235JR",
            "ROLO - SUPORTE ROLO"
        ],
        "QTY": [1, 1, 2, 2, 1, 4],
        "Material": ["AW-5083", "Estrutural", "Aluminio", "Chapa Zincada", "S235JR", "Aço"],
        "Tratamento": ["sim", "sim", "", "Laser", "", "Torno"],
        "Stock": ["OK", "OK", "Baixo", "OK", "OK", "OK"]
    }
    return pd.DataFrame(data)

df = load_bom()

# SIDEBAR FILTROS
st.sidebar.header("🔍 **Filtros**")
material_filter = st.sidebar.multiselect("Material", df['Material'].unique())
stock_filter = st.sidebar.multiselect("Stock", df['Stock'].unique())

# APLICAR FILTROS
df_filtered = df.copy()
if material_filter:
    df_filtered = df_filtered[df_filtered['Material'].isin(material_filter)]
if stock_filter:
    df_filtered = df_filtered[df_filtered['Stock'].isin(stock_filter)]

# MÉTRICAS
col1, col2, col3, col4 = st.columns(4)
col1.metric("📦 Total Peças", len(df_filtered), delta=1)
col2.metric("🔢 Total QTY", int(df_filtered['QTY'].sum()))
col3.metric("⚠️ Stock Baixo", len(df_filtered[df_filtered['Stock']=='Baixo']))
col4.metric("🏭 Materiais", df_filtered['Material'].nunique())

# TABELA PRINCIPAL
st.subheader("📋 **Lista Completa BOM**")
st.dataframe(df_filtered, use_container_width=True, height=400)

# FORM ADICIONAR
st.subheader("➕ **Adicionar Nova Peça**")
with st.form("nova_peca"):
    col_a, col_b = st.columns(2)
    with col_a:
        part_num = st.text_input("**Part Number**", placeholder="701357019")
        desc = st.text_area("**Descrição**", height=60)
    with col_b:
        qty = st.number_input("**QTY**", min_value=1, value=1)
        material = st.selectbox("**Material**", df['Material'].unique())
        stock = st.selectbox("**Stock**", ["OK", "Baixo", "Esgotado"])
        tratamento = st.multiselect("**Tratamento**", ["sim", "Laser", "Torno", "Oxicorte"])
    
    col_btn1, _ = st.columns(2)
    with col_btn1:
        add_btn = st.form_submit_button("✅ **ADICIONAR PEÇA**", use_container_width=True)
    
    if add_btn and part_num:
        new_row = pd.DataFrame({
            "Part_Number": [part_num], "Descrição": [desc], "QTY": [qty],
            "Material": [material], "Tratamento": [", ".join(tratamento)], "Stock": [stock]
        })
        df = pd.concat([df, new_row], ignore_index=True)
        st.success(f"✅ **{part_num}** adicionado!")
        st.balloons()
        st.rerun()

# GRÁFICO
st.subheader("📊 **Resumo por Material**")
resumo = df.groupby('Material')['QTY'].sum()
st.bar_chart(resumo)

# DOWNLOAD
st.subheader("💾 **Exportar BOM**")
csv = df.to_csv(index=False, encoding='utf-8').encode()
st.download_button("📥 CSV Completo", csv, "BOM_MAQ_COMPLETA.csv", "csv")

# INFO EQUIPE
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: green; font-weight: bold'>
👥 **INSTRUÇÕES PARA A EQUIPE:**
• 🔍 Use filtros na barra lateral
• ➕ Adicione peças novas no formulário
• 📥 Faça download sempre atualizado
• 📱 Funciona em telemóvel!
</div>
""")

# RODAPÉ
st.markdown("---")
st.markdown("*Aplicação BOM Máquina 2 - Online 24/7*")
