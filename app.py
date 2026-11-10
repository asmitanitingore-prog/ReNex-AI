import os
import requests
import streamlit as st
from dotenv import load_dotenv

load_dotenv()
st.set_page_config(page_title="ReNex | Intelligent Circularity", page_icon="♻", layout="wide", initial_sidebar_state="expanded")

API_URL = os.getenv("NUGEN_API_URL", "https://api.nugen.in/api/v3/inference/chat/completions")
API_KEY = os.getenv("NUGEN_API_KEY", "")
MODEL_ID = os.getenv("NUGEN_MODEL_ID", "")

SYSTEM_PROMPT = """
You are ReNex, an AI-powered electronics circularity and second-life decision-support assistant.
Help users decide between continued use, repair, refurbishment, component recovery and responsible recycling.
Do not recommend recycling merely because a device is old. A short battery runtime alone does not prove danger. If a battery is swollen, leaking, unusually hot, smoking, sparking, smells burnt or visibly damaged, advise stopping use and charging, do not open or handle it, and seek qualified help; move away and contact emergency services for active fire/smoke.
Recommend repair first when the issue may be limited or replaceable and no serious safety concern is reported. Recommend refurbishment when multiple upgrades/repairs may be worthwhile and the device remains viable. Never assume RAM/SSD/battery compatibility without exact model verification. Recommend recycling/component recovery only when unsafe, impractical, majorly failed, or uneconomical after an actual quote. Never invent prices, recycler locations, laws, carbon savings, measured impact, certifications or compatibility. Do not claim physical inspection or diagnosis.
Always give a preliminary recommendation before questions. Explain why, practical next steps, relevant safety/data precautions, and alternatives. Ask at most two useful questions. Keep the answer clear and concise.
Before resale/donation/recycling, advise backup, account sign-out, SIM/memory-card removal where relevant and secure data erasure. Never instruct users to dismantle, puncture, bend, crush, heat or repair lithium-ion cells.
"""

# ---------- PREMIUM VISUAL SYSTEM ----------
st.markdown(r"""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@400;500;600;700;800&display=swap');
:root{--ink:#102c22;--muted:#64766d;--green:#087a55;--green2:#15966b;--deep:#092f24;--mint:#e5f2e9;--paper:#f5f6f0;--line:#dce4dc;--white:#fffefa;}
html,body,[class*="css"]{font-family:'DM Sans',sans-serif!important;color:var(--ink)}
.stApp{background:var(--paper)}
[data-testid="stHeader"]{background:rgba(245,246,240,.92);height:2.7rem}
[data-testid="stToolbar"]{right:1rem}
.block-container{max-width:1600px;padding:1.55rem 2.4rem 3.4rem}
h1,h2,h3,h4{font-family:'Manrope',sans-serif!important;color:var(--ink)!important;letter-spacing:-.045em}
h1{font-size:2.8rem!important;line-height:1.08!important;font-weight:700!important}
h2{font-size:1.85rem!important;font-weight:700!important}
h3{font-size:1.15rem!important;font-weight:700!important}
p,li{color:#53675d;line-height:1.65}
small,.stCaption{color:#78877e!important}
/* sidebar */
[data-testid="stSidebar"]{background:linear-gradient(180deg,#fbfbf6 0%,#f2f4ec 100%);border-right:1px solid #dce3d9;min-width:270px!important;max-width:270px!important}
[data-testid="stSidebar"]>div:first-child{padding:1.45rem 1rem 1.4rem}
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p{color:#66776d}
[data-testid="stSidebar"] hr{border-color:#dce4db;margin:1.15rem 0}
.brand-wrap{display:flex;align-items:center;gap:12px;padding:.3rem .35rem 1.1rem}
.brand-symbol{width:46px;height:46px;border-radius:15px;background:linear-gradient(145deg,#0c5039,#138b60);display:flex;align-items:center;justify-content:center;color:#fff;font:800 24px Manrope;box-shadow:0 8px 20px #0c50392a}
.brand-title{font:800 1.55rem Manrope;color:#102c22;letter-spacing:-.06em}
.brand-subtitle{font-size:.65rem;letter-spacing:.14em;text-transform:uppercase;color:#7b8b80;margin-top:1px}
.nav-label{font-size:.65rem;font-weight:800;letter-spacing:.18em;text-transform:uppercase;color:#8b9a8e;padding:.25rem .6rem .65rem}
[data-testid="stSidebar"] .stRadio>label{display:none}
[data-testid="stSidebar"] .stRadio [role="radiogroup"]{gap:.34rem}
[data-testid="stSidebar"] .stRadio [role="radiogroup"] label{display:flex;align-items:center;padding:.78rem .8rem;border:1px solid transparent;border-radius:13px;transition:all .18s ease;min-height:46px}
[data-testid="stSidebar"] .stRadio [role="radiogroup"] label:hover{background:#eaf1e9;border-color:#dce7dc}
[data-testid="stSidebar"] .stRadio [role="radiogroup"] label:has(input:checked){background:linear-gradient(100deg,#e1efe4,#edf5ed);border-color:#c8ddce;box-shadow:inset 3px 0 0 #13865d}
[data-testid="stSidebar"] .stRadio [role="radiogroup"] label p{font-size:.9rem;font-weight:600;color:#294237!important;margin:0!important}
[data-testid="stSidebar"] .stRadio [role="radiogroup"] label>div:first-child{display:none}
.sidebar-bottom{margin-top:2.5rem;padding:.95rem;border:1px solid #d9e4d9;border-radius:16px;background:#fffefa}
.live-dot{display:inline-block;width:8px;height:8px;border-radius:50%;background:#19a66e;box-shadow:0 0 0 4px #19a66e1d;margin-right:8px}
.sidebar-foot{font-size:.72rem;color:#7c8b80;margin-top:.7rem}
/* surfaces */
.eyebrow{font-size:.68rem;font-weight:800;letter-spacing:.2em;text-transform:uppercase;color:#18835e}
.hero{position:relative;overflow:hidden;border:1px solid #d6e1d7;border-radius:25px;background:linear-gradient(105deg,#fdfdf8 0%,#edf3e9 58%,#dfeee3 100%);padding:2.9rem 3rem;min-height:310px;margin:.2rem 0 1.45rem;box-shadow:0 14px 35px #183c2810}
.hero:after{content:'✳';position:absolute;right:5%;top:-68px;font-size:23rem;line-height:1;color:#0c6d4b0b;transform:rotate(14deg)}
.hero-copy{position:relative;z-index:2;max-width:720px}
.hero h1{font-size:3.2rem!important;max-width:720px;margin:.85rem 0 .85rem}
.hero p{font-size:1.04rem;max-width:640px;margin-bottom:1.3rem;color:#53685d}
.hero-art{position:absolute;right:3.5%;top:8%;width:32%;height:85%;display:flex;align-items:center;justify-content:center;z-index:1}
.hero-art svg{width:100%;height:100%;max-height:270px}
.pill{display:inline-flex;align-items:center;padding:.4rem .75rem;border:1px solid #cbded0;border-radius:99px;background:#ffffffa8;color:#315c47;font-size:.75rem;font-weight:600;margin-right:.4rem}
.section-head{display:flex;align-items:center;justify-content:space-between;margin:1.6rem 0 .8rem}
.section-kicker{font-size:.67rem;letter-spacing:.19em;font-weight:800;color:#16835c;text-transform:uppercase;margin-bottom:.35rem}
.panel{background:var(--white);border:1px solid var(--line);border-radius:19px;padding:1.25rem 1.35rem;box-shadow:0 7px 22px #183c2808;height:100%}
.panel h3{margin:.35rem 0 .45rem}
.panel p{font-size:.88rem;margin:0;color:#65776c}
.panel-icon{width:43px;height:43px;border-radius:13px;background:#e8f2e8;color:#126b4a;display:flex;align-items:center;justify-content:center;font-size:1.3rem}
.workflow{display:flex;gap:.7rem;align-items:stretch}
.workflow-step{flex:1;background:#fffefa;border:1px solid #dce4dc;border-radius:15px;padding:1rem;min-height:105px}
.workflow-step.active{background:#103c2c;color:#fff;border-color:#103c2c;box-shadow:0 10px 22px #0b38261c}
.workflow-step.active .wf-num,.workflow-step.active .wf-desc{color:#c6e2d0}
.wf-num{font-size:.67rem;font-weight:800;letter-spacing:.14em;color:#14805a}
.wf-title{font:700 1rem Manrope;margin:.35rem 0;color:inherit}
.wf-desc{font-size:.77rem;color:#74847a;line-height:1.45}
.stat-card{background:#fffefa;border:1px solid #dce4dc;border-radius:16px;padding:1rem 1.1rem;min-height:95px}
.stat-label{font-size:.76rem;color:#6c7d72}.stat-value{font:700 1.45rem Manrope;color:#123d2d;margin-top:.25rem}.stat-note{font-size:.68rem;color:#8b988f}
/* buttons / inputs */
div.stButton>button,div.stFormSubmitButton>button{border-radius:12px!important;min-height:2.9rem;padding:.65rem 1.1rem;font-weight:700!important;border:1px solid #0e7652!important;background:linear-gradient(135deg,#0b6547,#12865e)!important;color:#fff!important;box-shadow:0 7px 18px #0a68451c;transition:all .18s ease}
div.stButton>button:hover,div.stFormSubmitButton>button:hover{transform:translateY(-2px);box-shadow:0 11px 22px #0a68452c;background:linear-gradient(135deg,#084d37,#0b7450)!important}
div.stButton>button p,div.stFormSubmitButton>button p{color:#fff!important;font-weight:700!important}
[data-testid="stForm"]{background:#fffefa;border:1px solid #dce4dc;border-radius:20px;padding:1.45rem 1.55rem;box-shadow:0 8px 25px #183c2808}
[data-testid="stTextInput"] input,[data-testid="stTextArea"] textarea,[data-testid="stSelectbox"] div[data-baseweb="select"]>div{background:#fcfdf9;border:1px solid #d5e0d6;border-radius:11px;color:#17382b}
[data-testid="stTextInput"] input:focus,[data-testid="stTextArea"] textarea:focus{border-color:#16835c;box-shadow:0 0 0 2px #16835c19}
[data-testid="stChatMessage"]{background:#fffefa;border:1px solid #dce4dc;border-radius:17px;padding:.8rem 1rem}
[data-testid="stAlert"]{border-radius:14px}
.stTabs [data-baseweb="tab"]{font-weight:700}
.result-banner{background:linear-gradient(110deg,#e4f1e6,#f7f8f1);border:1px solid #cddfd0;border-radius:18px;padding:1.25rem 1.4rem;margin:.7rem 0 1rem}
.result-label{font-size:.65rem;letter-spacing:.16em;font-weight:800;color:#16835c;text-transform:uppercase}
.result-title{font:700 1.45rem Manrope;color:#123d2d;margin:.35rem 0}
.result-copy{font-size:.88rem;color:#5f7467}
.arch-node{background:#fffefa;border:1px solid #d7e2d8;border-radius:15px;padding:1rem;text-align:center;min-height:100px}
.arch-node strong{display:block;color:#123d2d;font:700 1rem Manrope;margin:.3rem 0}
.arch-node span{font-size:.76rem;color:#6f8075}
.guide-card{background:#fffefa;border:1px solid #dce4dc;border-radius:17px;padding:1.15rem;min-height:150px}
.guide-icon{font-size:1.35rem;color:#13805a}
footer{visibility:hidden}
@media(max-width:1050px){.block-container{padding:1.2rem}.hero{padding:2rem}.hero h1{font-size:2.35rem!important}.hero-art{opacity:.2;width:45%}.workflow{flex-wrap:wrap}.workflow-step{min-width:42%}}
</style>
""", unsafe_allow_html=True)

st.markdown(r"""
<style>
:root{--rx-ink:#10281f;--rx-muted:#687a70;--rx-green:#087a53;--rx-emerald:#12a875;--rx-deep:#092d22;--rx-ivory:#f7f7f1;--rx-line:#dce5dc;--rx-card:#fffefa}
.stApp{background:radial-gradient(ellipse at 82% 0%,rgba(204,229,211,.34),transparent 34%),linear-gradient(180deg,#f8f8f3 0%,#f2f5ef 100%)!important}
.block-container{max-width:1660px!important;padding:1.35rem 2.65rem 3.5rem!important}
[data-testid="stHeader"]{background:rgba(248,248,243,.88)!important;backdrop-filter:blur(18px)}
[data-testid="stSidebar"]{background:linear-gradient(180deg,#fbfcf7 0%,#f1f5ed 100%)!important;border-right:1px solid #dce6dc!important;min-width:286px!important;max-width:286px!important}
[data-testid="stSidebar"]>div:first-child{padding:1.55rem 1.1rem 1.35rem!important}
.brand-wrap{padding:.45rem .45rem 1.5rem!important;gap:13px!important;border-bottom:1px solid #dfe7df;margin-bottom:1.35rem}
.brand-symbol{width:50px!important;height:50px!important;border-radius:17px!important;background:linear-gradient(145deg,#0b3b2b,#11966a)!important;box-shadow:0 10px 24px rgba(8,91,62,.22),inset 0 1px 0 rgba(255,255,255,.24)!important;font-size:25px!important}
.brand-title{font-size:1.68rem!important;letter-spacing:-.07em!important}
.brand-subtitle{font-size:.61rem!important;letter-spacing:.17em!important;color:#71857a!important}
.nav-label{padding:.35rem .65rem .75rem!important;font-size:.62rem!important;letter-spacing:.2em!important;color:#8a9a8e!important}
[data-testid="stSidebar"] .stRadio [role="radiogroup"]{gap:.42rem!important}
[data-testid="stSidebar"] .stRadio [role="radiogroup"] label{min-height:51px!important;padding:.78rem .85rem!important;border-radius:15px!important;border:1px solid transparent!important;transition:all .2s ease!important}
[data-testid="stSidebar"] .stRadio [role="radiogroup"] label:hover{background:#edf4ed!important;border-color:#dce8dd!important;transform:translateX(2px)}
[data-testid="stSidebar"] .stRadio [role="radiogroup"] label:has(input:checked){background:linear-gradient(105deg,#e0efe5,#f0f6ef)!important;border-color:#c8dfce!important;box-shadow:inset 3px 0 0 #10875d,0 5px 16px rgba(22,77,48,.055)!important}
[data-testid="stSidebar"] .stRadio [role="radiogroup"] label p{color:#244334!important;font-size:.89rem!important;font-weight:650!important;letter-spacing:-.01em}
.sidebar-bottom{margin-top:2.8rem!important;padding:1.05rem!important;border-radius:18px!important;background:linear-gradient(145deg,#fffefa,#edf5ed)!important;border:1px solid #d8e5d9!important;box-shadow:0 9px 24px rgba(20,61,39,.06)!important}
.sidebar-foot{font-size:.68rem!important;letter-spacing:.02em!important;color:#87958b!important}
.hero{border:1px solid #d6e4d8!important;border-radius:28px!important;background:linear-gradient(112deg,#fffefa 0%,#f1f6ee 50%,#dceee2 100%)!important;padding:3.15rem 3.2rem!important;min-height:350px!important;box-shadow:0 22px 55px rgba(17,61,38,.085),inset 0 1px 0 rgba(255,255,255,.9)!important}
.hero:before{content:"";position:absolute;inset:0;pointer-events:none;background:linear-gradient(115deg,transparent 35%,rgba(255,255,255,.38) 68%,transparent 100%)}
.hero:after{right:3%;top:-95px;font-size:26rem!important;color:#0b6c4a0a!important}
.hero h1{font-size:3.45rem!important;line-height:1.04!important;max-width:700px!important;letter-spacing:-.065em!important}
.hero p{font-size:1.04rem!important;line-height:1.75!important;color:#5b7064!important;max-width:610px!important}
.eyebrow,.section-kicker{letter-spacing:.2em!important}
.pill{padding:.48rem .85rem!important;background:rgba(255,255,255,.72)!important;border-color:#d3e2d5!important;box-shadow:0 3px 10px rgba(23,65,40,.035)}
.panel,.guide-card,.stat-card,.workflow-step,.arch-node{border-radius:21px!important;border-color:#dce6dc!important;box-shadow:0 10px 28px rgba(18,57,36,.045)!important;transition:transform .2s ease,box-shadow .2s ease,border-color .2s ease}
.panel:hover,.guide-card:hover,.stat-card:hover{transform:translateY(-3px);box-shadow:0 16px 34px rgba(18,57,36,.085)!important;border-color:#c8ddce!important}
.panel{padding:1.45rem 1.5rem!important}
.panel-icon{width:47px!important;height:47px!important;border-radius:15px!important;background:linear-gradient(145deg,#e5f3e8,#d6eadb)!important}
.workflow-step{padding:1.15rem!important;min-height:118px!important}
.workflow-step.active{background:linear-gradient(145deg,#0b3829,#145c41)!important}
.stat-card{padding:1.2rem 1.3rem!important}
div.stButton>button,div.stFormSubmitButton>button{min-height:3.05rem!important;border-radius:14px!important;background:linear-gradient(120deg,#0a6547,#11966a)!important;border:1px solid #0a7652!important;box-shadow:0 9px 20px rgba(9,105,71,.17)!important;letter-spacing:.005em!important}
div.stButton>button:hover,div.stFormSubmitButton>button:hover{transform:translateY(-2px)!important;filter:brightness(1.04);box-shadow:0 14px 27px rgba(9,105,71,.23)!important}
[data-testid="stForm"]{border-radius:23px!important;padding:1.7rem 1.8rem!important;box-shadow:0 14px 36px rgba(18,57,36,.055)!important}
[data-testid="stTextInput"] input,[data-testid="stTextArea"] textarea,[data-testid="stSelectbox"] div[data-baseweb="select"]>div{min-height:2.85rem!important;border-radius:12px!important;background:#fdfefa!important}
[data-testid="stChatMessage"]{border-radius:19px!important;box-shadow:0 6px 18px rgba(18,57,36,.035)!important}
.result-banner{border-radius:22px!important;padding:1.5rem 1.65rem!important;box-shadow:0 10px 25px rgba(18,57,36,.05)}
.arch-node{padding:1.3rem!important;min-height:120px!important}
.stTabs [data-baseweb="tab"]{padding:.8rem 1rem!important}
hr{border-color:#e0e8df!important}
@media(max-width:1100px){.block-container{padding:1rem 1.2rem 2.5rem!important}.hero{padding:2rem!important}.hero h1{font-size:2.55rem!important}}
</style>
""", unsafe_allow_html=True)


def ask_nugen(prompt, history=None):
    if not API_KEY or not MODEL_ID:
        return None, "Nugen setup is incomplete. Check the API key and deployed model ID in your local .env file.", None
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    if history:
        messages.extend({"role": m["role"], "content": m["content"]} for m in history if m.get("role") in ("user", "assistant"))
    else:
        messages.append({"role": "user", "content": prompt})
    payload = {"model": MODEL_ID, "messages": messages, "max_tokens": 900, "temperature": 0.2, "stream": False}
    try:
        r = requests.post(API_URL, headers={"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}, json=payload, timeout=100)
        if r.status_code == 401: return None, "401: Nugen rejected the API key. Check your local .env configuration.", None
        if r.status_code == 403: return None, "403: The API key may not have access to this deployed model.", None
        if r.status_code == 404: return None, "404: Check the deployed model ID and API endpoint.", None
        if not r.ok: return None, f"Nugen API error {r.status_code}: {r.text[:350]}", None
        data = r.json()
        answer = data.get("choices", [{}])[0].get("message", {}).get("content")
        if not answer: return None, "Nugen returned an empty or unexpected response.", None
        return answer, None, data.get("confidence_score")
    except requests.Timeout: return None, "Nugen request timed out. Try again.", None
    except requests.RequestException as e: return None, f"Network error: {e}", None
    except (ValueError, KeyError, IndexError, TypeError): return None, "Could not interpret the Nugen response.", None


def render_answer(answer, confidence):
    st.markdown(answer)
    if confidence is not None:
        st.caption(f"Nugen confidence indicator: {confidence} · This is a model-provided indicator, not a verified accuracy score.")
    st.caption("AI decision support only — not a physical inspection or certified technical diagnosis. Confirm repair and safety decisions with a qualified professional.")


def go(page):
    st.session_state["nav_page"] = page
    st.rerun()

# ---------- SIDEBAR ----------
nav = {
    "◫   Overview": "Overview",
    "▣   Device assessment": "Assess a device",
    "✧   Ask ReNex AI": "Ask ReNex",
    "↻   Circularity guide": "Circularity Guide",
    "⌘   Technology & architecture": "Technology",
}
with st.sidebar:
    st.markdown("""<div class="brand-wrap"><div class="brand-symbol">R</div><div><div class="brand-title">ReNex</div><div class="brand-subtitle">Intelligent circularity</div></div></div>""", unsafe_allow_html=True)
    st.markdown('<div class="nav-label">YOUR WORKSPACE</div>', unsafe_allow_html=True)
    default_page = st.session_state.pop("nav_page", "Overview")
    labels = list(nav.keys())
    default_label = next((k for k,v in nav.items() if v == default_page), labels[0])
    choice = st.radio("Navigation", labels, index=labels.index(default_label), label_visibility="collapsed")
    page = nav[choice]
    st.markdown("<div style='height:1.1rem'></div>", unsafe_allow_html=True)
    st.markdown(f"""<div class="sidebar-bottom"><div style="font-size:.65rem;letter-spacing:.15em;font-weight:800;color:#87968b">AI ENGINE</div><div style="margin-top:.55rem;font-weight:700;color:#193b2c"><span class="live-dot"></span>NUGEN { 'CONNECTED' if API_KEY and MODEL_ID else 'SETUP REQUIRED' }</div><div style="font-size:.76rem;color:#718176;margin-top:.25rem">Llama 3.2 · 3B Inference</div></div><div class="sidebar-foot">ReNex · Electronics second-life intelligence</div>""", unsafe_allow_html=True)

# ---------- OVERVIEW ----------
if page == "Overview":
    st.markdown("""<div class="hero"><div class="hero-copy"><div class="eyebrow">SMARTER ELECTRONICS · LESS WASTE</div><h1>Intelligent circularity<br>for electronics.</h1><p>Turn device condition into a clearer next step. ReNex helps explore repair, reuse, refurbishment, component recovery and responsible recycling.</p><span class="pill">✦ AI-assisted assessment</span><span class="pill">↻ Repair-first thinking</span><span class="pill">♧ Circular decisions</span></div><div class="hero-art"><svg viewBox="0 0 420 300" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M206 248C133 210 85 141 117 82C146 28 224 31 250 79C284 16 357 20 365 84C373 147 300 220 206 248Z" fill="#B9D9C0" fill-opacity=".42" stroke="#4D9870" stroke-width="2"/><path d="M205 247C220 173 239 111 344 42M207 245C179 179 149 122 119 83M207 245C218 196 250 153 326 103" stroke="#347D58" stroke-width="2"/><path d="M161 116L193 93L225 116V151L193 174L161 151V116Z" stroke="#0F7653" stroke-width="2"/><path d="M193 93V174M161 116L225 151M225 116L161 151" stroke="#0F7653" stroke-width="1.5"/><circle cx="290" cy="78" r="7" fill="#15966B"/><circle cx="108" cy="175" r="6" fill="#15966B"/><circle cx="330" cy="177" r="5" fill="#15966B"/><path d="M70 222C109 252 149 267 204 274C266 280 331 259 367 223" stroke="#75B58A" stroke-width="2" stroke-dasharray="5 7"/></svg></div></div>""", unsafe_allow_html=True)
    st.markdown('<div class="section-kicker">THE RENEX WORKFLOW</div>', unsafe_allow_html=True)
    st.markdown("## From device problem to informed decision")
    steps = [("01","IDENTIFY","Describe the device and its symptoms."),("02","ASSESS","Understand condition, risks and constraints."),("03","COMPARE","Explore practical second-life pathways."),("04","DECIDE","Choose a responsible next action.")]
    cols = st.columns(4)
    for i,(n,t,d) in enumerate(steps):
        with cols[i]:
            st.markdown(f'<div class="workflow-step {"active" if i==0 else ""}"><div class="wf-num">{n} / PROCESS</div><div class="wf-title">{t}</div><div class="wf-desc">{d}</div></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-head"><div><div class="section-kicker">BUILT FOR PRACTICAL DECISIONS</div><h2 style="margin:0">What ReNex helps you evaluate</h2></div></div>', unsafe_allow_html=True)
    features = [("⌁","Repair & restore","Identify faults that may be repairable before considering end-of-life routes."),("↻","Reuse & refurbish","Consider continued use, upgrades and refurbishment when technically viable."),("♧","Recover responsibly","Understand when component recovery or responsible recycling may be appropriate.")]
    cols = st.columns(3)
    for col,(ic,title,desc) in zip(cols,features):
        with col: st.markdown(f'<div class="panel"><div class="panel-icon">{ic}</div><h3>{title}</h3><p>{desc}</p></div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    left,right = st.columns([1.5,1])
    with left:
        st.markdown('<div class="panel"><div class="section-kicker">START HERE</div><h3>What should happen to your device next?</h3><p>Share the condition details to receive a preliminary recommendation and practical next steps.</p></div>', unsafe_allow_html=True)
        x,y = st.columns(2)
        with x:
            if st.button("▣  Assess a device", use_container_width=True): go("Assess a device")
        with y:
            if st.button("◌  Ask ReNex AI", use_container_width=True): go("Ask ReNex")
    with right:
        st.markdown(f'<div class="stat-card"><div class="stat-label">DOMAIN KNOWLEDGE</div><div class="stat-value">5 knowledge areas</div><div class="stat-note">Curated ReNex domain documents</div></div><br><div class="stat-card"><div class="stat-label">INFERENCE ENGINE</div><div class="stat-value">Llama 3.2 · 3B</div><div class="stat-note">Deployed through Nugen AI</div></div>', unsafe_allow_html=True)
    st.caption("ReNex is an AI decision-support prototype. It does not physically inspect devices, certify repairs or verify recycler authorization.")

# ---------- ASSESSMENT ----------
elif page == "Assess a device":
    st.markdown('<div class="eyebrow">DEVICE INTELLIGENCE / ASSESSMENT</div>', unsafe_allow_html=True)
    st.title("Understand your device.")
    st.write("Tell us what you know. ReNex will compare practical next-life options using the details you provide.")
    st.markdown('<div class="workflow"><div class="workflow-step active"><div class="wf-num">01</div><div class="wf-title">Identify</div><div class="wf-desc">Device details</div></div><div class="workflow-step"><div class="wf-num">02</div><div class="wf-title">Assess</div><div class="wf-desc">Condition and symptoms</div></div><div class="workflow-step"><div class="wf-num">03</div><div class="wf-title">Compare</div><div class="wf-desc">Possible pathways</div></div><div class="workflow-step"><div class="wf-num">04</div><div class="wf-title">Decide</div><div class="wf-desc">Responsible next step</div></div></div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    with st.form("assessment_form"):
        st.markdown("### 01 · Device identity")
        categories = ["Laptop", "Smartphone", "Desktop computer", "Tablet", "Server", "TV / monitor", "Printer", "Router / IoT device", "Small appliance", "Other"]
        c1,c2,c3 = st.columns([1,1,1])
        with c1: device = st.selectbox("Device category", categories)
        with c2: brand = st.text_input("Brand and model", placeholder="e.g. Lenovo ThinkPad T14")
        with c3: age = st.selectbox("Approximate age", ["Under 1 year","1–2 years","3–5 years","6–8 years","Over 8 years","Not sure"])
        st.markdown("### 02 · Current condition")
        c1,c2,c3 = st.columns(3)
        with c1: condition = st.selectbox("Overall condition", ["Working","Partially working","Not working","Physically damaged","Not sure"])
        with c2: power = st.selectbox("Does it power on?", ["Yes","No","Sometimes","Not sure"])
        with c3: hazard = st.selectbox("Safety warning signs", ["None noticed","Swollen / leaking battery","Unusually hot battery or device","Smoke, sparks or burning smell","Liquid exposure","Other damage","Not sure"])
        st.markdown("### 03 · Hardware and symptoms")
        c1,c2 = st.columns(2)
        with c1: specs = st.text_input("Known specifications (optional)", placeholder="e.g. 8 GB RAM, 1 TB HDD, 256 GB SSD")
        with c2: battery = st.selectbox("Battery condition", ["Not applicable","Normal","Short runtime","Does not charge","Unknown"])
        issue = st.text_area("Describe the issue", placeholder="Example: Laptop works slowly, takes a long time to start and battery lasts around 10 minutes.", height=105)
        data = st.selectbox("Does it contain personal data?", ["Yes","No","Not sure","Not applicable"])
        submitted = st.form_submit_button("✦  Generate AI assessment", use_container_width=True)
    if submitted:
        if not issue.strip() and condition == "Not sure":
            st.warning("Add a short description or select the closest known condition.")
        else:
            prompt = f"Assess this device and provide a preliminary next-step recommendation. Device: {device}. Brand/model: {brand or 'Not supplied'}. Age: {age}. Condition: {condition}. Powers on: {power}. Safety warning signs: {hazard}. Specifications: {specs or 'Not supplied'}. Battery: {battery}. Issue: {issue or 'Not supplied'}. Personal data: {data}. Prioritize diagnosis and repair where appropriate. Suggest specific checks/upgrades only conditionally; verify compatibility for exact model. Do not invent costs or compatibility. Explain when refurbishment, reuse, component recovery or recycling becomes appropriate."
            if hazard in ["Swollen / leaking battery","Unusually hot battery or device","Smoke, sparks or burning smell"]:
                st.error("SAFETY PRIORITY: Stop using and charging the device. Do not open or handle the battery. Seek qualified assistance. If there is active smoke or fire, move away and contact emergency services.")
            with st.spinner("ReNex is evaluating the device information..."):
                answer,error,confidence = ask_nugen(prompt)
            if error: st.error(error)
            else:
                st.markdown('<div class="result-banner"><div class="result-label">RENEX / PRELIMINARY RESULT</div><div class="result-title">Your device assessment</div><div class="result-copy">A decision-support response based on the information submitted. Confirm technical findings with a qualified professional.</div></div>', unsafe_allow_html=True)
                render_answer(answer,confidence)

# ---------- CHAT ----------
elif page == "Ask ReNex":
    st.markdown('<div class="eyebrow">RENEX INTELLIGENCE / AI ASSISTANT</div>', unsafe_allow_html=True)
    st.title("Ask ReNex.")
    st.write("A focused assistant for electronics repair, second-life options and responsible e-waste handling.")
    if "chat" not in st.session_state: st.session_state.chat = []
    st.markdown('<div class="panel"><div class="panel-icon">◌</div><h3>What can I help you decide?</h3><p>Describe a device issue, compare repair and refurbishment, or ask about safe end-of-life handling.</p></div>', unsafe_allow_html=True)
    qcols = st.columns(3)
    suggestions = ["My laptop is slow. Should I upgrade it or replace it?", "How do I know if a battery is unsafe?", "What should I do before donating an old phone?"]
    for col,q in zip(qcols,suggestions):
        with col:
            if st.button(q, use_container_width=True):
                st.session_state.pending_question = q
                st.rerun()
    top1,top2 = st.columns([5,1])
    with top2:
        if st.button("Clear chat", use_container_width=True): st.session_state.chat=[]; st.rerun()
    for m in st.session_state.chat:
        with st.chat_message(m["role"]): st.markdown(m["content"])
    question = st.chat_input("Ask about a device, repair or recycling...")
    if st.session_state.get("pending_question"):
        question = st.session_state.pop("pending_question")
    if question:
        st.session_state.chat.append({"role":"user","content":question})
        with st.chat_message("user"): st.markdown(question)
        with st.chat_message("assistant"):
            with st.spinner("ReNex is thinking..."):
                answer,error,confidence = ask_nugen(question,st.session_state.chat[-10:])
            if error: st.error(error)
            else:
                render_answer(answer,confidence)
                st.session_state.chat.append({"role":"assistant","content":answer})

# ---------- CIRCULARITY GUIDE ----------
elif page == "Circularity Guide":
    st.markdown('<div class="eyebrow">KNOWLEDGE / CIRCULARITY PATHWAYS</div>', unsafe_allow_html=True)
    st.title("Keep value in the loop.")
    st.write("The most responsible route depends on device condition, safety, repairability and actual costs—not age alone.")
    pathways = [
        ("01","↻","Continue using","Choose this when the device works safely and still meets your needs. Keep software updated and maintain it appropriately."),
        ("02","⚙","Repair","Choose this when a specific fault may be fixable, such as a replaceable battery, charging port or damaged component. Get a qualified diagnosis and quote."),
        ("03","✧","Refurbish","Consider this when several repairs or upgrades could extend useful life. Verify compatibility and compare total cost with the device's value."),
        ("04","◈","Component recovery","When the whole device is no longer practical to restore, qualified handlers may recover usable components and materials."),
        ("05","♧","Responsible recycling","Use an appropriate collection or take-back channel when the device is unsafe, irreparable or uneconomical to restore."),
    ]
    for i in range(0,len(pathways),2):
        cols = st.columns(2)
        for j,item in enumerate(pathways[i:i+2]):
            n,ic,title,desc=item
            with cols[j]: st.markdown(f'<div class="guide-card"><div class="guide-icon">{ic}</div><div class="section-kicker">PATHWAY {n}</div><h3>{title}</h3><p>{desc}</p></div>',unsafe_allow_html=True)
    st.markdown("<br>",unsafe_allow_html=True)
    st.info("Battery safety: swelling, leakage, unusual heat, smoke, sparks or burning smell require stopping use/charging and seeking qualified assistance. Do not open or dismantle lithium-ion batteries.")
    st.markdown("### Before handing a device over")
    st.markdown("Back up important files · Sign out of accounts · Remove SIM/memory cards where relevant · Securely erase personal data · Confirm the collection provider accepts the device and battery condition.")

# ---------- TECHNOLOGY ----------
elif page == "Technology":
    st.markdown('<div class="eyebrow">ENGINEERING / SYSTEM OVERVIEW</div>', unsafe_allow_html=True)
    st.title("The ReNex architecture.")
    st.write("A lightweight application layer connects device information to a domain-aligned language model for preliminary circularity guidance.")
    st.markdown("### Inference workflow")
    nodes = [("01 · INPUT","Device details","Category, age, symptoms and known specifications"),("02 · APP LAYER","Python + Streamlit","Collects inputs, applies system instructions and formats results"),("03 · INFERENCE","Nugen API","Secure request to the deployed model"),("04 · MODEL","Llama 3.2 · 3B","Domain-aligned response generation"),("05 · OUTPUT","Decision support","Preliminary options, safety notes and next steps")]
    for i in range(0,5,3):
        cols=st.columns(3)
        for col,node in zip(cols,nodes[i:i+3]):
            with col: st.markdown(f'<div class="arch-node"><div class="section-kicker">{node[0]}</div><strong>{node[1]}</strong><span>{node[2]}</span></div>',unsafe_allow_html=True)
        if i==0: st.markdown("<div style='text-align:center;color:#17815b;font-size:1.3rem;padding:.25rem'>↓ &nbsp;&nbsp; ↓ &nbsp;&nbsp; ↓</div>",unsafe_allow_html=True)
    st.markdown("### Technology stack")
    tech = [("Application","Python · Streamlit"),("Model","Llama 3.2 3B Instruct base model"),("AI platform","Nugen inference API"),("API communication","REST · Requests"),("Configuration","Python-dotenv · local .env")]
    cols=st.columns(5)
    for col,(k,v) in zip(cols,tech):
        with col: st.markdown(f'<div class="stat-card"><div class="stat-label">{k.upper()}</div><div style="font-weight:700;color:#163c2c;margin-top:.5rem">{v}</div></div>',unsafe_allow_html=True)
    st.markdown("### ReNex domain knowledge")
    docs = ["Domain overview","Device classification and assessment","Repair, reuse and refurbishment guidelines","Responsible e-waste handling and recycling","Environmental impact methodology"]
    cols=st.columns(2)
    for i,d in enumerate(docs):
        with cols[i%2]: st.markdown(f'<div class="panel" style="padding:.8rem 1rem;margin-bottom:.5rem"><span style="color:#16835c;font-weight:700">✓</span> &nbsp;{d}</div>',unsafe_allow_html=True)
    st.warning("The prototype does not physically inspect hardware, certify repairability, verify recycler authorization or calculate measured lifecycle savings. The Nugen confidence indicator is not a verified accuracy metric.")
    st.caption("ReNex · AI-powered second-life decision support for a more circular electronics future.")
