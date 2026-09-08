# ==========================================================
# AI SMART SURVEILLANCE — PREMIUM LANDSCAPE v4.0
# Cyberpunk Command Center | Satellite Map | Neon UI
# ==========================================================
import streamlit as st
import pandas as pd
import numpy as np
import ast, re, warnings
import plotly.express as px
import plotly.graph_objects as go
from io import StringIO
from sklearn.ensemble import IsolationForest
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler
from datetime import datetime
warnings.filterwarnings("ignore")

st.set_page_config(
    page_title="AI Smart Surveillance",
    page_icon="🚔",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==========================================================
# PREMIUM CYBERPUNK CSS
# ==========================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;600;700;800;900&family=Inter:wght@300;400;500;600;700&family=Share+Tech+Mono&display=swap');

/* ── Reset & Global ───────────────────────────────────── */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
html, body { overflow-x: hidden; }
body { background: #020812 !important; }
.stApp {
    background: #020812 !important;
    background-image:
        linear-gradient(rgba(0,212,255,0.04) 1px, transparent 1px),
        linear-gradient(90deg, rgba(0,212,255,0.04) 1px, transparent 1px) !important;
    background-size: 40px 40px !important;
    font-family: 'Inter', sans-serif !important;
}

/* ── Remove ALL Streamlit chrome ─────────────────────── */
#MainMenu, header, footer, [data-testid="collapseSidebar"],
button[data-testid="baseButton-headerNoPadding"],
[data-testid="stToolbar"], .streamlit-wide,
section[data-testid="stSidebar"] { display: none !important; }

/* ── Main container — zero padding ───────────────────── */
.main .block-container {
    padding: 0 !important; max-width: 100% !important;
    margin: 0 !important; width: 100% !important;
}

/* ── Scrollbar ────────────────────────────────────────── */
::-webkit-scrollbar { width: 4px; height: 4px; }
::-webkit-scrollbar-track { background: #020812; }
::-webkit-scrollbar-thumb { background: rgba(0,212,255,0.4); border-radius: 2px; }

/* ── Neon text glow ───────────────────────────────────── */
.neon-cyan { color: #00d4ff; text-shadow: 0 0 8px #00d4ff, 0 0 20px rgba(0,212,255,0.5); }
.neon-green { color: #00ff88; text-shadow: 0 0 8px #00ff88; }
.neon-orange { color: #ff6b35; text-shadow: 0 0 8px #ff6b35; }
.neon-red { color: #ff1744; text-shadow: 0 0 10px #ff1744; }

/* ── Panel card ───────────────────────────────────────── */
.panel {
    background: linear-gradient(135deg, rgba(0,20,50,0.95), rgba(0,10,30,0.98));
    border: 1px solid rgba(0,212,255,0.25);
    border-radius: 8px;
    box-shadow: 0 0 20px rgba(0,212,255,0.08), inset 0 1px 0 rgba(0,212,255,0.1);
    padding: 12px 14px;
    position: relative;
    overflow: hidden;
}
.panel::before {
    content: ''; position: absolute; top: 0; left: 0; right: 0; height: 1px;
    background: linear-gradient(90deg, transparent, #00d4ff, transparent);
}

/* ── KPI card ─────────────────────────────────────────── */
.kpi-top {
    background: linear-gradient(135deg, rgba(0,25,60,0.95), rgba(0,15,40,0.95));
    border: 1px solid rgba(0,212,255,0.3); border-radius: 6px;
    padding: 8px 14px; text-align: center; min-width: 120px;
    box-shadow: 0 0 15px rgba(0,212,255,0.12);
}
.kpi-top .k-label { font-size: 9px; font-weight: 700; letter-spacing: 1.5px;
    text-transform: uppercase; color: #7ab8e8; font-family:'Inter'; }
.kpi-top .k-val { font-size: 28px; font-weight: 900; line-height: 1.1;
    font-family: 'Orbitron', monospace; }
.kpi-top .k-icon { font-size: 16px; margin-bottom: 2px; }

/* ── Nav item ─────────────────────────────────────────── */
.nav-item {
    display: flex; flex-direction: column; align-items: center; justify-content: center;
    padding: 10px 6px; border-radius: 8px; margin: 4px 0; cursor: pointer;
    border: 1px solid transparent; transition: all 0.3s; text-decoration: none;
}
.nav-item:hover, .nav-item.active {
    background: rgba(0,212,255,0.12); border-color: rgba(0,212,255,0.35);
    box-shadow: 0 0 12px rgba(0,212,255,0.2);
}
.nav-icon { font-size: 18px; }
.nav-label { font-size: 8px; color: #7ab8e8; font-weight: 700; letter-spacing: 1px;
    text-transform: uppercase; margin-top: 3px; font-family:'Inter'; }

/* ── Alert row ────────────────────────────────────────── */
.alert-row {
    display: flex; align-items: center; gap: 8px;
    padding: 6px 10px; border-radius: 6px; margin-bottom: 5px;
    border-left: 3px solid;
}
.alert-row .ar-id { font-size: 11px; font-weight: 800; font-family: 'Share Tech Mono', monospace; }
.alert-row .ar-badge {
    font-size: 9px; font-weight: 700; letter-spacing: 1px;
    padding: 2px 7px; border-radius: 3px; text-transform: uppercase;
}
.alert-row .ar-time { font-size: 10px; color: #7ab8e8; margin-left: auto; }

/* ── Section heading ──────────────────────────────────── */
.sec-head {
    font-family: 'Orbitron', monospace; font-size: 11px; font-weight: 700;
    letter-spacing: 2px; text-transform: uppercase; color: #00d4ff;
    text-shadow: 0 0 8px rgba(0,212,255,0.6);
    border-bottom: 1px solid rgba(0,212,255,0.2);
    padding-bottom: 6px; margin-bottom: 10px;
}

/* ── Bottom info card ─────────────────────────────────── */
.info-card {
    background: linear-gradient(135deg,rgba(0,20,50,0.9),rgba(0,10,28,0.95));
    border: 1px solid rgba(0,212,255,0.2); border-radius: 8px;
    padding: 12px 14px; height: 100%;
    box-shadow: 0 0 15px rgba(0,212,255,0.06);
}
.info-card h4 {
    font-family: 'Orbitron'; font-size: 10px; font-weight: 700;
    letter-spacing: 2px; text-transform: uppercase; color: #00d4ff;
    margin-bottom: 10px; padding-bottom: 6px;
    border-bottom: 1px solid rgba(0,212,255,0.2);
}

/* ── Flow box ─────────────────────────────────────────── */
.flow-box {
    background: rgba(0,25,60,0.8); border: 1px solid rgba(0,212,255,0.3);
    border-radius: 6px; padding: 6px 10px; font-size: 10px; color: #c8e8ff;
    text-align: center; font-weight: 600; font-family:'Inter';
}
.flow-arrow { color: #00d4ff; font-size: 14px; text-align: center; line-height: 1; }

/* ── Detect check ─────────────────────────────────────── */
.det-row {
    display: flex; align-items: center; gap: 8px; padding: 4px 0;
    font-size: 11px; color: #c8e8ff; font-family: 'Inter';
    border-bottom: 1px solid rgba(0,212,255,0.08);
}
.det-row:last-child { border-bottom: none; }
.det-check { color: #00ff88; font-size: 13px; }

/* ── Live badge ───────────────────────────────────────── */
.dataset-badge {
    display: inline-flex; align-items: center; gap: 5px;
    background: rgba(0,255,136,0.08); border: 1px solid rgba(0,255,136,0.3);
    border-radius: 4px; padding: 3px 10px; font-size: 10px; font-weight: 700;
    color: #00ff88; letter-spacing: 1px; text-transform: uppercase; font-family:'Inter';
}
.live-dot { width: 6px; height: 6px; background: #00ff88; border-radius: 50%;
    box-shadow: 0 0 6px #00ff88; animation: blink 1.2s infinite; }
@keyframes blink { 0%,100%{opacity:1;} 50%{opacity:0.2;} }

/* ── Plotly charts transparent ────────────────────────── */
.js-plotly-plot, .plotly { background: transparent !important; }

/* ── Streamlit widget overrides ───────────────────────── */
[data-testid="stSlider"] [data-testid="stWidgetLabel"] p { color:#7ab8e8 !important; font-size:11px !important; }
[data-testid="stSlider"] * { color:#c8e8ff !important; }
[data-baseweb="select"] { background:rgba(0,15,40,0.9) !important; border-color:rgba(0,212,255,0.3) !important; }
[data-baseweb="select"] * { color:#c8e8ff !important; }
[data-testid="stWidgetLabel"] p { color:#7ab8e8 !important; font-size:11px !important; font-weight:600 !important; }
.stDownloadButton button {
    background: linear-gradient(135deg,#003580,#005ec2) !important;
    border: 1px solid rgba(0,212,255,0.4) !important; border-radius:6px !important;
    color: white !important; font-weight:700 !important; font-size:11px !important;
    box-shadow: 0 0 12px rgba(0,212,255,0.2) !important;
}
[data-testid="stDataFrame"] * { color: #c8e8ff !important; font-size:11px !important; }
[data-testid="stTabs"] [data-baseweb="tab"] { color:#7ab8e8 !important; font-weight:600 !important; background:transparent !important; font-size:11px !important; }
[data-testid="stTabs"] [aria-selected="true"][data-baseweb="tab"] { color:#00d4ff !important; font-weight:700 !important; }
[data-testid="stTabs"] [data-baseweb="tab-list"] { background:rgba(0,15,40,0.7) !important; border:1px solid rgba(0,212,255,0.15) !important; border-radius:6px !important; }
[data-testid="stAlert"] p, [data-testid="stAlert"] * { color:white !important; }
p, span, div { color: #c8e8ff; }
h1,h2,h3,h4,h5,h6 { color: #ffffff !important; }
[data-testid="stMarkdownContainer"] h1,[data-testid="stMarkdownContainer"] h2,
[data-testid="stMarkdownContainer"] h3,[data-testid="stMarkdownContainer"] h4 { color:#ffffff !important; }
[data-testid="metric-container"] { background:rgba(0,20,55,0.8) !important; border:1px solid rgba(0,212,255,0.25) !important; border-radius:8px !important; }
[data-testid="stMetricValue"] * { color:white !important; font-weight:800 !important; }
[data-testid="stMetricLabel"] * { color:#7ab8e8 !important; font-size:10px !important; }
</style>
""", unsafe_allow_html=True)

# ==========================================================
# HELPERS
# ==========================================================
CLR = {"CRITICAL":"#ff1744","HIGH":"#ff6b35","MEDIUM":"#ffc107","LOW":"#00ff88"}
PLT = dict(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
           font=dict(color="#c8e8ff", family="Inter", size=11),
           legend=dict(font=dict(color="#c8e8ff"), bgcolor="rgba(0,0,0,0)"),
           margin=dict(t=10,b=5,l=5,r=5))
AX = dict(gridcolor="rgba(0,212,255,0.08)", color="#7ab8e8", tickfont=dict(color="#c8e8ff", size=10),
          linecolor="rgba(0,212,255,0.2)", zerolinecolor="rgba(0,212,255,0.1)")
now_str = datetime.now().strftime("%d %b %Y  %H:%M:%S IST")

def find_csv():
    for n in ["dashboard_dataset.csv","surveillance_features.csv","data.csv"]:
        try: return pd.read_csv(n), n
        except: continue
    return None, None

# ==========================================================
# DATA LOAD / UPLOAD
# ==========================================================
_found, _fname = find_csv()
if _found is None:
    st.markdown("""<div style="display:flex;align-items:center;justify-content:center;height:100vh;
    background:#020812;flex-direction:column;gap:20px;">
    <div style="font-size:60px;">📂</div>
    <h2 style="color:#00d4ff;font-family:Orbitron;letter-spacing:2px;">DATASET REQUIRED</h2>
    <p style="color:#7ab8e8;font-size:14px;">Upload surveillance_features.csv to launch the dashboard</p>
    </div>""", unsafe_allow_html=True)
    up = st.file_uploader("Upload CSV", type=["csv"])
    if up:
        with open("dashboard_dataset.csv","wb") as f: f.write(up.read())
        st.success("✅ Uploaded! Refreshing..."); st.rerun()
    st.stop()

@st.cache_data
def load_data():
    df, _ = find_csv()
    df.columns = df.columns.str.upper().str.strip()
    for c in ["DATETIME","TIMESTAMP"]:
        if c in df.columns:
            df[c] = pd.to_datetime(df[c], errors="coerce")
            df["TIMESTAMP"] = df[c]; break
    if "TIMESTAMP" in df.columns:
        df["HOUR"] = df["TIMESTAMP"].dt.hour
        df["DAY"]  = df["TIMESTAMP"].dt.day_name()
        df["DATE"] = df["TIMESTAMP"].dt.date
    r = {"TOTAL_DISTANCE_KM":"TRIP_DISTANCE","DURATION_MIN":"TRAVEL_TIME"}
    for o,n in r.items():
        if o in df.columns: df.rename(columns={o:n}, inplace=True)
    if "TRIP_ID" not in df.columns:
        df["TRIP_ID"] = df.get("VEHICLE_ID", pd.Series([f"VEH-{i:05d}" for i in range(len(df))]))
    df["RISK_LEVEL"] = df["RISK_LEVEL"].astype(str).str.upper().str.strip()
    if "CRITICAL" not in df["RISK_LEVEL"].unique() and "RISK_SCORE" in df.columns:
        df.loc[df["RISK_SCORE"]>=85,"RISK_LEVEL"]="CRITICAL"
    if "PEAK_HOUR" not in df.columns and "HOUR" in df.columns:
        df["PEAK_HOUR"] = df["HOUR"].apply(lambda h:"Peak" if h in list(range(7,10))+list(range(17,20)) else "Off-Peak")
    if "TRIP_TYPE" not in df.columns:
        df["TRIP_TYPE"] = df.apply(lambda r:"Commercial" if r.get("TRIP_DISTANCE",10)>20 else("Short" if r.get("TRIP_DISTANCE",10)<5 else "Standard"),axis=1)
    fcols=[c for c in ["PARKING_ANOMALY","SPEED_ANOMALY","ROUTE_DEVIATION","RESTRICTED_ZONE_ENTRY","COORDINATED_MOVEMENT"] if c in df.columns]
    df["FLAG_COUNT"] = df[fcols].sum(axis=1) if fcols else 0
    df["SUSPICION_SCORE"]=(df["RISK_SCORE"].fillna(0)*0.5+df["FLAG_COUNT"]*8+
                           df.get("RZ_HIT_COUNT",pd.Series(0,index=df.index)).fillna(0)*2).round(1)
    return df

df = load_data()

# ==========================================================
# METRICS
# ==========================================================
total=len(df); crit=(df["RISK_LEVEL"]=="CRITICAL").sum()
high=(df["RISK_LEVEL"]=="HIGH").sum(); med=(df["RISK_LEVEL"]=="MEDIUM").sum()
low=(df["RISK_LEVEL"]=="LOW").sum(); low_risk=low
avg_risk=round(df["RISK_SCORE"].mean(),1); max_risk=round(df["RISK_SCORE"].max(),1)
avg_spd=round(df["AVG_SPEED_KMH"].mean(),1); max_spd=round(df["MAX_SPEED_KMH"].mean(),1) if "MAX_SPEED_KMH" in df.columns else 0
active_alerts=crit+high
rz=int(df["RESTRICTED_ZONE_ENTRY"].sum()) if "RESTRICTED_ZONE_ENTRY" in df.columns else 0
sp=int(df["SPEED_ANOMALY"].sum()) if "SPEED_ANOMALY" in df.columns else 0
pk=int(df["PARKING_ANOMALY"].sum()) if "PARKING_ANOMALY" in df.columns else 0
rd=int(df["ROUTE_DEVIATION"].sum()) if "ROUTE_DEVIATION" in df.columns else 0
cm=int(df["COORDINATED_MOVEMENT"].sum()) if "COORDINATED_MOVEMENT" in df.columns else 0

# Top recent alerts
recent_alerts = df.nlargest(6,"RISK_SCORE")[["TRIP_ID","RISK_LEVEL","RISK_SCORE"]].values.tolist()

# ==========================================================
# ① HEADER BAR
# ==========================================================
st.markdown(f"""
<div style="background:linear-gradient(90deg,#020c1e,#031628 30%,#041e38 60%,#031628 80%,#020c1e);
border-bottom:2px solid rgba(0,212,255,0.4);padding:10px 20px;
display:flex;align-items:center;justify-content:space-between;
box-shadow:0 2px 30px rgba(0,212,255,0.15);">

  <!-- Left: Logo + Title -->
  <div style="display:flex;align-items:center;gap:14px;">
    <div style="width:42px;height:42px;background:rgba(0,212,255,0.1);border:2px solid rgba(0,212,255,0.5);
    border-radius:8px;display:flex;align-items:center;justify-content:center;font-size:22px;
    box-shadow:0 0 15px rgba(0,212,255,0.3);">🚔</div>
    <div>
      <div style="font-family:Orbitron;font-size:16px;font-weight:900;color:#00d4ff;
      text-shadow:0 0 12px rgba(0,212,255,0.7);letter-spacing:2px;">AI POWERED SMART SURVEILLANCE PROTOTYPE</div>
      <div style="font-size:10px;color:#7ab8e8;letter-spacing:3px;font-weight:600;margin-top:1px;">
        SUSPICIOUS VEHICLE DETECTION SYSTEM</div>
    </div>
  </div>

  <!-- Center: KPI Cards -->
  <div style="display:flex;gap:10px;align-items:center;">
    <div class="kpi-top">
      <div class="k-icon">🚗</div>
      <div class="k-label">Total Vehicles</div>
      <div class="k-val" style="color:#00d4ff;">{total:,}</div>
    </div>
    <div class="kpi-top">
      <div class="k-icon">🟢</div>
      <div class="k-label">Low Risk</div>
      <div class="k-val" style="color:#00ff88;">{low_risk:,}</div>
    </div>
    <div class="kpi-top">
      <div class="k-icon">⚠️</div>
      <div class="k-label">Medium Risk</div>
      <div class="k-val" style="color:#ffc107;">{med:,}</div>
    </div>
    <div class="kpi-top">
      <div class="k-icon">🔺</div>
      <div class="k-label">High Risk</div>
      <div class="k-val" style="color:#ff6b35;">{high:,}</div>
    </div>
    <div class="kpi-top" style="border-color:rgba(255,23,68,0.5);box-shadow:0 0 15px rgba(255,23,68,0.2);">
      <div class="k-icon">🚨</div>
      <div class="k-label">Active Alerts</div>
      <div class="k-val" style="color:#ff1744;">{active_alerts:,}</div>
    </div>
  </div>

  <!-- Right: Status -->
  <div style="text-align:right;">
    <div class="dataset-badge"><div class="dataset-dot"></div> DATASET MODE</div>
    <div style="font-size:10px;color:#7ab8e8;margin-top:5px;font-family:Share Tech Mono;">DATASET: 19,599 TRIPS</div>
    <div style="font-size:9px;color:#004080;margin-top:2px;">Mode: <span style="color:#00ff88;">PROTOTYPE ANALYSIS</span></div>
  </div>
</div>
""", unsafe_allow_html=True)

# ==========================================================
# ② MAIN CONTENT — 3 columns: Nav | Map | Analytics
# ==========================================================
nav_col, map_col, analytics_col = st.columns([1, 9, 4])

# ── LEFT NAV ──────────────────────────────────────────────
with nav_col:
    st.markdown("""
    <div style="background:linear-gradient(180deg,#020c1e,#020810);
    border-right:1px solid rgba(0,212,255,0.2);height:100%;padding:12px 6px;
    display:flex;flex-direction:column;align-items:center;gap:4px;min-height:520px;">

      <div style="font-size:10px;color:#00d4ff;font-family:Orbitron;font-weight:700;
      letter-spacing:2px;text-align:center;margin-bottom:10px;writing-mode:horizontal-tb;">
        SMART<br>SURVEILLANCE</div>

      <div class="nav-item active"><div class="nav-icon">🗺️</div><div class="nav-label">MAP VIEW</div></div>
      <div class="nav-item"><div class="nav-icon">🚗</div><div class="nav-label">VEHICLES</div></div>
      <div class="nav-item"><div class="nav-icon">🔔</div><div class="nav-label">ALERTS</div></div>
      <div class="nav-item"><div class="nav-icon">📊</div><div class="nav-label">ANALYTICS</div></div>
      <div class="nav-item"><div class="nav-icon">🚫</div><div class="nav-label">ZONES</div></div>
      <div class="nav-item"><div class="nav-icon">📋</div><div class="nav-label">HISTORY</div></div>
      <div class="nav-item"><div class="nav-icon">⚙️</div><div class="nav-label">SETTINGS</div></div>
    </div>
    """, unsafe_allow_html=True)

# ── CENTER MAP ─────────────────────────────────────────────
with map_col:
    map_sample = st.slider("Map Sample Size", 100, 800, 350, 50, key="mapsz",
                           help="Number of vehicles to show on map")

    @st.cache_data
    def build_plotly_map(djson, n):
        dm = pd.read_json(StringIO(djson))
        samp = dm.sample(min(n, len(dm)), random_state=42).copy()
        if "LATITUDE" not in samp.columns:
            rng = np.random.default_rng(42)
            samp["LATITUDE"]  = rng.normal(41.1579, 0.035, len(samp))
            samp["LONGITUDE"] = rng.normal(-8.6291, 0.045, len(samp))
        samp["LATITUDE"]   = pd.to_numeric(samp["LATITUDE"],  errors="coerce")
        samp["LONGITUDE"]  = pd.to_numeric(samp["LONGITUDE"], errors="coerce")
        samp = samp.dropna(subset=["LATITUDE","LONGITUDE"])
        samp["RISK_LEVEL"] = samp["RISK_LEVEL"].astype(str).str.upper()
        samp["RISK_SCORE"] = pd.to_numeric(samp.get("RISK_SCORE", 0), errors="coerce").fillna(0)
        samp["TRIP_ID"]    = samp["TRIP_ID"].astype(str).str[:14]
        clr = {"CRITICAL":"#ff1744","HIGH":"#ff6b35","MEDIUM":"#ffc107","LOW":"#00ff88"}
        szm = {"CRITICAL":14,"HIGH":10,"MEDIUM":7,"LOW":5}
        samp["_color"] = samp["RISK_LEVEL"].map(clr).fillna("#00d4ff")
        samp["_size"]  = samp["RISK_LEVEL"].map(szm).fillna(5)
        fig = go.Figure()
        for rl, grp in samp.groupby("RISK_LEVEL"):
            fig.add_trace(go.Scattermap(
                lat=grp["LATITUDE"], lon=grp["LONGITUDE"],
                mode="markers", name=rl,
                marker=dict(size=grp["_size"], color=clr.get(rl,"#00d4ff"), opacity=0.85),
                text=grp["TRIP_ID"]+"<br>Risk: "+grp["RISK_SCORE"].astype(int).astype(str)+"/100",
                hovertemplate="<b>%{text}</b><br>Lat: %{lat:.4f}<br>Lon: %{lon:.4f}<extra>"+rl+"</extra>"
            ))
        fig.update_layout(
            map=dict(style="dark",
                     center=dict(lat=samp["LATITUDE"].mean(), lon=samp["LONGITUDE"].mean()),
                     zoom=11),
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(t=0,b=0,l=0,r=0), height=480,
            legend=dict(bgcolor="rgba(0,15,40,.85)",bordercolor="rgba(0,212,255,.3)",
                        borderwidth=1,font=dict(color="#c8e8ff",size=10)),
            font=dict(color="#c8e8ff")
        )
        return fig

    fig_map = build_plotly_map(df.to_json(), map_sample)
    st.plotly_chart(fig_map, use_container_width=True, config={"displayModeBar":False}, key="main_map")

    # ── Map bottom status bar ──────────────────────────────
    st.markdown(f"""
    <div style="background:rgba(0,15,40,0.9);border:1px solid rgba(0,212,255,0.2);
    border-radius:0 0 8px 8px;padding:6px 16px;display:flex;gap:24px;align-items:center;
    margin-top:-6px;font-size:10px;">
      <div class="dataset-badge"><div class="dataset-dot"></div> DATASET MODE</div>
      <span style="color:#7ab8e8;">📍 Last Update: <b style="color:#00d4ff;">3 sec ago</b></span>
      <span style="color:#7ab8e8;">🗺️ Vehicles on Map: <b style="color:#00d4ff;">{min(map_sample,total):,}</b></span>
      <span style="color:#7ab8e8;">🔴 Critical: <b style="color:#ff1744;">{crit}</b></span>
      <span style="color:#7ab8e8;">🟠 High: <b style="color:#ff6b35;">{high}</b></span>
      <span style="color:#7ab8e8;">System Status: <b style="color:#00ff88;">ONLINE</b></span>
    </div>
    """, unsafe_allow_html=True)

# ── RIGHT ANALYTICS PANEL ──────────────────────────────────
with analytics_col:
    # Detection Engine
    st.markdown("""<div class='sec-head'>🔍 AI ANALYTICS</div>""", unsafe_allow_html=True)
    st.markdown(f"""
    <div class="panel" style="margin-bottom:10px;">
      <div style="font-size:10px;font-weight:700;color:#7ab8e8;letter-spacing:1px;margin-bottom:8px;">DETECTION ENGINE</div>
      {''.join([
        f'<div class="det-row"><span class="det-check">✓</span><span style="flex:1;">{lbl}</span><span style="color:#ffc107;font-weight:700;font-size:10px;">{cnt:,}</span></div>'
        for lbl,cnt in [
          ("Long Parking Detected", pk),
          ("Restricted Zone Entry", rz),
          ("Circular Movement",     cm),
          ("Speed Anomaly",         sp),
          ("Route Deviation",       rd),
          ("Speed Spikes",          int(df["SPEED_SPIKES"].sum()) if "SPEED_SPIKES" in df.columns else 0),
          ("Coordinated Movement",  cm),
        ]
      ])}
    </div>
    """, unsafe_allow_html=True)

    # Risk Distribution donut
    risk_counts = df["RISK_LEVEL"].value_counts()
    fig_donut = go.Figure(go.Pie(
        labels=list(risk_counts.index), values=list(risk_counts.values), hole=0.62,
        marker=dict(colors=[CLR.get(r,"#aaa") for r in risk_counts.index],
                    line=dict(color="#020812",width=2)),
        textfont=dict(color="white",size=10),
        textposition="outside", textinfo="percent"
    ))
    fig_donut.update_layout(**PLT, height=170,
        annotations=[dict(text=f"<b>{total:,}</b><br><span style='font-size:9px;'>Total</span>",
                         x=0.5,y=0.5,font=dict(size=14,color="white"),showarrow=False)],
        showlegend=True,
        legend=dict(orientation="v",x=1,y=0.5,font=dict(size=9,color="#c8e8ff")))
    st.markdown('<div style="font-size:10px;font-weight:700;color:#7ab8e8;letter-spacing:1px;margin:4px 0 2px;">RISK DISTRIBUTION</div>', unsafe_allow_html=True)
    st.plotly_chart(fig_donut, use_container_width=True)

    # Recent Alerts
    st.markdown('<div class="sec-head" style="margin-top:6px;">🚨 RECENT ALERTS</div>', unsafe_allow_html=True)
    for trip_id, risk, score in recent_alerts:
        color = CLR.get(risk,"#aaa")
        bg = f"{color}15"
        st.markdown(f"""
        <div class="alert-row" style="background:{bg};border-left-color:{color};">
          <div class="ar-id" style="color:{color};">{str(trip_id)[:12]}</div>
          <div class="ar-badge" style="background:{color}22;color:{color};border:1px solid {color}44;">{risk}</div>
          <div class="ar-time">{score:.0f}/100</div>
        </div>""", unsafe_allow_html=True)

# ==========================================================
# ③ ANALYTICS TABS — Full width below
# ==========================================================
st.markdown('<div style="height:8px;"></div>', unsafe_allow_html=True)
st.markdown('<div style="font-family:Orbitron;font-size:10px;font-weight:700;letter-spacing:2px;color:#00d4ff;padding:4px 8px;border-left:3px solid #00d4ff;margin-bottom:8px;">📊 ADVANCED ANALYTICS ENGINE</div>', unsafe_allow_html=True)

tab_overview, tab_temporal, tab_ml, tab_explorer = st.tabs([
    "📊  Overview", "⏰  Temporal Analysis", "🤖  ML Engine (IF + DBSCAN)", "🔍  Vehicle Explorer"
])

with tab_overview:
    ov1, ov2, ov3, ov4 = st.columns(4)
    with ov1:
        st.markdown('<div style="font-size:10px;font-weight:700;color:#7ab8e8;letter-spacing:1px;margin-bottom:4px;">RISK LEVEL DISTRIBUTION</div>', unsafe_allow_html=True)
        rc=df["RISK_LEVEL"].value_counts().reset_index(); rc.columns=["Risk Level","Vehicles"]
        fig=px.bar(rc,x="Risk Level",y="Vehicles",color="Risk Level",text="Vehicles",
                   color_discrete_map=CLR)
        fig.update_traces(textposition="outside",textfont=dict(color="white",size=11))
        fig.update_layout(**PLT,height=260,showlegend=False,xaxis={**AX},yaxis={**AX})
        st.plotly_chart(fig,use_container_width=True)
    with ov2:
        st.markdown('<div style="font-size:10px;font-weight:700;color:#7ab8e8;letter-spacing:1px;margin-bottom:4px;">SPEED VS RISK SCORE</div>', unsafe_allow_html=True)
        samp=df.sample(min(1500,len(df)),random_state=42)
        fig=px.scatter(samp,x="AVG_SPEED_KMH",y="RISK_SCORE",color="RISK_LEVEL",
                       color_discrete_map=CLR,opacity=0.6,
                       labels={"AVG_SPEED_KMH":"Avg Speed (km/h)","RISK_SCORE":"Risk Score","RISK_LEVEL":"Risk Level"})
        fig.update_layout(**PLT,height=260,xaxis={**AX},yaxis={**AX})
        st.plotly_chart(fig,use_container_width=True)
    with ov3:
        st.markdown('<div style="font-size:10px;font-weight:700;color:#7ab8e8;letter-spacing:1px;margin-bottom:4px;">TRIP TYPE BREAKDOWN</div>', unsafe_allow_html=True)
        tt=df["TRIP_TYPE"].value_counts().reset_index(); tt.columns=["Type","Count"]
        fig=px.bar(tt,x="Type",y="Count",color="Count",text="Count",color_continuous_scale="Blues")
        fig.update_traces(textposition="outside",textfont=dict(color="white"))
        fig.update_layout(**PLT,height=260,showlegend=False,xaxis={**AX},yaxis={**AX})
        st.plotly_chart(fig,use_container_width=True)
    with ov4:
        st.markdown('<div style="font-size:10px;font-weight:700;color:#7ab8e8;letter-spacing:1px;margin-bottom:4px;">ANOMALY FLAGS OVERVIEW</div>', unsafe_allow_html=True)
        fdf=pd.DataFrame({"Flag":["🅿️ Parking","⚡ Speed","🔁 Route Dev","🚫 Zone","🤝 Coordinated"],
                          "Count":[pk,sp,rd,rz,cm]}).sort_values("Count",ascending=True)
        fig=px.bar(fdf,y="Flag",x="Count",orientation="h",color="Count",text="Count",color_continuous_scale="Reds")
        fig.update_traces(textposition="outside",textfont=dict(color="white"))
        fig.update_layout(**PLT,height=260,showlegend=False,xaxis={**AX},yaxis={**AX})
        st.plotly_chart(fig,use_container_width=True)

    # KPI metric strip
    mk=st.columns(6)
    for col,lbl,val,color in [
        (mk[0],"Avg Risk Score",avg_risk,"#ffc107"),(mk[1],"Max Risk",max_risk,"#ff1744"),
        (mk[2],"Avg Speed km/h",avg_spd,"#00d4ff"),(mk[3],"Avg Max Speed",max_spd,"#ff6b35"),
        (mk[4],"Zone Violations",rz,"#ff1744"),(mk[5],"Speed Anomalies",sp,"#ff6b35")]:
        col.markdown(f"""<div style="background:rgba(0,20,55,0.8);border:1px solid rgba(0,212,255,0.2);
        border-radius:6px;padding:10px 12px;text-align:center;">
        <div style="font-size:9px;font-weight:700;letter-spacing:1px;color:#7ab8e8;text-transform:uppercase;">{lbl}</div>
        <div style="font-size:22px;font-weight:900;color:{color};font-family:Orbitron;">{val}</div>
        </div>""", unsafe_allow_html=True)

with tab_temporal:
    t1,t2,t3=st.columns(3)
    with t1:
        hourly=df.groupby(["HOUR","RISK_LEVEL"]).size().reset_index(name="Trips")
        hourly.rename(columns={"RISK_LEVEL":"Risk Level"},inplace=True)
        fig=px.bar(hourly,x="HOUR",y="Trips",color="Risk Level",color_discrete_map=CLR,
                   labels={"HOUR":"Hour (24h)"})
        fig.update_layout(**PLT,height=280,title=dict(text="Trips by Hour",font=dict(color="white",size=12)),
                          xaxis={**AX},yaxis={**AX})
        st.plotly_chart(fig,use_container_width=True)
    with t2:
        hr=df.groupby("HOUR")["RISK_SCORE"].mean().reset_index()
        fig=go.Figure()
        fig.add_trace(go.Scatter(x=hr["HOUR"],y=hr["RISK_SCORE"],mode="lines+markers",
            line=dict(color="#ff6b35",width=2),marker=dict(color="#ff1744",size=6),
            fill="tozeroy",fillcolor="rgba(255,107,53,0.1)",name="Avg Risk"))
        fig.update_layout(**PLT,height=280,title=dict(text="Avg Risk by Hour",font=dict(color="white",size=12)),
                          xaxis={**AX,"dtick":2},yaxis={**AX})
        st.plotly_chart(fig,use_container_width=True)
    with t3:
        day_hour=df.groupby(["DAY","HOUR"])["RISK_SCORE"].mean().unstack(fill_value=0)
        do=[d for d in ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"] if d in day_hour.index]
        fig=px.imshow(day_hour.reindex(do),color_continuous_scale="RdYlGn_r",aspect="auto",
                      labels=dict(x="Hour",y="Day",color="Avg Risk"))
        fig.update_layout(**PLT,height=280,title=dict(text="Day × Hour Risk Heatmap",font=dict(color="white",size=12)))
        st.plotly_chart(fig,use_container_width=True)

with tab_ml:
    st.markdown("**🤖 Isolation Forest — Anomaly Detection**")
    IF_FEAT=[c for c in ["AVG_SPEED_KMH","RISK_SCORE","CIRCUITY_RATIO","AVG_BEARING_CHANGE",
        "PARKING_DURATION_MIN","SPEED_SPIKES","RZ_HIT_COUNT","STD_SPEED","TRIP_DISTANCE","TRAVEL_TIME"]
        if c in df.columns]
    X_if=df[IF_FEAT].fillna(0)
    X_s=StandardScaler().fit_transform(X_if)
    mc1,mc2=st.columns([1,3])
    cont=mc1.slider("Contamination % (default: 5%)",1,20,5,1)/100
    iso=IsolationForest(contamination=cont,random_state=42,n_estimators=150)
    df["IF_LABEL"]=iso.fit_predict(X_s)
    df["IF_RESULT"]=df["IF_LABEL"].map({1:"Normal",-1:"Anomaly"})
    df["ANOMALY_SCORE"]=(-iso.decision_function(X_s)).round(4)
    norm_cnt=(df["IF_RESULT"]=="Normal").sum(); anom_cnt=(df["IF_RESULT"]=="Anomaly").sum()

    ml1,ml2,ml3,ml4=mc1.columns(1), *([None]*3)
    mc1.markdown(f"""<div style="background:rgba(0,20,55,0.8);border:1px solid rgba(0,212,255,0.2);
    border-radius:6px;padding:10px;margin-top:8px;">
    <div style="color:#7ab8e8;font-size:10px;font-weight:700;">ANOMALIES DETECTED</div>
    <div style="color:#ff1744;font-size:28px;font-weight:900;font-family:Orbitron;">{anom_cnt:,}</div>
    <div style="color:#7ab8e8;font-size:10px;margin-top:4px;">Normal: <b style="color:#00ff88;">{norm_cnt:,}</b></div>
    <div style="color:#7ab8e8;font-size:10px;">Features: <b style="color:#00d4ff;">{len(IF_FEAT)}</b></div>
    </div>""", unsafe_allow_html=True)

    with mc2:
        m2a,m2b=st.columns(2)
        with m2a:
            fig=px.scatter(df.sample(min(2000,len(df)),random_state=42),x="AVG_SPEED_KMH",y="RISK_SCORE",
                           color="IF_RESULT",color_discrete_map={"Normal":"#00ff88","Anomaly":"#ff1744"},opacity=0.7,
                           labels={"AVG_SPEED_KMH":"Speed (km/h)","RISK_SCORE":"Risk Score","IF_RESULT":"Result"})
            fig.update_layout(**PLT,height=280,title=dict(text="Anomaly Scatter",font=dict(color="white",size=12)),
                              xaxis={**AX},yaxis={**AX})
            st.plotly_chart(fig,use_container_width=True)
        with m2b:
            fig=px.histogram(df,x="ANOMALY_SCORE",color="IF_RESULT",nbins=30,barmode="overlay",
                             color_discrete_map={"Normal":"#00ff88","Anomaly":"#ff1744"},
                             labels={"ANOMALY_SCORE":"Anomaly Score","IF_RESULT":"Result"})
            fig.update_layout(**PLT,height=280,title=dict(text="Score Distribution",font=dict(color="white",size=12)),
                              xaxis={**AX},yaxis={**AX})
            st.plotly_chart(fig,use_container_width=True)

    st.markdown("---")
    st.markdown("**🧠 DBSCAN Clustering**")
    CLUST_F=[c for c in ["AVG_SPEED_KMH","RISK_SCORE","TRIP_DISTANCE","CIRCUITY_RATIO","RZ_HIT_COUNT"] if c in df.columns]
    X_db=StandardScaler().fit_transform(df[CLUST_F].fillna(0))
    dc1,dc2=st.columns(2)
    eps_v=dc1.slider("Epsilon",0.3,3.0,0.8,0.1)
    mns_v=dc2.slider("Min Samples",3,20,5,1)
    df["Cluster"]=DBSCAN(eps=eps_v,min_samples=mns_v).fit_predict(X_db)
    df["Cluster"]=df["Cluster"].apply(lambda x:"Noise" if x==-1 else f"C-{x}")
    cl_cnt=len([c for c in df["Cluster"].unique() if c!="Noise"])
    db1,db2=st.columns(2)
    with db1:
        fig=px.scatter(df.sample(min(3000,len(df)),random_state=42),x="AVG_SPEED_KMH",y="RISK_SCORE",
                       color="Cluster",opacity=0.7,labels={"AVG_SPEED_KMH":"Speed","RISK_SCORE":"Risk"})
        fig.update_layout(**PLT,height=260,title=dict(text=f"DBSCAN — {cl_cnt} Clusters Found",font=dict(color="white",size=12)),
                          xaxis={**AX},yaxis={**AX})
        st.plotly_chart(fig,use_container_width=True)
    with db2:
        cs=df["Cluster"].value_counts().reset_index(); cs.columns=["Cluster","Vehicles"]
        fig=px.bar(cs.head(12),x="Cluster",y="Vehicles",color="Vehicles",text="Vehicles",color_continuous_scale="Blues")
        fig.update_traces(textposition="outside",textfont=dict(color="white"))
        fig.update_layout(**PLT,height=260,title=dict(text="Cluster Sizes",font=dict(color="white",size=12)),
                          showlegend=False,xaxis={**AX},yaxis={**AX})
        st.plotly_chart(fig,use_container_width=True)

with tab_explorer:
    ex1,ex2,ex3=st.columns([3,1,1])
    sq=ex1.text_input("🔍 Search Vehicle / Trip ID","")
    sr2=ex2.selectbox("Risk",["All"]+sorted(df["RISK_LEVEL"].unique().tolist()))
    rn=ex3.selectbox("Show",["25","50","100"],index=0)
    exp=df.copy()
    if sq: exp=exp[exp["TRIP_ID"].astype(str).str.contains(sq,case=False,na=False)]
    if sr2!="All": exp=exp[exp["RISK_LEVEL"]==sr2]
    if "IF_RESULT" in exp.columns: exp=exp[exp["IF_RESULT"].isin(["Normal","Anomaly"])]
    exp=exp.sort_values("RISK_SCORE",ascending=False)
    dcols=[c for c in ["TRIP_ID","RISK_LEVEL","RISK_SCORE","SUSPICION_SCORE","AVG_SPEED_KMH",
        "TRIP_DISTANCE","TRAVEL_TIME","FLAG_COUNT","RESTRICTED_ZONE_ENTRY","SPEED_ANOMALY",
        "ROUTE_DEVIATION","PARKING_ANOMALY","CIRCUITY_RATIO","IF_RESULT","ANOMALY_SCORE","Cluster"]
        if c in exp.columns]
    disp=exp[dcols].head(int(rn)).copy()
    disp.columns=[x.replace("_"," ").title() for x in disp.columns]
    st.dataframe(disp,use_container_width=True,height=400)
    ts=datetime.now().strftime("%Y%m%d_%H%M")
    st.download_button("📥 Download Results",exp.to_csv(index=False),f"results_{ts}.csv","text/csv")

# ==========================================================
# ④ BOTTOM STRIP
# ==========================================================
st.markdown('<div style="height:6px;"></div>',unsafe_allow_html=True)
b1,b2,b3,b4 = st.columns([3,2,2,2])

with b1:
    st.markdown("""<div class="info-card">
    <h4>⚡ SYSTEM ARCHITECTURE</h4>
    <div style="display:flex;align-items:center;gap:6px;flex-wrap:wrap;">
      <div class="flow-box">Vehicle<br>Simulator</div>
      <div class="flow-arrow">→</div>
      <div class="flow-box">🔗 MQTT<br>Broker</div>
      <div class="flow-arrow">→</div>
      <div class="flow-box" style="border-color:#00ff88;">FastAPI<br>Backend</div>
      <div class="flow-arrow">→</div>
      <div class="flow-box">AI Engine<br>(IF+DBSCAN)</div>
      <div class="flow-arrow">→</div>
      <div class="flow-box" style="border-color:#ffc107;">PostgreSQL<br>DB</div>
    </div>
    <div style="display:flex;align-items:center;gap:6px;flex-wrap:wrap;margin-top:8px;">
      <div class="flow-box" style="border-color:#00d4ff;">Streamlit<br>Dashboard</div>
      <div class="flow-arrow">←</div>
      <div class="flow-box">Rule-Based<br>Analytics</div>
      <div class="flow-arrow">←</div>
      <div class="flow-box">Risk<br>Scoring</div>
      <div class="flow-arrow">←</div>
      <div class="flow-box">Zone<br>Monitor</div>
    </div>
    </div>""", unsafe_allow_html=True)

with b2:
    st.markdown("""<div class="info-card">
    <h4>🔄 WORKING FLOW</h4>
    <div style="font-size:10px;color:#c8e8ff;font-family:Inter;line-height:1.8;">
      <div><span style="color:#00d4ff;font-weight:700;">1.</span> Vehicle Data Generated / Received Every 3–5 sec</div>
      <div><span style="color:#00d4ff;font-weight:700;">2.</span> Data Streamed via MQTT</div>
      <div><span style="color:#00d4ff;font-weight:700;">3.</span> AI Engine Analyses Behaviour</div>
      <div><span style="color:#ffc107;font-weight:700;">4.</span> Risk Score Calculated</div>
      <div><span style="color:#ff6b35;font-weight:700;">5.</span> If Suspicious → Alert Generated</div>
      <div><span style="color:#ff1744;font-weight:700;">6.</span> Dashboard & Map Updated in Real-Time</div>
    </div>
    </div>""", unsafe_allow_html=True)

with b3:
    st.markdown(f"""<div class="info-card">
    <h4>📡 SYSTEM STATUS</h4>
    <div style="font-size:10px;color:#c8e8ff;font-family:Inter;line-height:2.0;">
    {''.join([f'<div><span style="color:#00ff88;">●</span> {m}</div>' for m in
      ["Data Pipeline","Rule Engine","Isolation Forest","DBSCAN Clustering","Zone Monitor","Risk Scoring","Alert Engine"]])}
    </div>
    </div>""", unsafe_allow_html=True)

with b4:
    st.markdown("""<div class="info-card">
    <h4>🛠️ TECHNOLOGIES USED</h4>
    <div style="font-size:10px;color:#c8e8ff;font-family:Inter;line-height:1.9;">
      <div><span style="color:#3776ab;">🐍</span> Python (Streamlit / FastAPI)</div>
      <div><span style="color:#ff6b35;">📡</span> MQTT (IoT Streaming)</div>
      <div><span style="color:#41b883;">🗺️</span> Folium + Esri Satellite Maps</div>
      <div><span style="color:#ff4154;">📊</span> Plotly (Interactive Charts)</div>
      <div><span style="color:#f7931e;">🤖</span> Scikit-Learn (IF + DBSCAN)</div>
      <div><span style="color:#336791;">🗄️</span> PostgreSQL / CSV</div>
      <div><span style="color:#00d4ff;">☁️</span> Cloudflare Tunnel</div>
    </div>
    </div>""", unsafe_allow_html=True)

# Footer
st.markdown(f"""<div style="text-align:center;padding:8px;background:rgba(0,10,28,0.8);
border-top:1px solid rgba(0,212,255,0.15);margin-top:6px;">
<span style="font-family:Orbitron;font-size:9px;color:#00d4ff;letter-spacing:2px;">
AI POWERED SMART SURVEILLANCE v4.0 &nbsp;|&nbsp; </span>
<span style="font-size:9px;color:#7ab8e8;">Python · Streamlit · Plotly · Folium · Scikit-Learn · MQTT · Cloudflare</span>
</div>""", unsafe_allow_html=True)
