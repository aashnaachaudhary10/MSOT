import streamlit as st
import pandas as pd
import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

# -----------------------------
# Page Configuration
# -----------------------------

st.set_page_config(
    page_title="Life-OS",
    page_icon="📱",
    layout="wide"
)

# -----------------------------
# Title
# -----------------------------

st.title("📱 Life-OS")
st.write("Your personal screen-time and productivity dashboard")

# -----------------------------
# Gemini Setup
# -----------------------------

api_key = os.getenv("GEMINI_API_KEY")

if api_key:
    client = genai.Client(api_key=api_key)
else:
    client = None

# -----------------------------
# Load Dataset
# -----------------------------

df = pd.read_csv("screentime.csv")

df["Date"] = pd.to_datetime(df["Date"])

# -----------------------------
# Sidebar
# -----------------------------

st.sidebar.title("⚙️ Life-OS Settings")

selected_date = st.sidebar.selectbox(
    "Select Day",
    sorted(
        df["Date"].dt.date.unique(),
        reverse=True
    )
)

daily_goal = st.sidebar.slider(
    "Daily Screen-Time Goal (minutes)",
    min_value=60,
    max_value=600,
    value=300,
    step=30
)

# -----------------------------
# Filter Selected Day
# -----------------------------

day_data = df[
    df["Date"].dt.date == selected_date
]

# Total screen time
total_minutes = day_data["Minutes_Used"].sum()

hours = total_minutes // 60
minutes = total_minutes % 60

# -----------------------------
# Most Used App
# -----------------------------

app_usage = (
    day_data
    .groupby("App_Name")["Minutes_Used"]
    .sum()
    .sort_values(ascending=False)
)

most_used_app = app_usage.index[0]
most_used_minutes = app_usage.iloc[0]

# -----------------------------
# Goal Difference
# -----------------------------

difference = total_minutes - daily_goal

# -----------------------------
# KPI Section
# -----------------------------

st.subheader("📊 Today's Overview")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Screen Time",
        f"{hours}h {minutes}m",
        f"{difference:+} min"
    )

with col2:
    st.metric(
        "Most Used App",
        most_used_app,
        f"{most_used_minutes} min"
    )

with col3:
    st.metric(
        "Daily Goal",
        f"{daily_goal} min",
        f"{difference:+} min",
        delta_color="inverse"
    )

# -----------------------------
# Goal Status
# -----------------------------

if total_minutes > daily_goal:

    st.warning(
        f"⚠️ You exceeded your daily goal by "
        f"{difference} minutes."
    )

else:

    remaining = daily_goal - total_minutes

    st.success(
        f"✅ Great! You are {remaining} minutes "
        f"under your daily goal."
    )

# -----------------------------
# Category Breakdown
# -----------------------------

st.subheader("📱 Category Breakdown")

category_usage = (
    day_data
    .groupby("Category")["Minutes_Used"]
    .sum()
    .sort_values(ascending=False)
)

st.bar_chart(category_usage)

# -----------------------------
# App Usage
# -----------------------------

st.subheader("📲 App Usage")

st.bar_chart(app_usage)

# -----------------------------
# 14-Day Trend
# -----------------------------

st.subheader("📈 14-Day Screen-Time Trend")

daily_usage = (
    df
    .groupby("Date")["Minutes_Used"]
    .sum()
)

st.line_chart(daily_usage)

# -----------------------------
# Detailed Data
# -----------------------------

with st.expander("🔎 View Today's Detailed Data"):

    st.data_editor(
        day_data,
        disabled=True,
        hide_index=True
    )

# -----------------------------
# AI Life Coach
# -----------------------------

st.subheader("🤖 AI Life Coach")

st.write(
    "Let Gemini analyze your screen-time habits "
    "and give you a realistic action plan."
)

if st.button("🧠 Get My Productivity Analysis"):

    if client is None:

        st.error(
            "Gemini API key not found. "
            "Please add GEMINI_API_KEY to your .env file."
        )

    else:

        # Convert category data into a clean string
        category_summary = category_usage.to_string()

        # -----------------------------
        # Dynamic AI Prompt
        # -----------------------------

        prompt = f"""
You are Life-OS, a brutally honest but fair
productivity and lifestyle coach.

Analyze the user's actual screen-time data.

DATE:
{selected_date}

TOTAL SCREEN TIME:
{total_minutes} minutes

DAILY GOAL:
{daily_goal} minutes

MOST USED APP:
{most_used_app}

MOST USED APP TIME:
{most_used_minutes} minutes

CATEGORY BREAKDOWN:
{category_summary}

Your job is to analyze the user's behavior.

Give your response in this structure:

## 🔍 Today's Analysis

Explain what the numbers say about the user's
screen-time habits.

## 🚨 Biggest Problem

Identify the biggest source of wasted time.

## 💡 Real-World Replacement

Suggest physical, real-world activities that
could replace the wasted screen time.

For example:
- exercise
- walking
- reading
- cooking
- studying
- meeting friends
- hobbies

## 🎯 Tomorrow's Action Plan

Give exactly 3 practical actions.

Be specific and use the actual numbers.
Do not give generic advice such as
"use your phone less."

Be honest but encouraging.
"""

        try:

            with st.spinner(
                "🤖 Life-OS is analyzing your habits..."
            ):

                # First attempt
                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=prompt
                )

            st.success("AI analysis generated successfully!")

            st.markdown(response.text)

        except Exception:

            # -----------------------------
            # Fallback Model
            # -----------------------------

            try:

                with st.spinner(
                    "🔄 Primary AI model is busy. "
                    "Trying backup model..."
                ):

                    response = client.models.generate_content(
                        model="gemini-2.5-flash-lite",
                        contents=prompt
                    )

                st.success(
                    "AI analysis generated using the backup model."
                )

                st.markdown(response.text)

            except Exception:

                st.error(
                    "🤖 Gemini is temporarily unavailable. "
                    "Please try again in a few minutes."
                )