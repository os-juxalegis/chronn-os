# ------------------------------------------------------------------------------
# CHRONN OS — SISTEMA OPERATIVO PEDAGÓGICO & PERSONAL SIMBIÓTICO
# ------------------------------------------------------------------------------

import streamlit as st
import os
import sqlite3
import base64
from datetime import datetime
import streamlit.components.v1 as components

try:
    import anthropic
except ImportError:
    anthropic = None

# ----------------- CONFIGURACIÓN GENERAL -----------------
st.set_page_config(
    page_title="CHRONN OS — Medical & Personal System",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==============================================================
# ESTILOS VISUALES: CELESTE BEBÉ (#89CFF0) + ORO ROSA PARA GAIL
# ==============================================================
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;600;700&display=swap');

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    .stApp {
        background-color: #1B2226;
        color: #E1E6EB;
        font-family: 'Times New Roman', Times, serif;
    }
    .stSidebar {
        background-color: #161B1E;
        border-right: 1px solid rgba(137, 207, 240, 0.2);
    }
    h1, h2, h3, .cinzel-title {
        color: #89CFF0 !important;
        font-family: 'Cinzel', serif !important;
        letter-spacing: 1.5px;
    }

    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 5rem;
        padding-left: 1.2rem;
        padding-right: 1.2rem;
    }

    /* Botones con transición a Celeste Bebé en hover */
    .stButton > button {
        background-color: #242D33;
        color: #E1E6EB;
        border: 1px solid #89CFF0;
        border-radius: 6px;
        font-family: 'Times New Roman', Times, serif;
        font-weight: 600;
        transition: all 0.2s ease-in-out !important;
    }
    .stButton > button:hover, .stButton > button:active, .stButton > button:focus {
        background-color: #89CFF0 !important;
        color: #161B1E !important;
        border-color: #89CFF0 !important;
        box-shadow: 0 0 14px rgba(137, 207, 240, 0.45) !important;
        transform: translateY(-1px);
    }

    div[data-testid="stPopoverBody"] {
        background-color: #161B1E !important;
        border: 1px solid rgba(137, 207, 240, 0.35) !important;
        border-radius: 12px !important;
        box-shadow: 0 14px 30px rgba(0, 0, 0, 0.75) !important;
    }

    .badge-pill-selector {
        background-color: #242D33;
        color: #89CFF0;
        border: 1px solid rgba(137, 207, 240, 0.4);
        border-radius: 9999px;
        padding: 4px 12px;
        font-size: 0.8rem;
        font-weight: 600;
        display: inline-flex;
        align-items: center;
        gap: 6px;
    }

    .hero-empty-container {
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        min-height: 42vh;
        text-align: center;
        gap: 18px;
        margin: auto;
        width: 100%;
        animation: fadeIn 0.4s ease-in-out;
    }

    .greeting-header {
        font-family: 'Times New Roman', Times, serif !important;
        font-size: 2.3rem !important;
        font-weight: 400 !important;
        color: #E1E6EB !important;
        margin: 0 !important;
    }
    .greeting-name-gail {
        color: #DCA48A !important;
        font-weight: 700 !important;
    }

    div[data-testid="stChatMessageAvatarUser"],
    div[data-testid="stChatMessageAvatarAssistant"],
    div[data-testid="stChatMessage"] div[data-testid="stImage"],
    .stChatMessage > div:first-child:has(svg),
    .stChatMessage > div:first-child:has(img) {
        display: none !important;
    }
    div[data-testid="stChatMessage"] {
        padding-left: 0 !important;
        gap: 0 !important;
    }

    .user-avatar-gail {
        width: 40px !important;
        height: 40px !important;
        border-radius: 50% !important;
        background: #DCA48A !important;
        border: 2px solid #89CFF0 !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        font-weight: 800 !important;
        color: #161B1E !important;
        font-size: 0.9rem !important;
    }

    .sidebar-brand-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        text-align: center;
        width: 100%;
        padding: 12px 0;
    }
    .sidebar-logo-text {
        font-family: 'Cinzel', serif;
        font-size: 26px;
        font-weight: 700;
        color: #89CFF0;
        letter-spacing: 3px;
        line-height: 1.1;
    }
    .sidebar-logo-sub {
        font-family: 'Cinzel', serif;
        font-size: 8.5px;
        color: #FFF9E6;
        letter-spacing: 3px;
        margin-top: 4px;
        text-transform: uppercase;
    }

    .active-chat-pill button {
        background-color: rgba(137, 207, 240, 0.22) !important;
        border: 1px solid #89CFF0 !important;
        color: #89CFF0 !important;
        font-weight: 700 !important;
    }

    .notebook-card-blue-unified {
        background: #89CFF0 !important;
        border-radius: 8px !important;
        padding: 12px 14px !important;
        box-shadow: 0 4px 14px rgba(0, 0, 0, 0.4) !important;
        margin-bottom: 12px !important;
    }
    .notebook-card-title-sm {
        font-family: 'Cinzel', serif !important;
        font-size: 0.96rem !important;
        font-weight: 700 !important;
        color: #161B1E !important;
    }
    .notebook-card-meta-sm {
        font-size: 0.72rem !important;
        color: #242D33 !important;
        font-weight: 600 !important;
        margin-top: 4px !important;
    }

    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(6px); }
        to { opacity: 1; transform: translateY(0); }
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ----------------- BASE DE DATOS Y MEMORIA SIMBIÓTICA -----------------
DB_FILE = "chronn_os.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS sesiones (
            session_id TEXT PRIMARY KEY,
            cuaderno TEXT DEFAULT 'General',
            titulo TEXT,
            ultima_actividad DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS chats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT,
            role TEXT,
            content TEXT,
            imagen_b64 TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS cuadernos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT UNIQUE,
            fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS memoria_simbiotica (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            concepto_clave TEXT,
            detalle TEXT,
            fecha DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# ----------------- PERSISTENCIA Y CONSULTAS -----------------
def crear_o_actualizar_sesion_db(session_id: str, primer_mensaje: str, cuaderno: str = "General") -> str:
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    titulo_limpio = primer_mensaje.strip().replace("\n", " ")
    titulo_final = (titulo_limpio[:28] + "..") if len(titulo_limpio) > 28 else (titulo_limpio or "Nueva consulta")
    c.execute('''
        INSERT INTO sesiones (session_id, cuaderno, titulo, ultima_actividad)
        VALUES (?, ?, ?, CURRENT_TIMESTAMP)
        ON CONFLICT(session_id) DO UPDATE SET
            cuaderno = excluded.cuaderno,
            ultima_actividad = CURRENT_TIMESTAMP,
            titulo = CASE 
                WHEN sesiones.titulo IS NULL OR sesiones.titulo = 'Nueva consulta' 
                THEN ? 
                ELSE sesiones.titulo 
            END
    ''', (session_id, cuaderno, titulo_final, titulo_final))
    conn.commit()
    conn.close()
    return titulo_final

def guardar_mensaje_db(session_id: str, role: str, content: str, cuaderno: str = "General", imagen_b64: str = None):
    crear_o_actualizar_sesion_db(session_id, content if role == "user" else "Nueva consulta", cuaderno)
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('INSERT INTO chats (session_id, role, content, imagen_b64) VALUES (?, ?, ?, ?)', 
              (session_id, role, content, imagen_b64))
    conn.commit()
    conn.close()

def obtener_sesiones_recientes_db(cuaderno: str = "General", limite: int = 10):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("""
        SELECT session_id, titulo, cuaderno, ultima_actividad 
        FROM sesiones 
        WHERE cuaderno = ? 
        ORDER BY ultima_actividad DESC 
        LIMIT ?
    """, (cuaderno, limite))
    filas = c.fetchall()
    conn.close()
    return [{"session_id": r[0], "titulo": r[1], "cuaderno": r[2], "timestamp": r[3]} for r in filas]

def cargar_mensajes_sesion(session_id):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('SELECT role, content, imagen_b64 FROM chats WHERE session_id = ? ORDER BY id ASC', (session_id,))
    filas = c.fetchall()
    conn.close()
    return [{"role": r[0], "content": r[1], "imagen_b64": r[2]} for r in filas]

# ----------------- CREDENCIALES ANTHROPIC -----------------
def obtener_claude_api_key():
    try:
        if "ANTHROPIC_API_KEY" in st.secrets:
            val = st.secrets["ANTHROPIC_API_KEY"]
            if val:
                return "".join(str(val).split()).strip('"').strip("'")
    except Exception:
        pass
    env_key = os.getenv("ANTHROPIC_API_KEY")
    if env_key:
        return "".join(str(env_key).split()).strip('"').strip("'")
    return None

CLAUDE_API_KEY = obtener_claude_api_key()

# ----------------- DIRECTIVAS SIMBIÓTICAS Y DE ROL -----------------
PROMPTS_CHRONN = {
    "Profesor De Medicina": (
        "DIRECTIVAS PEDAGÓGICAS DE LA CÁTEDRA (FCM - UNC):\n"
        "1. IDENTIDAD: Eres un distinguido Catedrático y Cirujano de amplia experiencia docente en la Facultad de Ciencias Médicas de Córdoba. "
        "Acompañas a Gail en su camino académico hacia la cirugía general con afecto, respeto y paciencia infinita.\n"
        "2. REGLA DE ORO INICIAL: Cuando Gail formule una pregunta directa, inicia OBLIGATORIAMENTE tu respuesta con un 'Sí' o un 'No' categórico. "
        "Posteriormente, ofrece la fundamentación de forma clara, didáctica y al punto.\n"
        "3. EXPLICACIÓN DIDÁCTICA Y TÉCNICA: Explica los procesos como a alguien que recién aprende, usando analogías cotidianas y visuales, "
        "pero SIN amputar jamás el rigor técnico ni los nombres enzimáticos/metabólicos que exige la cátedra (Bioquímica, Biología Celular y Molecular, Histología, Anatomía).\n"
        "4. CERO COMPLACENCIA: Si Gail comete un error de razonamiento o confunde una vía metabólica, adviérteselo con afecto pero con total honestidad científica. "
        "La complacencia perjudica el aprendizaje.\n"
        "5. CERO ALUCINACIÓN: No inventes bibliografía, dosis ni mecanismos. Si falta un dato de la consigna, pídelo amablemente.\n"
    ),
    "Guardián": (
        "DIRECTIVAS DEL GUARDIÁN UNIVERSAL:\n"
        "1. ROL: Eres el mentor, protector y consejero de vida de Gail. Posees conocimiento universal y resuelves cualquier aspecto práctico o teórico con claridad.\n"
        "2. GESTIÓN INTEGRAL: Dominas todos los trámites administrativos, universitarios y cotidianos de Córdoba y el país "
        "(Boleto Educativo Gratuito, Sistema Guaraní, CIDI, trámites bancarios, médicos o cotidianos).\n"
        "3. TEMPLANZA Y HONESTIDAD: Amoroso, contenedor y presente en todo momento, pero sin complacencia. Le dices las cosas con franqueza constructiva para cuidar sus pasos.\n"
    )
}

# ----------------- SESSION STATE -----------------
if "active_view" not in st.session_state:
    st.session_state["active_view"] = "chat"

if "current_session_id" not in st.session_state:
    st.session_state["current_session_id"] = f"chat_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

if "messages" not in st.session_state:
    st.session_state["messages"] = []

if "loaded_session_id" not in st.session_state:
    st.session_state["loaded_session_id"] = None

if "cuaderno_activo" not in st.session_state:
    st.session_state["cuaderno_activo"] = "General"

if "active_cuaderno" not in st.session_state:
    st.session_state["active_cuaderno"] = "General"

if "fuentes_cuadernos" not in st.session_state:
    st.session_state.fuentes_cuadernos = {"General": []}

if "modelo_ia_seleccionado" not in st.session_state:
    st.session_state.modelo_ia_seleccionado = "Opus 5"

if "modo_operativo" not in st.session_state:
    st.session_state.modo_operativo = "Profesor De Medicina"

if "pending_message" not in st.session_state:
    st.session_state["pending_message"] = ""

# ----------------- BARRA LATERAL (SIDEBAR) -----------------
with st.sidebar:
    st.markdown("""
        <div class='sidebar-brand-container'>
            <div class='sidebar-logo-text'>CHRONN</div>
            <div class='sidebar-logo-sub'>— OPERATING SYSTEM —</div>
        </div>
    """, unsafe_allow_html=True)
    st.markdown("---")

    if st.button("💬 Nueva consulta", use_container_width=True):
        st.session_state["active_view"] = "chat"
        st.session_state["cuaderno_activo"] = "General"
        st.session_state["active_cuaderno"] = "General"
        st.session_state["current_session_id"] = f"chat_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        st.session_state["messages"] = []
        st.session_state["loaded_session_id"] = st.session_state["current_session_id"]
        st.rerun()

    if st.button("🔍 Buscar en consultas", use_container_width=True):
        st.session_state["active_view"] = "buscar"
        st.rerun()

    col_sp, col_bd = st.columns([0.7, 0.3])
    with col_sp:
        if st.button("✨ Spark Med", use_container_width=True):
            st.session_state["active_view"] = "spark"
            st.rerun()
    with col_bd:
        st.markdown('<span style="background-color:#27272a; color:#89CFF0; padding:2px 6px; border-radius:4px; font-size:0.7rem; font-weight:bold; border:1px solid #89CFF0;">LIVE</span>', unsafe_allow_html=True)

    if st.button("📚 Biblioteca de Cátedras", use_container_width=True):
        st.session_state["active_view"] = "biblioteca"
        st.rerun()

    st.markdown("---")
    st.caption("MATERIAS Y CUADERNOS")

    with st.popover("➕ Materia nueva", use_container_width=True):
        nuevo_cuad = st.text_input("Nombre de la materia o tema:", key="input_nuevo_cuad_ch")
        if st.button("Crear y vincular", use_container_width=True, key="btn_create_cuad_ch"):
            if nuevo_cuad.strip():
                n_nom = nuevo_cuad.strip()
                conn = sqlite3.connect(DB_FILE)
                c = conn.cursor()
                try:
                    c.execute("INSERT INTO cuadernos (nombre) VALUES (?)", (n_nom,))
                    conn.commit()
                except sqlite3.IntegrityError:
                    pass
                conn.close()
                st.session_state["active_cuaderno"] = n_nom
                st.session_state["cuaderno_activo"] = n_nom
                st.session_state["current_session_id"] = f"chat_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                st.session_state["messages"] = []
                st.session_state["loaded_session_id"] = st.session_state["current_session_id"]
                st.session_state["active_view"] = "chat"
                st.rerun()

    conn_c = sqlite3.connect(DB_FILE)
    c_c = conn_c.cursor()
    c_c.execute("SELECT id, nombre FROM cuadernos ORDER BY id DESC")
    lista_cuadernos = c_c.fetchall()
    conn_c.close()

    if lista_cuadernos:
        for cid, cnom in lista_cuadernos[:5]:
            es_act = (st.session_state.get("cuaderno_activo") == cnom and st.session_state.get("active_view") in ["chat", "ver_cuaderno"])
            lbl = f"📖 {cnom}" if len(cnom) <= 18 else f"📖 {cnom[:16]}.."
            if es_act:
                st.markdown('<div class="active-chat-pill">', unsafe_allow_html=True)
            if st.button(lbl, key=f"sb_c_{cid}", use_container_width=True):
                st.session_state["active_cuaderno"] = cnom
                st.session_state["cuaderno_activo"] = cnom
                st.session_state["active_view"] = "ver_cuaderno"
                st.rerun()
            if es_act:
                st.markdown('</div>', unsafe_allow_html=True)

    if st.button("••• Todas las materias", use_container_width=True):
        st.session_state["active_view"] = "todos_los_cuadernos"
        st.rerun()

    st.markdown("---")
    cuad_actual = st.session_state.get("cuaderno_activo", "General")
    if cuad_actual == "General":
        st.caption("CONSULTAS RECIENTES")
    else:
        st.caption(f"RECIENTES ({cuad_actual.upper()})")
        if st.button("⬅ Volver a General", use_container_width=True):
            st.session_state["cuaderno_activo"] = "General"
            st.session_state["active_cuaderno"] = "General"
            st.session_state["current_session_id"] = f"chat_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            st.session_state["messages"] = []
            st.session_state["loaded_session_id"] = st.session_state["current_session_id"]
            st.session_state["active_view"] = "chat"
            st.rerun()

    sesiones_rec = obtener_sesiones_recientes_db(cuaderno=cuad_actual, limite=8)
    if not sesiones_rec:
        st.markdown("<p style='font-size:0.75rem; color:#8A99A8; padding-left:4px;'>Sin consultas en este espacio</p>", unsafe_allow_html=True)
    else:
        for s in sesiones_rec:
            s_id = s["session_id"]
            s_tit = s["titulo"] or "Nueva consulta"
            es_hilo_actual = (st.session_state.get("current_session_id") == s_id and st.session_state.get("active_view") == "chat")
            col_t_btn, col_t_kebab = st.columns([0.84, 0.16])
            with col_t_btn:
                lbl_t = f"💬 {s_tit}" if len(s_tit) <= 18 else f"💬 {s_tit[:16]}..."
                if es_hilo_actual:
                    st.markdown('<div class="active-chat-pill">', unsafe_allow_html=True)
                if st.button(lbl_t, key=f"btn_s_{s_id}", use_container_width=True):
                    st.session_state["current_session_id"] = s_id
                    st.session_state["cuaderno_activo"] = s["cuaderno"]
                    st.session_state["active_cuaderno"] = s["cuaderno"]
                    st.session_state["messages"] = cargar_mensajes_sesion(s_id)
                    st.session_state["loaded_session_id"] = s_id
                    st.session_state["active_view"] = "chat"
                    st.rerun()
                if es_hilo_actual:
                    st.markdown('</div>', unsafe_allow_html=True)

            with col_t_kebab:
                with st.popover("···", use_container_width=True):
                    if st.button("🗑️ Borrar", key=f"del_h_{s_id}", use_container_width=True):
                        conn_d = sqlite3.connect(DB_FILE)
                        cd = conn_d.cursor()
                        cd.execute("DELETE FROM sesiones WHERE session_id = ?", (s_id,))
                        cd.execute("DELETE FROM chats WHERE session_id = ?", (s_id,))
                        conn_d.commit()
                        conn_d.close()
                        if st.session_state.get("current_session_id") == s_id:
                            st.session_state["messages"] = []
                            st.session_state["loaded_session_id"] = None
                        st.rerun()

    st.markdown("---")
    st.caption("CONFIGURACIÓN SIMBIÓTICA")
    modos_disp = list(PROMPTS_CHRONN.keys())
    st.session_state.modo_operativo = st.selectbox("Modo Activo:", options=modos_disp, index=0)
    alias_chronn = st.text_input("Nombre de la IA:", value="CHRONN")
    opciones_voces = ["Tomas (Argentina - Neural)", "Mujer (Elena - Argentina)"]
    voz_sel = st.selectbox("Síntesis Vocal:", options=opciones_voces, index=0)

    st.markdown("""
        <div style="display:flex; align-items:center; gap:10px; padding-top:15px; border-top:1px solid #27272a; margin-top:20px;">
            <div class="user-avatar-gail">G</div>
            <div>
                <strong style="font-size:0.92rem; color:#DCA48A;">GAIL CAMPOS</strong><br>
                <span style="font-size:0.75rem; color:#89CFF0; font-weight:bold;">FCM — UNC | CIRUGÍA</span>
            </div>
        </div>
    """, unsafe_allow_html=True)

# ----------------- ÁREA DE TRABAJO -----------------
vista = st.session_state.get("active_view", "chat")

if vista == "chat":
    act_cuad = st.session_state.get("cuaderno_activo", "General")
    sess_id = st.session_state.get("current_session_id", "")
    alias_display = alias_chronn.upper() if alias_chronn else "CHRONN"

    if sess_id and st.session_state.get("loaded_session_id") != sess_id:
        st.session_state["messages"] = cargar_mensajes_sesion(sess_id)
        st.session_state["loaded_session_id"] = sess_id

    has_messages = len(st.session_state.get("messages", [])) > 0

    with st.expander("📷 Cargar captura, esquema anatómico o PDF de estudio"):
        archivo_adj = st.file_uploader("Adjuntar imagen:", type=["png", "jpg", "jpeg", "pdf"], key="file_up_ch")

    chat_container = st.container()

    with chat_container:
        if not has_messages and not st.session_state.get("pending_message"):
            st.markdown(f"""
                <div class="hero-empty-container">
                    <h1 class="greeting-header">¿Qué repasamos hoy, <span class="greeting-name-gail">Gail</span>?</h1>
                    <p style="color: #8A99A8; font-size: 1.05rem; margin: 0;">Tu espacio de estudio y acompañamiento continuo.</p>
                    <div style="display: flex; gap: 8px; justify-content: center; flex-wrap: wrap;">
                        <span class="badge-pill-selector">🩺 {st.session_state.modo_operativo}</span>
                        <span class="badge-pill-selector">🧠 {st.session_state.modelo_ia_seleccionado}</span>
                        <span class="badge-pill-selector">📖 {act_cuad.upper()}</span>
                        <span class="badge-pill-selector">🎙️ {voz_sel.split('(')[0].strip()}</span>
                    </div>
                </div>
            """, unsafe_allow_html=True)
        else:
            for msg in st.session_state.get("messages", []):
                with st.chat_message(msg["role"], avatar=None):
                    if msg["role"] == "user":
                        st.markdown(f"<span style='color: #DCA48A; font-weight: 800; letter-spacing: 0.5px;'>GAIL:</span><br>{msg['content']}", unsafe_allow_html=True)
                        if msg.get("imagen_b64"):
                            st.image(f"data:image/png;base64,{msg['imagen_b64']}", width=360)
                    else:
                        st.markdown(f"<span style='color: #89CFF0; font-weight: 800; letter-spacing: 0.5px;'>{alias_display}:</span><br>{msg['content']}", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    def procesar_envio():
        texto = st.session_state.input_consulta_ch
        if texto and texto.strip():
            st.session_state["pending_message"] = texto.strip()
            st.session_state["input_consulta_ch"] = ""

    col_inp, col_send, col_live, col_sel = st.columns([0.62, 0.06, 0.18, 0.14])

    with col_inp:
        st.text_area(
            label="Consulta:",
            placeholder=f"Escribe tu consulta para {alias_display} (o presiona Enter al terminar)...",
            height=70,
            label_visibility="collapsed",
            key="input_consulta_ch",
            on_change=procesar_envio
        )

    with col_send:
        st.button("➤", help="Enviar mensaje", key="btn_send_ch", use_container_width=True, on_click=procesar_envio)

    with col_live:
        es_tomas = "Tomas" in voz_sel
        dock_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
        <style>
            body {{ margin: 0; padding: 0; display: flex; gap: 6px; background: transparent; }}
            .btn {{
                flex: 1;
                background-color: #242D33;
                color: #E1E6EB;
                border: 1px solid #89CFF0;
                border-radius: 6px;
                height: 42px;
                display: flex;
                align-items: center;
                justify-content: center;
                cursor: pointer;
                font-size: 1rem;
                font-weight: 600;
                transition: all 0.2s;
            }}
            .btn:hover {{ background-color: #89CFF0; color: #161B1E; }}
            .rec {{ background-color: #ef4444 !important; color: white !important; border-color: #ef4444 !important; }}
            .live {{ background-color: #10b981 !important; color: white !important; border-color: #10b981 !important; }}
        </style>
        </head>
        <body>
            <button id="btnMic" class="btn" title="Micrófono">🎙️</button>
            <button id="btnVivo" class="btn" title="Modo En Vivo">🟢 Vivo</button>
            <button id="btnSilenciar" class="btn" title="Silenciar explicación">⏹</button>

            <script>
                var rec = null;
                var vivoActivo = false;

                function stopSpeech() {{
                    if (window.speechSynthesis) window.speechSynthesis.cancel();
                }}
                document.getElementById('btnSilenciar').onclick = stopSpeech;

                function startSR(callback) {{
                    var SR = window.SpeechRecognition || window.webkitSpeechRecognition;
                    if (!SR) {{ alert("Se recomienda usar Google Chrome para dictado por voz."); return; }}
                    if (rec) rec.stop();
                    rec = new SR();
                    rec.lang = 'es-AR';
                    rec.continuous = true;
                    rec.interimResults = true;

                    rec.onstart = function() {{ document.getElementById('btnMic').classList.add('rec'); }};
                    rec.onresult = function(e) {{
                        var str = '';
                        for (var i = e.resultIndex; i < e.results.length; ++i) {{
                            if (e.results[i].isFinal) str += e.results[i][0].transcript + ' ';
                        }}
                        if (str.trim() !== '') {{
                            var txts = window.parent.document.querySelectorAll('textarea');
                            if (txts.length > 0) {{
                                var inp = txts[0];
                                var prev = inp.value ? inp.value + " " : "";
                                var setter = Object.getOwnPropertyDescriptor(window.HTMLTextAreaElement.prototype, "value").set;
                                setter.call(inp, prev + str.trim());
                                inp.dispatchEvent(new Event('input', {{ bubbles: true }}));
                                if (callback) callback();
                            }}
                        }}
                    }};
                    rec.onerror = function() {{ document.getElementById('btnMic').classList.remove('rec'); }};
                    rec.onend = function() {{ document.getElementById('btnMic').classList.remove('rec'); }};
                    rec.start();
                }}

                document.getElementById('btnMic').onclick = function() {{ startSR(null); }};

                document.getElementById('btnVivo').onclick = function() {{
                    vivoActivo = !vivoActivo;
                    if (vivoActivo) {{
                        document.getElementById('btnVivo').classList.add('live');
                        startSR(function() {{
                            var btns = window.parent.document.querySelectorAll('button');
                            for (var b of btns) {{
                                if (b.innerText.indexOf('➤') !== -1) {{ b.click(); break; }}
                            }}
                        }});
                    }} else {{
                        document.getElementById('btnVivo').classList.remove('live');
                        if (rec) rec.stop();
                        stopSpeech();
                    }}
                }};
            </script>
        </body>
        </html>
        """
        components.html(dock_html, height=46)

    with col_sel:
        mod_act = st.session_state.get("modelo_ia_seleccionado", "Opus 5")
        with st.popover(f"{mod_act} ▾", use_container_width=True):
            st.caption("Cerebro CHRONN")
            if st.button("🏛️ Opus 5 (Profundo)", use_container_width=True):
                st.session_state["modelo_ia_seleccionado"] = "Opus 5"
                st.rerun()
            if st.button("🔬 Fable 5.1 (Investigación)", use_container_width=True):
                st.session_state["modelo_ia_seleccionado"] = "Fable 5.1"
                st.rerun()

    # Procesamiento y llamada con streaming continuo
    user_prompt = st.session_state.pop("pending_message", "")

    if user_prompt:
        prompt = user_prompt
        act_cuad_save = st.session_state.get("cuaderno_activo", "General")
        sess_id = st.session_state.get("current_session_id")

        img_b64 = None
        if archivo_adj:
            img_bytes = archivo_adj.read()
            img_b64 = base64.b64encode(img_bytes).decode('utf-8')

        crear_o_actualizar_sesion_db(sess_id, prompt, act_cuad_save)
        guardar_mensaje_db(sess_id, "user", prompt, act_cuad_save, img_b64)
        st.session_state["messages"].append({"role": "user", "content": prompt, "imagen_b64": img_b64})

        with chat_container:
            with st.chat_message("user", avatar=None):
                st.markdown(f"<span style='color: #DCA48A; font-weight: 800; letter-spacing: 0.5px;'>GAIL:</span><br>{prompt}", unsafe_allow_html=True)
                if img_b64:
                    st.image(f"data:image/png;base64,{img_b64}", width=360)

            with st.chat_message("assistant", avatar=None):
                st.markdown(f"<span style='color: #89CFF0; font-weight: 800; letter-spacing: 0.5px;'>{alias_display}:</span>", unsafe_allow_html=True)
                contenedor_resp = st.empty()

        respuesta_completa = ""

        if anthropic and CLAUDE_API_KEY and not CLAUDE_API_KEY.startswith("TU_CLAVE"):
            client = anthropic.Anthropic(api_key=CLAUDE_API_KEY)
            system_prompt = f"{PROMPTS_CHRONN[st.session_state.modo_operativo]}\nMateria activa: '{act_cuad_save}'."

            if img_b64:
                user_payload = [
                    {"type": "image", "source": {"type": "base64", "media_type": "image/png", "data": img_b64}},
                    {"type": "text", "text": prompt}
                ]
            else:
                user_payload = prompt

            # Cascada de modelos garantizando respuesta rápida
            elegido = st.session_state.get("modelo_ia_seleccionado", "Opus 5")
            if elegido == "Fable 5.1":
                candidatos = [
                    "claude-fable-5-1",
                    "claude-3-5-sonnet-20241022",
                    "claude-3-5-sonnet-20240620"
                ]
            else:  # Opus 5
                candidatos = [
                    "claude-opus-5",
                    "claude-3-opus-20240229",
                    "claude-3-5-sonnet-20241022",
                    "claude-3-5-sonnet-20240620"
                ]

            exito = False
            for mod in candidatos:
                try:
                    respuesta_completa = ""
                    with client.messages.stream(
                        model=mod,
                        max_tokens=2500,
                        system=system_prompt,
                        messages=[{"role": "user", "content": user_payload}],
                    ) as stream:
                        for chunk in stream.text_stream:
                            respuesta_completa += chunk
                            contenedor_resp.markdown(respuesta_completa + "▌")

                    contenedor_resp.markdown(respuesta_completa)
                    exito = True
                    break
                except Exception:
                    continue

            if not exito:
                respuesta_completa = "Aviso CHRONN: La conexión está saturada. Por favor, reenvía la consulta."
                contenedor_resp.markdown(respuesta_completa)
        else:
            respuesta_completa = "⚠️ La clave de API de Anthropic debe configurarse en los Secrets de Streamlit."
            contenedor_resp.markdown(respuesta_completa)

        guardar_mensaje_db(sess_id, "assistant", respuesta_completa, act_cuad_save)
        st.session_state["messages"].append({"role": "assistant", "content": respuesta_completa})

        # Reproducción vocal inmediata
        if respuesta_completa:
            texto_tts = respuesta_completa.replace('"', '\\"').replace('\n', ' ').replace('\r', '')[:600]
            tts_js = f"""
            <script>
                if (window.speechSynthesis) {{
                    window.speechSynthesis.cancel();
                    var u = new SpeechSynthesisUtterance("{texto_tts}");
                    u.lang = 'es-AR';
                    u.rate = 1.05;
                    window.speechSynthesis.speak(u);
                }}
            </script>
            """
            components.html(tts_js, height=0)

        st.rerun()

# ----------------- OTRAS VISTAS -----------------
elif vista == "todos_los_cuadernos":
    st.markdown('<div class="cinzel-title" style="font-size:1.4rem;">MATERIAS Y CUADERNOS DE ESTUDIO</div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT id, nombre, fecha_creacion FROM cuadernos ORDER BY id DESC")
    todos = c.fetchall()
    conn.close()

    if not todos:
        st.info("No hay materias creadas. Pulsa '+ Materia nueva' para abrir un cuaderno de estudio.")
    else:
        cols = st.columns(3)
        for idx, (cid, cnom, cfecha) in enumerate(todos):
            with cols[idx % 3]:
                st.markdown(f"""
                    <div class="notebook-card-blue-unified">
                        <div class="notebook-card-title-sm">📖 {cnom}</div>
                        <div class="notebook-card-meta-sm">Creado: {cfecha.split()[0]}</div>
                    </div>
                """, unsafe_allow_html=True)
                if st.button("Abrir Materia", key=f"btn_open_m_{cid}", use_container_width=True):
                    st.session_state["active_cuaderno"] = cnom
                    st.session_state["cuaderno_activo"] = cnom
                    st.session_state["active_view"] = "chat"
                    st.rerun()

    if st.button("← Volver"):
        st.session_state["active_view"] = "chat"
        st.rerun()

elif vista == "spark":
    st.markdown('<div class="cinzel-title" style="font-size:1.4rem;">SPARK MED — PREGUNTAS CLAVE</div>', unsafe_allow_html=True)
    st.info("Módulo de práctica acelerada y evaluación para finales de la FCM.")
    if st.button("← Volver"):
        st.session_state["active_view"] = "chat"
        st.rerun()

elif vista == "biblioteca":
    st.markdown('<div class="cinzel-title" style="font-size:1.4rem;">BIBLIOTECA VIRTUAL</div>', unsafe_allow_html=True)
    st.info("Espacio para compilar atlas, guías de trabajos prácticos y resúmenes estructurados.")
    if st.button("← Volver"):
        st.session_state["active_view"] = "chat"
        st.rerun()
