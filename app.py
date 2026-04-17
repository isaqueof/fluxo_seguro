import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
import random

# --- CONFIGURAÇÕES GLOBAIS ---
PAGE_TITLE = "Fluxo Seguro - Centro de Comando Logístico"

# Base de Dados Geográfica Real Expandida
GEO_DATABASE = {
    "Niterói, RJ": [
        {"name": "Av. Visconde do Rio Branco", "lat": -22.8962, "lon": -43.1255},
        {"name": "Rua Moreira César", "lat": -22.9061, "lon": -43.1065},
        {"name": "Av. Roberto Silveira", "lat": -22.9022, "lon": -43.1022},
        {"name": "Rua Gavião Peixoto", "lat": -22.9055, "lon": -43.1055},
        {"name": "Alameda São Boaventura", "lat": -22.8805, "lon": -43.0805},
        {"name": "Av. Quintino Bocaiúva", "lat": -22.9155, "lon": -43.0955},
        {"name": "Rua Dr. Celestino", "lat": -22.8955, "lon": -43.1205},
        {"name": "Rua Benjamin Constant", "lat": -22.8820, "lon": -43.1150},
        {"name": "Av. Sete de Setembro", "lat": -22.9080, "lon": -43.1010},
        {"name": "Estrada Francisco da Cruz Nunes", "lat": -22.9461, "lon": -43.0361},
        {"name": "Rua Santa Rosa", "lat": -22.9010, "lon": -43.1090},
        {"name": "Largo do Marrão", "lat": -22.9035, "lon": -43.1050},
        {"name": "Rua Noronha Torrezão", "lat": -22.9020, "lon": -43.1095},
        {"name": "Rua Lopes Trovão", "lat": -22.9050, "lon": -43.1080},
        {"name": "Av. Ernani do Amaral Peixoto", "lat": -22.8940, "lon": -43.1225},
        {"name": "Rua Dr. Paulo Alves", "lat": -22.9030, "lon": -43.1250},
        {"name": "Av. Rui Barbosa", "lat": -22.9220, "lon": -43.0930},
        {"name": "Estrada Caetano Monteiro", "lat": -22.9125, "lon": -43.0550},
        {"name": "Rua Desembargador Lima Castro", "lat": -22.8780, "lon": -43.1020},
        {"name": "Av. Jansen de Melo", "lat": -22.8900, "lon": -43.1180},
        {"name": "Rua Marechal Deodoro", "lat": -22.8920, "lon": -43.1215},
        {"name": "Av. Almirante Ary Parreiras", "lat": -22.9075, "lon": -43.0970},
        {"name": "Estrada Cel. Miranda", "lat": -22.8800, "lon": -43.1100},
        {"name": "Rua Passos da Pátria", "lat": -22.9050, "lon": -43.1280},
        {"name": "Av. Central Ewerton Xavier", "lat": -22.9400, "lon": -43.0200}
    ],
    "Maricá, RJ": [
        {"name": "Rodovia Amaral Peixoto (RJ-106)", "lat": -22.9105, "lon": -42.8205},
        {"name": "Rua Ribeiro de Almeida", "lat": -22.9194, "lon": -42.8186},
        {"name": "Avenida Ivan Mundin", "lat": -22.9310, "lon": -42.8415},
        {"name": "Avenida Carlos Marighella", "lat": -22.9650, "lon": -42.9250},
        {"name": "Estrada de Itaipuaçu", "lat": -22.9520, "lon": -42.9810},
        {"name": "Rua Domício da Gama", "lat": -22.9180, "lon": -42.8220},
        {"name": "Avenida Maysa", "lat": -22.9450, "lon": -42.7500},
        {"name": "Rua Abreu Rangel", "lat": -22.9185, "lon": -42.8170},
        {"name": "Av. Vitória Régia", "lat": -22.9610, "lon": -42.7050},
        {"name": "Rua Barão de Inoã", "lat": -22.9180, "lon": -42.8215},
        {"name": "Estrada do Boqueirão", "lat": -22.9250, "lon": -42.8055},
        {"name": "Rua Van Lerbergue", "lat": -22.9655, "lon": -42.9455},
        {"name": "Avenida Zumbi dos Palmares", "lat": -22.9700, "lon": -42.9150},
        {"name": "Rua Professor José de Souza Herdy", "lat": -22.9175, "lon": -42.8195},
        {"name": "Avenida Roberto Silveira", "lat": -22.9225, "lon": -42.8255},
        {"name": "Estrada de Cassorotiba", "lat": -22.8855, "lon": -42.8955},
        {"name": "Estrada de Bambuí", "lat": -22.9150, "lon": -42.7455},
        {"name": "Rua Ari Spindola", "lat": -22.9150, "lon": -42.8150},
        {"name": "Estrada do Espraiado", "lat": -22.9300, "lon": -42.7000},
        {"name": "Av. Gilberto de Carvalho", "lat": -22.9250, "lon": -42.9350}
    ]
}

CITY_CENTER = {
    "Niterói, RJ": {"lat": -22.9050, "lon": -43.1050, "zoom": 12.5},
    "Maricá, RJ": {"lat": -22.9200, "lon": -42.8500, "zoom": 12.0}
}

def get_risk_color(risk):
    if risk > 85: return [255, 50, 50, 200]
    if risk > 60: return [255, 140, 0, 180]
    return [0, 204, 150, 100]

# --- LÓGICA DE NEGÓCIO ---

@st.cache_data(show_spinner="Sincronizando malha viária...")
def generate_scenario(city_name, rainfall):
    base_points = GEO_DATABASE[city_name]
    np.random.seed(42)
    random.seed(42)
    
    risk_data = []
    for point in base_points:
        r = float(np.clip(np.random.randint(0, 45) + rainfall, 0, 100))
        risk_data.append({
            "lat": point["lat"],
            "lon": point["lon"],
            "street": point["name"],
            "risk": r,
            "color": get_risk_color(r),
            "radius": 250 if r > 85 else (120 if r > 60 else 60)
        })
        
    df_risk = pd.DataFrame(risk_data)
    
    fleet_data = []
    # Aumentado para 10 caminhões para maior densidade
    for i in range(min(10, len(risk_data))):
        point = risk_data[i]
        truck_id = f"FLUXO-{(i+1)*10}"
        risk_level = point["risk"]
        
        if risk_level > 60:
            status = "BLOQUEIO TOTAL" if risk_level > 85 else "RISCO IMINENTE"
            safe_streets = [p for p in risk_data if p["risk"] < 60 and p["street"] != point["street"]]
            
            if safe_streets:
                recommended_point = random.choice(safe_streets)
            else:
                other_streets = [p for p in risk_data if p["street"] != point["street"]]
                recommended_point = min(other_streets, key=lambda x: x["risk"])
            
            recommended = recommended_point["street"]
            detour = f"Risco em {point['street']}. Desvie agora pela {recommended}."
        else:
            status = "OPERANDO NORMAL"
            detour = "Mantenha a rota planejada. Via segura."
            
        fleet_data.append({
            "truck_id": truck_id,
            "lat": point["lat"],
            "lon": point["lon"],
            "street": point["street"],
            "status": status,
            "risk": risk_level,
            "cargo_value": random.randint(250, 950) * 1000,
            "detour": detour,
            "contact": f"(21) 9{random.randint(8000,9999)}-{random.randint(1000,9999)}"
        })
        
    time_labels = ["Agora", "+30m", "+60m", "+90m", "+120m"]
    vazao_results = {"Tempo": time_labels}
    for i in range(min(4, len(base_points))):
        street_name = base_points[i]["name"]
        start_val = min(100, rainfall + random.randint(10, 25))
        vazao_results[street_name] = [int(start_val * (0.76 ** step)) for step in range(len(time_labels))]
        
    return df_risk, pd.DataFrame(fleet_data), pd.DataFrame(vazao_results).set_index("Tempo")

def format_br(val): 
    return f"R$ {val:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def main():
    st.set_page_config(page_title=PAGE_TITLE, layout="wide", page_icon="🌊")
    st.title("🌊 Fluxo Seguro - Centro de Comando Logístico")
    st.caption("Inteligência Geográfica Real: Monitoramento de Frotas e Riscos Pluviais")
    
    st.sidebar.header("⚙️ Configurações")
    city_name = st.sidebar.selectbox("Escolha a Cidade:", list(GEO_DATABASE.keys()))
    rainfall = st.sidebar.slider("Volume de Chuva (mm/h)", 0, 100, 45)
    
    df_risk, df_fleet, df_vazao = generate_scenario(city_name, rainfall)
    at_risk = df_fleet[df_fleet["risk"] > 60]
    # --- CABEÇALHO DE KPIS (DESIGN FULL COLOR GRADIENT) ---
    st.markdown("""
        <style>
        .kpi-card {
            border-radius: 10px 10px 0 0;
            padding: 20px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            text-align: center;
            color: white !important;
            margin-bottom: 0px;
        }
        .kpi-title { font-size: 12px; font-weight: bold; text-transform: uppercase; opacity: 0.95; color: white !important; }
        .kpi-value { font-size: 30px; font-weight: bold; margin: 5px 0; color: white !important; }
        .kpi-desc { font-size: 11px; opacity: 0.85; color: white !important; }
        
        /* Ajuste para o botão de popover se integrar ao card full color */
        div[data-testid="stPopover"] > button {
            border-top-left-radius: 0px !important;
            border-top-right-radius: 0px !important;
            width: 100%;
            border: none !important;
            background-color: rgba(0,0,0,0.2) !important;
            color: white !important;
            font-size: 12px !important;
            margin-top: 0px;
            transition: 0.3s;
        }
        div[data-testid="stPopover"] > button:hover {
            background-color: rgba(0,0,0,0.4) !important;
        }
        </style>
    """, unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.markdown(f"""
            <div class="kpi-card" style="background: linear-gradient(135deg, #ef4444, #b91c1c);">
                <div class="kpi-title">⚠️ Caminhões em Risco</div>
                <div class="kpi-value">{len(at_risk)}</div>
                <div class="kpi-desc">Alerta Crítico da Frota</div>
            </div>
        """, unsafe_allow_html=True)
        
        if not at_risk.empty:
            with st.popover("🔍 Ver detalhes da frota", use_container_width=True):
                st.write("### 🚛 Veículos Impactados")
                st.table(at_risk[["truck_id", "street", "risk", "status"]].rename(columns={"truck_id": "Caminhão", "street": "Rua", "risk": "Risco (%)", "status": "Status"}))
        else:
            st.markdown("""<div style='text-align:center; font-size:12px; padding:10px; background:#1e1e1e; color:#4ade80; border-radius:0 0 10px 10px; font-weight:bold;'>✅ OPERAÇÃO SEGURA</div>""", unsafe_allow_html=True)

    with c2:
        st.markdown(f"""
            <div class="kpi-card" style="background: linear-gradient(135deg, #f59e0b, #d97706); border-radius: 10px;">
                <div class="kpi-title">📦 Patrimônio Exposto</div>
                <div class="kpi-value">{format_br(at_risk["cargo_value"].sum())}</div>
                <div class="kpi-desc">Carga em Áreas Críticas</div>
            </div>
        """, unsafe_allow_html=True)

    with c3:
        roi_valor = at_risk["cargo_value"].sum() * 0.98
        st.markdown(f"""
            <div class="kpi-card" style="background: linear-gradient(135deg, #10b981, #059669); border-radius: 10px;">
                <div class="kpi-title">💰 Prejuízo Evitado</div>
                <div class="kpi-value">{format_br(roi_valor)}</div>
                <div class="kpi-desc">Economia via Desvios IA</div>
            </div>
        """, unsafe_allow_html=True)

    with c4:
        status_grad = "linear-gradient(135deg, #10b981, #059669)" if rainfall < 50 else \
                     ("linear-gradient(135deg, #f59e0b, #d97706)" if rainfall < 80 else \
                      "linear-gradient(135deg, #ef4444, #b91c1c)")
        st.markdown(f"""
            <div class="kpi-card" style="background: {status_grad}; border-radius: 10px;">
                <div class="kpi-title">🌧️ Intensidade Pluvial</div>
                <div class="kpi-value">{rainfall} mm/h</div>
                <div class="kpi-desc">Monitoramento Climático</div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.divider()
    
    st.subheader(f"🗺️ Situação Geográfica em Tempo Real: {city_name}")
    view_state = pdk.ViewState(
        latitude=CITY_CENTER[city_name]["lat"], 
        longitude=CITY_CENTER[city_name]["lon"], 
        zoom=CITY_CENTER[city_name]["zoom"], pitch=0
    )
    
    layer_risk = pdk.Layer(
        "ScatterplotLayer", df_risk,
        get_position=["lon", "lat"], get_color="color", get_radius="radius", pickable=True
    )
    
    ICON_DATA = {"url": "https://img.icons8.com/color/48/truck.png", "width": 128, "height": 128, "anchorY": 128}
    df_fleet["icon_data"] = [ICON_DATA for _ in range(len(df_fleet))]
    
    layer_trucks = pdk.Layer(
        "IconLayer", df_fleet,
        get_icon="icon_data", get_position=["lon", "lat"],
        get_size=45, pickable=True
    )
    
    st.pydeck_chart(
        pdk.Deck(
            layers=[layer_risk, layer_trucks], 
            initial_view_state=view_state, 
            map_style=None,
            tooltip={
                "html": """
                <div style='font-family: sans-serif; padding: 10px; background-color: #1e1e1e; color: white; border-radius: 5px;'>
                    <b style='font-size: 14px;'>🚚 Caminhão: {truck_id}</b><br/>
                    <hr style='margin: 5px 0;'/>
                    <b>Rua Atual:</b> {street}<br/>
                    <b>Risco:</b> {risk}%<br/>
                    <b>Status:</b> {status}<br/>
                    <div style='margin-top: 5px; color: #3b82f6;'><b>🧭 Desvio:</b> {detour}</div>
                </div>
                """,
                "style": {"backgroundColor": "transparent", "color": "white", "zIndex": 1000}
            }
        )
    )

    st.divider()
    
    col_a, col_b = st.columns([1, 1.2])
    with col_a:
        st.subheader("📉 Previsão de Vazão por Logradouro")
        st.line_chart(df_vazao)
        
    with col_b:
        st.subheader("⚠️ Central de Despacho (Contingência)")
        if len(at_risk) == 0:
            st.success("Operação normalizada. Nenhuma obstrução nas rotas.")
        else:
            for _, truck in at_risk.iterrows():
                with st.expander(f"🚛 {truck['truck_id']} na {truck['street']}", expanded=True):
                    st.error(f"**Situação:** {truck['status']} ({truck['risk']}% de Risco)")
                    detour_address = truck['detour'].split("pela")[-1].strip().replace(".", "")
                    st.info(f"**🧭 Comando de Desvio:** {truck['detour']}")
                    st.success(f"📍 **Endereço da Rota Alternativa:** {detour_address}")
                    st.markdown(f"**📞 Contato:** {truck['contact']} | **📦 Valor:** {format_br(truck['cargo_value'])}")
                    if st.button(f"📲 Notificar Motorista", key=truck['truck_id']):
                        st.toast(f"✅ Alerta e Rota Alternativa enviados para {truck['truck_id']}!")

if __name__ == "__main__":
    main()
