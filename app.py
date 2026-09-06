# ------------------------------------------------------------------------------
# CHRONN OS — SISTEMA OPERATIVO PEDAGÓGICO & PERSONAL SIMBIÓTICO
# ------------------------------------------------------------------------------

import streamlit as st
import os
import sqlite3
import base64
import asyncio
from datetime import datetime
import streamlit.components.v1 as components

# --- MOTOR DE INTELIGENCIA ARTIFICIAL: GOOGLE CLOUD VERTEX AI ---
try:
    import vertexai
    from google.oauth2 import service_account
    from vertexai.generative_models import GenerativeModel, Part, HarmBlockThreshold, HarmCategory
except ImportError:
    vertexai = None

# --- SÍNTESIS DE VOZ NEURAL HUMANA ---
try:
    import edge_tts
except ImportError:
    edge_tts = None

# ----------------- CONFIGURACIÓN GENERAL -----------------
st.set_page_config(
    page_title="CHRONN OS — Medical & Personal System",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==============================================================
# ESTILOS VISUALES: CELESTE BEBÉ (#89CFF0) + ORO ROSADO PARA GAIL
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
        padding: 14px 16px !important;
        box-shadow: 0 4px 14px rgba(0, 0, 0, 0.4) !important;
        margin-bottom: 10px !important;
    }
    .notebook-card-title-sm {
        font-family: 'Cinzel', serif !important;
        font-size: 1.05rem !important;
        font-weight: 700 !important;
        color: #161B1E !important;
    }
    .notebook-card-meta-sm {
        font-size: 0.76rem !important;
        color: #242D33 !important;
        font-weight: 600 !important;
        margin-top: 4px !important;
    }

    /* Tipografía sans-serif limpia con capitalización natural para la caja de texto */
    div[data-testid="stForm"] textarea,
    textarea#input_consulta_area {
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif !important;
        font-size: 0.95rem !important;
        letter-spacing: normal !important;
        text-transform: none !important;
        font-variant: normal !important;
        color: #E1E6EB !important;
    }
    div[data-testid="stForm"] textarea::placeholder,
    textarea#input_consulta_area::placeholder {
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif !important;
        font-size: 0.92rem !important;
        letter-spacing: normal !important;
        text-transform: none !important;
        font-variant: normal !important;
        color: #8A99A8 !important;
    }

    div[data-testid="stForm"] {
        border: none !important;
        padding: 0 !important;
        background: transparent !important;
    }

    /* Estilo del reproductor de audio neural integrado */
    audio {
        height: 32px;
        margin-top: 4px;
        filter: drop-shadow(0 2px 6px rgba(0,0,0,0.5));
    }

    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(6px); }
        to { opacity: 1; transform: translateY(0); }
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ----------------- BASE DE DATOS Y MIGRACIONES -----------------
DB_FILE = "chronn_os.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS sesiones (
            session_id TEXT PRIMARY KEY,
            cuaderno TEXT DEFAULT 'General',
            titulo TEXT,
            fijado INTEGER DEFAULT 0,
            ultima_actividad DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    try:
        c.execute("ALTER TABLE sesiones ADD COLUMN fijado INTEGER DEFAULT 0")
    except sqlite3.OperationalError:
        pass

    c.execute('''
        CREATE TABLE IF NOT EXISTS chats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT,
            role TEXT,
            content TEXT,
            imagen_b64 TEXT,
            audio_b64 TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    try:
        c.execute("ALTER TABLE chats ADD COLUMN audio_b64 TEXT")
    except sqlite3.OperationalError:
        pass

    c.execute('''
        CREATE TABLE IF NOT EXISTS cuadernos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT UNIQUE,
            fijado INTEGER DEFAULT 0,
            fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    try:
        c.execute("ALTER TABLE cuadernos ADD COLUMN fijado INTEGER DEFAULT 0")
    except sqlite3.OperationalError:
        pass

    c.execute('''
        CREATE TABLE IF NOT EXISTS biblioteca (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT,
            tipo TEXT,
            contenido_b64 TEXT,
            fecha DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    conn.commit()
    conn.close()

init_db()

# ----------------- MOTOR DE AUDIO NEURAL HUMANO (EDGE-TTS) -----------------
async def sintetizar_voz_neural_async(texto: str, nombre_voz: str) -> str:
    """Genera audio neural auténtico rioplatense en MP3 y devuelve base64"""
    if not edge_tts or not texto.strip():
        return None
    try:
        voz_cod = "es-AR-TomasNeural" if "Tomas" in nombre_voz else "es-AR-ElenaNeural"
        # Limpieza de fragmento para síntesis óptima
        texto_limpio = texto.replace("*", "").replace("#", "").replace("`", "")[:750]
        communicate = edge_tts.Communicate(texto_limpio, voz_cod, rate="-2%", pitch="+0Hz")
        audio_data = bytearray()
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                audio_data.extend(chunk["data"])
        if audio_data:
            return base64.b64encode(bytes(audio_data)).decode("utf-8")
    except Exception:
        pass
    return None

def generar_audio_neural(texto: str, nombre_voz: str) -> str:
    try:
        return asyncio.run(sintetizar_voz_neural_async(texto, nombre_voz))
    except Exception:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        res = loop.run_until_complete(sintetizar_voz_neural_async(texto, nombre_voz))
        loop.close()
        return res

# ----------------- OPERACIONES DE BASE DE DATOS -----------------
def crear_o_actualizar_sesion_db(session_id: str, primer_mensaje: str, cuaderno: str = "General") -> str:
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    titulo_limpio = primer_mensaje.strip().replace("\n", " ")
    titulo_final = (titulo_limpio[:30] + "..") if len(titulo_limpio) > 30 else (titulo_limpio or "Nueva consulta")
    c.execute('''
        INSERT INTO sesiones (session_id, cuaderno, titulo, fijado, ultima_actividad)
        VALUES (?, ?, ?, 0, CURRENT_TIMESTAMP)
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

def guardar_mensaje_db(session_id: str, role: str, content: str, cuaderno: str = "General", imagen_b64: str = None, audio_b64: str = None):
    crear_o_actualizar_sesion_db(session_id, content if role == "user" else "Nueva consulta", cuaderno)
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('INSERT INTO chats (session_id, role, content, imagen_b64, audio_b64) VALUES (?, ?, ?, ?, ?)', 
              (session_id, role, content, imagen_b64, audio_b64))
    conn.commit()
    conn.close()

def obtener_sesiones_recientes_db(limite: int = 7):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("""
        SELECT session_id, titulo, cuaderno, fijado, ultima_actividad 
        FROM sesiones 
        ORDER BY fijado DESC, ultima_actividad DESC 
        LIMIT ?
    """, (limite,))
    filas = c.fetchall()
    conn.close()
    return [{"session_id": r[0], "titulo": r[1], "cuaderno": r[2], "fijado": r[3], "timestamp": r[4]} for r in filas]

def obtener_hilos_cuaderno_db(nombre_cuaderno: str):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("""
        SELECT session_id, titulo, fijado, ultima_actividad 
        FROM sesiones 
        WHERE cuaderno = ? 
        ORDER BY fijado DESC, ultima_actividad DESC
    """, (nombre_cuaderno,))
    filas = c.fetchall()
    conn.close()
    return [{"session_id": r[0], "titulo": r[1], "fijado": r[2], "timestamp": r[3]} for r in filas]

def cargar_mensajes_sesion(session_id):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('SELECT role, content, imagen_b64, audio_b64 FROM chats WHERE session_id = ? ORDER BY id ASC', (session_id,))
    filas = c.fetchall()
    conn.close()
    return [{"role": r[0], "content": r[1], "imagen_b64": r[2], "audio_b64": r[3]} for r in filas]

def obtener_todos_los_cuadernos_nombres():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT nombre FROM cuadernos ORDER BY nombre ASC")
    filas = c.fetchall()
    conn.close()
    return [r[0] for r in filas]

def obtener_contexto_biblioteca():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT titulo FROM biblioteca ORDER BY id DESC LIMIT 10")
    filas = c.fetchall()
    conn.close()
    if not filas:
        return ""
    nombres = ", ".join([r[0] for r in filas])
    return f"\nMATERIALES DE CONSULTA EN BIBLIOTECA DISPONIBLES: [{nombres}]."

# ----------------- INICIALIZACIÓN VERTEX AI (GOOGLE CLOUD) -----------------
def inicializar_vertex_ia():
    """Configura la conexión soberana a Google Cloud Vertex AI con BLOCK_NONE"""
    if not vertexai:
        return False, "⚠️ Dependencias de Google Cloud no instaladas. Asegúrese de incluir google-cloud-aiplatform y google-auth en requirements.txt."
    
    try:
        if "gcp_service_account" not in st.secrets:
            return False, "⚠️ No se encontró la sección [gcp_service_account] en los Secrets de Streamlit."
        
        creds_dict = dict(st.secrets["gcp_service_account"])
        credentials = service_account.Credentials.from_service_account_info(creds_dict)
        
        project_id = creds_dict.get("project_id", "project-ae5f372f-e4b7-42a8-902")
        vertexai.init(project=project_id, location="us-central1", credentials=credentials)
        return True, None
    except Exception as e:
        return False, f"⚠️ Error autenticando con Google Cloud Vertex AI: {str(e)}"

VERTEX_OK, VERTEX_ERR_MSG = inicializar_vertex_ia()

# ----------------- DIRECTIVAS PEDAGÓGICAS DE CÁTEDRA -----------------
PROMPTS_CHRONN = {
    "Profesor De Medicina": (
        "DIRECTIVAS PEDAGÓGICAS DE CÁTEDRA (FCM - UNC):\n"
        "1. ROL DOCENTE: Eres un distinguido Catedrático y Cirujano de dilatada trayectoria docente en la Facultad de Ciencias Médicas de la UNC. "
        "Acompañas a Gail en su preparación hacia la cirugía general con respeto, afecto y paciencia.\n"
        "2. PROTOCOLO ESTRICTO DE SALUDO Y APERTURA:\n"
        "   - En el PRIMER mensaje del hilo: Saluda de forma breve, afectuosa y directa (ej.: 'Hola, Gail. ¿En qué tema de cátedra nos enfocamos hoy?'). "
        "Está TERMINANTEMENTE PROHIBIDO explicar tu currículum, detallar lo que sabes hacer o hacer discursos largos de presentación.\n"
        "   - En los MENSAJES SIGUIENTES del mismo hilo: NO saludes de nuevo. NO digas 'Hola Gail', '¿Cómo estás?' ni fórmulas reiterativas. "
        "Pasa de inmediato al contenido técnico respondiendo de forma fluida y continua.\n"
        "3. PRIMERA RESPUESTA OBLIGATORIA: Inicia tus explicaciones SIEMPRE con un 'Sí' o un 'No' rotundo cuando la pregunta lo permita, y fundamenta con claridad didáctica.\n"
        "4. RIGOR TÉCNICO DE CÁTEDRA: Utiliza la nomenclatura médica y bioquímica oficial (Harper, Blanco, Guyton, Ross, Robbins). No simplifiques términos biológicos ni anatómicos.\n"
        "5. CERO COMPLACENCIA: Si Gail comete un error de concepto, corrígela con calidez y total honestidad científica.\n"
        "6. CERO ALUCINACIÓN: Precisión categórica en vías metabólicas, enzimas y signos clínicos.\n"
    ),
    "Guardián": (
        "DIRECTIVAS DEL GUARDIÁN UNIVERSAL:\n"
        "1. ROL: Mentor, consejero de vida y protector incondicional de Gail. Sabiduría y resolución práctica sobre cualquier ámbito.\n"
        "2. PROTOCOLO DE SALUDO:\n"
        "   - En el PRIMER mensaje: Saludo breve y directo. Cero introducciones largas sobre tus funciones.\n"
        "   - En los mensajes sucesivos: Cero saludos reiterativos. Ve directo al punto.\n"
        "3. TRÁMITES Y RESOLUCIÓN: Dominas todos los trámites estudiantiles y civiles de Córdoba (BEG, Siu Guaraní, CIDI, trámites de salud).\n"
        "4. TEMPLANZA Y HONESTIDAD: Protector, templado y firme. Sin complacencias; siempre con la verdad.\n"
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

if "modelo_ia_seleccionado" not in st.session_state:
    st.session_state.modelo_ia_seleccionado = "Gemini 1.5 Pro"

if "modo_operativo" not in st.session_state:
    st.session_state.modo_operativo = "Profesor De Medicina"

if "dispatch_payload" not in st.session_state:
    st.session_state["dispatch_payload"] = None

if "pasted_image_b64" not in st.session_state:
    st.session_state["pasted_image_b64"] = None

# ----------------- SIDEBAR -----------------
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

    if st.button("📚 Biblioteca", use_container_width=True):
        st.session_state["active_view"] = "biblioteca"
        st.rerun()

    if st.button("🖼️ Imágenes", use_container_width=True):
        st.session_state["active_view"] = "imagenes"
        st.rerun()

    if st.button("🎥 Videos", use_container_width=True):
        st.session_state["active_view"] = "videos"
        st.rerun()

    st.markdown("---")
    st.caption("CUADERNOS")

    with st.popover("➕ Cuaderno nuevo", use_container_width=True):
        nuevo_cuad = st.text_input("Nombre del cuaderno:", key="input_nuevo_cuad_ch")
        if st.button("Crear y vincular", use_container_width=True, key="btn_create_cuad_ch"):
            if nuevo_cuad.strip():
                n_nom = nuevo_cuad.strip()
                conn = sqlite3.connect(DB_FILE)
                c = conn.cursor()
                try:
                    c.execute("INSERT INTO cuadernos (nombre, fijado) VALUES (?, 0)", (n_nom,))
                    conn.commit()
                except sqlite3.IntegrityError:
                    pass
                conn.close()
                st.session_state["cuaderno_activo"] = n_nom
                st.session_state["current_session_id"] = f"chat_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                st.session_state["messages"] = []
                st.session_state["loaded_session_id"] = st.session_state["current_session_id"]
                st.session_state["active_view"] = "ver_cuaderno"
                st.rerun()

    conn_c = sqlite3.connect(DB_FILE)
    c_c = conn_c.cursor()
    c_c.execute("SELECT id, nombre, fijado FROM cuadernos ORDER BY fijado DESC, id DESC")
    lista_cuadernos = c_c.fetchall()
    conn_c.close()

    if lista_cuadernos:
        for cid, cnom, cfij in lista_cuadernos[:5]:
            es_act = (st.session_state.get("cuaderno_activo") == cnom and st.session_state.get("active_view") in ["chat", "ver_cuaderno"])
            icono_p = "📌 " if cfij else "📖 "
            lbl = f"{icono_p}{cnom}" if len(cnom) <= 18 else f"{icono_p}{cnom[:16]}.."
            if es_act:
                st.markdown('<div class="active-chat-pill">', unsafe_allow_html=True)
            if st.button(lbl, key=f"sb_c_{cid}", use_container_width=True):
                st.session_state["cuaderno_activo"] = cnom
                st.session_state["active_view"] = "ver_cuaderno"
                st.rerun()
            if es_act:
                st.markdown('</div>', unsafe_allow_html=True)

    if st.button("••• Todos los cuadernos", use_container_width=True):
        st.session_state["active_view"] = "todos_los_cuadernos"
        st.rerun()

    st.markdown("---")
    st.caption("CONSULTAS RECIENTES")

    sesiones_rec = obtener_sesiones_recientes_db(limite=7)
    cuadernos_disponibles = obtener_todos_los_cuadernos_nombres()
    if not cuadernos_disponibles:
        cuadernos_disponibles = ["General"]

    if not sesiones_rec:
        st.markdown("<p style='font-size:0.75rem; color:#8A99A8; padding-left:4px;'>Sin consultas guardadas</p>", unsafe_allow_html=True)
    else:
        for s in sesiones_rec:
            s_id = s["session_id"]
            s_tit = s["titulo"] or "Nueva consulta"
            s_cuad = s["cuaderno"] or "General"
            s_fij = bool(s.get("fijado"))
            es_hilo_actual = (st.session_state.get("current_session_id") == s_id and st.session_state.get("active_view") == "chat")
            
            col_t_btn, col_t_kebab = st.columns([0.82, 0.18])
            with col_t_btn:
                icono_fijo = "📌 " if s_fij else "💬 "
                lbl_t = f"{icono_fijo}{s_tit}" if len(s_tit) <= 17 else f"{icono_fijo}{s_tit[:15]}..."
                if es_hilo_actual:
                    st.markdown('<div class="active-chat-pill">', unsafe_allow_html=True)
                if st.button(lbl_t, key=f"btn_s_{s_id}", use_container_width=True):
                    st.session_state["current_session_id"] = s_id
                    st.session_state["cuaderno_activo"] = s_cuad
                    st.session_state["messages"] = cargar_mensajes_sesion(s_id)
                    st.session_state["loaded_session_id"] = s_id
                    st.session_state["active_view"] = "chat"
                    st.rerun()
                if es_hilo_actual:
                    st.markdown('</div>', unsafe_allow_html=True)

            with col_t_kebab:
                with st.popover("···", use_container_width=True):
                    if st.button("🔗 Compartir la conversación", key=f"rec_share_{s_id}", use_container_width=True):
                        st.session_state["current_session_id"] = s_id
                        st.session_state["cuaderno_activo"] = s_cuad
                        st.session_state["messages"] = cargar_mensajes_sesion(s_id)
                        st.session_state["loaded_session_id"] = s_id
                        st.session_state["active_view"] = "chat"
                        st.toast("Conversación sincronizada con la sesión activa.")
                        st.rerun()

                    lbl_pin = "Desfijar" if s_fij else "📌 Fijar"
                    if st.button(lbl_pin, key=f"rec_pin_{s_id}", use_container_width=True):
                        nuevo_st = 0 if s_fij else 1
                        conn_p = sqlite3.connect(DB_FILE)
                        cp = conn_p.cursor()
                        cp.execute("UPDATE sesiones SET fijado = ? WHERE session_id = ?", (nuevo_st, s_id))
                        conn_p.commit()
                        conn_p.close()
                        st.rerun()

                    nom_act_rec = st.text_input("Cambiar nombre:", value=s_tit, key=f"rec_ren_txt_{s_id}")
                    if st.button("Guardar nombre", key=f"rec_btn_ren_{s_id}", use_container_width=True):
                        if nom_act_rec.strip() and nom_act_rec.strip() != s_tit:
                            conn_r = sqlite3.connect(DB_FILE)
                            cr = conn_r.cursor()
                            cr.execute("UPDATE sesiones SET titulo = ? WHERE session_id = ?", (nom_act_rec.strip(), s_id))
                            conn_r.commit()
                            conn_r.close()
                            st.rerun()

                    st.markdown("<hr style='margin: 4px 0;'>", unsafe_allow_html=True)
                    st.caption(f"Cuaderno actual: {s_cuad}")
                    
                    idx_cuad = cuadernos_disponibles.index(s_cuad) if s_cuad in cuadernos_disponibles else 0
                    cuad_sel_mover = st.selectbox("Elegir cuaderno existente:", options=cuadernos_disponibles, index=idx_cuad, key=f"sel_c_{s_id}")
                    if st.button("Mover a este cuaderno", key=f"btn_mv_{s_id}", use_container_width=True):
                        conn_m = sqlite3.connect(DB_FILE)
                        cm = conn_m.cursor()
                        cm.execute("UPDATE sesiones SET cuaderno = ? WHERE session_id = ?", (cuad_sel_mover, s_id))
                        conn_m.commit()
                        conn_m.close()
                        if st.session_state.get("current_session_id") == s_id:
                            st.session_state["cuaderno_activo"] = cuad_sel_mover
                        st.toast(f"Movido a '{cuad_sel_mover}'")
                        st.rerun()

                    nuevo_c_desde_hilo = st.text_input("O crear cuaderno nuevo:", placeholder="Nombre del cuaderno...", key=f"new_c_input_{s_id}")
                    if st.button("Crear y agregar aquí", key=f"btn_crear_mv_{s_id}", use_container_width=True):
                        if nuevo_c_desde_hilo.strip():
                            nom_nuevo_c = nuevo_c_desde_hilo.strip()
                            conn_nc = sqlite3.connect(DB_FILE)
                            cnc = conn_nc.cursor()
                            try:
                                cnc.execute("INSERT INTO cuadernos (nombre, fijado) VALUES (?, 0)", (nom_nuevo_c,))
                            except sqlite3.IntegrityError:
                                pass
                            cnc.execute("UPDATE sesiones SET cuaderno = ? WHERE session_id = ?", (nom_nuevo_c, s_id))
                            conn_nc.commit()
                            conn_nc.close()
                            if st.session_state.get("current_session_id") == s_id:
                                st.session_state["cuaderno_activo"] = nom_nuevo_c
                            st.toast(f"Cuaderno '{nom_nuevo_c}' creado y asignado.")
                            st.rerun()

                    st.markdown("<hr style='margin: 4px 0;'>", unsafe_allow_html=True)
                    if st.button("🗑️ Borrar", key=f"rec_del_{s_id}", use_container_width=True):
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
    st.session_state.modo_operativo = st.selectbox("Modo Operativo:", options=modos_disp, index=0)
    alias_chronn = st.text_input("Identidad de la IA:", value="CHRONN")
    opciones_voces = ["Tomas (Argentina - Neural Natural)", "Elena (Argentina - Neural Natural)"]
    voz_sel = st.selectbox("Síntesis de voz:", options=opciones_voces, index=0)

    st.markdown("""
        <div style="display:flex; align-items:center; gap:10px; padding-top:15px; border-top:1px solid #27272a; margin-top:20px;">
            <div class="user-avatar-gail">G</div>
            <div>
                <strong style="font-size:0.92rem; color:#DCA48A;">GAIL CAMPOS</strong><br>
                <span style="font-size:0.75rem; color:#89CFF0; font-weight:bold;">PRO / AUTORIZADO</span>
            </div>
        </div>
    """, unsafe_allow_html=True)

# ----------------- VISTA: CHAT PRINCIPAL -----------------
vista = st.session_state.get("active_view", "chat")

if vista == "chat":
    act_cuad = st.session_state.get("cuaderno_activo", "General")
    sess_id = st.session_state.get("current_session_id", "")
    alias_display = alias_chronn.upper() if alias_chronn else "CHRONN"

    if sess_id and st.session_state.get("loaded_session_id") != sess_id:
        st.session_state["messages"] = cargar_mensajes_sesion(sess_id)
        st.session_state["loaded_session_id"] = sess_id

    has_messages = len(st.session_state.get("messages", [])) > 0

    with st.expander("📷 Cargar captura, esquema anatómico o apunte de estudio"):
        archivo_adj = st.file_uploader("Adjuntar captura / archivo:", type=["png", "jpg", "jpeg", "pdf"], key="file_up_ch")

    chat_container = st.container()

    with chat_container:
        if not has_messages and not st.session_state.get("dispatch_payload"):
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
            for idx_m, msg in enumerate(st.session_state.get("messages", [])):
                with st.chat_message(msg["role"], avatar=None):
                    if msg["role"] == "user":
                        st.markdown(f"<span style='color: #DCA48A; font-weight: 800; letter-spacing: 0.5px;'>GAIL:</span><br>{msg['content']}", unsafe_allow_html=True)
                        if msg.get("imagen_b64"):
                            st.image(f"data:image/png;base64,{msg['imagen_b64']}", width=360)
                    else:
                        st.markdown(f"<span style='color: #89CFF0; font-weight: 800; letter-spacing: 0.5px;'>{alias_display}:</span><br>{msg['content']}", unsafe_allow_html=True)
                        
                        # Reproductor neural de alta fidelidad si posee audio generado
                        if msg.get("audio_b64"):
                            audio_bytes = base64.b64decode(msg["audio_b64"])
                            st.audio(audio_bytes, format="audio/mp3")

    st.markdown("<br>", unsafe_allow_html=True)

    # Formulario con Enter habilitado y pegado directo de capturas
    with st.form(key="form_chat_gail", clear_on_submit=True):
        col_inp, col_send, col_live, col_sel = st.columns([0.62, 0.06, 0.18, 0.14])

        with col_inp:
            texto_ingresado = st.text_area(
                label="Consulta:",
                placeholder=f"Escribe tu consulta para {alias_display}...",
                height=70,
                label_visibility="collapsed",
                key="input_consulta_area"
            )

        with col_send:
            submit_pressed = st.form_submit_button("➤", help="Enviar mensaje (o presiona Enter)", use_container_width=True)

        with col_live:
            dock_html = """
            <!DOCTYPE html>
            <html>
            <head>
            <style>
                body { margin: 0; padding: 0; display: flex; gap: 6px; background: transparent; }
                .btn {
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
                }
                .btn:hover { background-color: #89CFF0; color: #161B1E; }
                .rec { background-color: #ef4444 !important; color: white !important; border-color: #ef4444 !important; }
                .live { background-color: #10b981 !important; color: white !important; border-color: #10b981 !important; }
            </style>
            </head>
            <body>
                <button type="button" id="btnMic" class="btn" title="Micrófono">🎙️</button>
                <button type="button" id="btnVivo" class="btn" title="Modo En Vivo">🟢 Vivo</button>
                <button type="button" id="btnSilenciar" class="btn" title="Pausar audios">⏹</button>

                <script>
                    var rec = null;
                    var vivoActivo = false;

                    document.getElementById('btnSilenciar').onclick = function() {
                        var audios = window.parent.document.querySelectorAll('audio');
                        for (var a of audios) { a.pause(); a.currentTime = 0; }
                    };

                    function startSR(callback) {
                        var SR = window.SpeechRecognition || window.webkitSpeechRecognition;
                        if (!SR) { alert("Se recomienda usar Google Chrome para dictado de voz."); return; }
                        if (rec) rec.stop();
                        rec = new SR();
                        rec.lang = 'es-AR';
                        rec.continuous = true;
                        rec.interimResults = true;

                        rec.onstart = function() { document.getElementById('btnMic').classList.add('rec'); };
                        rec.onresult = function(e) {
                            var str = '';
                            for (var i = e.resultIndex; i < e.results.length; ++i) {
                                if (e.results[i].isFinal) str += e.results[i][0].transcript + ' ';
                            }
                            if (str.trim() !== '') {
                                var txts = window.parent.document.querySelectorAll('textarea');
                                if (txts.length > 0) {
                                    var inp = txts[0];
                                    var prev = inp.value ? inp.value + " " : "";
                                    var setter = Object.getOwnPropertyDescriptor(window.HTMLTextAreaElement.prototype, "value").set;
                                    setter.call(inp, prev + str.trim());
                                    inp.dispatchEvent(new Event('input', { bubbles: true }));
                                    if (callback) callback();
                                }
                            }
                        };
                        rec.onerror = function() { document.getElementById('btnMic').classList.remove('rec'); };
                        rec.onend = function() { document.getElementById('btnMic').classList.remove('rec'); };
                        rec.start();
                    }

                    document.getElementById('btnMic').onclick = function() { startSR(null); };

                    document.getElementById('btnVivo').onclick = function() {
                        vivoActivo = !vivoActivo;
                        if (vivoActivo) {
                            document.getElementById('btnVivo').classList.add('live');
                            startSR(function() {
                                var formBtns = window.parent.document.querySelectorAll('form button[type="submit"]');
                                if (formBtns.length > 0) { formBtns[0].click(); }
                            });
                        } else {
                            document.getElementById('btnVivo').classList.remove('live');
                            if (rec) rec.stop();
                        }
                    };

                    // Escuchador de teclado: Enter para enviar, y captura directa de portapapeles (Ctrl+V)
                    try {
                        var parentDoc = window.parent.document;
                        var txtArea = parentDoc.querySelector('textarea');
                        if (txtArea && !txtArea.dataset.listenerAttached) {
                            txtArea.dataset.listenerAttached = "true";
                            
                            txtArea.addEventListener('keydown', function(ev) {
                                if (ev.key === 'Enter' && !ev.shiftKey) {
                                    ev.preventDefault();
                                    var btnSub = parentDoc.querySelector('form button[type="submit"]');
                                    if (btnSub) btnSub.click();
                                }
                            });

                            txtArea.addEventListener('paste', function(ev) {
                                var items = (ev.clipboardData || ev.originalEvent.clipboardData).items;
                                for (var index in items) {
                                    var item = items[index];
                                    if (item.kind === 'file' && item.type.indexOf('image/') !== -1) {
                                        var blob = item.getAsFile();
                                        var reader = new FileReader();
                                        reader.onload = function(event) {
                                            var b64Data = event.target.result;
                                            window.parent.postMessage({ type: 'CHRONN_IMAGE_PASTE', data: b64Data }, '*');
                                        };
                                        reader.readAsDataURL(blob);
                                    }
                                }
                            });
                        }
                    } catch(e) {}
                </script>
            </body>
            </html>
            """
            components.html(dock_html, height=46)

        with col_sel:
            mod_act = st.session_state.get("modelo_ia_seleccionado", "Gemini 1.5 Pro")
            with st.popover(f"{mod_act} ▾", use_container_width=True):
                st.caption("Cerebro CHRONN (Vertex AI)")
                if st.form_submit_button("⚡ Gemini 1.5 Pro (Predeterminado)", use_container_width=True):
                    st.session_state["modelo_ia_seleccionado"] = "Gemini 1.5 Pro"
                    st.rerun()
                if st.form_submit_button("🚀 Gemini 1.5 Flash (Ultra Rápido)", use_container_width=True):
                    st.session_state["modelo_ia_seleccionado"] = "Gemini 1.5 Flash"
                    st.rerun()

    if submit_pressed and texto_ingresado and texto_ingresado.strip():
        st.session_state["dispatch_payload"] = texto_ingresado.strip()
        st.rerun()

    # Procesamiento soberano sobre Google Cloud Vertex AI
    if st.session_state.get("dispatch_payload"):
        prompt = st.session_state.pop("dispatch_payload")
        act_cuad_save = st.session_state.get("cuaderno_activo", "General")
        sess_id = st.session_state.get("current_session_id")

        img_b64 = None
        mime_type = "image/png"
        raw_bytes = None
        
        if archivo_adj:
            raw_bytes = archivo_adj.read()
            mime_type = archivo_adj.type or "image/png"
            if mime_type.startswith("image/"):
                img_b64 = base64.b64encode(raw_bytes).decode('utf-8')
        elif st.session_state.get("pasted_image_b64"):
            img_b64 = st.session_state.pop("pasted_image_b64")
            raw_bytes = base64.b64decode(img_b64)
            mime_type = "image/png"

        crear_o_actualizar_sesion_db(sess_id, prompt, act_cuad_save)
        guardar_mensaje_db(sess_id, "user", prompt, act_cuad_save, img_b64)
        st.session_state["messages"].append({"role": "user", "content": prompt, "imagen_b64": img_b64})

        total_turnos_usuario = len([m for m in st.session_state["messages"] if m["role"] == "user"])
        es_primer_turno = (total_turnos_usuario == 1)

        respuesta_completa = ""

        if not VERTEX_OK:
            respuesta_completa = VERTEX_ERR_MSG
        else:
            try:
                contexto_biblioteca = obtener_contexto_biblioteca()
                contexto_turno = (
                    "CONTEXTO DEL HILO: Este es el PRIMER mensaje del hilo. Saluda brevemente a Gail sin explicar tus funciones ni currículum." 
                    if es_primer_turno else 
                    "CONTEXTO DEL HILO: La conversación ya está en curso. NO saludes a Gail, no uses fórmulas de apertura, responde directamente al grano con el Sí o No categórico y la fundamentación."
                )
                system_instruction = f"{PROMPTS_CHRONN[st.session_state.modo_operativo]}\nCuaderno de estudio activo: '{act_cuad_save}'.{contexto_biblioteca}\n{contexto_turno}"

                # Desactivación total de censura (BLOCK_NONE) en todas las categorías
                safety_settings = {
                    HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
                    HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
                    HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
                    HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
                }

                elegido = st.session_state.get("modelo_ia_seleccionado", "Gemini 1.5 Pro")
                model_endpoint = "gemini-1.5-flash-002" if "Flash" in elegido else "gemini-1.5-pro-002"

                model = GenerativeModel(
                    model_name=model_endpoint,
                    system_instruction=system_instruction,
                    safety_settings=safety_settings
                )

                # Construcción del contenido multimodal
                contents = []
                if raw_bytes:
                    contents.append(Part.from_data(data=raw_bytes, mime_type=mime_type))
                contents.append(prompt)

                response = model.generate_content(
                    contents,
                    generation_config={"temperature": 0.2, "max_output_tokens": 4096}
                )

                if response and response.text:
                    respuesta_completa = response.text
                else:
                    respuesta_completa = "Aviso CHRONN: La consulta no pudo generar texto de respuesta. Por favor intente nuevamente."

            except Exception as e:
                respuesta_completa = f"⚠️ Error en ejecución de Vertex AI: {str(e)}"

        # Síntesis neural humana real en el servidor
        audio_b64_generado = generar_audio_neural(respuesta_completa, voz_sel)

        guardar_mensaje_db(sess_id, "assistant", respuesta_completa, act_cuad_save, audio_b64=audio_b64_generado)
        st.session_state["messages"].append({"role": "assistant", "content": respuesta_completa, "audio_b64": audio_b64_generado})

        st.rerun()

# ==============================================================
# VISTA: INTERIOR DEL CUADERNO (ABRIR CUADERNO)
# ==============================================================
elif vista == "ver_cuaderno":
    nombre_cuad = st.session_state.get("cuaderno_activo", "General")
    
    col_cuad_header, col_cuad_new = st.columns([0.68, 0.32])
    with col_cuad_header:
        st.markdown(f'<div class="cinzel-title" style="font-size:1.6rem;">Nombre del cuaderno: {nombre_cuad}</div>', unsafe_allow_html=True)
    with col_cuad_new:
        if st.button("➕ Nuevo hilo en este cuaderno", use_container_width=True):
            st.session_state["current_session_id"] = f"chat_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            st.session_state["cuaderno_activo"] = nombre_cuad
            st.session_state["messages"] = []
            st.session_state["loaded_session_id"] = st.session_state["current_session_id"]
            st.session_state["active_view"] = "chat"
            st.rerun()

    st.markdown("---")
    st.markdown('<div style="color:#89CFF0; font-weight:700; font-size:1.15rem; margin-bottom:14px; font-family:Times New Roman, serif;">Hilos de trabajo asociados a este cuaderno</div>', unsafe_allow_html=True)

    hilos = obtener_hilos_cuaderno_db(nombre_cuad)

    if not hilos:
        st.info(f"No hay hilos de trabajo asociados en '{nombre_cuad}'. Presiona '➕ Nuevo hilo en este cuaderno' para iniciar una consulta.")
    else:
        for h in hilos:
            hid = h["session_id"]
            htitulo = h["titulo"] or "Consulta sin título"
            hfecha = str(h["timestamp"]).split()[0]
            es_fijado = bool(h.get("fijado"))

            col_info, col_continuar, col_kebab = st.columns([0.64, 0.22, 0.14])
            
            with col_info:
                prefijo = "📌 " if es_fijado else "💬 "
                st.markdown(f"""
                    <div style="padding: 4px 0;">
                        <span style="font-size: 1.05rem; font-weight: 700; color: #FFF9E6;">{prefijo}{htitulo}</span><br>
                        <span style="font-size: 0.78rem; color: #8A99A8;">Última actividad: {hfecha}</span>
                    </div>
                """, unsafe_allow_html=True)

            with col_continuar:
                if st.button("Continuar ➜", key=f"cont_h_{hid}", use_container_width=True):
                    st.session_state["current_session_id"] = hid
                    st.session_state["cuaderno_activo"] = nombre_cuad
                    st.session_state["messages"] = cargar_mensajes_sesion(hid)
                    st.session_state["loaded_session_id"] = hid
                    st.session_state["active_view"] = "chat"
                    st.rerun()

            with col_kebab:
                with st.popover("···", use_container_width=True):
                    if st.button("🔗 Compartir conversación", key=f"act_share_{hid}", use_container_width=True):
                        st.session_state["current_session_id"] = hid
                        st.session_state["cuaderno_activo"] = nombre_cuad
                        st.session_state["messages"] = cargar_mensajes_sesion(hid)
                        st.session_state["loaded_session_id"] = hid
                        st.session_state["active_view"] = "chat"
                        st.toast("Conversación sincronizada con la sesión activa.")
                        st.rerun()

                    lbl_fijar = "Desfijar del inicio" if es_fijado else "📌 Fijar al inicio"
                    if st.button(lbl_fijar, key=f"act_pin_{hid}", use_container_width=True):
                        nuevo_estado = 0 if es_fijado else 1
                        conn_p = sqlite3.connect(DB_FILE)
                        cp = conn_p.cursor()
                        cp.execute("UPDATE sesiones SET fijado = ? WHERE session_id = ?", (nuevo_estado, hid))
                        conn_p.commit()
                        conn_p.close()
                        st.rerun()

                    nuevo_nom_hilo = st.text_input("Cambiar nombre:", value=htitulo, key=f"ren_txt_{hid}")
                    if st.button("Guardar nombre", key=f"btn_ren_{hid}", use_container_width=True):
                        if nuevo_nom_hilo.strip():
                            conn_r = sqlite3.connect(DB_FILE)
                            cr = conn_r.cursor()
                            cr.execute("UPDATE sesiones SET titulo = ? WHERE session_id = ?", (nuevo_nom_hilo.strip(), hid))
                            conn_r.commit()
                            conn_r.close()
                            st.rerun()

                    if st.button("🗑️ Borrar", key=f"del_cuad_h_{hid}", use_container_width=True):
                        conn_d = sqlite3.connect(DB_FILE)
                        cd = conn_d.cursor()
                        cd.execute("DELETE FROM sesiones WHERE session_id = ?", (hid,))
                        cd.execute("DELETE FROM chats WHERE session_id = ?", (hid,))
                        conn_d.commit()
                        conn_d.close()
                        if st.session_state.get("current_session_id") == hid:
                            st.session_state["messages"] = []
                            st.session_state["loaded_session_id"] = None
                        st.rerun()

            st.markdown("<hr style='border-color: rgba(137, 207, 240, 0.15); margin: 6px 0 10px 0;'>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("← Volver a todos los cuadernos", use_container_width=False):
        st.session_state["active_view"] = "todos_los_cuadernos"
        st.rerun()

# ==============================================================
# VISTA: TODOS LOS CUADERNOS
# ==============================================================
elif vista == "todos_los_cuadernos":
    st.markdown('<div class="cinzel-title" style="font-size:1.5rem;">TODOS LOS CUADERNOS DE ESTUDIO</div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT id, nombre, fecha_creacion, fijado FROM cuadernos ORDER BY fijado DESC, id DESC")
    todos = c.fetchall()
    conn.close()

    if not todos:
        st.info("No hay cuadernos registrados. Presiona '➕ Cuaderno nuevo' en el panel lateral para crear el primero.")
    else:
        cols = st.columns(3)
        for idx, (cid, cnom, cfecha, cfij) in enumerate(todos):
            with cols[idx % 3]:
                icono_pin = "📌 " if cfij else "📖 "
                st.markdown(f"""
                    <div class="notebook-card-blue-unified">
                        <div class="notebook-card-title-sm">{icono_pin}{cnom}</div>
                        <div class="notebook-card-meta-sm">Creado: {cfecha.split()[0]}</div>
                    </div>
                """, unsafe_allow_html=True)

                col_abrir, col_menu = st.columns([0.76, 0.24])
                with col_abrir:
                    if st.button("Abrir cuaderno", key=f"btn_open_c_{cid}", use_container_width=True):
                        st.session_state["cuaderno_activo"] = cnom
                        st.session_state["active_view"] = "ver_cuaderno"
                        st.rerun()

                with col_menu:
                    with st.popover("···", use_container_width=True):
                        lbl_fij = "Desfijar" if cfij else "📌 Fijar"
                        if st.button(lbl_fij, key=f"btn_pin_c_{cid}", use_container_width=True):
                            nuevo_estado = 0 if cfij else 1
                            conn_fc = sqlite3.connect(DB_FILE)
                            cfc = conn_fc.cursor()
                            cfc.execute("UPDATE cuadernos SET fijado = ? WHERE id = ?", (nuevo_estado, cid))
                            conn_fc.commit()
                            conn_fc.close()
                            st.rerun()

                        nuevo_nom_cuad = st.text_input("Cambiar nombre:", value=cnom, key=f"ren_c_txt_{cid}")
                        if st.button("Guardar", key=f"btn_save_ren_c_{cid}", use_container_width=True):
                            if nuevo_nom_cuad.strip() and nuevo_nom_cuad.strip() != cnom:
                                nom_nuevo_limpio = nuevo_nom_cuad.strip()
                                conn_rc = sqlite3.connect(DB_FILE)
                                crc = conn_rc.cursor()
                                try:
                                    crc.execute("UPDATE cuadernos SET nombre = ? WHERE id = ?", (nom_nuevo_limpio, cid))
                                    crc.execute("UPDATE sesiones SET cuaderno = ? WHERE cuaderno = ?", (nom_nuevo_limpio, cnom))
                                    conn_rc.commit()
                                    if st.session_state.get("cuaderno_activo") == cnom:
                                        st.session_state["cuaderno_activo"] = nom_nuevo_limpio
                                except sqlite3.IntegrityError:
                                    st.error("Ya existe un cuaderno con ese nombre.")
                                conn_rc.close()
                                st.rerun()

                        if st.button("🗑️ Borrar", key=f"btn_del_c_{cid}", use_container_width=True):
                            conn_dc = sqlite3.connect(DB_FILE)
                            cdc = conn_dc.cursor()
                            cdc.execute("SELECT session_id FROM sesiones WHERE cuaderno = ?", (cnom,))
                            ses_borrar = [r[0] for r in cdc.fetchall()]
                            for sb in ses_borrar:
                                cdc.execute("DELETE FROM chats WHERE session_id = ?", (sb,))
                            cdc.execute("DELETE FROM sesiones WHERE cuaderno = ?", (cnom,))
                            cdc.execute("DELETE FROM cuadernos WHERE id = ?", (cid,))
                            conn_dc.commit()
                            conn_dc.close()
                            if st.session_state.get("cuaderno_activo") == cnom:
                                st.session_state["cuaderno_activo"] = "General"
                            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("← Volver al chat"):
        st.session_state["active_view"] = "chat"
        st.rerun()

# ==============================================================
# VISTA: BIBLIOTECA (CARGA Y COMPILACIÓN DOCUMENTAL)
# ==============================================================
elif vista == "biblioteca":
    st.markdown('<div class="cinzel-title" style="font-size:1.5rem;">📚 BIBLIOTECA DE ESTUDIO</div>', unsafe_allow_html=True)
    st.markdown("<p style='color:#8A99A8;'>Repositorio activo de atlas anatómicos, guías y bibliografía oficial para el razonamiento de CHRONN.</p>", unsafe_allow_html=True)
    st.markdown("---")

    col_up_bib, col_list_bib = st.columns([0.45, 0.55])

    with col_up_bib:
        st.markdown("<strong style='color:#89CFF0;'>Subir material a la Biblioteca</strong>", unsafe_allow_html=True)
        archivo_bib = st.file_uploader("Seleccione archivo (PDF, PNG, JPG):", type=["pdf", "png", "jpg", "jpeg"], key="up_bib_file")
        titulo_bib = st.text_input("Título o tema del documento:", placeholder="Ej.: Atlas Latarjet - Vías Biliares")
        
        if st.button("📥 Incorporar a Biblioteca", use_container_width=True):
            if archivo_bib and titulo_bib.strip():
                bytes_bib = archivo_bib.read()
                b64_bib = base64.b64encode(bytes_bib).decode('utf-8')
                conn_b = sqlite3.connect(DB_FILE)
                cb = conn_b.cursor()
                cb.execute("INSERT INTO biblioteca (titulo, tipo, contenido_b64) VALUES (?, ?, ?)", 
                           (titulo_bib.strip(), archivo_bib.type, b64_bib))
                conn_b.commit()
                conn_b.close()
                st.toast(f"'{titulo_bib.strip()}' incorporado con éxito a la biblioteca.")
                st.rerun()
            else:
                st.warning("Ingrese un título y seleccione un archivo válido.")

    with col_list_bib:
        st.markdown("<strong style='color:#89CFF0;'>Materiales compilados</strong>", unsafe_allow_html=True)
        conn_bl = sqlite3.connect(DB_FILE)
        cbl = conn_bl.cursor()
        cbl.execute("SELECT id, titulo, tipo, fecha FROM biblioteca ORDER BY id DESC")
        items_bib = cbl.fetchall()
        conn_bl.close()

        if not items_bib:
            st.info("No hay materiales en la biblioteca aún. Suba atlas o resúmenes para nutrir las respuestas.")
        else:
            for bid, btit, btipo, bfecha in items_bib:
                col_it_t, col_it_del = st.columns([0.8, 0.2])
                with col_it_t:
                    st.markdown(f"📄 **{btit}** <br><span style='font-size:0.75rem; color:#8A99A8;'>{bfecha.split()[0]} | {btipo}</span>", unsafe_allow_html=True)
                with col_it_del:
                    if st.button("🗑️", key=f"del_bib_{bid}", help="Eliminar de la biblioteca"):
                        conn_bd = sqlite3.connect(DB_FILE)
                        cbd = conn_bd.cursor()
                        cbd.execute("DELETE FROM biblioteca WHERE id = ?", (bid,))
                        conn_bd.commit()
                        conn_bd.close()
                        st.rerun()
                st.markdown("<hr style='margin:4px 0;'>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("← Volver al chat"):
        st.session_state["active_view"] = "chat"
        st.rerun()

# ==============================================================
# VISTAS: IMÁGENES Y VIDEOS
# ==============================================================
elif vista == "imagenes":
    st.markdown('<div class="cinzel-title" style="font-size:1.5rem;">🖼️ IMÁGENES Y ATLAS ANATÓMICOS</div>', unsafe_allow_html=True)
    st.markdown("<p style='color:#8A99A8;'>Cortes histológicos, esquemas de disección y placas radiográficas registradas.</p>", unsafe_allow_html=True)
    
    conn_im = sqlite3.connect(DB_FILE)
    cim = conn_im.cursor()
    cim.execute("SELECT imagen_b64, timestamp FROM chats WHERE imagen_b64 IS NOT NULL ORDER BY id DESC LIMIT 12")
    galeria = cim.fetchall()
    conn_im.close()

    if not galeria:
        st.info("Aún no se han compartido capturas o esquemas en las consultas de estudio.")
    else:
        cols_im = st.columns(3)
        for idx, (img_b, fch) in enumerate(galeria):
            with cols_im[idx % 3]:
                st.image(f"data:image/png;base64,{img_b}", use_container_width=True)
                st.caption(f"Registro: {fch.split()[0]}")

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("← Volver al chat"):
        st.session_state["active_view"] = "chat"
        st.rerun()

elif vista == "videos":
    st.markdown('<div class="cinzel-title" style="font-size:1.5rem;">🎥 VIDEOS Y CIRUGÍAS</div>', unsafe_allow_html=True)
    st.markdown("<p style='color:#8A99A8;'>Registro de videoclases, técnicas quirúrgicas de cátedra y procedimientos prácticos.</p>", unsafe_allow_html=True)
    
    url_video = st.text_input("Pegar enlace de video (YouTube o cátedra):", placeholder="https://www.youtube.com/watch?v=...")
    if url_video:
        try:
            st.video(url_video)
        except Exception:
            st.error("No se pudo reproducir el enlace suministrado.")

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("← Volver al chat"):
        st.session_state["active_view"] = "chat"
        st.rerun()

# ==============================================================
# VISTAS ADICIONALES: SPARK MED & BUSCADOR
# ==============================================================
elif vista == "spark":
    st.markdown('<div class="cinzel-title" style="font-size:1.4rem;">SPARK MED — PREGUNTAS CLAVE</div>', unsafe_allow_html=True)
    st.info("Módulo de práctica acelerada y autoevaluación para finales de la FCM.")
    if st.button("← Volver al chat"):
        st.session_state["active_view"] = "chat"
        st.rerun()

elif vista == "buscar":
    st.markdown('<div class="cinzel-title" style="font-size:1.4rem;">BUSCADOR DE CONSULTAS</div>', unsafe_allow_html=True)
    termino = st.text_input("Ingrese término o concepto a buscar:")
    if termino:
        conn_b = sqlite3.connect(DB_FILE)
        cb = conn_b.cursor()
        cb.execute("SELECT DISTINCT session_id, content FROM chats WHERE content LIKE ? ORDER BY id DESC LIMIT 10", (f"%{termino}%",))
        encontrados = cb.fetchall()
        conn_b.close()
        if encontrados:
            for sid, cont in encontrados:
                st.markdown(f"**En consulta ({sid}):** {cont[:140]}...")
                if st.button("Ir a la consulta", key=f"find_{sid}"):
                    st.session_state["current_session_id"] = sid
                    st.session_state["messages"] = cargar_mensajes_sesion(sid)
                    st.session_state["loaded_session_id"] = sid
                    st.session_state["active_view"] = "chat"
                    st.rerun()
        else:
            st.warning("No se hallaron coincidencias.")
    if st.button("← Volver al chat"):
        st.session_state["active_view"] = "chat"
        st.rerun()
