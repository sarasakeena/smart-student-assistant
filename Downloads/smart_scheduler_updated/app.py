import streamlit as st
import requests
from datetime import date, datetime

API_URL = "http://localhost:8000/generate_schedule"

st.set_page_config(page_title="Smart Study Scheduler", layout="wide")
st.title("📅 Smart Study Scheduler")

# 🧠 Track number of tasks dynamically
if "task_count" not in st.session_state:
    st.session_state.task_count = 3

def add_task():
    st.session_state.task_count += 1

st.sidebar.markdown("## 🗓️ Weekly Priority Overview")
st.button("➕ Add Another Task", on_click=add_task)

task_data = []
with st.form("task_form"):
    st.subheader("📌 Your Tasks")
    for i in range(st.session_state.task_count):
        with st.expander(f"Task {i + 1}", expanded=True):
            col1, col2, col3 = st.columns(3)
            with col1:
                name = st.text_input("Task Name", key=f"name{i}")
            with col2:
                hours = st.number_input("Hours", min_value=0, key=f"hours{i}")
            with col3:
                minutes = st.number_input("Minutes", min_value=0, max_value=59, key=f"minutes{i}")

            col4, col5 = st.columns(2)
            with col4:
                deadline = st.date_input("Deadline", min_value=date.today(), key=f"dl{i}")
            with col5:
                priority = st.selectbox("Priority", ["High", "Medium", "Low"], key=f"priority{i}")

            if name:
                task_data.append({
                    "name": name,
                    "hours": hours,
                    "minutes": minutes,
                    "deadline": deadline.strftime("%Y-%m-%d"),
                    "priority": {"High": 1, "Medium": 2, "Low": 3}[priority]
                })

    daily_hours = st.slider("📆 Available Hours per Day", 1, 12, 4)
    submitted = st.form_submit_button("Generate Schedule")

# 🔁 SUBMIT and process
if submitted:
    with st.spinner("Generating your smart schedule..."):
        try:
            response = requests.post(API_URL,
                                     json={"tasks": task_data, "daily_hours": daily_hours})
            if response.status_code == 200:
                try:
                    result = response.json()
                    st.success("✅ Smart Schedule Ready!")

                    # 🧠 Build Weekly Overview in Sidebar
                    weekly = {"High": 0, "Medium": 0, "Low": 0}
                    for day in result.values():
                        for task in day["tasks"]:
                            if task["priority"] == 1:
                                weekly["High"] += 1
                            elif task["priority"] == 2:
                                weekly["Medium"] += 1
                            elif task["priority"] == 3:
                                weekly["Low"] += 1

                    st.sidebar.metric("🔴 High Priority", weekly["High"])
                    st.sidebar.metric("🟡 Medium Priority", weekly["Medium"])
                    st.sidebar.metric("🟢 Low Priority", weekly["Low"])

                    # 📅 Main Content: Full Schedule View
                    for day, content in result.items():
                        st.markdown(f"## 📅 {day}")
                        st.info(content["quote"])
                        st.write(f"**Summary**: {content['summary']['total_hours']:.2f} hrs, {content['summary']['total_tasks']} tasks")

                        high = [t for t in content["tasks"] if t["priority"] == 1]
                        med = [t for t in content["tasks"] if t["priority"] == 2]
                        low = [t for t in content["tasks"] if t["priority"] == 3]

                        if high:
                            st.markdown("### 🔴 High Priority Tasks")
                            for t in high:
                                st.write(f"- 📝 {t['task']} → ⏱ {t['hours']} hrs")

                        if med:
                            st.markdown("### 🟡 Medium Priority Tasks")
                            for t in med:
                                st.write(f"- 📝 {t['task']} → ⏱ {t['hours']} hrs")

                        if low:
                            st.markdown("### 🟢 Low Priority Tasks")
                            for t in low:
                                st.write(f"- 📝 {t['task']} → ⏱ {t['hours']} hrs")

                except Exception as json_err:
                    st.error(f"🚨 Failed to decode response: {json_err}")
            else:
                st.error(f"❌ Server Error: {response.status_code} - {response.text}")
        except Exception as e:
            st.error(f"💥 Could not connect to FastAPI server.\n\n{e}")
