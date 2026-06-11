import streamlit as st
from fsm import DonationFSM

# =====================================================
# CONFIG
# =====================================================

st.set_page_config(
    page_title="Donasi Pendidikan",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
/* ======================
   GLOBAL DARK THEME
====================== */
.stApp {
    background: #0F172A;
    color: white;
}

header[data-testid="stHeader"] {
    background: transparent !important;
}

footer {
    visibility: hidden;
}

hr {
    border-color: rgba(255, 255, 255, 0.1) !important;
}

/* ======================
   SIDEBAR
====================== */
section[data-testid="stSidebar"] {
    background: #111827;
    border-right: 1px solid rgba(255,255,255,0.08);
}
section[data-testid="stSidebar"] * {
    color: white !important;
}

/* ======================
   BUTTONS
====================== */
.stButton > button {
    background: #F59E0B;
    color: white;
    border: none;
    border-radius: 20px;
    font-weight: 600;
    transition: all 0.3s;
}
.stButton > button:hover {
    background: #D97706;
}

/* ======================
   KATALOG CARDS 
====================== */
.katalog-card {
    background: #1E293B;
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 20px;
    padding: 24px;
    height: 240px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    transition: all 0.3s;
    margin-bottom: 20px;
}

.katalog-card:hover {
    transform: translateY(-5px);
    border-color: #3b82f6;
    background: #232f45;
}

.kategori-header {
    background: linear-gradient(90deg, #1E3A8A, #3B82F6);
    color: white;
    padding: 14px 24px;
    border-radius: 15px;
    margin-top: 40px;
    margin-bottom: 24px;
    font-weight: 700;
}

/* ======================
   CHAT BUBBLES
====================== */
[data-testid="stChatMessageAssistant"] {
    background-color: #1E293B !important;
}
[data-testid="stChatMessageUser"] {
    background-color: #334155 !important;
}
div[data-testid="stChatInput"] {
    background: white !important;
    border-radius: 30px !important;
}
div[data-testid="stChatInput"] textarea {
    color: #0F172A !important;
}
button[data-testid="stChatInputButton"] {
    background-color: #F59E0B !important;
    border-radius: 50% !important;
}

/* ======================
   INFO CARDS
====================== */
.info-card {
    background: #1E293B;
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 20px;
    padding: 20px;
    margin-bottom: 30px;
}
.info-card h3 {
    color: #F59E0B;
    margin-bottom: 15px;
}

/* ======================
   HERO SECTION - RATA TENGAH
====================== */
.hero-container {
    display: flex;
    justify-content: center;
    align-items: center;
    width: 100%;
}

.hero-card {
    text-align: center;
    padding: 50px 30px;
    background: linear-gradient(135deg, #1E293B 0%, #0F172A 100%);
    border-radius: 25px;
    border: 1px solid rgba(255,255,255,0.1);
    margin-bottom: 40px;
    width: 100%;
}

.hero-title {
    color: white;
    font-size: 2.2rem;
    margin-bottom: 20px;
    text-align: center;
}

.hero-subtitle {
    font-size: 1rem;
    color: #cbd5e1;
    max-width: 800px;
    margin: 0 auto;
    line-height: 1.6;
    text-align: center;
}

/* Stats container */
.stats-container {
    display: flex;
    justify-content: center;
    gap: 40px;
    margin: 30px 0;
}

/* Timeline */
.timeline-item {
    margin-bottom: 20px;
    padding-left: 20px;
    border-left: 2px solid #F59E0B;
}
.timeline-period {
    color: #F59E0B;
    font-weight: bold;
    margin-bottom: 8px;
}

/* Law article */
.law-article {
    background: #0F172A;
    border-left: 4px solid #F59E0B;
    padding: 12px 15px;
    margin: 12px 0;
    border-radius: 0 12px 12px 0;
}
.law-title {
    color: #F59E0B;
    font-weight: bold;
}
.law-quote {
    color: #CBD5E1;
    font-style: italic;
    margin: 8px 0 0 20px;
}

</style>
""", unsafe_allow_html=True)

# =====================================================
# SESSION STATE
# =====================================================

if "bot_fsm" not in st.session_state:
    st.session_state.bot_fsm = DonationFSM()
    st.session_state.bot_fsm.step()
    st.session_state.messages = [{"role": "assistant", "content": st.session_state.bot_fsm.get_response()}]

if "show_success" not in st.session_state:
    st.session_state.show_success = False

if "current_page" not in st.session_state:
    st.session_state.current_page = "Beranda"

if "form_kecamatan" not in st.session_state:
    st.session_state.form_kecamatan = "Banyumanik"
if "form_program" not in st.session_state:
    st.session_state.form_program = "SD"

bot = st.session_state.bot_fsm
bot.lokasi = st.session_state.form_kecamatan
bot.program = st.session_state.form_program

# =====================================================
# NAVBAR
# =====================================================

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    if st.button("🏠 Beranda", use_container_width=True):
        st.session_state.current_page = "Beranda"
with col2:
    if st.button("📜 Katalog", use_container_width=True):
        st.session_state.current_page = "Katalog"
with col3:
    if st.button(f"🛒 Keranjang ({len(bot.engine.cart)})", use_container_width=True):
        st.session_state.current_page = "Keranjang"
with col4:
    if st.button("🤖 Chatbot", use_container_width=True):
        st.session_state.current_page = "Chatbot"
with col5:
    if st.button("🔄 Reset", use_container_width=True):
        st.session_state.bot_fsm = DonationFSM()
        st.session_state.bot_fsm.step()
        st.session_state.messages = [{"role": "assistant", "content": st.session_state.bot_fsm.get_response()}]
        st.session_state.current_page = "Beranda"
        st.rerun()

st.markdown("---")

# =====================================================
# HALAMAN BERANDA
# =====================================================
if st.session_state.current_page == "Beranda":
    
    # HERO SECTION - RATA TENGAH
    st.markdown("""
    <div class="hero-card">
        <h1 class="hero-title">🎓 Donasi Fasilitas Pembelajaran Anak Kurang Mampu</h1>
        <p class="hero-subtitle">
            Program donasi sosial untuk membantu penyediaan buku pembelajaran, alat tulis siswa, fasilitas belajar, biaya operasional pengajar sukarela, dan beasiswa bagi anak-anak kurang mampu di Kota Semarang.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # STATISTIK - RATA TENGAH
    col_left, col_mid, col_right = st.columns([1, 3, 1])
    with col_mid:
        c1, c2, c3 = st.columns(3)
        with c1:
            st.metric("📚 Buku Disalurkan", "1.000+")
        with c2:
            st.metric("🎓 Siswa Terbantu", "500+")
        with c3:
            st.metric("🏫 Lokasi Belajar", "50+")

    st.markdown("<br>", unsafe_allow_html=True)
    
    # VISI MISI
    st.markdown("<h2 style='text-align: center; margin-bottom: 30px;'>🎯 Visi dan Misi Program</h2>", unsafe_allow_html=True)
    
    v1, v2 = st.columns(2)
    with v1:
        st.markdown("""
        <div style="background:#1E293B; border-radius:20px; padding:25px;">
            <h3 style="color:#F59E0B;">🎯 Visi</h3>
            <p style="color:#CBD5E1;">Mewujudkan akses pendidikan yang layak, inklusif, dan berkualitas bagi anak-anak kurang mampu di Kota Semarang.</p>
        </div>
        """, unsafe_allow_html=True)
    with v2:
        st.markdown("""
        <div style="background:#1E293B; border-radius:20px; padding:25px;">
            <h3 style="color:#10B981;">🚀 Misi</h3>
            <ul style="color:#CBD5E1; padding-left:20px;">
                <li>Menyediakan fasilitas belajar yang memadai</li>
                <li>Membantu kebutuhan alat tulis siswa</li>
                <li>Mendukung operasional pengajar sukarela</li>
                <li>Memberikan bantuan beasiswa pendidikan</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    # SEJARAH PENDIDIKAN
    st.markdown("---")
    st.markdown("<div class='info-card'><h3>📜 Sejarah Pendidikan Indonesia</h3></div>", unsafe_allow_html=True)
    
    sejarah_col1, sejarah_col2 = st.columns(2)
    with sejarah_col1:
        st.markdown("""
        <div class="timeline-item">
            <div class="timeline-period">🏛️ Masa Pra-Kolonial</div>
            <ul><li>Pendidikan berpusat pada agama dan nilai moral</li><li>Dilaksanakan melalui padepokan, pesantren, surau, dan masjid</li></ul>
        </div>
        <div class="timeline-item">
            <div class="timeline-period">⛵ Masa Kolonial</div>
            <ul><li>Pendidikan diperkenalkan oleh Portugis dan Belanda</li><li>Akses pendidikan terbatas dan diskriminatif</li></ul>
        </div>
        """, unsafe_allow_html=True)
    with sejarah_col2:
        st.markdown("""
        <div class="timeline-item">
            <div class="timeline-period">🇮🇩 Masa Pergerakan Nasional</div>
            <ul><li>Tokoh pribumi mendirikan lembaga pendidikan sendiri</li><li>Pendidikan untuk membangun kesadaran kebangsaan</li></ul>
        </div>
        <div class="timeline-item">
            <div class="timeline-period">🚀 Masa Kemerdekaan hingga Modern</div>
            <ul><li>Pendidikan menjadi hak seluruh warga negara</li><li>Berlandaskan Pancasila dan UUD 1945</li></ul>
        </div>
        """, unsafe_allow_html=True)

    # PAHLAWAN PENDIDIKAN
    st.markdown("<div class='info-card'><h3>🦸 Pahlawan Pendidikan Indonesia</h3><p>Tokoh-tokoh yang berjasa memajukan pendidikan di Indonesia</p></div>", unsafe_allow_html=True)
    
    pahlawan_list = [
        {"nama": "Raden Ayu Lasminingrat", "img_path": "Pahlaawan Raden Ayu Lasminingrat.jpeg"},
        {"nama": "Roehana Koeddoes", "img_path": "Pahlaawan Roehana Koddoes.jpeg"},
        {"nama": "KH Ahmad Dahlan", "img_path": "Pahlawan KH.Ahmad Dahlan.jpeg"},
        {"nama": "Ki Hajar Dewantara", "img_path": "Pahlawan Ki Hajar Dewantara.jpeg"},
        {"nama": "Mohammad Sjafei", "img_path": "Pahlawan Mohammad Sjafei.jpeg"},
        {"nama": "Raden Dewi Sartika", "img_path": "Pahlawawan Raden Dewi Sartika.jpeg"}
    ]
    
    pahlawan_cols = st.columns(3)
    for idx, pahlawan in enumerate(pahlawan_list):
        with pahlawan_cols[idx % 3]:
            try:
                st.image(pahlawan["img_path"], use_container_width=True)
                st.markdown(f"<p style='text-align:center; color:#F59E0B; font-weight:600;'>{pahlawan['nama']}</p>", unsafe_allow_html=True)
            except:
                st.markdown(f"<div style='text-align:center; padding:40px; background:#1E293B; border-radius:12px;'>🖼️<br>{pahlawan['nama']}</div>", unsafe_allow_html=True)

    # DASAR HUKUM
    st.markdown("<div class='info-card'><h3>⚖️ Dasar Hukum Pendidikan Indonesia</h3></div>", unsafe_allow_html=True)
    
    hukum_col1, hukum_col2 = st.columns(2)
    with hukum_col1:
        st.markdown("""
        <div style="background:#0F172A; border-radius:15px; padding:15px;">
            <h4 style="color:#F59E0B;">📜 UUD 1945</h4>
            <div class="law-article"><div class="law-title">Pasal 31 Ayat (1)</div><div class="law-quote">"Setiap warga negara berhak memperoleh pendidikan."</div></div>
            <div class="law-article"><div class="law-title">Pasal 31 Ayat (2)</div><div class="law-quote">"Setiap warga negara wajib mengikuti pendidikan dasar dan pemerintah wajib membiayainya."</div></div>
            <div class="law-article"><div class="law-title">Pasal 31 Ayat (4)</div><div class="law-quote">"Anggaran pendidikan minimal 20% dari APBN dan APBD."</div></div>
        </div>
        """, unsafe_allow_html=True)
    with hukum_col2:
        st.markdown("""
        <div style="background:#0F172A; border-radius:15px; padding:15px;">
            <h4 style="color:#F59E0B;">📖 UU Nomor 20 Tahun 2003</h4>
            <div class="law-article"><div class="law-title">Pasal 5</div><div class="law-quote">"Hak setiap warga negara untuk memperoleh pendidikan bermutu."</div></div>
            <div class="law-article"><div class="law-title">Pasal 6</div><div class="law-quote">"Kewajiban mengikuti pendidikan dasar bagi usia 7–15 tahun."</div></div>
            <div class="law-article"><div class="law-title">Pasal 11</div><div class="law-quote">"Pemerintah wajib menyediakan layanan pendidikan yang bermutu tanpa diskriminasi."</div></div>
        </div>
        """, unsafe_allow_html=True)

# =====================================================
# HALAMAN KATALOG
# =====================================================
elif st.session_state.current_page == "Katalog":

    st.markdown("""
    <div style="background:#1E293B; padding:30px; border-radius:20px; margin-bottom:30px;">
        <h2 style="color:white;">📍 Data Donatur</h2>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        kecamatan = st.selectbox("Kecamatan", ["Banyumanik", "Candisari", "Gajahmungkur", "Gayamsari", "Genuk", "Gunungpati", "Mijen", "Ngaliyan", "Pedurungan", "Semarang Barat", "Semarang Selatan", "Semarang Tengah", "Semarang Timur", "Semarang Utara", "Tembalang", "Tugu"], index=15)
        st.session_state.form_kecamatan = kecamatan
        bot.lokasi = kecamatan
    with col2:
        program = st.selectbox("Program Akademik", ["SD", "SMP", "SMA/SMK"], index=0)
        st.session_state.form_program = program
        bot.program = program
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("<h2 style='font-size:2rem;'>📚 Katalog Donasi</h2>", unsafe_allow_html=True)
    search = st.text_input("🔍 Cari Donasi", placeholder="Contoh: Pulpen, Buku, Beasiswa...")

    categories = {
        "📚 Buku Pembelajaran Akademik": ["Buku SD", "Buku SMP", "Buku SMA/SMK"],
        "✏️ Alat Tulis Siswa": ["Pulpen", "Pensil", "Penggaris", "Penghapus", "Penghapus Pulpen", "Kotak Alat Tulis", "Buku Tulis", "Tas Punggung"],
        "👨‍🏫 Alat Pembelajaran Pengajar": ["Papan Tulis", "Spidol", "Penghapus Papan"],
        "🪑 Alat Penunjang Pembelajaran": ["Meja Siswa", "Kursi Siswa"],
        "🏫 Operasional Pembelajaran": ["Sewa Ruangan Belajar", "Upah Pengajar Sukarela", "Sewa Fasilitas Pelaksanaan Kegiatan"],
        "🎓 Beasiswa Siswa": ["Beasiswa Uang Saku"]
    }

    catalog = bot.engine.catalog
    for category, items in categories.items():
        filtered_items = [item for item in items if not search or search.lower() in item.lower()]
        if filtered_items:
            st.markdown(f"<div class='kategori-header'>{category}</div>", unsafe_allow_html=True)
            cols = st.columns(3)
            for i, item_name in enumerate(filtered_items):
                if item_name in catalog:
                    data = catalog[item_name]
                    with cols[i % 3]:
                        st.markdown(f"""
                        <div class="katalog-card">
                            <div><h4>{data['emoji']} {item_name}</h4><p style="color:#94A3B8;">{data['desc']}</p></div>
                            <h3 style="color:#F59E0B;">Rp {data['price']:,}</h3>
                        </div>
                        """, unsafe_allow_html=True)

# =====================================================
# HALAMAN KERANJANG
# =====================================================
elif st.session_state.current_page == "Keranjang":
    st.header("🛒 Keranjang Donasi")
    if not bot.engine.cart:
        st.warning("Belum ada item donasi.")
    else:
        for item in bot.engine.cart:
            subtotal = item["price"] * item["qty"]
            st.markdown(f"<div style='background:#1E293B; padding:15px; border-radius:15px; margin-bottom:10px;'><b>{item['emoji']} {item['item']}</b> (x{item['qty']}) - Rp {subtotal:,}</div>", unsafe_allow_html=True)
        total = bot.calculate_total()
        st.success(f"### 💰 Total Donasi : Rp {total:,}")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📤 Checkout", use_container_width=True):
                st.session_state.show_success = True
                bot.engine.clear_cart()
                st.rerun()
        with col2:
            if st.button("🗑️ Kosongkan Keranjang", use_container_width=True):
                bot.engine.clear_cart()
                st.rerun()
    if st.session_state.show_success:
        st.balloons()
        st.markdown("<div style='background:#10B981; padding:30px; border-radius:15px; text-align:center;'><h1>🎉 DONASI BERHASIL</h1><p>Terima kasih atas donasi Anda.</p></div>", unsafe_allow_html=True)
        if st.button("Kembali ke Beranda", use_container_width=True):
            st.session_state.bot_fsm = DonationFSM()
            st.session_state.bot_fsm.step()
            st.session_state.messages = [{"role": "assistant", "content": st.session_state.bot_fsm.get_response()}]
            st.session_state.show_success = False
            st.session_state.current_page = "Beranda"
            st.rerun()

# =====================================================
# HALAMAN CHATBOT
# =====================================================
elif st.session_state.current_page == "Chatbot":
    st.header("🤖 Chatbot Donasi")
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    prompt = st.chat_input("Contoh: halo, menu, 2 pulpen, keranjang, checkout")
    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        bot.step(prompt)
        response = bot.get_response()
        st.session_state.messages.append({"role": "assistant", "content": response})
        if "🎉 Donasi Berhasil" in response:
            st.session_state.show_success = True
        st.rerun()

# =====================================================
# SIDEBAR
# =====================================================
with st.sidebar:
    st.header("📋 Informasi Donasi")
    st.write(f"📍 Kecamatan : **{st.session_state.form_kecamatan}**")
    st.write(f"🎓 Program : **{st.session_state.form_program}**")
    st.divider()
    st.subheader("🛒 Ringkasan")
    st.write(f"Jumlah Item : **{sum(item['qty'] for item in bot.engine.cart)}**")
    st.write(f"Total Donasi : **Rp {bot.calculate_total():,}**")
    st.divider()
    st.subheader("💡 Contoh Perintah Chatbot")
    st.markdown("""
    - Halo
    - Menu
    - Keranjang
    - 2 Pulpen
    - 3 Buku IPA
    - Checkout
    - Reset
    """)
