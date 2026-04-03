import os
import streamlit as st
from google import genai
from google.genai import types

# -------------------------------------------------
# CONFIGURACION GENERAL
# -------------------------------------------------
st.set_page_config(
    page_title="Cerebrito IA | Samudev",
    page_icon="🧠",
    layout="wide"
)

DEFAULT_MODEL = "gemini-2.5-flash"

SYSTEM_PROMPT = """
Eres Cerebrito IA, un tutor inteligente creado por Samudev.

Tu estilo:
- Explica de forma clara, breve, profesional y atractiva.
- Ayuda a estudiantes de 11 a 40 años.
- Usa ejemplos faciles de recordar y a veces divertidos.
- Si el tema es matematicas, explica paso a paso.
- Si el usuario pide resumen, hazlo corto pero util.
- Si el usuario pide profundidad, explica mejor sin volverte confuso.
- Habla principalmente en español.
- Usa emojis con moderacion.
- No inventes datos.
- Si algo no esta claro, dilo con honestidad.
"""

# -------------------------------------------------
# ESTILOS Y UI
# -------------------------------------------------
def inject_ui():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Outfit', sans-serif;
    }

    [data-testid="stAppViewContainer"] {
        background:
            radial-gradient(circle at top left, rgba(106, 17, 203, 0.22), transparent 30%),
            radial-gradient(circle at top right, rgba(37, 117, 252, 0.18), transparent 30%),
            linear-gradient(180deg, #020308 0%, #050816 45%, #070b1f 100%);
        color: #ffffff;
        overflow: hidden;
    }

    .stApp {
        background: transparent;
    }

    #galaxy {
        position: fixed;
        inset: 0;
        width: 100vw;
        height: 100vh;
        z-index: -2;
        pointer-events: none;
    }

    .hero {
        text-align: center;
        padding: 1rem 0 1.5rem 0;
        animation: fadeUp 0.8s ease-out;
    }

    .hero h1 {
        font-size: 3rem;
        margin-bottom: 0.2rem;
        background: linear-gradient(90deg, #9b5cff, #48d8ff, #b2f1ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .hero p {
        color: #d3dbff;
        margin-top: 0;
        font-size: 1rem;
    }

    .brand {
        color: #48d8ff !important;
        text-decoration: none;
        font-weight: 700;
    }

    .glass-box {
        background: rgba(255,255,255,0.05);
        border: 1px solid rgba(255,255,255,0.10);
        border-radius: 24px;
        padding: 1rem;
        backdrop-filter: blur(14px);
        box-shadow: 0 8px 30px rgba(0,0,0,0.25);
    }

    div.stChatMessage {
        background: rgba(255, 255, 255, 0.045) !important;
        border: 1px solid rgba(255, 255, 255, 0.10) !important;
        backdrop-filter: blur(14px);
        border-radius: 22px !important;
        margin-bottom: 14px !important;
        animation: fadeUp 0.35s ease-out;
    }

    .stButton > button {
        background: linear-gradient(90deg, #7b2ff7, #38bdf8) !important;
        color: white !important;
        border: none !important;
        border-radius: 14px !important;
        font-weight: 700 !important;
        transition: all 0.25s ease !important;
    }

    .stButton > button:hover {
        transform: translateY(-2px) scale(1.01);
        box-shadow: 0 10px 24px rgba(56, 189, 248, 0.25);
    }

    [data-testid="stSidebar"] {
        background: rgba(7, 11, 31, 0.88);
        border-right: 1px solid rgba(255,255,255,0.08);
    }

    .small-note {
        color: #bfc7ea;
        font-size: 0.92rem;
    }

    @keyframes fadeUp {
        from {
            opacity: 0;
            transform: translateY(14px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    </style>

    <canvas id="galaxy"></canvas>

    <script>
    consGEMINI_API_KEY=tu_clave existing = window.__cerebritoGalaxyInitialized;
    if (!existing) {
        window.__cerebritoGalaxyInitialized = true;

        const canvas = document.getElementById('galaxy');
        const ctx = canvas.getContext('2d');

        let w = canvas.width = window.innerWidth;
        let h = canvas.height = window.innerHeight;

        const stars = Array.from({ length: 180 }, () => ({
            x: Math.random() * w,
            y: Math.random() * h,
            z: Math.random() * 0.8 + 0.2,
            r: Math.random() * 1.8 + 0.2,
            dx: (Math.random() - 0.5) * 0.08,
            dy: Math.random() * 0.18 + 0.02
        }));

        const nebulae = Array.from({ length: 4 }, () => ({
            x: Math.random() * w,
            y: Math.random() * h,
            radius: Math.random() * 180 + 140,
            alpha: Math.random() * 0.08 + 0.03
        }));

        function resize() {
            w = canvas.width = window.innerWidth;
            h = canvas.height = window.innerHeight;
        }

        window.addEventListener('resize', resize);

        function drawNebulae(time) {
            nebulae.forEach((n, i) => {
                const pulse = Math.sin(time * 0.0003 + i) * 25;
                const gradient = ctx.createRadialGradient(
                    n.x, n.y, 0,
                    n.x, n.y, n.radius + pulse
                );
                gradient.addColorStop(0, `rgba(120, 80, 255, ${n.alpha})`);
                gradient.addColorStop(0.5, `rgba(0, 212, 255, ${n.alpha * 0.6})`);
                gradient.addColorStop(1, 'rgba(0, 0, 0, 0)');

                ctx.fillStyle = gradient;
                ctx.beginPath();
                ctx.arc(n.x, n.y, n.radius + pulse, 0, Math.PI * 2);
                ctx.fill();
            });
        }

        function drawStars() {
            stars.forEach(s => {
                ctx.beginPath();
                ctx.fillStyle = `rgba(255,255,255,${0.55 + s.z * 0.45})`;
                ctx.arc(s.x, s.y, s.r * s.z, 0, Math.PI * 2);
                ctx.fill();

                s.x += s.dx;
                s.y += s.dy * s.z;

                if (s.y > h) s.y = -10;
                if (s.x > w) s.x = 0;
                if (s.x < 0) s.x = w;
            });
        }

        function draw(time = 0) {
            ctx.clearRect(0, 0, w, h);
            drawNebulae(time);
            drawStars();
            requestAnimationFrame(draw);
        }

        draw();
    }
    </script>
    """, unsafe_allow_html=True)


# -------------------------------------------------
# CLIENTE GEMINI
# -------------------------------------------------
@st.cache_resource
def get_client():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError(
            "No se encontro la variable de entorno GEMINI_API_KEY. "
            "Configúrala antes de ejecutar la app."
        )
    return genai.Client(api_key=api_key)


def build_contents(history, user_input):
    """
    Convierte el historial de Streamlit al formato simple esperado por Gemini.
    """
    contents = []

    for msg in history:
        role = "model" if msg["role"] == "assistant" else "user"
        contents.append({
            "role": role,
            "parts": [{"text": msg["content"]}]
        })

    contents.append({
        "role": "user",
        "parts": [{"text": user_input}]
    })

    return contents


def get_cerebrito_response(user_input, history, model_name):
    try:
        client = get_client()

        contents = build_contents(history, user_input)

        response = client.models.generate_content(
            model=model_name,
            contents=contents,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_PROMPT,
                temperature=0.7,
                top_p=0.9,
                max_output_tokens=900
            )
        )

        text = getattr(response, "text", None)
        if text and text.strip():
            return text.strip()

        return "⚠️ El modelo respondió, pero no devolvió texto legible."

    except Exception as e:
        return f"❌ Error: {e}"


# -------------------------------------------------
# APP
# -------------------------------------------------
def main():
    inject_ui()

    st.markdown("""
    <div class="hero">
        <h1>🧠 Cerebrito IA</h1>
        <p>
            Aprende más fácil, recuerda mejor y estudia con estilo galáctico ✨<br>
            By <a href="https://samudevcol.online" target="_blank" class="brand">Samudev</a>
        </p>
    </div>
    """, unsafe_allow_html=True)

    if "messages" not in st.session_state:
        st.session_state.messages = []

    if "selected_model" not in st.session_state:
        st.session_state.selected_model = DEFAULT_MODEL

    with st.sidebar:
        st.title("⚙️ Panel de Control")
        st.markdown('<div class="small-note">Configura tu experiencia de estudio.</div>', unsafe_allow_html=True)

        st.session_state.selected_model = st.selectbox(
            "Modelo Gemini",
            options=[
                "gemini-2.5-flash",
                "gemini-2.5-flash-lite",
                "gemini-3-flash-preview"
            ],
            index=0
        )

        tone = st.selectbox(
            "Estilo de respuesta",
            options=["Equilibrado", "Más corto", "Más explicativo"]
        )

        if st.button("🗑️ Limpiar chat", use_container_width=True):
            st.session_state.messages = []
            st.rerun()

        st.markdown("---")
        st.markdown(
            """
            **Tip:** Haz tu pregunta clara y directa 🧠✨ así Cerebrito te dará una respuesta más top :

            `BY: **TECNOLAB** `
            """
        )

    # Ajuste ligero del prompt según el modo elegido
    extra_instruction = ""
    if tone == "Más corto":
        extra_instruction = "\nResponde más breve de lo normal."
    elif tone == "Más explicativo":
        extra_instruction = "\nExplica con más detalle y con pasos más claros."

    global SYSTEM_PROMPT
    SYSTEM_PROMPT = SYSTEM_PROMPT.split("\nResponde más breve de lo normal.")[0].split("\nExplica con más detalle y con pasos más claros.")[0]
    SYSTEM_PROMPT = SYSTEM_PROMPT + extra_instruction

    chat_container = st.container()

    with chat_container:
        for message in st.session_state.messages:
            avatar = "🧑‍🎓" if message["role"] == "user" else "🧠"
            with st.chat_message(message["role"], avatar=avatar):
                st.markdown(message["content"])

    prompt = st.chat_input("Pregúntale algo a Cerebrito...")

    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user", avatar="🧑‍🎓"):
            st.markdown(prompt)

        with st.chat_message("assistant", avatar="🧠"):
            with st.spinner("Cerebrito está pensando..."):
                answer = get_cerebrito_response(
                    user_input=prompt,
                    history=st.session_state.messages[:-1],
                    model_name=st.session_state.selected_model
                )
                st.markdown(answer)

        st.session_state.messages.append({"role": "assistant", "content": answer})


if __name__ == "__main__":
    main()