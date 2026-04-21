import streamlit as st
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import time

st.set_page_config(
    page_title="Quantum Laboratory",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for a dark, futuristic scientific UI
st.markdown("""
<style>
    .main { background-color: #05060a; }
    .stApp { background-color: #05060a; color: #e0e8f0; }
    .metric-card {
        background: rgba(0,20,35,0.9);
        border: 1px solid rgba(0,200,255,0.2);
        border-radius: 8px;
        padding: 12px;
        text-align: center;
        margin: 4px;
    }
    .metric-val { font-size: 22px; color: #00e5ff; font-weight: bold; }
    .metric-key { font-size: 11px; color: rgba(180,210,240,0.5); margin-top: 2px; }
    .result-box {
        background: rgba(0,30,15,0.9);
        border: 1px solid rgba(0,200,100,0.4);
        border-radius: 8px;
        padding: 16px;
        text-align: center;
    }
    .info-box {
        background: rgba(0,20,35,0.8);
        border: 1px solid rgba(0,200,255,0.1);
        border-radius: 8px;
        padding: 14px;
        font-size: 13px;
        color: rgba(180,210,240,0.7);
        line-height: 1.7;
    }
    h1, h2, h3 { color: #00e5ff !important; }
    .stSlider > label { color: rgba(0,200,255,0.8) !important; }
    .stButton > button {
        background: rgba(255,80,80,0.1) !important;
        border: 1px solid rgba(255,80,80,0.5) !important;
        color: #ff8080 !important;
        border-radius: 8px !important;
        width: 100% !important;
        font-size: 13px !important;
        letter-spacing: 0.08em !important;
        padding: 10px !important;
    }
    .stButton > button:hover {
        background: rgba(255,80,80,0.2) !important;
    }
    [data-testid="stSidebar"] {
        background-color: #080c14 !important;
        border-right: 1px solid rgba(0,200,255,0.1) !important;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("## 🌌 Quantum Superposition Simulator")
st.markdown("""
<div class='info-box'>
<b style='color:#00e5ff'>What is Superposition?</b> In classical computing, a bit is either 0 <i>or</i> 1. 
A <b>qubit</b> exists as a quantum mixture of both states until measured:
&nbsp;&nbsp;<b>|ψ⟩ = α|0⟩ + β|1⟩</b> &nbsp;
where |α|² + |β|² = 1 (probability conservation). α and β are <i>complex</i> numbers; the phase φ of β 
creates observable effects in interference experiments. Upon measurement, the wavefunction collapses 
into a single state — a fundamentally irreversible process.
</div>
""", unsafe_allow_html=True)

st.markdown("")

# --- SIDEBAR CONFIGURATION ---
with st.sidebar:
    st.markdown("### ⚙️ State Parameters")

    st.markdown("**Basis State Presets**")
    preset_cols = st.columns(5)
    presets = {"|0⟩": (0, 0), "|1⟩": (180, 0), "|+⟩": (90, 0), "|−⟩": (90, 180), "|i⟩": (90, 90)}
    
    if "theta_deg" not in st.session_state:
        st.session_state.theta_deg = 90
        st.session_state.phi_deg = 0
        st.session_state.measure_counts = {0: 0, 1: 0}

    for i, (label, (th, ph)) in enumerate(presets.items()):
        with preset_cols[i]:
            if st.button(label, key=f"preset_{label}"):
                st.session_state.theta_deg = th
                st.session_state.phi_deg = ph

    st.markdown("")
    theta_deg = st.slider("θ — Polar Angle (State Mixture)", 0, 180,
                          st.session_state.theta_deg, key="theta_slider")
    phi_deg = st.slider("φ — Phase Angle", 0, 360,
                        st.session_state.phi_deg, key="phi_slider")

    st.session_state.theta_deg = theta_deg
    st.session_state.phi_deg = phi_deg

    st.markdown("---")
    st.markdown("### 📐 Mathematical State")

    theta = theta_deg * np.pi / 180
    phi_rad = phi_deg * np.pi / 180

    alpha = np.cos(theta / 2)
    beta_r = np.cos(phi_rad) * np.sin(theta / 2)
    beta_i = np.sin(phi_rad) * np.sin(theta / 2)
    beta_mag = np.sqrt(beta_r**2 + beta_i**2)
    p0 = alpha**2
    p1 = beta_r**2 + beta_i**2

    st.latex(r"|\psi\rangle = \alpha|0\rangle + \beta e^{i\varphi}|1\rangle")
    st.markdown(f"**α =** `{alpha:.4f}`")
    st.markdown(f"**|β| =** `{beta_mag:.4f}`")
    st.markdown(f"**φ =** `{phi_deg}°`")

    st.markdown("")
    # Derived metrics
    entropy = -(p0 * np.log2(p0 + 1e-10) + p1 * np.log2(p1 + 1e-10))
    coherence = 2 * abs(alpha) * beta_mag

    col_m1, col_m2 = st.columns(2)
    with col_m1:
        st.markdown(f"""<div class='metric-card'>
            <div class='metric-val'>{entropy:.3f}</div>
            <div class='metric-key'>Entropy (bits)</div>
        </div>""", unsafe_allow_html=True)
    with col_m2:
        st.markdown(f"""<div class='metric-card'>
            <div class='metric-val'>{coherence:.3f}</div>
            <div class='metric-key'>Coherence</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 🔬 Measurement")
    if st.button("MEASURE — COLLAPSE WAVEFUNCTION"):
        with st.spinner("Performing quantum measurement..."):
            time.sleep(0.6)
        outcome = 0 if np.random.random() < p0 else 1
        st.session_state.measure_counts[outcome] += 1
        st.balloons()
        st.markdown(f"""<div class='result-box'>
            <div style='font-size:22px;color:#00ff88;font-weight:bold'>|{outcome}⟩ Measured</div>
            <div style='font-size:11px;color:rgba(0,200,100,0.6);margin-top:4px'>WAVEFUNCTION COLLAPSED</div>
        </div>""", unsafe_allow_html=True)

    total = st.session_state.measure_counts[0] + st.session_state.measure_counts[1]
    if total > 0:
        st.markdown(f"**Total measurements:** {total}")
        st.markdown(f"|0⟩: {st.session_state.measure_counts[0]} &nbsp;|&nbsp; |1⟩: {st.session_state.measure_counts[1]}")

    if st.button("Reset Statistics", key="reset_btn"):
        st.session_state.measure_counts = {0: 0, 1: 0}

# --- BLOCH SPHERE VISUALIZATION ---
x_bloch = np.sin(theta) * np.cos(phi_rad)
y_bloch = np.sin(theta) * np.sin(phi_rad)
z_bloch = np.cos(theta)

u, v = np.mgrid[0:2*np.pi:40j, 0:np.pi:20j]
xs = np.cos(u) * np.sin(v)
ys = np.sin(u) * np.sin(v)
zs = np.cos(v)

bloch_fig = go.Figure()

# Sphere surface
bloch_fig.add_trace(go.Surface(
    x=xs, y=ys, z=zs,
    opacity=0.06,
    showscale=False,
    colorscale=[[0, '#001830'], [1, '#003060']],
    hoverinfo='skip'
))

# Grid lines
for lat in np.linspace(-np.pi/2, np.pi/2, 7):
    lx = np.cos(lat) * np.cos(np.linspace(0, 2*np.pi, 60))
    ly = np.cos(lat) * np.sin(np.linspace(0, 2*np.pi, 60))
    lz = np.sin(lat) * np.ones(60)
    bloch_fig.add_trace(go.Scatter3d(x=lx, y=ly, z=lz,
        mode='lines', line=dict(color='rgba(0,150,200,0.15)', width=1),
        hoverinfo='skip', showlegend=False))

# Equatorial line
eq_t = np.linspace(0, 2*np.pi, 120)
bloch_fig.add_trace(go.Scatter3d(
    x=np.cos(eq_t), y=np.sin(eq_t), z=np.zeros(120),
    mode='lines', line=dict(color='rgba(0,200,255,0.4)', width=2),
    hoverinfo='skip', showlegend=False))

# Axes
for ax_v, ax_col, ax_lbl in [
    ([1,0,0], '#ff6060', 'X'), ([0,1,0], '#60ff60', 'Y'), ([0,0,1], '#6090ff', 'Z')]:
    bloch_fig.add_trace(go.Scatter3d(
        x=[-ax_v[0], ax_v[0]], y=[-ax_v[1], ax_v[1]], z=[-ax_v[2], ax_v[2]],
        mode='lines+text',
        line=dict(color=ax_col, width=2),
        text=['', ax_lbl], textfont=dict(color=ax_col, size=12),
        hoverinfo='skip', showlegend=False))

# Basis labels
bloch_fig.add_trace(go.Scatter3d(
    x=[0, 0], y=[0, 0], z=[-1.25, 1.25],
    mode='text',
    text=['|1⟩', '|0⟩'],
    textfont=dict(color='rgba(100,180,255,0.8)', size=13),
    hoverinfo='skip', showlegend=False))

# Trajectory to current state
n_traj = 20
traj_angles = np.linspace(0, theta, n_traj)
traj_x = np.sin(traj_angles) * np.cos(phi_rad)
traj_y = np.sin(traj_angles) * np.sin(phi_rad)
traj_z = np.cos(traj_angles)
bloch_fig.add_trace(go.Scatter3d(
    x=traj_x, y=traj_y, z=traj_z,
    mode='lines',
    line=dict(color=[f'rgba(0,{int(150+i*3)},{int(200+i*2)},{0.1+i*0.04})' for i in range(n_traj)],
              width=3),
    hoverinfo='skip', showlegend=False))

# State Vector
bloch_fig.add_trace(go.Scatter3d(
    x=[0, x_bloch], y=[0, y_bloch], z=[0, z_bloch],
    mode='lines+markers',
    line=dict(color='#00e5ff', width=6),
    marker=dict(size=[0, 8], color=['#00e5ff', '#00e5ff'],
                symbol=['circle', 'circle'],
                line=dict(color='white', width=1)),
    name='State Vector |ψ⟩'
))

# Layout update
bloch_fig.update_layout(
    scene=dict(
        xaxis=dict(title='X (Interference)', showgrid=False, zeroline=False),
        yaxis=dict(title='Y (Phase)', showgrid=False, zeroline=False),
        zaxis=dict(title='Z (Computational)', showgrid=False, zeroline=False),
        bgcolor='rgba(5,6,10,1)',
        camera=dict(eye=dict(x=1.4, y=1.4, z=0.8))
    ),
    paper_bgcolor='rgba(5,6,10,1)',
    margin=dict(l=0, r=0, t=0, b=0),
    height=480,
    showlegend=True,
    legend=dict(x=0, y=1, font=dict(color='rgba(0,200,255,0.7)', size=11))
)

# --- WAVEFUNCTION PLOT ---
t_arr = np.linspace(0, 4*np.pi, 500)
psi_x_comp = np.abs(alpha) * np.cos(t_arr)
psi_y_comp = beta_mag * np.cos(t_arr + phi_rad)
psi_total = psi_x_comp + psi_y_comp
psi_prob = psi_total**2

wave_fig = make_subplots(
    rows=2, cols=1,
    subplot_titles=("Wavefunction Components", "Probability Density |ψ|²"),
    vertical_spacing=0.12
)

wave_fig.add_trace(go.Scatter(x=t_arr, y=psi_x_comp, name='α|0⟩', line=dict(color='#00e5ff')), row=1, col=1)
wave_fig.add_trace(go.Scatter(x=t_arr, y=psi_y_comp, name='β|1⟩', line=dict(color='#ff6b6b', dash='dash')), row=1, col=1)
wave_fig.add_trace(go.Scatter(x=t_arr, y=psi_total, name='|ψ⟩ total', line=dict(color='#80ffb0', width=2.5)), row=1, col=1)
wave_fig.add_trace(go.Scatter(x=t_arr, y=psi_prob, name='|ψ|²', fill='tozeroy', line=dict(color='#ffcc44')), row=2, col=1)

wave_fig.update_layout(height=360, paper_bgcolor='rgba(5,6,10,1)', plot_bgcolor='rgba(0,10,20,0.8)', font=dict(color='white'))

# --- MEASUREMENT HISTOGRAM ---
total = st.session_state.measure_counts[0] + st.session_state.measure_counts[1]
r0_emp = st.session_state.measure_counts[0] / total if total > 0 else 0
r1_emp = st.session_state.measure_counts[1] / total if total > 0 else 0

histo_fig = go.Figure()
histo_fig.add_trace(go.Bar(x=['|0⟩ (Theoretical)', '|1⟩ (Theoretical)'], y=[p0, p1], name='Born Rule Prediction', marker_color='rgba(0,200,255,0.3)'))
histo_fig.add_trace(go.Bar(x=['|0⟩ (Experimental)', '|1⟩ (Experimental)'], y=[r0_emp, r1_emp], name='Actual Observations', marker_color='rgba(0,200,255,0.8)'))
histo_fig.update_layout(height=280, barmode='group', paper_bgcolor='rgba(5,6,10,1)', plot_bgcolor='rgba(0,10,20,0.8)', font=dict(color='white'))

# --- MAIN PAGE LAYOUT ---
col1, col2 = st.columns([3, 2])

with col1:
    st.markdown("### 🔮 Bloch Sphere Visualization")
    st.plotly_chart(bloch_fig, use_container_width=True)

with col2:
    st.markdown("### 📊 Probability Distribution")
    prob_bar = go.Figure(go.Bar(
        x=['|0⟩', '|1⟩'], y=[p0, p1],
        marker_color=['#00e5ff', '#ff6b6b'],
        text=[f'{p0*100:.1f}%', f'{p1*100:.1f}%'],
        textposition='inside'
    ))
    prob_bar.update_layout(height=200, paper_bgcolor='rgba(5,6,10,1)', plot_bgcolor='rgba(0,10,20,0.8)', font=dict(color='white'), margin=dict(t=10))
    st.plotly_chart(prob_bar, use_container_width=True)

    st.markdown("### 🎯 State Intelligence")
    # Metric rows
    mc0, mc1, mc2, mc3 = st.columns(4)
    with mc0: st.markdown(f"<div class='metric-card'><div class='metric-val'>{theta_deg}°</div><div class='metric-key'>θ</div></div>", unsafe_allow_html=True)
    with mc1: st.markdown(f"<div class='metric-card'><div class='metric-val'>{phi_deg}°</div><div class='metric-key'>φ</div></div>", unsafe_allow_html=True)
    with mc2: st.markdown(f"<div class='metric-card'><div class='metric-val'>{entropy:.2f}</div><div class='metric-key'>Entropy</div></div>", unsafe_allow_html=True)
    with mc3: st.markdown(f"<div class='metric-card'><div class='metric-val'>{coherence:.2f}</div><div class='metric-key'>Coherence</div></div>", unsafe_allow_html=True)

    # Contextual info based on state
    if theta_deg == 0:
        info = "θ=0°: Ground State |0⟩. Zero uncertainty, measurement always yields 0."
    elif theta_deg == 180:
        info = "θ=180°: Excited State |1⟩. Pure state, measurement always yields 1."
    elif theta_deg == 90 and phi_deg == 0:
        info = "|+⟩ Hadamard State: Balanced superposition. Maximum quantum uncertainty (1 bit entropy)."
    else:
        info = f"Current State: θ={theta_deg}°, φ={phi_deg}°. Phase angle φ dictates quantum interference patterns."
    st.markdown(f"<div class='info-box'>{info}</div>", unsafe_allow_html=True)

st.markdown("---")
col3, col4 = st.columns(2)
with col3:
    st.markdown("### 〰️ Wavefunction Analysis")
    st.plotly_chart(wave_fig, use_container_width=True)
with col4:
    st.markdown("### 📈 Measurement Statistics")
    st.plotly_chart(histo_fig, use_container_width=True)

st.markdown("---")
st.caption("Engineered with Quantum Physics principles (Born Rule, Bloch Sphere Formalism) using Python, Streamlit, and Plotly.")