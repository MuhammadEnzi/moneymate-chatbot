# MoneyMate: Your Personal Finance Coach Chatbot
# Built with Streamlit and Google Gemini API

import streamlit as st
import google.generativeai as genai
import pandas as pd
import plotly.express as px
from fpdf import FPDF
import base64
from io import BytesIO
import datetime
import time

# --- Konfigurasi Halaman dan Judul ---
st.set_page_config(
    page_title="MoneyMate",
    page_icon="🤖",
    layout="wide"
)

# --- DESAIN UI BARU: NEON-INFUSED GLASS & ANIMATED GRADIENT ---
st.markdown("""
<style>
    /* 1. FONT IMPORT */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;900&family=Orbitron:wght@900&display=swap');

    /* 2. PALET WARNA & TEMA UTAMA */
    :root {
        --bg-color: #0A0A0A;
        --glass-bg: rgba(25, 25, 30, 0.7); /* Made it slightly more opaque */
        --border-color: rgba(255, 255, 255, 0.1);
        --accent-green: #00FFC2;
        --accent-red: #FF3B3B;
        --text-primary: #FFFFFF;
        --text-secondary: #A0A0A0;
    }

    /* 3. ANIMATED GRADIENT BACKGROUND (GEN Z THEME) */
    @keyframes gradient-animation {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    html, body, .stApp {
        font-family: 'Inter', sans-serif;
        background-color: var(--bg-color);
        color: var(--text-primary);
    }
    .stApp {
        background: linear-gradient(-45deg, #0A0A0A, #2A004A, #0A0A0A, #004A4A);
        background-size: 400% 400%;
        animation: gradient-animation 15s ease infinite;
    }

    /* 4. TIPOGRAFI & WARNA JUDUL */
    h1, h2, h3 {
        font-weight: 900;
        color: var(--text-primary);
        letter-spacing: -2px;
    }
    h3 {
        letter-spacing: -1px;
        font-weight: 700;
    }
    [data-testid="stSidebar"] h1 {
        color: var(--accent-green);
    }

    /* 5. SIDEBAR */
    [data-testid="stSidebar"] {
        background: rgba(10, 10, 10, 0.8);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border-right: 1px solid var(--border-color);
    }

    /* 6. GLASSMORPHISM CARD STYLING with NEON BORDER & INTERACTIVITY */
    .st-emotion-cache-1b0udgb, [data-testid="stDataFrameContainer"], [data-testid="stPlotlyChart"], #hero-card, .stTabs {
        background: var(--glass-bg);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border-radius: 24px;
        padding: 2rem;
        border: 1px solid var(--border-color);
        transition: box-shadow 0.3s ease, border 0.3s ease, transform 0.3s ease;
    }
    .st-emotion-cache-1b0udgb:hover, [data-testid="stPlotlyChart"]:hover, #hero-card:hover {
        box-shadow: 0 0 40px rgba(0, 255, 194, 0.2);
        border: 1px solid rgba(0, 255, 194, 0.5);
        transform: translateY(-5px);
    }

    /* 7. METRIC STYLING DENGAN WARNA SPESIFIK */
    [data-testid="stMetricValue"] {
        font-size: 2.5rem;
        font-weight: 900;
    }
    #metric-pemasukan [data-testid="stMetricLabel"] { color: var(--accent-green) !important; font-weight: 700 !important; }
    #metric-pemasukan [data-testid="stMetricValue"] { color: var(--accent-green); }
    #metric-pengeluaran [data-testid="stMetricLabel"] { color: var(--accent-red) !important; font-weight: 700 !important; }
    #metric-pengeluaran [data-testid="stMetricValue"] { color: var(--accent-red); }

    /* 8. TOMBOL with GRADIENT & GLOW */
    .stButton > button {
        border: none;
        border-radius: 12px;
        color: #000000;
        background: var(--accent-green);
        transition: all 0.3s ease;
        font-weight: 700;
        padding: 0.8rem 1.5rem;
        width: 100%;
        box-shadow: 0 0 15px rgba(0, 255, 194, 0.3);
    }
    .stButton > button:hover {
        background: var(--text-primary);
        box-shadow: 0 0 35px var(--accent-green);
        transform: scale(1.02);
    }

    /* 9. CHAT CONTAINER & MESSAGES (FIXED) */
    [data-testid="stVerticalBlock"] > [style*="flex-direction: column;"] > [data-testid="stVerticalBlock"] {
        background: var(--glass-bg);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border-radius: 24px;
        padding: 2rem;
        border: 1px solid var(--border-color);
        margin-top: 2rem;
    }
    [data-testid="stChatMessage"] {
        background: rgba(0,0,0,0.2);
        border-radius: 16px;
    }
    
    /* 10. ANIMASI KETIK BERULANG (CSS-ONLY) - DIPERLAMBAT */
    #animated-title h1 {
        font-family: 'Orbitron', sans-serif; /* FONT FUTURISTIK */
        display: inline-block;
        overflow: hidden;
        border-right: .1em solid var(--accent-green);
        white-space: nowrap;
        margin: 0;
        letter-spacing: .1em;
        animation: typing 8s steps(30, end) infinite, blink-caret .75s step-end infinite;
    }
    @keyframes typing {
        from { width: 0 }
        to { width: 100% }
    }
    @keyframes blink-caret {
        from, to { border-color: transparent }
        50% { border-color: var(--accent-green); }
    }

</style>
""", unsafe_allow_html=True)


# --- FUNGSI & LOGIKA ---
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error("🔑 **Kesalahan Konfigurasi API**: Harap atur `GEMINI_API_KEY` di Streamlit Secrets.")
    model = None

if 'history' not in st.session_state:
    st.session_state.history = []
if 'transactions' not in st.session_state:
    st.session_state.transactions = pd.DataFrame(columns=["Tanggal", "Jenis", "Kategori", "Jumlah", "Deskripsi"])
if 'goals' not in st.session_state:
    st.session_state.goals = {}

def get_gemini_response(question, chat_history):
    if not model: return "Maaf, koneksi API sedang bermasalah."
    financial_summary = "Data keuangan pengguna saat ini belum ada."
    if not st.session_state.transactions.empty:
        total_income = st.session_state.transactions[st.session_state.transactions['Jenis'] == 'Pemasukan']['Jumlah'].sum()
        total_expense = st.session_state.transactions[st.session_state.transactions['Jenis'] == 'Pengeluaran']['Jumlah'].sum()
        balance = total_income - total_expense
        financial_summary = (f"Ringkasan keuangan: Pemasukan Rp {total_income:,.0f}, Pengeluaran Rp {total_expense:,.0f}, Saldo Rp {balance:,.0f}.")
    context = f"Anda adalah MoneyMate, AI financial coach yang modern dan ramah. {financial_summary} Berikan saran berdasarkan aturan 50/30/20."
    full_prompt = f"{context}\n\nRiwayat: {chat_history}\n\nPengguna: {question}\nMoneyMate:"
    try:
        response = model.generate_content(full_prompt)
        return response.text
    except Exception as e:
        return f"Oops, terjadi kesalahan: {e}"

def add_transaction(trans_type, category, amount, description):
    new_transaction = pd.DataFrame([{"Tanggal": pd.to_datetime(datetime.date.today()), "Jenis": trans_type, "Kategori": category, "Jumlah": amount, "Deskripsi": description}])
    st.session_state.transactions = pd.concat([st.session_state.transactions, new_transaction], ignore_index=True)
    st.toast(f"{trans_type} Rp {amount:,.0f}", icon="✅")

def create_download_link(df, file_format, filename):
    if file_format == 'csv':
        data = df.to_csv(index=False).encode('utf-8')
        st.download_button("Unduh CSV", data, f"{filename}.csv", "text/csv")

# --- TATA LETAK & UI BARU ---

# SIDEBAR
with st.sidebar:
    st.title("MoneyMate")
    st.markdown("---")
    st.header("Input Transaksi")
    with st.form("transaction_form", clear_on_submit=True, border=False):
        trans_type = st.selectbox("Jenis", ["Pemasukan", "Pengeluaran"])
        amount = st.number_input("Jumlah (Rp)", min_value=0, step=1000)
        if trans_type == "Pemasukan":
            category = st.selectbox("Kategori", ["Gaji", "Bonus", "Bisnis", "Lainnya"])
        else:
            category = st.selectbox("Kategori", ["Kebutuhan (50%)", "Keinginan (30%)", "Tabungan (20%)", "Lainnya"])
        description = st.text_input("Deskripsi (Opsional)")
        if st.form_submit_button("Simpan Transaksi"):
            if amount > 0: add_transaction(trans_type, category, amount, description)

    st.header("Target Finansial")
    with st.form("goal_form", clear_on_submit=True, border=False):
        goal_name = st.text_input("Nama Target")
        goal_target = st.number_input("Target (Rp)", min_value=0, step=100000)
        if st.form_submit_button("Set Target"):
            if goal_name and goal_target > 0:
                st.session_state.goals[goal_name] = {"target": goal_target, "saved": 0}
                st.toast(f"Target '{goal_name}' berhasil dibuat!", icon="🎯")
    
    st.markdown("---")
    st.info("MoneyMate adalah chatbot edukasi, bukan penasihat finansial profesional.")


# HALAMAN UTAMA
if st.session_state.transactions.empty:
    st.markdown('<div id="animated-title"><h1>Selamat Datang di MoneyMate 🤖</h1></div>', unsafe_allow_html=True)
    st.info("Mulai perjalanan finansialmu dengan mencatat transaksi pertama di panel sebelah kiri.")
else:
    st.header("Dashboard Finansial")
    total_income = st.session_state.transactions[st.session_state.transactions['Jenis'] == 'Pemasukan']['Jumlah'].sum()
    total_expense = st.session_state.transactions[st.session_state.transactions['Jenis'] == 'Pengeluaran']['Jumlah'].sum()
    balance = total_income - total_expense
    
    # --- BAGIAN 1: HERO SECTION - SALDO UTAMA ---
    st.markdown(f"""
    <div id="hero-card" style="padding: 2.5rem; text-align: center;">
        <p style="color: var(--text-secondary); font-weight: 600; margin:0; letter-spacing: 1px; text-transform: uppercase;">Saldo Saat Ini</p>
        <h1 style="font-size: 5rem; margin:0; letter-spacing: -4px; color: var(--text-primary); text-shadow: 0 0 20px rgba(255,255,255,0.3);">Rp {balance:,.0f}</h1>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)

    # --- BAGIAN 2: TABS UNTUK RINGKASAN & RIWAYAT ---
    tab1, tab2 = st.tabs(["📊 Ringkasan", "📜 Riwayat Transaksi"])

    with tab1:
        sub_col1, sub_col2 = st.columns([0.4, 0.6], gap="large")
        with sub_col1:
            st.markdown('<div id="metric-pemasukan">', unsafe_allow_html=True)
            st.metric(label="Total Pemasukan", value=f"Rp {total_income:,.0f}")
            st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            st.markdown('<div id="metric-pengeluaran">', unsafe_allow_html=True)
            st.metric(label="Total Pengeluaran", value=f"Rp {total_expense:,.0f}")
            st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)

            st.markdown("### Progress Target")
            if st.session_state.goals:
                savings = st.session_state.transactions[st.session_state.transactions['Kategori'] == 'Tabungan (20%)']['Jumlah'].sum()
                for name, info in st.session_state.goals.items():
                    progress = (savings / info['target']) * 100 if info['target'] > 0 else 0
                    st.progress(min(progress / 100, 1.0), text=f"{name}: {progress:.1f}%")
            else:
                st.info("Anda belum memiliki target.")

        with sub_col2:
            st.markdown("### Alokasi Pengeluaran")
            expense_data = st.session_state.transactions[st.session_state.transactions['Jenis'] == 'Pengeluaran']
            if not expense_data.empty:
                category_summary = expense_data.groupby('Kategori')['Jumlah'].sum().reset_index()
                color_map = px.colors.qualitative.Pastel
                fig = px.bar(category_summary, x='Kategori', y='Jumlah', text_auto='.2s', color='Kategori', color_discrete_sequence=color_map)
                fig.update_traces(marker_line_width=0, textposition='outside')
                fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                                  font_color="var(--text-secondary)", yaxis_title=None, xaxis_title=None,
                                  showlegend=False)
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Belum ada data pengeluaran.")

    with tab2:
        st.markdown("### Riwayat Transaksi")
        # Format kolom 'Jumlah' sebelum menampilkannya
        display_df = st.session_state.transactions.copy()
        display_df['Jumlah'] = display_df['Jumlah'].apply(lambda x: f"{x:,.0f}")
        st.dataframe(display_df.sort_values(by="Tanggal", ascending=False), use_container_width=True)
        create_download_link(st.session_state.transactions, 'csv', 'laporan_moneymate')

# --- BAGIAN CHATBOT (FIXED) ---
with st.container(border=True):
    st.markdown("### 🤖 Financial AI")

    # Display chat history
    chat_history_container = st.container(height=300)
    with chat_history_container:
        for role, text in st.session_state.history:
            with st.chat_message(role):
                st.markdown(text)

    # Chat input
    prompt = st.chat_input("Tanya apa saja...")
    if prompt:
        st.session_state.history.append(("user", prompt))
        # No need to display user message here, it's handled by rerun
        
        with st.spinner("Financial AI Sedang berpikir..."):
            response = get_gemini_response(prompt, st.session_state.history)
            st.session_state.history.append(("assistant", response))
            # This will force a re-run to display the new messages
            st.rerun()
