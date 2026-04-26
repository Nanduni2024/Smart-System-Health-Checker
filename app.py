import streamlit as st
import psutil
import time
from datetime import datetime

# page config
st.set_page_config(page_title="System Monitor", layout="centered")

st.title("🚀 System Health Monitor Dashboard")
st.write("Live CPU, RAM, Disk usage with Graph")

# data storage
if "cpu_history" not in st.session_state:
    st.session_state.cpu_history = []
if "time_history" not in st.session_state:
    st.session_state.time_history = []

placeholder = st.empty()


while True:
    # system stats
    cpu = psutil.cpu_percent(interval=1)
    ram = psutil.virtual_memory().percent
    disk = psutil.disk_usage('/').percent

    now = datetime.now().strftime("%H:%M:%S")

    # store history
    st.session_state.cpu_history.append(cpu)
    st.session_state.time_history.append(now)

    # keep only last 20 values
    st.session_state.cpu_history = st.session_state.cpu_history[-20:]
    st.session_state.time_history = st.session_state.time_history[-20:]

    with placeholder.container():

        st.subheader("📊 Current System Status")
        st.metric("CPU Usage", f"{cpu}%")
        st.metric("RAM Usage", f"{ram}%")
        st.metric("Disk Usage", f"{disk}%")

        st.subheader("📈 CPU Usage History")

        st.line_chart(
            data=st.session_state.cpu_history
        )

        st.caption(f"Last updated: {now}")

    time.sleep(3)