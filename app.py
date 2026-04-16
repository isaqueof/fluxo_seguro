import streamlit as st
import pandas as pd
import numpy as np

# Configuração da Página
st.set_page_config(page_title="Fluxo Seguro - MVP B2B", layout="wide")

st.title("🌊 Fluxo Seguro - Monitoramento Preditivo de Frotas")
st.markdown("Bem-vindo ao painel B2B. A nossa IA calcula o risco de alagamento nas rotas da sua frota com 30 minutos de antecedência.")

# Painel Lateral (Filtros)
st.sidebar.header("⚙️ Controle da Frota")
st.sidebar.markdown("Simule a condição climática para ver o desvio de rota:")
nivel_chuva = st.sidebar.slider("Volume de Chuva Previsto (mm/h)", 0, 100, 10)

# Coordenadas base (Centro de Maricá, RJ)
LAT_BASE = -22.9194
LON_BASE = -42.8186

# Gerar dados fictícios de vias e riscos
np.random.seed(42)
pontos = 100
lats = LAT_BASE + np.random.normal(0, 0.05, pontos)
lons = LON_BASE + np.random.normal(0, 0.05, pontos)

# A IA simulada: quanto mais chuva, maior o risco
risco_base = np.random.randint(0, 50, pontos)
risco_atual = risco_base + nivel_chuva

# Definindo cores baseadas no risco (Verde = Seguro, Vermelho = Alagamento)
cores = []
tamanhos = []
for r in risco_atual:
    if r > 85:
        cores.append("#FF0000") # Vermelho (Alerta Máximo - Rota Bloqueada)
        tamanhos.append(300)
    elif r > 60:
        cores.append("#FFA500") # Laranja (Atenção)
        tamanhos.append(150)
    else:
        cores.append("#00FF00") # Verde (Via Livre)
        tamanhos.append(50)

df_vias = pd.DataFrame({
    "lat": lats,
    "lon": lons,
    "risco": risco_atual,
    "cor": cores,
    "tamanho": tamanhos
})

# Exibição do Mapa
st.subheader("🗺️ Mapa de Calor - Alerta de Vias")
# O Streamlit renderiza o mapa com as cores e tamanhos definidos
st.map(df_vias, latitude="lat", longitude="lon", color="cor", size="tamanho")

# Métricas de Economia Simulada
st.divider()
st.subheader("📊 Relatório de Proteção (Tempo Real)")
col1, col2, col3 = st.columns(3)
col1.metric("Veículos em Rota", "45 caminhões")
col2.metric("Rotas Desviadas pela IA", f"{len(df_vias[df_vias['risco'] > 85])} rotas")
col3.metric("Prejuízo Evitado", f"R$ {len(df_vias[df_vias['risco'] > 85]) * 15000:,.2f}")