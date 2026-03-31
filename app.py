import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import os

FILE_NAME = "habit_data.csv"

# Initialize file if not exists
if not os.path.exists(FILE_NAME):
    df = pd.DataFrame(columns=["date", "habit", "status"])
    df.to_csv(FILE_NAME, index=False)

# Load data
def load_data():
    return pd.read_csv(FILE_NAME)

# Add entry
def add_entry(habit, status):
    df = load_data()
    today = datetime.now().strftime("%Y-%m-%d")

    new_entry = pd.DataFrame({
        "date": [today],
        "habit": [habit],
        "status": [status]
    })

    df = pd.concat([df, new_entry], ignore_index=True)
    df.to_csv(FILE_NAME, index=False)

# Page config
st.set_page_config(page_title="Habit Tracker", layout="wide")

# Title
st.title("📊 Habit Tracker Dashboard")

# Sidebar
st.sidebar.header("Add Habit")

habit = st.sidebar.text_input("Habit Name")
status = st.sidebar.selectbox(
    "Completed?",
    [1, 0],
    format_func=lambda x: "Yes" if x == 1 else "No"
)

if st.sidebar.button("Add Entry"):
    if habit.strip() != "":
        add_entry(habit, status)
        st.sidebar.success("Entry added!")
    else:
        st.sidebar.error("Please enter a habit name")

# Load data
df = load_data()

if not df.empty:
    df['date'] = pd.to_datetime(df['date'])

    col1, col2 = st.columns(2)

    # 📊 Completion Rate Chart
    with col1:
        st.subheader("📊 Habit Completion Rate")

        summary = df.groupby("habit")["status"].mean().reset_index()

        fig = px.bar(
            summary,
            x="habit",
            y="status",
            labels={"status": "Completion Rate", "habit": "Habit"},
            title="Habit Completion Rate"
        )

        st.plotly_chart(fig, use_container_width=True)

    # 📈 Daily Trend Chart
    with col2:
        st.subheader("📈 Daily Progress")

        daily = df.groupby("date")["status"].mean().reset_index()

        fig = px.line(
            daily,
            x="date",
            y="status",
            labels={"status": "Completion Rate", "date": "Date"},
            title="Daily Habit Performance"
        )

        st.plotly_chart(fig, use_container_width=True)

    # 📋 Raw Data
    st.subheader("📋 Your Data")
    st.dataframe(df, use_container_width=True)

else:
    st.info("No data yet. Start adding habits!")
