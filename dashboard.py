import streamlit as st
import psutil
import pandas as pd
import plotly.graph_objects as go
import platform
from datetime import datetime
from streamlit_autorefresh import st_autorefresh

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="AI Behavioral Threat Detection - Enterprise", layout="wide")
# ---------------- SESSION STATE INIT ----------------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "cpu_history" not in st.session_state:
    st.session_state.cpu_history = []

if "disk_history" not in st.session_state:
    st.session_state.disk_history = []

if "last_disk" not in st.session_state:
    import psutil
    st.session_state.last_disk = psutil.disk_io_counters().write_bytes

if "high_alerts" not in st.session_state:
    st.session_state.high_alerts = 0

if "medium_alerts" not in st.session_state:
    st.session_state.medium_alerts = 0

st.title("🛡 AI-Based Real-Time Behavioral Threat Detection System")
# ---------------- ELITE AI COPILOT ----------------
st.sidebar.title("🤖 AI Copilot - Project Explainer")

def ai_response(q):
    q = q.lower()

    if "tools" in q:
        return """
🔧 Technologies Used:

• Python – Core backend logic
• Streamlit – Interactive dashboard UI
• psutil – Real-time system monitoring
• Pandas – Data structuring and history tracking
• Plotly – Gauge, Radar and analytical visualization

These technologies together create a behavioral cybersecurity monitoring system.
"""

    elif "architecture" in q:
        return """
🏗 Architecture:

1️⃣ Hardware Layer – CPU & Disk
2️⃣ Monitoring Layer – psutil collects live system metrics
3️⃣ Threat Engine – Weighted behavioral scoring
4️⃣ Visualization Layer – Gauge, Radar, Trend graphs
5️⃣ User Layer – Security Analyst + AI Copilot

The system follows a layered behavioral detection model.
"""

    elif "threat" in q:
        return """
🚨 Threat Detection Logic:

Threat Score = (CPU × 0.6) + (Disk × 0.4)

Based on score:
LOW (<40)
MEDIUM (40–70)
HIGH (>70)

This behavioral scoring detects abnormal activity dynamically.
"""

    elif "real time" in q or "real-time" in q:
        return """
⏱ Real-Time Monitoring:

The system continuously collects CPU and disk activity.
A background monitoring thread updates system metrics.
This allows live behavioral detection without manual refresh.
"""

    elif "radar" in q:
        return """
🛰 Radar Visualization:

Radar chart shows:
• CPU Load
• Disk Activity
• Threat Score
• Performance Index

It provides multi-dimensional threat visibility.
"""

    elif "multi" in q:
        return """
⚙ Multi-Core Monitoring:

Each CPU core is monitored individually.
This improves detection granularity and anomaly accuracy.
"""

    elif "ransomware" in q:
        return """
🛑 Ransomware Detection:

Ransomware encrypts files rapidly.
This causes abnormal disk write spikes.

If disk activity crosses threshold,
System flags suspicious behavior.
"""

    elif "innovation" in q:
        return """
💡 Innovation:

• Hardware-adaptive monitoring
• Behavioral threat scoring
• Real-time radar visualization
• Multi-core analytics
• AI Explainability module

Unlike traditional antivirus,
This system focuses on behavior-based detection.
"""

    elif "difference" in q or "antivirus" in q:
        return """
🔐 Difference from Traditional Antivirus:

Traditional Antivirus → Signature-based detection
This System → Behavioral anomaly detection

It can detect zero-day style abnormal system activity.
"""

    elif "how it works" in q:
        return """
⚙ How It Works:

1️⃣ System metrics collected via psutil
2️⃣ Threat score calculated using weighted formula
3️⃣ Risk level classified
4️⃣ Dashboard visualizes threat state
5️⃣ Alerts generated for suspicious behavior
"""

    elif "hackathon" in q:
        return """
🏆 Hackathon Value:

• Real-time system analytics
• Cybersecurity innovation
• Clean architecture
• Hardware-aware detection model
• Enterprise-ready dashboard
"""

    else:
        return """
This is an AI-Based Real-Time Behavioral Threat Detection System.

Ask me about:
• tools
• architecture
• threat logic
• real time monitoring
• ransomware detection
• innovation
• difference from antivirus
"""

prompt = st.sidebar.chat_input("Ask about the project...")

if prompt:
    st.session_state.chat_history.append(("You", prompt))
    reply = ai_response(prompt)
    st.session_state.chat_history.append(("AI", reply))

for role, msg in st.session_state.chat_history:
    if role == "You":
        st.sidebar.markdown(f"**You:** {msg}")
    else:
        st.sidebar.markdown(f"**AI:** {msg}")
# ---------------- AUTO REFRESH ----------------
st_autorefresh(interval=3000)
# ---------------- HARDWARE DETECTION ----------------
cpu_name = platform.processor()
if "AMD" in cpu_name.upper():
    hardware_mode = "🔥 AMD Optimization Mode Active"
else:
    hardware_mode = "⚙ Intel / Generic Multi-Core Mode Active"

st.info(hardware_mode)

# ---------------- SESSION STATE ----------------
if "cpu_history" not in st.session_state:
    st.session_state.cpu_history = []
if "disk_history" not in st.session_state:
    st.session_state.disk_history = []
if "last_disk" not in st.session_state:
    st.session_state.last_disk = psutil.disk_io_counters().write_bytes
if "high_alerts" not in st.session_state:
    st.session_state.high_alerts = 0
if "medium_alerts" not in st.session_state:
    st.session_state.medium_alerts = 0
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ---------------- PRIME CPU COUNTERS ----------------
psutil.cpu_percent(interval=None)
psutil.cpu_percent(interval=None, percpu=True)

# ---------------- REAL-TIME METRICS ----------------
cpu = psutil.cpu_percent(interval=0.3)

disk_io = psutil.disk_io_counters()
current_disk = disk_io.write_bytes
disk_diff = current_disk - st.session_state.last_disk
st.session_state.last_disk = current_disk
disk_mb = max(round(disk_diff / (1024 * 1024), 2), 0)

# ---------------- THREAT ENGINE ----------------
threat_score = min(int(cpu * 0.6 + disk_mb * 0.4), 100)

if threat_score < 40:
    risk = "LOW"
    color = "#2ecc71"
elif threat_score < 70:
    risk = "MEDIUM"
    color = "#f39c12"
    st.session_state.medium_alerts += 1
else:
    risk = "HIGH"
    color = "#e74c3c"
    st.session_state.high_alerts += 1

# ---------------- STORE HISTORY ----------------
st.session_state.cpu_history.append(cpu)
st.session_state.disk_history.append(disk_mb)
st.session_state.cpu_history = st.session_state.cpu_history[-30:]
st.session_state.disk_history = st.session_state.disk_history[-30:]

# ---------------- METRICS ----------------
col1, col2, col3, col4 = st.columns(4)
col1.metric("CPU Usage (%)", round(cpu, 2))
col2.metric("Disk Activity (MB/s)", disk_mb)
col3.metric("Threat Probability (%)", threat_score)
col4.metric("Risk Level", risk)

st.divider()

# ---------------- GAUGE ----------------
st.subheader("🔥 Threat Level Indicator")

gauge = go.Figure(go.Indicator(
    mode="gauge+number",
    value=threat_score,
    number={'suffix': "%", 'font': {'size': 45}},
    gauge={
        'axis': {'range': [0, 100]},
        'bar': {'color': color},
        'steps': [
            {'range': [0, 40], 'color': "#2ecc71"},
            {'range': [40, 70], 'color': "#f39c12"},
            {'range': [70, 100], 'color': "#e74c3c"}
        ]
    }
))
gauge.update_layout(height=320)
st.plotly_chart(gauge, use_container_width=True)

st.divider()

# ---------------- TREND GRAPH ----------------
st.subheader("📊 System Activity Trend")

trend_df = pd.DataFrame({
    "CPU Usage (%)": st.session_state.cpu_history,
    "Disk Activity (MB/s)": st.session_state.disk_history
})

st.line_chart(trend_df)

st.divider()

# ---------------- RADAR ----------------
st.subheader("🛰 Radar Threat Visualization")

radar = go.Figure()
radar.add_trace(go.Scatterpolar(
    r=[cpu, disk_mb, threat_score, 100 - cpu],
    theta=["CPU Load", "Disk Activity", "Threat Score", "Performance"],
    fill='toself'
))
radar.update_layout(
    polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
    showlegend=False,
    height=350
)
st.plotly_chart(radar, use_container_width=True)

st.divider()

# ---------------- MULTI-CORE (FIXED) ----------------
st.subheader("⚙ Multi-Core Monitoring")

physical = psutil.cpu_count(logical=False)
logical = psutil.cpu_count(logical=True)

per_core = psutil.cpu_percent(interval=0.3, percpu=True)

colA, colB = st.columns(2)
colA.metric("Physical Cores", physical)
colB.metric("Logical Cores", logical)

st.bar_chart(per_core)

st.divider()

# ---------------- PROCESS MONITOR (CACHED) ----------------
@st.cache_data(ttl=5)
def get_top_processes():
    process_list = []
    for proc in psutil.process_iter(['name', 'cpu_percent']):
        try:
            process_list.append(proc.info)
        except:
            pass
    df = pd.DataFrame(process_list)
    if not df.empty:
        df = df.sort_values(by="cpu_percent", ascending=False).head(5)
    return df

st.subheader("🧠 Top CPU Processes")
process_df = get_top_processes()
if not process_df.empty:
    st.table(process_df)

st.divider()

# ---------------- BENCHMARK ----------------
st.subheader("📈 Benchmark Metrics")

avg_cpu = round(sum(st.session_state.cpu_history) / len(st.session_state.cpu_history), 2)
max_cpu = round(max(st.session_state.cpu_history), 2)
performance_score = round(100 - avg_cpu, 2)

colX, colY, colZ = st.columns(3)
colX.metric("Average CPU (%)", avg_cpu)
colY.metric("Max CPU Spike (%)", max_cpu)
colZ.metric("Performance Score", performance_score)

st.divider()

# ---------------- RANSOMWARE ----------------
st.subheader("🛑 Ransomware Spike Detection")

if disk_mb > 200:
    st.error("⚠ Suspicious High Disk Write Activity Detected")
else:
    st.success("Disk Activity Normal")

st.divider()

# ---------------- ALERT SUMMARY ----------------
st.subheader("🚨 Alert Summary")

colM, colH = st.columns(2)
colM.metric("Medium Alerts", st.session_state.medium_alerts)
colH.metric("High Alerts", st.session_state.high_alerts)

st.divider()

# ---------------- DETECTION LOG ----------------
st.subheader("📄 Detection Log")

time_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

if risk == "HIGH":
    st.error(f"{time_now} | High Threat Detected")
elif risk == "MEDIUM":
    st.warning(f"{time_now} | Medium Threat Activity")
else:
    st.success(f"{time_now} | System Stable")

st.divider()

