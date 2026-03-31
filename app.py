import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import os

FILE_NAME = "habit_data.csv"

# Initialize data file
if not os.path.exists(FILE_NAME):
    df = pd.DataFrame(columns=["date", "habit", "status"])
    df.to_csv(FILE_NAME, index=False)

# Load data
def load_data():
    return pd.read_csv(FILE_NAME)

# Save entry
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

# UI
st.set_page_config(page_title="Habit Tracker", layout="wide")

st.title("📊 Habit Tracker Dashboard")

# Sidebar input
st.sidebar.header("Add Habit")

habit = st.sidebar.text_input("Habit Name")
status = st.sidebar.selectbox("Completed?", [1, 0], format_func=lambda x: "Yes" if x == 1 else "No")

if st.sidebar.button("Add Entry"):
    if habit:
        add_entry(habit, status)
        st.sidebar.success("Entry added!")
    else:
        st.sidebar.error("Please enter a habit name")

# Load data
df = load_data()

if not df.empty:
    df['date'] = pd.to_datetime(df['date'])

    col1, col2 = st.columns(2)

    # Completion rate chart
    with col1:
        st.subheader("📊 Habit Completion Rate")
        summary = df.groupby("habit")["status"].mean()

        fig, ax = plt.subplots()
        summary.plot(kind='bar', ax=ax)
        ax.set_ylabel("Completion Rate")
        ax.set_xlabel("Habit")
        st.pyplot(fig)

    # Daily trend chart
    with col2:
        st.subheader("📈 Daily Progress")
        daily = df.groupby("date")["status"].mean()

        fig, ax = plt.subplots()
        daily.plot(ax=ax)
        ax.set_ylabel("Completion Rate")
        ax.set_xlabel("Date")
        st.pyplot(fig)

    # Show raw data
    st.subheader("📋 Data")
    st.dataframe(df)

else:
    st.info("No data yet. Start adding habits!")
