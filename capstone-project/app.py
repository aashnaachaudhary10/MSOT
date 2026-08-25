"""
The Expense Roaster
--------------------
A Streamlit dashboard that ingests a user's monthly expenses (CSV upload or
manual entry), visualizes spending with KPI cards + charts, and calls the
Gemini API to "roast" the user's discretionary spending and generate a
strict budget recovery plan.

Author: <Aashna Chaudhary>
Capstone: MirAI School of Technology - B.Tech Streamlit & AI Capstone
"""

import os
import io
from datetime import datetime

import pandas as pd
import streamlit as st
from google import genai

st.set_page_config(
    page_title="The Expense Roaster",
    page_icon="🔥",
    layout="wide",
    initial_sidebar_state="expanded",
)


DEFAULT_CATEGORIES = [
    "Food & Dining", "Groceries", "Rent", "Transport", "Shopping",
    "Entertainment", "Subscriptions", "Utilities", "Healthcare",
    "Education", "Travel", "Other",
]
NEEDS = {"Rent", "Groceries", "Utilities", "Healthcare", "Education", "Transport"}


if "expenses_df" not in st.session_state:
    st.session_state.expenses_df = pd.DataFrame(
        columns=["Date", "Category", "Description", "Amount"]
    )
if "roast_result" not in st.session_state:
    st.session_state.roast_result = None
if "budget_goal" not in st.session_state:
    st.session_state.budget_goal = 20000
if "monthly_income" not in st.session_state:
    st.session_state.monthly_income = 50000


def get_client():
    """Create a Gemini client from an API key in secrets, env var, or sidebar input."""
    api_key = (
        st.session_state.get("api_key_override")
        or st.secrets.get("GEMINI_API_KEY", None)
        if hasattr(st, "secrets") else None
    )
    api_key = api_key or os.environ.get("GEMINI_API_KEY")
    if not api_key:
        return None
    return genai.Client(api_key=api_key)


def call_gemini_roast(df: pd.DataFrame, income: float, goal: float) -> str:
    """Build a data-grounded system + user prompt and call Gemini for the roast
    + recovery plan. Uses an f-string to inject live dashboard context."""
    client = get_client()
    if client is None:
        raise RuntimeError("No Gemini API key found. Add one in the sidebar.")

    by_category = (
        df.groupby("Category")["Amount"].sum().sort_values(ascending=False)
    )
    total_spent = df["Amount"].sum()
    needs_spent = df[df["Category"].isin(NEEDS)]["Amount"].sum()
    wants_spent = total_spent - needs_spent
    savings_rate = ((income - total_spent) / income * 100) if income else 0

    category_breakdown = "\n".join(
        f"- {cat}: ₹{amt:,.0f}" for cat, amt in by_category.items()
    )

    system_prompt = (
        "You are 'Roast-AI', a brutally funny but ultimately caring financial "
        "coach for Indian college students and young professionals. You speak "
        "in witty, savage one-liners (think stand-up comedian meets CA), but "
        "every roast must be followed by genuinely useful, specific, numbered "
        "financial advice. Never be cruel about things outside the user's "
        "control (job loss, medical bills). Keep the tone playful, not mean."
    )

    user_prompt = f"""
Here is this user's real monthly financial data. Use these EXACT numbers in your response.

Monthly income: ₹{income:,.0f}
Total spent this month: ₹{total_spent:,.0f}
Spent on Needs (rent, groceries, utilities, healthcare, education, transport): ₹{needs_spent:,.0f}
Spent on Wants (everything else - discretionary): ₹{wants_spent:,.0f}
Current savings rate: {savings_rate:.1f}%
User's stated monthly savings goal: ₹{goal:,.0f}

Spending by category:
{category_breakdown}

Respond in this exact structure using Markdown:

### 🔥 The Roast
2-4 punchy, funny sentences specifically calling out the worst discretionary
spending category above using the real rupee amount. Be specific, not generic.

### 📊 The Reality Check
One short paragraph translating the numbers into a relatable comparison
(e.g. "that's X months of rent" or "that's Y coffees a week").

### 💊 The Strict Recovery Plan
A numbered list of exactly 5 concrete, specific actions to hit the ₹{goal:,.0f}
savings goal next month, each tied to a real category and rupee amount above.

### 🏆 Verdict
One-line savings grade out of 10 with a short justification.
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=user_prompt,
        config={
            "system_instruction": system_prompt,
            "temperature": 0.9,
        },
    )
    return response.text


with st.sidebar:
    st.title("🔥 Roaster Controls")

    st.session_state["api_key_override"] = st.text_input(
        "Gemini API Key",
        type="password",
        help="Get a free key at aistudio.google.com/apikey. "
             "Not stored anywhere except this session.",
    )

    st.divider()
    st.subheader("📁 Load Expense Data")

    uploaded_file = st.file_uploader("Upload monthly expenses (CSV)", type=["csv"])
    st.caption("Expected columns: Date, Category, Description, Amount")

    if st.button("✨ Load Sample Data", use_container_width=True):
        sample = pd.DataFrame({
            "Date": pd.date_range("2026-08-01", periods=14, freq="2D"),
            "Category": ["Rent", "Groceries", "Food & Dining", "Shopping",
                         "Entertainment", "Subscriptions", "Transport",
                         "Food & Dining", "Shopping", "Utilities",
                         "Entertainment", "Food & Dining", "Travel", "Shopping"],
            "Description": ["Monthly rent", "BigBasket order", "Swiggy order",
                             "Myntra haul", "Netflix + BookMyShow", "Spotify+ChatGPT+Cloud",
                             "Uber rides", "Zomato order", "Amazon impulse buy",
                             "Electricity bill", "Concert tickets", "Cafe hangouts",
                             "Weekend trip", "Sneakers"],
            "Amount": [15000, 3200, 850, 4500, 1200, 1800, 2100,
                       920, 3600, 1500, 2800, 1650, 6000, 4200],
        })
        st.session_state.expenses_df = sample
        st.rerun()

    if uploaded_file is not None:
        try:
            new_df = pd.read_csv(uploaded_file)
            required = {"Date", "Category", "Description", "Amount"}
            if not required.issubset(new_df.columns):
                st.error(f"CSV must contain columns: {required}")
            else:
                new_df["Amount"] = pd.to_numeric(new_df["Amount"], errors="coerce")
                st.session_state.expenses_df = new_df
                st.success(f"Loaded {len(new_df)} transactions.")
        except Exception as e:
            st.error(f"Couldn't read that file: {e}")

    st.divider()

    # st.form batches these inputs into ONE rerun/API call instead of one per keystroke
    with st.form("goals_form"):
        st.subheader("🎯 Your Targets")
        income = st.number_input("Monthly income (₹)", min_value=0,
                                  value=st.session_state.monthly_income, step=1000)
        goal = st.number_input("Savings goal (₹)", min_value=0,
                                value=st.session_state.budget_goal, step=500)
        submitted = st.form_submit_button("💾 Save Targets", use_container_width=True)
        if submitted:
            st.session_state.monthly_income = income
            st.session_state.budget_goal = goal
            st.toast("Targets saved!", icon="✅")


st.title("🔥 The Expense Roaster")
st.caption(
    "Upload your monthly spending. Gemini reads your real numbers, roasts your "
    "discretionary spending, and hands you a strict recovery plan."
)

df = st.session_state.expenses_df

if df.empty:
    st.info("👈 Upload a CSV or click **Load Sample Data** in the sidebar to get started.")
    st.stop()


total_spent = df["Amount"].sum()
income = st.session_state.monthly_income
goal = st.session_state.budget_goal
remaining = income - total_spent
savings_rate = (remaining / income * 100) if income else 0
top_category = df.groupby("Category")["Amount"].sum().idxmax() if not df.empty else "-"
top_amount = df.groupby("Category")["Amount"].sum().max() if not df.empty else 0

k1, k2, k3, k4 = st.columns(4)
k1.metric("💸 Total Spent", f"₹{total_spent:,.0f}",
          delta=f"{total_spent - goal:,.0f} vs goal", delta_color="inverse")
k2.metric("🏦 Left to Save", f"₹{remaining:,.0f}",
          delta=f"{remaining - goal:,.0f} vs target", delta_color="normal")
k3.metric("📈 Savings Rate", f"{savings_rate:.1f}%",
          delta=f"{savings_rate - (goal/income*100 if income else 0):.1f} pp vs goal")
k4.metric("🎯 Biggest Culprit", top_category, delta=f"₹{top_amount:,.0f}",
          delta_color="off")

st.divider()


col1, col2 = st.columns([3, 2])

with col1:
    st.subheader("📊 Spending by Category")
    cat_summary = df.groupby("Category")["Amount"].sum().sort_values(ascending=False)
    st.bar_chart(cat_summary)

with col2:
    st.subheader("🥧 Needs vs Wants")
    needs_total = df[df["Category"].isin(NEEDS)]["Amount"].sum()
    wants_total = total_spent - needs_total
    split_df = pd.DataFrame({"Type": ["Needs", "Wants"],
                              "Amount": [needs_total, wants_total]}).set_index("Type")
    st.bar_chart(split_df)

if "Date" in df.columns:
    try:
        trend_df = df.copy()
        trend_df["Date"] = pd.to_datetime(trend_df["Date"])
        trend = trend_df.groupby("Date")["Amount"].sum().sort_index()
        st.subheader("📉 Spending Trend Over Time")
        st.line_chart(trend)
    except Exception:
        pass


with st.expander("📝 View & Edit Transactions", expanded=False):
    edited_df = st.data_editor(
        df,
        num_rows="dynamic",
        use_container_width=True,
        column_config={
            "Category": st.column_config.SelectboxColumn(
                "Category", options=DEFAULT_CATEGORIES
            ),
            "Amount": st.column_config.NumberColumn("Amount (₹)", format="₹%d"),
        },
    )
    if st.button("Save edits"):
        st.session_state.expenses_df = edited_df
        st.rerun()

st.divider()


st.subheader("🤖 Get Roasted")
roast_col, _ = st.columns([1, 3])
with roast_col:
    roast_clicked = st.button("🔥 Roast My Spending", type="primary", use_container_width=True)

if roast_clicked:
    try:
        with st.spinner("Gemini is judging your life choices..."):
            st.session_state.roast_result = call_gemini_roast(df, income, goal)
    except RuntimeError as e:
        st.error(str(e))
    except Exception as e:
        st.error(f"Gemini API call failed: {e}")

if st.session_state.roast_result:
    st.markdown(st.session_state.roast_result)
    st.download_button(
        "⬇️ Download Recovery Plan",
        data=st.session_state.roast_result,
        file_name=f"budget_recovery_plan_{datetime.now().strftime('%Y%m%d')}.md",
        mime="text/markdown",
    )

st.divider()
st.caption("Built for MirAI School of Technology · B.Tech Capstone · Powered by Gemini API")
