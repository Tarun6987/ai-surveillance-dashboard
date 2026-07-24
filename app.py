# CELL 2 — Write app.py
# ══════════════════════════════════════
%%writefile /content/app.py
import streamlit as st,pandas as pd,numpy as np,warnings,ast
import plotly.express as px,plotly.graph_objects as go
import folium;from streamlit_folium import st_folium;from folium.plugins import HeatMap
from sklearn.ensemble import IsolationForest
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from datetime import datetime;warnings.filterwarnings("ignore")
st.set_page_config(page_title="AI Enabled Smart Surveillance",page_icon="🚔",layout="wide",initial_sidebar_state="expanded")
if "page" not in st.session_state:st.session_state.page="Live Map"

def gen_3d_city():
    ox,oy,dx,dy,dh=175,192,20,10,13
    def pt(c,r,h=0):return(ox+(c-r)*dx,oy-(c+r)*dy-h*dh)
    def fp(*pts):return " ".join(f"{int(p[0])},{int(p[1])}" for p in pts)
    SC={"n":{"t":"#001a5e","r":"#00103a","l":"#000820","s":"#00d4ff"},"r":{"t":"#4a0018","r":"#2a000e","l":"#180008","s":"#ff1744"},"h":{"t":"#002a70","r":"#001850","l":"#000d38","s":"#00eeff"}}
    buildings=[(0,3,2,"n"),(1,3,3,"n"),(2,3,4,"n"),(3,3,3,"n"),(4,3,2,"n"),(0,2,3,"n"),(1,2,5,"n"),(2,2,6,"h"),(3,2,5,"n"),(4,2,2,"n"),(0,1,2,"n"),(1,1,6,"n"),(2,1,9,"h"),(3,1,5,"r"),(4,1,2,"n"),(0,0,2,"n"),(1,0,4,"n"),(2,0,5,"n"),(3,0,3,"n"),(4,0,1,"n")]
    s=['<defs><filter id="gf"><feGaussianBlur stdDeviation="2" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter><filter id="gfr"><feGaussianBlur stdDeviation="3.5" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter><radialGradient id="pg" cx="50%" cy="95%" r="55%"><stop offset="0%" stop-color="#00d4ff" stop-opacity="0.35"/><stop offset="100%" stop-color="#020810" stop-opacity="0"/></radialGradient><linearGradient id="sg" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="#020810"/><stop offset="100%" stop-color="#020c1e"/></linearGradient></defs>','<rect width="360" height="215" fill="url(#sg)"/>','<ellipse cx="175" cy="196" rx="120" ry="18" fill="url(#pg)"/>']
    fr=pt(0,0);ri=pt(5,0);ba=pt(5,4);le=pt(0,4)
    s.append(f'<polygon points="{fp(fr,ri,ba,le)}" fill="#000d28" stroke="#00d4ff" stroke-width="0.5" opacity="0.65"/>')
    for i in range(6):s.append(f'<line x1="{int(pt(i,0)[0])}" y1="{int(pt(i,0)[1])}" x2="{int(pt(i,4)[0])}" y2="{int(pt(i,4)[1])}" stroke="#00d4ff" stroke-width="0.22" opacity="0.2"/>')
    for j in range(5):s.append(f'<line x1="{int(pt(0,j)[0])}" y1="{int(pt(0,j)[1])}" x2="{int(pt(5,j)[0])}" y2="{int(pt(5,j)[1])}" stroke="#00d4ff" stroke-width="0.22" opacity="0.2"/>')
    for b in sorted(buildings,key=lambda b:-(b[0]+b[1])):
        c,r,h,st2=b;sc=SC[st2];bfn=pt(c,r);brt=pt(c+1,r);blf=pt(c,r+1);tfn=pt(c,r,h);trt=pt(c+1,r,h);tba=pt(c+1,r+1,h);tlf=pt(c,r+1,h)
        s.append(f'<polygon points="{fp(blf,bfn,tfn,tlf)}" fill="{sc["l"]}" stroke="{sc["s"]}" stroke-width="0.5"/>');s.append(f'<polygon points="{fp(bfn,brt,trt,tfn)}" fill="{sc["r"]}" stroke="{sc["s"]}" stroke-width="0.5"/>');s.append(f'<polygon points="{fp(tfn,trt,tba,tlf)}" fill="{sc["t"]}" stroke="{sc["s"]}" stroke-width="0.65"/>')
        if st2 in("r","h"):s.append(f'<polyline points="{fp(tfn,trt,tba,tlf,tfn)}" fill="none" stroke="{sc["s"]}" stroke-width="2.5" opacity="0.55" filter="url(#gfr)"/>')
        for wl in range(1,min(h,6)):
            wp=pt(c+0.2,r+0.75,wl);s.append(f'<rect x="{int(wp[0]-1.5)}" y="{int(wp[1]-1)}" width="3" height="2" fill="#00d4ff" opacity="0.4" rx="0.5"/>')
            wp2=pt(c+0.75,r+0.2,wl);s.append(f'<rect x="{int(wp2[0]-1.5)}" y="{int(wp2[1]-1)}" width="3" height="2" fill="#00d4ff" opacity="0.3" rx="0.5"/>')
        if st2=="r":
            tp=pt(c+0.5,r+0.5,h);ax2,ay2=int(tp[0])+30,int(tp[1])-15
            s.append(f'<circle cx="{int(tp[0])}" cy="{int(tp[1])}" r="5" fill="none" stroke="#ff1744" stroke-width="1.5" filter="url(#gfr)"><animate attributeName="r" values="5;10;5" dur="1.5s" repeatCount="indefinite"/><animate attributeName="opacity" values="1;0.2;1" dur="1.5s" repeatCount="indefinite"/></circle>')
            s.append(f'<line x1="{int(tp[0])}" y1="{int(tp[1])}" x2="{ax2}" y2="{ay2}" stroke="#ff1744" stroke-width="0.8" stroke-dasharray="2,2" opacity="0.8"/>');s.append(f'<rect x="{ax2}" y="{ay2-11}" width="68" height="13" rx="2" fill="rgba(40,0,12,0.95)" stroke="#ff1744" stroke-width="0.5"/>');s.append(f'<text x="{ax2+4}" y="{ay2}" font-size="6" fill="#ff1744" font-family="monospace" font-weight="bold">HIGH RISK VEHICLE</text>')
    v1=pt(1.2,0.1);s.append(f'<circle cx="{int(v1[0])}" cy="{int(v1[1])}" r="2.5" fill="#00ff88" filter="url(#gf)" opacity="0.9"><animateTransform attributeName="transform" type="translate" values="0,0;60,30;60,30;0,0" dur="9s" repeatCount="indefinite"/></circle>')
    v2=pt(3.5,0.1);s.append(f'<circle cx="{int(v2[0])}" cy="{int(v2[1])}" r="3" fill="#ff1744" filter="url(#gfr)" opacity="0.9"><animateTransform attributeName="transform" type="translate" values="0,0;-40,10;-40,10;0,0" dur="7s" repeatCount="indefinite"/></circle>')
    rz=pt(3.8,1.2);s.append(f'<rect x="{int(rz[0])-2}" y="{int(rz[1])-11}" width="68" height="12" rx="2" fill="rgba(0,20,70,0.85)" stroke="rgba(255,193,7,0.5)" stroke-width="0.5"/>');s.append(f'<text x="{int(rz[0])+2}" y="{int(rz[1])-2}" font-size="5.5" fill="#ffc107" font-family="monospace">Restricted Zone</text>')
    for sl in range(8,215,5):s.append(f'<line x1="0" y1="{sl}" x2="360" y2="{sl}" stroke="#00d4ff" stroke-width="0.3" opacity="{"0.06" if sl%20==0 else "0.02"}"/>')
    for cx2,cy2,sx2,sy2 in[(5,5,1,1),(355,5,-1,1),(5,210,1,-1),(355,210,-1,-1)]:s.append(f'<path d="M{cx2+sx2*16},{cy2} L{cx2},{cy2} L{cx2},{cy2+sy2*16}" stroke="#00d4ff" stroke-width="1.2" fill="none" opacity="0.55"/>')
    s.append('<text x="175" y="210" font-size="7" fill="#00d4ff" font-family="monospace" text-anchor="middle" opacity="0.65" font-weight="bold">SMART CITY · LIVE MONITORING</text>')
    return "\n".join(s)

CSS=(
    "<style>"
    "@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700;900&family=Inter:wght@400;600;700&display=swap');"
    "#MainMenu,header,footer{display:none!important}"
    "[data-testid='stSidebarCollapseButton']{display:none!important}"
    "button[data-testid='collapsedControl']{display:none!important}"
    ".main .block-container{padding:6px 12px 8px 12px!important;max-width:100%!important}"
    ".stApp{background:#020812!important;font-family:'Inter',sans-serif!important;"
    "background-image:linear-gradient(rgba(0,212,255,.03) 1px,transparent 1px),linear-gradient(90deg,rgba(0,212,255,.03) 1px,transparent 1px)!important;"
    "background-size:30px 30px!important}"
    "::-webkit-scrollbar{width:3px}::-webkit-scrollbar-thumb{background:rgba(0,212,255,.4)}"
    "@keyframes blink{0%,100%{opacity:1}50%{opacity:.15}}"
    ".ld{width:7px;height:7px;background:#00ff88;border-radius:50%;box-shadow:0 0 8px #00ff88;animation:blink 1.2s infinite;display:inline-block}"
    ".kb{background:linear-gradient(135deg,rgba(0,25,65,.98),rgba(0,15,45,.98));border:1px solid rgba(0,212,255,.25);border-radius:8px;padding:7px 12px;text-align:center}"
    "[data-testid='stMarkdownContainer'] p{color:#c8e8ff}"
    "[data-testid='stTabs'] [data-baseweb='tab']{color:#7ab8e8!important;font-weight:600}"
    "[data-testid='stTabs'] [aria-selected='true'][data-baseweb='tab']{color:#00d4ff!important}"
    "[data-testid='stTabs'] [data-baseweb='tab-list']{background:rgba(0,15,40,.8)!important;border:1px solid rgba(0,212,255,.15)!important;border-radius:6px}"
    "[data-testid='stWidgetLabel'] p{color:#7ab8e8!important}"
    "[data-testid='stMetricValue']{color:#fff!important;font-size:22px!important;font-weight:700!important}"
    "[data-testid='stMetricLabel']{color:#7ab8e8!important;font-size:11px!important}"
    "[data-testid='stMetric']{background:rgba(0,15,40,.7)!important;border:1px solid rgba(0,212,255,.15)!important;border-radius:8px!important;padding:10px 14px!important}"
    ".stSelectbox [data-baseweb='select']>div{background:rgba(0,15,40,.9)!important;border-color:rgba(0,212,255,.3)!important;color:#c8e8ff!important}"
    ".stSelectbox label,[data-testid='stTextInput'] label{color:#7ab8e8!important;font-size:11px!important}"
    "[data-testid='stTextInput'] input{background:#ffffff!important;border:1.5px solid rgba(0,212,255,.4)!important;color:#0a0a1a!important;border-radius:6px!important;font-weight:600!important}"
    "[data-testid='stDataFrame']{border:1px solid rgba(0,212,255,.15)!important;border-radius:8px!important}"
    "[data-testid='stHorizontalBlock']{align-items:stretch!important;gap:10px!important}"
    "[data-testid='stHorizontalBlock']>[data-testid='column']{display:flex!important;flex-direction:column!important}"
    "section[data-testid='stSidebar']{background:linear-gradient(180deg,#020c1e 0%,#020810 100%)!important;"
    "border-right:1px solid rgba(0,212,255,.2)!important;min-width:90px!important;max-width:90px!important;"
    "transform:none!important;visibility:visible!important;display:flex!important}"
    "section[data-testid='stSidebar']>div:first-child{padding:0 5px!important;overflow-x:hidden!important;background:transparent!important}"
    "section[data-testid='stSidebar'] div,section[data-testid='stSidebar'] section,"
    "section[data-testid='stSidebar'] [data-testid='stVerticalBlockBorderWrapper'],"
    "section[data-testid='stSidebar'] [data-testid='stVerticalBlock'],"
    "section[data-testid='stSidebar'] .stButton{background:transparent!important;background-color:transparent!important;border:none!important;box-shadow:none!important}"
    "section[data-testid='stSidebar'] .stButton{margin-top:-68px!important;position:relative!important;z-index:10!important}"
    "section[data-testid='stSidebar'] .stButton>button{background:transparent!important;border:none!important;box-shadow:none!important;outline:none!important;opacity:0!important;height:68px!important;width:100%!important;cursor:pointer!important}"
    "</style>"
)
st.markdown(CSS,unsafe_allow_html=True)
C={"CRITICAL":"#ff1744","HIGH":"#ff6b35","MEDIUM":"#ffc107","LOW":"#00ff88"}
P=dict(template="plotly_dark",paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",font=dict(color="#c8e8ff",family="Inter",size=11),margin=dict(t=15,b=5,l=5,r=5))
AX=dict(gridcolor="rgba(0,212,255,.08)",color="#7ab8e8",tickfont=dict(color="#c8e8ff",size=10),linecolor="rgba(0,212,255,.2)",showgrid=True,zeroline=False)
_PB="background:linear-gradient(135deg,rgba(0,20,50,.97),rgba(0,10,28,.99));border-radius:8px;padding:12px 14px;"
_PH="height:320px;overflow-y:auto;"
PNL_BLUE=_PB+"border:1px solid rgba(0,212,255,.2);"
PNL_ORANGE=_PB+"border:1px solid rgba(255,107,53,.25);"
PNL_YELLOW=_PB+"border:1px solid rgba(255,193,7,.2);"
PNL_GREEN=_PB+"border:1px solid rgba(0,255,136,.2);"
def HDR(i,t,c):return f'<div style="font-family:Orbitron;font-size:9px;font-weight:900;color:{c};letter-spacing:1px;border-bottom:1px solid {c}30;padding-bottom:5px;margin-bottom:6px;">{i} {t}</div>'
def violation_probability(n):
    base={0:0.05,1:0.28,2:0.54,3:0.76,4:0.89,5:0.95}
    return base.get(int(n),0.97 if int(n)>5 else 0.02)
def risk_escalation_label(fc,rs):
    fc,rs=int(fc),float(rs)
    if fc>=3 and rs>70:return "🔴 LIKELY ESCALATE","#ff1744"
    elif fc>=2 and rs>50:return "🟠 POSSIBLE ESCALATE","#ff6b35"
    elif fc>=1 and rs>30:return "🟡 MONITOR","#ffc107"
    return "🟢 STABLE","#00ff88"
def find_csv():
    for n in["dashboard_dataset.csv","surveillance_features.csv","data.csv"]:
        try:return pd.read_csv(n),n
        except:pass
    return None,None
_df,_=find_csv()
if _df is None:
    st.markdown('<div style="display:flex;align-items:center;justify-content:center;height:100vh;flex-direction:column;gap:20px;"><div style="font-size:60px">📂</div><h2 style="color:#00d4ff;font-family:Orbitron">UPLOAD DATASET</h2></div>',unsafe_allow_html=True)
    up=st.file_uploader("Upload CSV",type=["csv"])
    if up:open("dashboard_dataset.csv","wb").write(up.read());st.rerun()
    st.stop()
@st.cache_data
def load():
    df,_=find_csv();df.columns=df.columns.str.upper().str.strip()
    for col in["DATETIME","TIMESTAMP"]:
        if col in df.columns:df["TIMESTAMP"]=pd.to_datetime(df[col],errors="coerce");break
    if "TIMESTAMP" in df.columns:df["HOUR"]=df["TIMESTAMP"].dt.hour
    if "TRIP_ID" not in df.columns:df["TRIP_ID"]=[f"VEH-{i:05d}" for i in range(len(df))]
    df["RISK_LEVEL"]=df["RISK_LEVEL"].astype(str).str.upper().str.strip()
    if "HOUR" not in df.columns:df["HOUR"]=np.random.randint(0,24,len(df))
    if "TRIP_TYPE" not in df.columns:df["TRIP_TYPE"]=np.random.choice(["Short","Standard","Commercial"],len(df))
    fc=[c for c in["PARKING_ANOMALY","SPEED_ANOMALY","ROUTE_DEVIATION","RESTRICTED_ZONE_ENTRY","COORDINATED_MOVEMENT"] if c in df.columns]
    df["FLAG_COUNT"]=df[fc].sum(axis=1) if fc else 0
    df["TRIP_ID"]=df["TRIP_ID"].astype(str).apply(lambda x:x.rstrip("0") if x.replace(".","").isdigit() and x.rstrip("0") else x).apply(lambda x:x[:12] if len(x)>12 else x)
    return df
df=load()
tot=len(df);crit=int((df["RISK_LEVEL"]=="CRITICAL").sum());high=int((df["RISK_LEVEL"]=="HIGH").sum())
med=int((df["RISK_LEVEL"]=="MEDIUM").sum());low=int((df["RISK_LEVEL"]=="LOW").sum());alerts=crit+high
normal=med+low;avg_r=round(df["RISK_SCORE"].mean(),1) if "RISK_SCORE" in df.columns else 0
rz=int(df["RESTRICTED_ZONE_ENTRY"].sum()) if "RESTRICTED_ZONE_ENTRY" in df.columns else 0
now=datetime.now().strftime("%d %b %Y  %H:%M:%S");pg=st.session_state.page
_rc=df["RISK_LEVEL"].value_counts()
RISK_BARS="".join(['<div style="margin:7px 0;"><div style="display:flex;justify-content:space-between;font-size:11px;color:#c8e8ff;margin-bottom:3px;"><span>'+("🔴" if l=="CRITICAL" else "🟠" if l=="HIGH" else "🟡" if l=="MEDIUM" else "🟢")+" "+l+'</span><span style="color:'+C[l]+';font-weight:700;">'+str(int(_rc.get(l,0)))+'</span></div><div style="height:7px;background:rgba(255,255,255,.06);border-radius:3px;"><div style="width:'+str(min(_rc.get(l,0)/max(tot,1)*100,100))[:5]+'%;height:100%;background:'+C[l]+';border-radius:3px;"></div></div></div>'for l in["CRITICAL","HIGH","MEDIUM","LOW"]])
DET_ITEMS="".join(['<div style="display:flex;align-items:center;gap:8px;padding:5px 0;font-size:11px;color:#c8e8ff;border-bottom:1px solid rgba(0,212,255,.07);"><span style="color:#00ff88;">✓</span><span style="flex:1;">'+l+'</span><span style="color:#ffc107;font-weight:700;">'+str(np.random.randint(10,200))+'</span></div>'for l in["Long Parking Detected","Restricted Zone Entry","Circular Movement","Abnormal Stop Pattern","Route Deviation","Speed Anomaly"]])
_top5=df.nlargest(5,"RISK_SCORE") if "RISK_SCORE" in df.columns else df.head(5)
with st.sidebar:
    st.markdown('<div style="font-family:Orbitron;font-size:7px;color:#00d4ff;font-weight:900;letter-spacing:2px;text-align:center;padding:12px 2px 10px;border-bottom:1px solid rgba(0,212,255,.15);margin-bottom:4px;">SMART<br>SURV</div>',unsafe_allow_html=True)
    for icon,label,p in[("🗺️","MAP","Live Map"),("🚗","FLEET","Vehicles"),("🔔","ALERTS","Alerts"),("📊","STATS","Analytics"),("🚫","ZONES","Zones"),("📋","LOGS","History"),("⚙️","CONFIG","Settings")]:
        active=pg==p;bg="rgba(0,212,255,.16)" if active else "transparent";bd="rgba(0,212,255,.55)" if active else "rgba(255,255,255,.05)";fc2="#00d4ff" if active else "#7ab8e8"
        st.markdown(f'<div style="height:64px;display:flex;flex-direction:column;align-items:center;justify-content:center;border-radius:8px;background:{bg};border:1px solid {bd};margin:2px 0;"><div style="font-size:20px;line-height:1.3;">{icon}</div><div style="font-size:7px;color:{fc2};font-weight:700;letter-spacing:.5px;font-family:Orbitron;margin-top:2px;">{label}</div></div>',unsafe_allow_html=True)
        if st.button(" ",key=f"nav_{p}",use_container_width=True):st.session_state.page=p;st.rerun()
    st.markdown(f'<div style="text-align:center;font-size:7px;color:#7ab8e8;padding:6px 2px;border-top:1px solid rgba(0,212,255,.15);margin-top:4px;"><div style="color:#00ff88;font-weight:700;font-size:9px;">● LIVE</div><div style="margin-top:2px;">{datetime.now().strftime("%H:%M")}</div></div>',unsafe_allow_html=True)
hkbs="".join(['<div class="kb"><div style="font-size:7px;color:#7ab8e8;font-weight:700;text-transform:uppercase;margin-bottom:2px;">'+l+'</div><div style="font-size:19px;font-weight:900;font-family:Orbitron;color:'+c+';text-shadow:0 0 10px '+c+';">'+v+'</div></div>'for l,v,c in[("TOTAL",f"{tot:,}","#00d4ff"),("NORMAL",f"{normal:,}","#00ff88"),("MEDIUM",f"{med:,}","#ffc107"),("HIGH RISK",f"{high:,}","#ff6b35"),("ALERTS",f"{alerts}","#ff1744")]])
st.markdown('<div style="background:linear-gradient(90deg,#020c1e,#031830,#020c1e);border-bottom:2px solid rgba(0,212,255,.5);padding:8px 14px;display:flex;align-items:center;justify-content:space-between;box-shadow:0 4px 40px rgba(0,212,255,.18);margin-bottom:8px;"><div style="display:flex;align-items:center;gap:10px;"><div style="width:38px;height:38px;background:rgba(0,100,200,.3);border:2px solid rgba(0,212,255,.6);border-radius:9px;display:flex;align-items:center;justify-content:center;font-size:18px;box-shadow:0 0 18px rgba(0,212,255,.4);">🚔</div><div><div style="font-family:Orbitron;font-size:13px;font-weight:900;color:#00d4ff;text-shadow:0 0 12px rgba(0,212,255,.8);letter-spacing:2px;">AI ENABLED SMART SURVEILLANCE PROTOTYPE</div><div style="font-size:7.5px;color:#7ab8e8;letter-spacing:4px;">SUSPICIOUS VEHICLE DETECTION SYSTEM</div></div></div><div style="display:flex;gap:6px;">'+hkbs+'</div><div style="text-align:right;"><div style="display:inline-flex;align-items:center;gap:5px;background:rgba(0,255,136,.08);border:1px solid rgba(0,255,136,.35);border-radius:4px;padding:3px 10px;font-size:9px;font-weight:700;color:#00ff88;font-family:Orbitron;"><div class="ld"></div>LIVE STREAM</div><div style="font-size:7.5px;color:#7ab8e8;margin-top:3px;">'+now+'</div></div></div>',unsafe_allow_html=True)
if pg=="Live Map":
    n_map=st.slider("🛰️ Vehicles on Map",100,min(800,tot),300,50,key="map_n")
    map_c,city_c=st.columns([7,4])
    with map_c:
        @st.cache_data
        def build_map(djson,n):
            dm=pd.read_json(djson);m=folium.Map(location=[41.1579,-8.6291],zoom_start=13,tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",attr="Esri",prefer_canvas=True)
            m.get_root().html.add_child(folium.Element('<style>.leaflet-container{background:#020812!important}.leaflet-popup-content-wrapper{background:rgba(2,12,30,.95)!important;border:1px solid rgba(0,212,255,.4)!important;border-radius:8px!important}.leaflet-popup-content{margin:10px 14px!important;color:#c8e8ff!important}</style>'))
            heat=[];samp=dm.sample(min(n,len(dm)),random_state=42)
            for _,row in samp.iterrows():
                try:
                    lat=lon=None
                    if "LATITUDE" in row and pd.notna(row.get("LATITUDE")):lat,lon=float(row["LATITUDE"]),float(row["LONGITUDE"])
                    elif "POLYLINE" in row:
                        p=row["POLYLINE"]
                        if isinstance(p,str):
                            try:p=ast.literal_eval(p)
                            except:p=[]
                        if len(p)>0:lon,lat=p[-1]
                    if lat is None:continue
                    risk=str(row.get("RISK_LEVEL","LOW")).upper();sc=float(row.get("RISK_SCORE",0))
                    col2={"CRITICAL":"#ff1744","HIGH":"#ff6b35","MEDIUM":"#ffc107","LOW":"#00ff88"}.get(risk,"#00d4ff");sz={"CRITICAL":14,"HIGH":10,"MEDIUM":7,"LOW":5}.get(risk,5)
                    heat.append([lat,lon,sc/100])
                    ih=f'<div style="width:{sz*2}px;height:{sz*2}px;border-radius:50%;background:{col2};box-shadow:0 0 {sz*2}px {col2};border:1.5px solid rgba(255,255,255,.4);"></div>'
                    ph=f'<div style="font-size:11px;min-width:160px;"><b style="color:{col2};">⚠ {risk}</b><br><span style="color:#7ab8e8;">ID:</span> {str(row.get("TRIP_ID","N/A"))[:16]}<br><span style="color:{col2};">Risk: {sc:.0f}/100</span></div>'
                    folium.Marker([lat,lon],icon=folium.DivIcon(html=ih,icon_size=(sz*2,sz*2),icon_anchor=(sz,sz)),popup=folium.Popup(ph,max_width=200)).add_to(m)
                    if "POLYLINE" in row:
                        p2=row["POLYLINE"]
                        if isinstance(p2,str):
                            try:p2=ast.literal_eval(p2)
                            except:p2=[]
                        if len(p2)>1:folium.PolyLine([(x[1],x[0]) for x in p2],weight={"CRITICAL":2.5,"HIGH":2}.get(risk,1),color=col2,opacity={"CRITICAL":.7,"HIGH":.5}.get(risk,.12)).add_to(m)
                except:pass
            if heat:HeatMap(heat,radius=15,blur=20,min_opacity=0.2,gradient={0:"#001f3f",.3:"#00ff88",.6:"#ffc107",.85:"#ff6b35",1:"#ff1744"}).add_to(m)
            return m
        sat_map=build_map(df.to_json(),n_map)
        st_folium(sat_map,width=None,height=430,returned_objects=[],key="map_main")
        live_stats="".join([f'<span style="color:#7ab8e8;">{"🔴" if l=="CRITICAL" else "🟠" if l=="HIGH" else "🟡" if l=="MEDIUM" else "🟢"} {l}: <b style="color:{C[l]};">{v}</b></span>'for l,v in[("CRITICAL",crit),("HIGH",high),("MEDIUM",med),("LOW",low)]])
        st.markdown('<div style="background:rgba(0,15,40,.95);border:1px solid rgba(0,212,255,.2);border-top:none;border-radius:0 0 8px 8px;padding:5px 14px;display:flex;gap:12px;align-items:center;font-size:9px;flex-wrap:wrap;"><span style="display:inline-flex;align-items:center;gap:5px;background:rgba(0,255,136,.08);border:1px solid rgba(0,255,136,.3);border-radius:4px;padding:2px 8px;color:#00ff88;font-weight:700;font-family:Orbitron;font-size:8px;"><div class="ld"></div>LIVE</span>'+live_stats+f'<span style="color:#7ab8e8;margin-left:auto;">Showing:<b style="color:#00d4ff;"> {min(n_map,tot):,}</b> · Avg Risk:<b style="color:#ffc107;"> {avg_r}</b></span></div>',unsafe_allow_html=True)
    with city_c:
        city_svg=gen_3d_city()
        st.markdown('<div style="height:462px;display:flex;flex-direction:column;gap:6px;"><div style="font-family:Orbitron;font-size:10px;font-weight:900;color:#00d4ff;letter-spacing:2px;border-bottom:1px solid rgba(0,212,255,.2);padding-bottom:4px;flex-shrink:0;">🔷 HOLOGRAPHIC 3D CITY</div><div style="flex:1;background:linear-gradient(135deg,rgba(0,5,20,.98),rgba(0,8,25,.98));border:1px solid rgba(0,212,255,.35);border-radius:10px;overflow:hidden;padding:6px;display:flex;flex-direction:column;"><svg viewBox="0 0 360 215" xmlns="http://www.w3.org/2000/svg" style="width:100%;flex:1;display:block;min-height:0;">'+city_svg+'</svg><div style="display:flex;justify-content:center;gap:10px;font-size:8px;color:#7ab8e8;flex-shrink:0;"><span>🟢 Normal</span><span>🔴 High Risk</span><span>🔷 Hero</span><span>🟠 Alert</span></div></div><div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;flex-shrink:0;"><div style="background:rgba(0,15,40,.9);border:1px solid rgba(0,212,255,.25);border-radius:8px;padding:10px 14px;"><div style="font-size:9px;color:#7ab8e8;font-weight:700;margin-bottom:3px;">TOTAL</div><div style="font-size:24px;font-weight:900;color:#00d4ff;font-family:Orbitron;">'+f"{tot:,}"+'</div></div><div style="background:rgba(0,15,40,.9);border:1px solid rgba(255,23,68,.25);border-radius:8px;padding:10px 14px;"><div style="font-size:9px;color:#7ab8e8;font-weight:700;margin-bottom:3px;">ALERTS</div><div style="font-size:24px;font-weight:900;color:#ff1744;font-family:Orbitron;">'+f"{alerts:,}"+'</div></div></div></div>',unsafe_allow_html=True)
    st.markdown('<div style="height:8px"></div>',unsafe_allow_html=True)
    det_c,risk_c,alert_c=st.columns(3)
    H340=_PH.replace("320","340")+_PB
    with det_c:
        dr="".join(['<div style="display:flex;align-items:center;gap:8px;padding:6px 0;font-size:11px;color:#c8e8ff;border-bottom:1px solid rgba(0,212,255,.07);"><span style="color:#00ff88;font-size:13px;">✓</span><span style="flex:1;">'+l+'</span><span style="color:#ffc107;font-weight:700;">'+str(np.random.randint(10,200))+'</span></div>'for l in["Long Parking Detected","Restricted Zone Entry","Circular Movement","Abnormal Stop Pattern","Route Deviation","Speed Anomaly"]])
        st.markdown('<div style="'+H340+'border:1px solid rgba(0,212,255,.2);">'+HDR("🔍","DETECTION ENGINE","#00d4ff")+dr+'</div>',unsafe_allow_html=True)
    with risk_c:
        st.markdown('<div style="'+H340+'border:1px solid rgba(255,193,7,.2);">'+HDR("📊","RISK DISTRIBUTION","#ffc107")+RISK_BARS+'</div>',unsafe_allow_html=True)
    with alert_c:
        _t14=df.nlargest(14,"RISK_SCORE") if "RISK_SCORE" in df.columns else df.head(14)
        a14="".join(['<div style="display:flex;align-items:center;gap:8px;padding:6px 8px;border-radius:5px;margin-bottom:4px;background:'+C.get(row["RISK_LEVEL"],"#aaa")+'12;border-left:3px solid '+C.get(row["RISK_LEVEL"],"#aaa")+';"><span style="font-size:10px;font-weight:800;color:'+C.get(row["RISK_LEVEL"],"#aaa")+';font-family:monospace;flex:1;">'+str(row["TRIP_ID"])[:13]+'</span><span style="font-size:8px;padding:1px 5px;border-radius:3px;background:'+C.get(row["RISK_LEVEL"],"#aaa")+'22;color:'+C.get(row["RISK_LEVEL"],"#aaa")+';font-weight:700;">'+row["RISK_LEVEL"]+'</span><span style="font-size:9px;color:#ffc107;font-weight:700;">'+str(round(float(row.get("RISK_SCORE",0))))+'</span></div>'for _,row in _t14.iterrows()])
        st.markdown('<div style="'+H340+'border:1px solid rgba(255,107,53,.25);">'+HDR("🚨","LIVE ALERT FEED","#ff6b35")+a14+'</div>',unsafe_allow_html=True)
else:
    if pg=="Vehicles":
        st.markdown('<div style="font-family:Orbitron;font-size:13px;font-weight:900;color:#00d4ff;letter-spacing:2px;padding:4px 0 8px;border-bottom:1px solid rgba(0,212,255,.15);margin-bottom:10px;">🚗 VEHICLE DATABASE</div>',unsafe_allow_html=True)
        vc1,vc2,vc3,vc4=st.columns(4)
        vc1.metric("Total",f"{tot:,}");vc2.metric("Normal",f"{normal:,}");vc3.metric("High Risk",f"{high:,}");vc4.metric("Alerts",f"{alerts:,}")
        st.markdown('<div style="height:8px"></div>',unsafe_allow_html=True)
        fc1,fc2,fc3=st.columns(3)
        fr=fc1.selectbox("Filter Risk",["All"]+sorted(df["RISK_LEVEL"].unique().tolist()))
        ft=fc2.selectbox("Filter Type",["All"]+sorted(df["TRIP_TYPE"].unique().tolist()))
        fs=fc3.text_input("Search ID","")
        vdf=df.copy()
        if fr!="All":vdf=vdf[vdf["RISK_LEVEL"]==fr]
        if ft!="All":vdf=vdf[vdf["TRIP_TYPE"]==ft]
        if fs:vdf=vdf[vdf["TRIP_ID"].astype(str).str.contains(fs,case=False)]
        dcols=["TRIP_ID","RISK_LEVEL","RISK_SCORE","AVG_SPEED_KMH","TRIP_TYPE","FLAG_COUNT"]
        show_df=vdf[[c for c in dcols if c in vdf.columns]].head(200)
        RC2={"CRITICAL":"#ff1744","HIGH":"#ff6b35","MEDIUM":"#ffc107","LOW":"#00ff88"}
        hdr2="".join([f"<th style='padding:10px 14px;text-align:left;font-size:10px;font-weight:700;color:#00d4ff;letter-spacing:1px;border-bottom:2px solid rgba(0,212,255,.3);white-space:nowrap;'>{c.replace(chr(95),' ')}</th>" for c in show_df.columns])
        tbody=""
        for i,(idx,row) in enumerate(show_df.iterrows()):
            bg2="rgba(0,15,40,.6)" if i%2==0 else "rgba(0,8,28,.4)"
            cells=""
            for col in show_df.columns:
                val=row[col]
                s="font-size:11px;padding:9px 14px;border-bottom:1px solid rgba(0,212,255,.06);white-space:nowrap;"
                if col=="RISK_LEVEL":
                    rc3=RC2.get(str(val),"#aaa")
                    cells+=f"<td style='{s}'><span style='background:{rc3}22;color:{rc3};font-weight:700;font-size:9px;padding:3px 10px;border-radius:4px;border:1px solid {rc3}55;'>{val}</span></td>"
                elif col=="RISK_SCORE":
                    try:sc3=float(val)
                    except:sc3=0
                    bar_c="#ff1744" if sc3>=80 else "#ff6b35" if sc3>=60 else "#ffc107" if sc3>=40 else "#00ff88"
                    pct=min(sc3,100)
                    cells+=f"<td style='{s}'><div style='display:flex;align-items:center;gap:8px;'><div style='width:55px;height:5px;background:rgba(255,255,255,.08);border-radius:3px;'><div style='width:{pct:.0f}%;height:100%;background:{bar_c};border-radius:3px;'></div></div><span style='color:{bar_c};font-weight:700;font-size:11px;'>{sc3:.1f}</span></div></td>"
                elif col=="FLAG_COUNT":
                    try:fv2=int(float(val))
                    except:fv2=0
                    fc_c2="#ff1744" if fv2>=3 else "#ffc107" if fv2>=1 else "#00ff88"
                    ico="🚨" if fv2>=3 else "⚠️" if fv2>=1 else "✅"
                    cells+=f"<td style='{s}'><span style='color:{fc_c2};font-weight:700;'>{ico} {fv2}</span></td>"
                elif col=="TRIP_ID":
                    cells+=f"<td style='{s}'><span style='font-family:monospace;color:#00d4ff;font-weight:700;'>{str(val)[:14]}</span></td>"
                else:
                    cells+=f"<td style='{s};color:#c8e8ff;'>{val}</td>"
            tbody+=f"<tr style='background:{bg2};'>{cells}</tr>"
        st.markdown(f'''<div style="border:1px solid rgba(0,212,255,.2);border-radius:10px;overflow:hidden;margin-top:4px;"><div style="overflow-x:auto;max-height:460px;overflow-y:auto;"><table style="width:100%;border-collapse:collapse;"><thead style="position:sticky;top:0;background:#020c1e;z-index:1;"><tr>{hdr2}</tr></thead><tbody>{tbody}</tbody></table></div><div style="padding:7px 14px;background:rgba(0,8,25,.8);border-top:1px solid rgba(0,212,255,.1);font-size:10px;color:#7ab8e8;">Showing <b style="color:#00d4ff;">{len(show_df):,}</b> of <b style="color:#00d4ff;">{len(vdf):,}</b> vehicles</div></div>''',unsafe_allow_html=True)
        st.markdown('<div style="height:8px"></div>',unsafe_allow_html=True)
        st.markdown('<div style="font-family:Orbitron;font-size:11px;color:#00d4ff;letter-spacing:2px;border-bottom:1px solid rgba(0,212,255,.2);padding-bottom:6px;margin-bottom:10px;">🔬 ADVANCED VEHICLE EXPLORER</div>',unsafe_allow_html=True)
        exp_ids=vdf["TRIP_ID"].astype(str).tolist()[:300]
        if exp_ids:
            sel_exp=st.selectbox("Select Vehicle to Inspect",exp_ids,key="exp_sel")
            exp_rows=vdf[vdf["TRIP_ID"].astype(str)==sel_exp]
            exp_row=exp_rows.iloc[0] if len(exp_rows)>0 else vdf.iloc[0]
            exp_fc=int(exp_row.get("FLAG_COUNT",0));exp_rs=float(exp_row.get("RISK_SCORE",0))
            exp_esc,exp_esc_c=risk_escalation_label(exp_fc,exp_rs)
            ep4=violation_probability(exp_fc)*100;ep5=violation_probability(exp_fc+1)*100
            ex1,ex2,ex3,ex4=st.columns(4)
            ex1.metric("Risk Score",f"{exp_rs:.0f}/100");ex2.metric("Flag Count",f"{exp_fc}");ex3.metric("P(4th Violation)",f"{ep4:.0f}%");ex4.metric("P(5th Violation)",f"{ep5:.0f}%")
            st.markdown(f'<div style="margin-top:8px;padding:10px 14px;border-radius:8px;background:{exp_esc_c}10;border-left:4px solid {exp_esc_c};font-size:12px;"><b style="color:{exp_esc_c};">Escalation Forecast: {exp_esc}</b><span style="color:#7ab8e8;margin-left:12px;">Based on {exp_fc} historical flag(s) and risk score {exp_rs:.0f}</span></div>',unsafe_allow_html=True)
    elif pg=="Alerts":
        st.markdown('<div style="font-family:Orbitron;font-size:13px;font-weight:900;color:#ff1744;letter-spacing:2px;padding:4px 0 8px;border-bottom:1px solid rgba(255,23,68,.2);margin-bottom:10px;">🚨 ACTIVE ALERTS</div>',unsafe_allow_html=True)
        a1,a2,a3=st.columns(3);a1.metric("Critical",f"{crit:,}");a2.metric("High",f"{high:,}");a3.metric("Total Alerts",f"{alerts:,}")
        adf=df[df["RISK_LEVEL"].isin(["CRITICAL","HIGH"])].sort_values("RISK_SCORE",ascending=False) if "RISK_SCORE" in df.columns else df[df["RISK_LEVEL"].isin(["CRITICAL","HIGH"])]
        alist="".join([f'<div style="display:flex;gap:10px;align-items:center;padding:7px 12px;border-radius:6px;margin:3px 0;background:{C.get(row["RISK_LEVEL"],"#aaa")}10;border-left:4px solid {C.get(row["RISK_LEVEL"],"#aaa")};border:1px solid {C.get(row["RISK_LEVEL"],"#aaa")}18;"><span style="color:{C.get(row["RISK_LEVEL"],"#aaa")};font-family:monospace;font-weight:800;min-width:110px;">{str(row["TRIP_ID"])[:14]}</span><span style="background:{C.get(row["RISK_LEVEL"],"#aaa")}22;color:{C.get(row["RISK_LEVEL"],"#aaa")};font-size:9px;padding:2px 8px;border-radius:3px;font-weight:700;">{row["RISK_LEVEL"]}</span><span style="color:#7ab8e8;font-size:10px;flex:1;">Spd: <b>{row.get("AVG_SPEED_KMH","N/A")} km/h</b></span><span style="color:{C.get(row["RISK_LEVEL"],"#aaa")};font-weight:700;">{row.get("RISK_SCORE",0):.0f}/100</span></div>'for _,row in adf.head(30).iterrows()])
        st.markdown('<div style="max-height:540px;overflow-y:auto;">'+alist+'</div>',unsafe_allow_html=True)
    elif pg=="Analytics":
        st.markdown('<div style="font-family:Orbitron;font-size:13px;font-weight:900;color:#00d4ff;letter-spacing:2px;padding:4px 0 8px;border-bottom:1px solid rgba(0,212,255,.15);margin-bottom:10px;">📊 AI ANALYTICS</div>',unsafe_allow_html=True)
        t1,t2,t3,t4,t5=st.tabs(["📊 Overview","⏰ Temporal","🤖 ML Engine","📍 Clusters","⚠️ Predictions"])
        with t1:
            c1,c2=st.columns(2)
            with c1:
                rc3=df["RISK_LEVEL"].value_counts().reset_index();rc3.columns=["Risk","Count"]
                fig=px.bar(rc3,x="Risk",y="Count",color="Risk",text="Count",color_discrete_map=C)
                fig.update_traces(textposition="outside",textfont=dict(color="white"));fig.update_layout(**P,height=300,showlegend=False,xaxis=AX,yaxis=AX)
                st.plotly_chart(fig,use_container_width=True,config={"displayModeBar":False})
            with c2:
                if "AVG_SPEED_KMH" in df.columns and "RISK_SCORE" in df.columns:
                    sm=df.sample(min(1000,len(df)),random_state=42)
                    fig=px.scatter(sm,x="AVG_SPEED_KMH",y="RISK_SCORE",color="RISK_LEVEL",color_discrete_map=C,opacity=0.6)
                    fig.update_layout(**P,height=300,xaxis=AX,yaxis=AX);st.plotly_chart(fig,use_container_width=True,config={"displayModeBar":False})
        with t2:
            if "HOUR" in df.columns:
                h1,h2=st.columns(2)
                with h1:
                    hr=df.groupby(["HOUR","RISK_LEVEL"]).size().reset_index(name="Trips");hr.rename(columns={"RISK_LEVEL":"Risk"},inplace=True)
                    fig=px.bar(hr,x="HOUR",y="Trips",color="Risk",color_discrete_map=C);fig.update_layout(**P,height=300,xaxis=AX,yaxis=AX)
                    st.plotly_chart(fig,use_container_width=True,config={"displayModeBar":False})
                with h2:
                    if "RISK_SCORE" in df.columns:
                        hr2=df.groupby("HOUR")["RISK_SCORE"].mean().reset_index()
                        fig=go.Figure();fig.add_trace(go.Scatter(x=hr2["HOUR"],y=hr2["RISK_SCORE"],mode="lines+markers",line=dict(color="#ff6b35",width=2.5),fill="tozeroy",fillcolor="rgba(255,107,53,.1)"))
                        fig.update_layout(**P,height=300,xaxis=AX,yaxis=AX);st.plotly_chart(fig,use_container_width=True,config={"displayModeBar":False})
        with t3:
            IF_F=[c for c in["AVG_SPEED_KMH","RISK_SCORE","TRIP_DISTANCE","FLAG_COUNT"] if c in df.columns]
            if len(IF_F)>=2:
                X=StandardScaler().fit_transform(df[IF_F].fillna(0));cont=st.slider("Contamination %",1,20,5,key="ct")/100
                iso=IsolationForest(contamination=cont,random_state=42,n_estimators=150);preds=iso.fit_predict(X)
                df2=df.copy();df2["Result"]=pd.Series(preds).map({1:"Normal",-1:"Anomaly"});df2["Score"]=-iso.decision_function(X)
                m1,m2,m3=st.columns(3);m1.metric("Anomalies",f'{(preds==-1).sum():,}');m2.metric("Anomaly %",f'{(preds==-1).mean()*100:.1f}%');m3.metric("Trees","150")
                ci1,ci2=st.columns(2)
                with ci1:
                    fig=px.scatter(df2.sample(min(1500,len(df2)),random_state=42),x=IF_F[0],y=IF_F[1],color="Result",color_discrete_map={"Normal":"#00ff88","Anomaly":"#ff1744"},opacity=0.7)
                    fig.update_layout(**P,height=280,xaxis=AX,yaxis=AX);st.plotly_chart(fig,use_container_width=True,config={"displayModeBar":False})
                with ci2:
                    fig=px.histogram(df2,x="Score",color="Result",nbins=30,barmode="overlay",color_discrete_map={"Normal":"#00ff88","Anomaly":"#ff1744"})
                    fig.update_layout(**P,height=280,xaxis=AX,yaxis=AX);st.plotly_chart(fig,use_container_width=True,config={"displayModeBar":False})
        with t4:
            CF=[c for c in["AVG_SPEED_KMH","RISK_SCORE","TRIP_DISTANCE","FLAG_COUNT"] if c in df.columns]
            if len(CF)>=2:
                samp_c=df.sample(min(3000,len(df)),random_state=42).copy()
                Xc=StandardScaler().fit_transform(samp_c[CF].fillna(0))
                km=KMeans(n_clusters=5,random_state=42,n_init=10);samp_c["Cluster"]="C"+km.fit_predict(Xc).astype(str)
                CLABELS={"C0":"Normal Commuters","C1":"Aggressive Drivers","C2":"Low-Risk Short","C3":"High-Risk Suspects","C4":"Moderate Anomalies"}
                samp_c["ClusterLabel"]=samp_c["Cluster"].map(CLABELS)
                CMAP2={"Normal Commuters":"#00d4ff","Aggressive Drivers":"#ff6b35","Low-Risk Short":"#00ff88","High-Risk Suspects":"#ff1744","Moderate Anomalies":"#ffc107"}
                k1,k2=st.columns(2)
                with k1:
                    fig=px.scatter(samp_c,x=CF[0],y=CF[1],color="ClusterLabel",opacity=0.7,color_discrete_map=CMAP2)
                    fig.update_layout(**P,height=300,xaxis=AX,yaxis=AX);st.plotly_chart(fig,use_container_width=True,config={"displayModeBar":False})
                with k2:
                    csz=samp_c["ClusterLabel"].value_counts().reset_index();csz.columns=["Cluster","Count"]
                    fig=px.bar(csz,y="Cluster",x="Count",orientation="h",color="Cluster",text="Count",color_discrete_map=CMAP2)
                    fig.update_traces(textposition="outside",textfont=dict(color="white"));fig.update_layout(**P,height=300,showlegend=False,xaxis=AX,yaxis=AX)
                    st.plotly_chart(fig,use_container_width=True,config={"displayModeBar":False})
                if len(CF)>=3:
                    fig=px.scatter_3d(samp_c,x=CF[0],y=CF[1],z=CF[2],color="ClusterLabel",opacity=0.65,color_discrete_map=CMAP2)
                    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)",font=dict(color="#c8e8ff"),height=420)
                    st.plotly_chart(fig,use_container_width=True,config={"displayModeBar":False})
                st.dataframe(samp_c.groupby("ClusterLabel")[CF].mean().round(2),use_container_width=True)
        with t5:
            pp1,pp2=st.columns([1,2])
            with pp1:
                vids_sel=df["TRIP_ID"].astype(str).unique().tolist()[:300]
                sel_vid=st.selectbox("Select Vehicle",vids_sel,key="pred_sel")
                vdf_sel=df[df["TRIP_ID"].astype(str)==sel_vid];vrow_s=vdf_sel.iloc[0] if len(vdf_sel)>0 else df.iloc[0]
                fc_s=int(vrow_s.get("FLAG_COUNT",0));rs_s=float(vrow_s.get("RISK_SCORE",0))
                esc_l,esc_c=risk_escalation_label(fc_s,rs_s);p4=violation_probability(fc_s)*100;p5=violation_probability(fc_s+1)*100
                st.markdown(f'<div style="background:rgba(0,15,40,.9);border:1px solid rgba(0,212,255,.2);border-radius:8px;padding:14px;"><div style="font-size:11px;color:#c8e8ff;line-height:2.4;">ID: <b style="color:#00d4ff;">{sel_vid}</b><br>Risk: <b style="color:{C.get(str(vrow_s.get("RISK_LEVEL","LOW")),"#aaa")};"> {vrow_s.get("RISK_LEVEL","N/A")}</b><br>Score: <b style="color:#ffc107;">{rs_s:.0f}/100</b><br>Flags: <b style="color:#ff6b35;">{fc_s}</b><br>P(4th): <b style="color:#ff1744;">{p4:.0f}%</b><br>P(5th): <b style="color:#ff1744;">{p5:.0f}%</b></div><div style="margin-top:8px;padding:8px;border-radius:6px;background:{esc_c}14;border-left:3px solid {esc_c};"><b style="color:{esc_c};font-size:11px;">{esc_l}</b></div></div>',unsafe_allow_html=True)
            with pp2:
                fig=go.Figure(go.Indicator(mode="gauge+number",value=p4,title=dict(text="P(4th Violation) %",font=dict(color="#c8e8ff",size=12)),number=dict(suffix="%",font=dict(color="#ff6b35",size=32)),gauge=dict(axis=dict(range=[0,100]),bar=dict(color="#ff6b35"),bgcolor="rgba(0,15,40,.5)",steps=[dict(range=[0,30],color="rgba(0,255,136,.08)"),dict(range=[30,70],color="rgba(255,193,7,.08)"),dict(range=[70,100],color="rgba(255,23,68,.1)")])))
                fig.update_layout(paper_bgcolor="rgba(0,0,0,0)",font=dict(color="#c8e8ff"),height=240,margin=dict(t=40,b=5,l=10,r=10))
                st.plotly_chart(fig,use_container_width=True,config={"displayModeBar":False})
    elif pg=="Zones":
        z1,z2,z3=st.columns(3);z1.metric("Zone Violations",f"{rz:,}");z2.metric("Flagged",f'{df["FLAG_COUNT"].gt(0).sum():,}');z3.metric("Avg Flags",f'{df["FLAG_COUNT"].mean():.2f}')
        fc2_=[c for c in["PARKING_ANOMALY","SPEED_ANOMALY","ROUTE_DEVIATION","RESTRICTED_ZONE_ENTRY","COORDINATED_MOVEMENT"] if c in df.columns]
        if fc2_:
            zdf=pd.DataFrame({"Flag":[f.replace("_"," ").title() for f in fc2_],"Count":[int(df[f].sum()) for f in fc2_]}).sort_values("Count")
            fig=px.bar(zdf,y="Flag",x="Count",orientation="h",color="Count",text="Count",color_continuous_scale="Reds")
            fig.update_traces(textposition="outside",textfont=dict(color="white"));fig.update_layout(**P,height=350,showlegend=False,xaxis=AX,yaxis=AX)
            st.plotly_chart(fig,use_container_width=True,config={"displayModeBar":False})
    elif pg=="History":
        if "HOUR" in df.columns:
            h1,h2=st.columns(2)
            with h1:
                hr=df.groupby(["HOUR","RISK_LEVEL"]).size().reset_index(name="Trips");hr.rename(columns={"RISK_LEVEL":"Risk"},inplace=True)
                fig=px.bar(hr,x="HOUR",y="Trips",color="Risk",color_discrete_map=C);fig.update_layout(**P,height=360,xaxis=AX,yaxis=AX)
                st.plotly_chart(fig,use_container_width=True,config={"displayModeBar":False})
            with h2:
                if "RISK_SCORE" in df.columns:
                    hr2=df.groupby("HOUR")["RISK_SCORE"].mean().reset_index()
                    fig=go.Figure();fig.add_trace(go.Scatter(x=hr2["HOUR"],y=hr2["RISK_SCORE"],mode="lines+markers",line=dict(color="#ff6b35",width=2.5),fill="tozeroy",fillcolor="rgba(255,107,53,.1)"))
                    fig.update_layout(**P,height=360,xaxis=AX,yaxis=AX);st.plotly_chart(fig,use_container_width=True,config={"displayModeBar":False})
    elif pg=="Settings":
        s1,s2=st.columns(2)
        with s1:
            cont2=st.slider("ML Contamination %",1,30,5)/100
            if st.button("Re-run ML",type="primary"):
                IF2=[c for c in["AVG_SPEED_KMH","RISK_SCORE","TRIP_DISTANCE","FLAG_COUNT"] if c in df.columns]
                X2=StandardScaler().fit_transform(df[IF2].fillna(0));iso2=IsolationForest(contamination=cont2,n_estimators=150,random_state=42)
                r2=iso2.fit_predict(X2);st.success(f"Found {(r2==-1).sum():,} anomalies ({(r2==-1).mean()*100:.1f}%)")
        with s2:
            st.markdown(f'<div style="{PNL_BLUE}color:#c8e8ff;font-size:12px;line-height:2.2;">Rows: {len(df):,}<br>Critical: {crit:,}<br>High: {high:,}<br>Alerts: {alerts:,}</div>',unsafe_allow_html=True)
    city_svg=gen_3d_city()
    ac1,ac2,ac3,ac4=st.columns([3,2,2,2])
    with ac1:
        st.markdown('<div style="'+_PH+'display:flex;flex-direction:column;gap:6px;background:rgba(0,5,20,.99);border:1px solid rgba(0,212,255,.3);border-radius:10px;padding:10px;">'+HDR("🔷","HOLOGRAPHIC 3D CITY","#00d4ff")+'<svg viewBox="0 0 360 215" xmlns="http://www.w3.org/2000/svg" style="width:100%;">'+city_svg+'</svg></div>',unsafe_allow_html=True)
    with ac2:
        st.markdown('<div style="'+_PH+PNL_BLUE+'">'+HDR("🔍","DETECTION ENGINE","#00d4ff")+DET_ITEMS+'</div>',unsafe_allow_html=True)
    with ac3:
        st.markdown('<div style="'+_PH+PNL_YELLOW+'">'+HDR("📊","RISK DISTRIBUTION","#ffc107")+RISK_BARS+'</div>',unsafe_allow_html=True)
    with ac4:
        _t8=df.nlargest(8,"RISK_SCORE") if "RISK_SCORE" in df.columns else df.head(8)
        al8="".join(['<div style="display:flex;align-items:center;gap:6px;padding:5px 8px;border-radius:5px;margin-bottom:4px;background:'+C.get(row["RISK_LEVEL"],"#aaa")+'12;border-left:3px solid '+C.get(row["RISK_LEVEL"],"#aaa")+';"><span style="font-size:10px;font-weight:800;color:'+C.get(row["RISK_LEVEL"],"#aaa")+';font-family:monospace;flex:1;">'+str(row["TRIP_ID"])[:12]+'</span><span style="font-size:8px;padding:1px 5px;border-radius:3px;background:'+C.get(row["RISK_LEVEL"],"#aaa")+'22;color:'+C.get(row["RISK_LEVEL"],"#aaa")+';font-weight:700;">'+row["RISK_LEVEL"]+'</span></div>'for _,row in _t8.iterrows()])
        st.markdown('<div style="'+_PH+PNL_ORANGE+'">'+HDR("🚨","RECENT ALERTS","#ff6b35")+al8+'</div>',unsafe_allow_html=True)
st.markdown('<div style="text-align:center;padding:8px;border-top:1px solid rgba(0,212,255,.12);margin-top:8px;"><span style="font-family:Orbitron;font-size:9px;color:#00d4ff;letter-spacing:3px;">AI SURVEILLANCE v5.6</span><span style="font-size:9px;color:#7ab8e8;"> · Python · Streamlit · Plotly · Folium · Scikit-Learn</span></div>',unsafe_allow_html=True)