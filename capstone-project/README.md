# 🔥 The Expense Roaster

```
$ whoami
> A Streamlit dashboard that reads your spending and roasts you for it.

$ ./expense_roaster.sh --status
[OK] Pandas pipeline........ online
[OK] Gemini API............. connected
[OK] session_state.......... persisted
[OK] judgment............... merciless
```

> **B.Tech Capstone — MirAI School of Technology**
> Streamlit UI · Pandas · Gemini API (gemini-2.5-flash) · Deployed on Streamlit Community Cloud

---

## 🖥️ Live Demo

**➡️ [expense-roaster.onrender.com](https://expense-roaster.onrender.com)** 
*'Note: this runs on Render's free tier, so the first load after inactivity may take 30-60 seconds to wake up.' *

---

## 📸 What It Does

Upload a month of expenses (or hit **Load Sample Data**) and the app:

1. Builds a live **KPI dashboard** — total spent, savings rate, biggest culprit category, all with deltas against your goal.
2. Visualizes spending by category and a **Needs vs Wants** split.
3. Lets you **edit transactions inline** with `st.data_editor`.
4. Sends your *real* numbers to **Gemini**, which returns:
   - 🔥 A savage, specific roast of your worst spending category
   - 📊 A reality-check comparison
   - 💊 A numbered, strict recovery plan to hit your savings goal
   - 🏆 A savings grade out of 10
5. Lets you **download the recovery plan** as Markdown.

---

## 🏗️ Architecture

Full system design, data flow diagram, and API integration strategy live in
[`ARCHITECTURE.md`](./ARCHITECTURE.md).

```
User → Streamlit UI → Pandas aggregation → Prompt builder (f-string context)
                                                 │
                                                 ▼
                                         Gemini API (gemini-2.5-flash)
                                                 │
                                                 ▼
                                     Markdown roast + recovery plan
```

---

## ⚙️ Setup — Run Locally

```bash
# 1. Clone the repo
git clone https://github.com/you/MSOT.git
cd MSOT/<this-project-folder>

# 2. Create a virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Add your Gemini API key
cp .env.example .env
# edit .env and paste your key from https://aistudio.google.com/apikey

# 5. Run it
streamlit run app.py
```

> No key handy? You can also paste it directly into the **sidebar** text
> input at runtime — nothing is stored outside the session.

---

## ☁️ Deploy — Streamlit Community Cloud

1. Push this folder to your GitHub repo (`MSOT`).
2. Go to [share.streamlit.io](https://share.streamlit.io) → **New app**.
3. Point it at your repo, branch, and `app.py`.
4. In **App Settings → Secrets**, add:
   ```toml
   GEMINI_API_KEY = "your_real_key_here"
   ```
5. Deploy. Copy the live URL back into this README.

---

## 📂 Project Structure

```
.
├── app.py                      # Main Streamlit app
├── requirements.txt            # Locked, cloud-safe dependencies
├── ARCHITECTURE.md             # System design + Mermaid diagrams
├── sample_expenses.csv         # Demo dataset for judges
├── .env.example                # API key template
├── .gitignore
└── .streamlit/
    ├── config.toml             # Custom dark theme
    └── secrets.toml.example    # Template for Streamlit Cloud secrets
```

---

## 🧠 Tech Stack

| Layer | Tech |
|---|---|
| UI Framework | Streamlit |
| Data Processing | Pandas |
| AI | Gemini API (`google-genai`, model `gemini-2.5-flash`) |
| State | `st.session_state` |
| Deployment | Streamlit Community Cloud |

---

## 📜 License

Built for academic submission — MirAI School of Technology Capstone, 2026.
