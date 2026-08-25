import streamlit as st
import pandas as pd
import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(
    page_title="Life-OS",
    page_icon="📱",
    layout="wide"
)

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
    sorted(df["Date"].dt.date.unique(), reverse=True)
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

day_data = df[df["Date"].dt.date == selected_date]

total_minutes = day_data["Minutes_Used"].sum()

hours = total_minutes // 60
minutes = total_minutes % 60

# Most used app
app_usage = day_data.groupby("App_Name")["Minutes_Used"].sum()

most_used_app = app_usage.idxmax()

# Difference from goal
difference = total_minutes - daily_goal

# -----------------------------
# KPI Cards
# -----------------------------

st.subheader("📊 Today's Overview")

col1, col2, col3 = st.columns(3)

col1.metric(
    "Screen Time",
    f"{hours}h {minutes}m",
    f"{difference:+} min"
)

col2.metric(
    "Most Used App",
    most_used_app,
    f"{app_usage.max()} min"
)

col3.metric(
    "Daily Goal",
    f"{daily_goal} min",
    f"{difference:+} min",
    delta_color="inverse"
)

# -----------------------------
# Warning
# -----------------------------

if total_minutes > daily_goal:
    st.warning(
        "⚠️ You exceeded your daily screen-time goal."
    )
else:
    st.success(
        "✅ You stayed within your screen-time goal!"
    )

# -----------------------------
# Category Analysis
# -----------------------------

st.subheader("📱 Category Breakdown")

category_usage = (
    day_data.groupby("Category")["Minutes_Used"]
    .sum()
    .sort_values(ascending=False)
)

st.bar_chart(category_usage)

# -----------------------------
# 14 Day Trend
# -----------------------------

st.subheader("📈 14-Day Screen-Time Trend")

daily_usage = (
    df.groupby("Date")["Minutes_Used"]
    .sum()
)

st.line_chart(daily_usage)

# -----------------------------
# Data Table
# -----------------------------

with st.expander("🔎 View Today's Detailed Data"):
    st.data_editor(
        day_data,
        disabled=True,
        hide_index=True
    )

# -----------------------------
# Gemini Coach
# -----------------------------

st.subheader("🤖 AI Life Coach")

if st.button("Get My Productivity Analysis"):

    if client is None:
        st.error(
            "Gemini API key not found. Please add GEMINI_API_KEY to your .env file."
        )

    else:

        category_summary = (
            category_usage
            .to_string()
        )

        prompt = f"""
You are Life-OS, a brutally honest but fair productivity
and lifestyle coach.

Analyze the user's screen-time data.

Selected Date:
{selected_date}

Total Screen Time:
{total_minutes} minutes

Daily Goal:
{daily_goal} minutes

Most Used App:
{most_used_app}

Category Usage:
{category_summary}

Give the user:

1. A short analysis of their screen-time behavior.
2. Identify their biggest problem.
3. Explain what behavior is wasting the most time.
4. Suggest realistic physical or real-world alternatives.
5. Give three actionable things they should do tomorrow.

Do not give generic advice.
Use the actual numbers above.
Be honest but encouraging.
"""

        try:

            with st.spinner("🤖 Life-OS is analyzing your habits..."):

                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=prompt
                )

            st.markdown(response.text)

        except Exception as e:

            st.error(
                f"Gemini could not analyze your data: {e}"
            )