import streamlit as st
import os
from dotenv import load_dotenv

load_dotenv()

if not os.getenv("OPENAI_API_KEY"):
    try:
        os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]
    except Exception:
        pass
import json
from datetime import datetime
if not os.getenv("OPENAI_API_KEY"):
    st.error("Configuration error. Please try again later.")
    st.stop()

from lama_engine_v2 import get_personalized_guidance
from plan_engine import create_personalized_plan
from plan_pdf_v2 import create_plan_pdf

st.set_page_config(
    page_title="Roots with Lama",
    page_icon="🌱",
    layout="centered"
)

# ---------- DESIGN ----------

import base64
from pathlib import Path

image_path = Path("lama_hero.jpg")

if not image_path.exists():
    raise FileNotFoundError("lama_hero.jpg not found")

lama_image = base64.b64encode(
    image_path.read_bytes()
).decode()


st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Alexandria:wght@400;500;600;700;800&family=Tajawal:wght@400;500;700;800&display=swap');


/* ROOTS WITH LAMA — LOVELY PREMIUM */

html, body {
    direction: rtl;
    font-family: "Tajawal", sans-serif;
}

.stApp {
    background:
        radial-gradient(circle at 90% 8%, rgba(214, 177, 211, .20), transparent 25%),
        radial-gradient(circle at 8% 18%, rgba(236, 184, 179, .18), transparent 25%),
        linear-gradient(180deg, #FFF9F5 0%, #FAF4F0 52%, #F8F3EE 100%);
    color: #4B3B42;
}

header[data-testid="stHeader"] {
    background: transparent;
}

.block-container {
    max-width: 1080px;
    padding-top: 2rem;
    padding-bottom: 8rem;
}


.stApp,
input,
textarea,
button,
label,
div[data-baseweb="select"],
div[data-testid="stMarkdownContainer"] {
    font-family: "Tajawal", sans-serif !important;
}

/* Lovely headings */
.hero-title,
.section-title,
div[data-testid="stMarkdownContainer"] h1,
div[data-testid="stMarkdownContainer"] h2,
div[data-testid="stMarkdownContainer"] h3,
div[data-testid="stMarkdownContainer"] h4 {
    font-family: "Alexandria", sans-serif !important;
}

/* Hero supporting copy */
.hero-kicker,
.hero-text,
.hero-signature,
.hero-pill,
.hero-brand,
.photo-badge {
    font-family: "Tajawal", sans-serif !important;
}

/* RTL */

div[data-testid="stAppViewContainer"] h1,
div[data-testid="stAppViewContainer"] h2,
div[data-testid="stAppViewContainer"] h3,
div[data-testid="stAppViewContainer"] h4,
div[data-testid="stAppViewContainer"] h5,
div[data-testid="stAppViewContainer"] h6,
div[data-testid="stMarkdownContainer"],
div[data-testid="stMarkdownContainer"] p,
div[data-testid="stMarkdownContainer"] li,
label,
label p {
    direction: rtl !important;
    text-align: right !important;
}

/* HERO */

.lama-hero {
    position: relative;
    overflow: hidden;
    border-radius: 42px;
    padding: 26px;
    margin-bottom: 58px;
    background:
        linear-gradient(
            135deg,
            #F8D9D7 0%,
            #F2D9E5 43%,
            #E3D5F1 100%
        );
    border: 1px solid rgba(255,255,255,.85);
    box-shadow:
        0 32px 80px rgba(112, 73, 91, .15),
        inset 0 1px 0 rgba(255,255,255,.80);
}

.lama-hero:before {
    content: "";
    position: absolute;
    width: 330px;
    height: 330px;
    border-radius: 50%;
    right: -160px;
    top: -180px;
    background: rgba(255,255,255,.23);
}

.lama-hero:after {
    content: "";
    position: absolute;
    width: 230px;
    height: 230px;
    border-radius: 50%;
    left: -100px;
    bottom: -145px;
    background: rgba(129, 105, 138, .08);
}

.hero-inner {
    position: relative;
    z-index: 2;
    display: grid;
    grid-template-columns: .88fr 1.12fr;
    gap: 42px;
    align-items: center;
}

/* IMAGE */

.lama-photo-wrap {
    position: relative;
    height: 540px;
    overflow: hidden !important;
    border-radius: 34px !important;
    clip-path: inset(0 round 34px);
}

.lama-photo {
    width: 100%;
    height: 100%;
    object-fit: cover;
    object-position: center 32%;
    display: block;
    border: none !important;
    border-radius: 34px !important;
    box-shadow: none !important;
}

.photo-badge {
    position: absolute;
    bottom: 22px;
    right: 22px;
    background: rgba(255, 250, 247, .92);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255,255,255,.80);
    border-radius: 20px;
    padding: 12px 16px;
    color: #624957;
    font-size: 12px;
    font-weight: 800;
    box-shadow: 0 12px 30px rgba(82,52,67,.12);
}

/* COPY */

.hero-copy {
    padding: 30px 20px 30px 10px;
    text-align: right;
}

.hero-brand {
    color: #875F75;
    font-size: 12px;
    font-weight: 850;
    letter-spacing: 1.5px;
    margin-bottom: 28px;
}

.hero-kicker {
    color: #A36D7C;
    font-size: 14px;
    font-weight: 800;
    margin-bottom: 14px;
}

.hero-title {
    color: #4C3743;
    font-size: 50px;
    line-height: 1.48;
    font-weight: 900;
    margin-bottom: 22px;
}

.hero-text {
    color: #705E66;
    font-size: 17px;
    line-height: 2.05;
    max-width: 590px;
}

.hero-signature {
    margin-top: 24px;
    color: #8C6878;
    font-size: 14px;
    font-weight: 700;
}

.hero-pills {
    display: flex;
    flex-wrap: wrap;
    gap: 9px;
    margin-top: 28px;
}

.hero-pill {
    padding: 9px 14px;
    border-radius: 999px;
    background: rgba(255,255,255,.50);
    border: 1px solid rgba(255,255,255,.82);
    color: #765866;
    font-size: 12px;
    font-weight: 700;
}

/* SECTION TITLE */

.section-title {
    position: relative;
    direction: rtl !important;
    text-align: right !important;
    color: #503D46;
    font-size: 26px;
    line-height: 1.55;
    font-weight: 900;
    margin-top: 52px;
    margin-bottom: 22px;
    padding-right: 20px;
}

.section-title:before {
    content: "";
    position: absolute;
    right: 0;
    top: 8px;
    width: 5px;
    height: 29px;
    border-radius: 999px;
    background:
        linear-gradient(
            180deg,
            #C9879D,
            #B49ACE
        );
}

/* FORM */

div[data-testid="stTextInput"],
div[data-testid="stTextArea"],
div[data-testid="stNumberInput"],
div[data-testid="stSelectbox"] {
    direction: rtl !important;
    background:
        linear-gradient(
            145deg,
            rgba(255,253,251,.96),
            rgba(252,246,248,.96)
        );
    border: 1px solid #EFDDE3;
    border-radius: 28px;
    padding: 16px 18px 13px;
    margin-bottom: 18px;
    box-shadow:
        0 16px 42px rgba(110, 73, 91, .055),
        inset 0 1px 0 rgba(255,255,255,.95);
    transition: all .22s ease;
}

div[data-testid="stTextInput"]:focus-within,
div[data-testid="stTextArea"]:focus-within,
div[data-testid="stNumberInput"]:focus-within,
div[data-testid="stSelectbox"]:focus-within {
    border-color: #C8AED8;
    box-shadow:
        0 0 0 4px rgba(197, 164, 216, .11),
        0 18px 46px rgba(110, 73, 91, .07);
    transform: translateY(-1px);
}

input,
textarea {
    direction: rtl !important;
    text-align: right !important;
    color: #59444F !important;
    font-size: 15px !important;
    line-height: 1.8 !important;
}

input::placeholder,
textarea::placeholder {
    color: #A998A0 !important;
    opacity: .85 !important;
}

div[data-baseweb="select"] {
    direction: rtl !important;
}

div[data-baseweb="select"] > div,
div[data-baseweb="input"] > div,
div[data-baseweb="textarea"] textarea {
    background:
        linear-gradient(
            180deg,
            #F9F4F6 0%,
            #F6F1F4 100%
        ) !important;
    border: 1px solid rgba(224, 208, 216, .45) !important;
    border-radius: 17px !important;
    min-height: 50px !important;
}

div[data-baseweb="textarea"] textarea {
    padding-top: 14px !important;
    padding-bottom: 14px !important;
}

label[data-testid="stWidgetLabel"] {
    width: 100%;
}

label[data-testid="stWidgetLabel"] p {
    color: #604A55 !important;
    font-size: 14px !important;
    font-weight: 800 !important;
    margin-bottom: 7px !important;
}

div[data-testid="stNumberInput"] button {
    border-radius: 12px !important;
    color: #8B6A79 !important;
}

div[data-testid="stSelectbox"] svg {
    color: #9B758A !important;
}

/* softer section rhythm */

.section-title {
    margin-top: 58px;
    margin-bottom: 24px;
}

.section-title:after {
    content: "";
    display: block;
    width: 58px;
    height: 2px;
    margin-top: 9px;
    margin-right: 0;
    border-radius: 999px;
    background:
        linear-gradient(
            90deg,
            #D996AA,
            #C2A7D6,
            transparent
        );
}

/* BUTTONS */

.stButton > button,
.stDownloadButton > button {
    width: 100%;
    min-height: 60px;
    border: none;
    border-radius: 999px;
    background:
        linear-gradient(
            135deg,
            #A86D82 0%,
            #866B99 100%
        );
    color: #FFFDFB;
    font-size: 16px;
    font-weight: 850;
    box-shadow:
        0 15px 36px rgba(128, 87, 107, .20),
        inset 0 1px 0 rgba(255,255,255,.18);
}

.stButton > button:hover,
.stDownloadButton > button:hover {
    transform: translateY(-1px);
    color: white;
    background:
        linear-gradient(
            135deg,
            #985F74 0%,
            #795E8D 100%
        );
}


/* ---------- LAMA ANSWER ---------- */

div[data-testid="stAlert"] {
    border: 1px solid #E9D6DF !important;
    background:
        linear-gradient(
            135deg,
            rgba(255,250,249,.96),
            rgba(247,238,246,.95)
        ) !important;
    border-radius: 26px !important;
    box-shadow: 0 14px 38px rgba(102,70,84,.055);
    padding: 18px 20px !important;
}

/* body copy below Lama sections */

div[data-testid="stMarkdownContainer"] p {
    color: #66545C;
    line-height: 2;
}

div[data-testid="stMarkdownContainer"] li {
    color: #66545C;
    line-height: 2;
    margin-bottom: 8px;
}

/* ---------- PLAN INTRO ---------- */

div[data-testid="stMarkdownContainer"] h2 {
    color: #513C47 !important;
    font-weight: 800 !important;
    margin-bottom: 12px !important;
}

div[data-testid="stMarkdownContainer"] h3 {
    color: #725463 !important;
    font-weight: 800 !important;
    margin-top: 32px !important;
}

/* ---------- 7 DAY CARDS ---------- */

div[data-testid="stVerticalBlockBorderWrapper"] {
    position: relative;
    overflow: hidden;
    margin-bottom: 22px;
    padding: 22px 24px !important;
    background:
        radial-gradient(
            circle at 100% 0%,
            rgba(221,184,211,.16),
            transparent 28%
        ),
        linear-gradient(
            145deg,
            rgba(255,253,251,.99),
            rgba(251,244,247,.98)
        ) !important;
    border: 1px solid #ECDADF !important;
    border-radius: 32px !important;
    box-shadow:
        0 20px 50px rgba(91,59,74,.065) !important;
}

div[data-testid="stVerticalBlockBorderWrapper"]:before {
    content: "";
    position: absolute;
    right: 0;
    top: 0;
    width: 6px;
    height: 100%;
    background:
        linear-gradient(
            180deg,
            #D991A8,
            #B8A0D2
        );
}

div[data-testid="stVerticalBlockBorderWrapper"] h4 {
    font-family: "Alexandria", sans-serif !important;
    color: #593E4B !important;
    font-size: 22px !important;
    font-weight: 800 !important;
    margin-bottom: 22px !important;
}

div[data-testid="stVerticalBlockBorderWrapper"] strong {
    color: #8B6377 !important;
    font-weight: 800 !important;
}

div[data-testid="stVerticalBlockBorderWrapper"] p {
    color: #66545C !important;
}

/* ---------- PLAN CTA ---------- */

.stDownloadButton {
    margin-top: 24px;
}

.stDownloadButton > button {
    min-height: 64px !important;
    background:
        linear-gradient(
            135deg,
            #B66F88 0%,
            #9372A8 100%
        ) !important;
    border: 1px solid rgba(255,255,255,.45) !important;
    box-shadow:
        0 18px 42px rgba(137,87,109,.22) !important;
}

/* subtle captions */

.stCaption,
small {
    color: #9A858E !important;
}

/* RESULT / PLAN CARDS */

div[data-testid="stVerticalBlockBorderWrapper"] {
    direction: rtl !important;
    text-align: right !important;
    background:
        linear-gradient(
            145deg,
            rgba(255,253,251,.98),
            rgba(252,245,247,.97)
        );
    border: 1px solid #ECDDDC !important;
    border-radius: 30px !important;
    box-shadow:
        0 20px 55px rgba(87,59,71,.055);
    padding: 10px !important;
}

div[data-testid="stVerticalBlockBorderWrapper"] h1,
div[data-testid="stVerticalBlockBorderWrapper"] h2,
div[data-testid="stVerticalBlockBorderWrapper"] h3,
div[data-testid="stVerticalBlockBorderWrapper"] h4 {
    direction: rtl !important;
    text-align: right !important;
    color: #624654 !important;
}

div[data-testid="stAlert"] {
    direction: rtl !important;
    text-align: right !important;
    border-radius: 24px;
}

/* DIVIDERS */

hr {
    border: 0 !important;
    height: 1px !important;
    background:
        linear-gradient(
            90deg,
            transparent,
            #E6D6D8,
            transparent
        ) !important;
    margin: 48px 0 !important;
}

/* MOBILE */

@media (max-width: 760px) {

    .block-container {
        padding: 1rem;
    }

    .lama-hero {
        border-radius: 30px;
        padding: 18px;
    }

    .hero-inner {
        grid-template-columns: 1fr;
    }

    .lama-photo {
        height: 410px;
    }

    .hero-copy {
        padding: 18px 8px 24px;
    }

    .hero-title {
        font-size: 35px;
    }
}


/* FINAL HERO PHOTO FIX */
.lama-photo-wrap {
    position: relative !important;
    width: 100% !important;
    height: 540px !important;
    padding: 0 !important;
    margin: 0 !important;
    overflow: hidden !important;
    border-radius: 34px !important;
    border: none !important;
}

.lama-photo-wrap .lama-photo {
    position: absolute !important;
    inset: 0 !important;
    width: 100% !important;
    height: 100% !important;
    max-width: none !important;
    margin: 0 !important;
    padding: 0 !important;

    object-fit: cover !important;
    object-position: center 32% !important;

    display: block !important;
    border: none !important;
    border-radius: 34px !important;
    box-shadow: none !important;
}

@media (max-width: 760px) {
    .lama-photo-wrap {
        height: 410px !important;
    }

    .lama-photo-wrap .lama-photo {
        height: 100% !important;
    }
}

</style>
""", unsafe_allow_html=True)


# ---------- BETA NOTICE ----------

st.markdown("""
<div style="
    direction: rtl;
    text-align: center;
    background: linear-gradient(135deg, #FCE8EC, #EEE4F6);
    border: 1px solid #E9D5DF;
    border-radius: 18px;
    padding: 11px 18px;
    margin-bottom: 18px;
    color: #765665;
    font-size: 13px;
    font-weight: 700;
">
🌷 نسخة تجريبية خاصة — رأيك رح يساعدنا نخلي التجربة أحسن للأمهات
</div>
""", unsafe_allow_html=True)


# ---------- HERO ----------

hero_html = f"""<div class="lama-hero"><div class="hero-inner"><div class="lama-photo-wrap"><img class="lama-photo" src="data:image/jpeg;base64,{lama_image}"><div class="photo-badge">معك لمى 🌷</div></div><div class="hero-copy"><div class="hero-brand">ROOTS WITH LAMA · جذور مع لمى</div><div class="hero-kicker">أحياناً كل اللي بدنا ياه… نفهم شو عم يصير.</div><div class="hero-title">احكيلي عن طفلك.<br>ومنبلّش من هون.</div><div class="hero-text">ما في وصفة واحدة لكل الأطفال. احكيلي شو شاغلك اليوم، ومنحوّل التفاصيل لبداية عملية تناسب طفلك وروتينكم الحقيقي.</div><div class="hero-signature">قرب، فهم، وخطوات صغيرة بتفرق 🤍</div><div class="hero-pills"><div class="hero-pill">مخصص لطفلك</div><div class="hero-pill">بدون أحكام</div><div class="hero-pill">خطوات بسيطة</div><div class="hero-pill">من واقع يومكم</div></div></div></div></div>"""

st.markdown(
    hero_html,
    unsafe_allow_html=True
)

st.markdown("""
<style>
div[data-testid="stPageLink"] a {
    background: linear-gradient(135deg, #FFF4F4 0%, #F3E8F6 100%);
    border: 1px solid #E3D0DC;
    border-radius: 20px;
    padding: 16px 18px;
    min-height: 58px;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #6F5061 !important;
    font-family: "Tajawal", sans-serif !important;
    font-weight: 800 !important;
    text-decoration: none !important;
    box-shadow: 0 10px 24px rgba(112,73,91,.09);
    transition: all .2s ease;
}

div[data-testid="stPageLink"] a:hover {
    transform: translateY(-2px);
    background: linear-gradient(135deg, #FBE7EA 0%, #EEDFF4 100%);
    border-color: #D8BDCD;
}
</style>
""", unsafe_allow_html=True)

st.page_link(
    "pages/4_💬_استشارة_مع_لمى.py",
    label="💬 احجزي استشارة الآن",
    width="stretch"
)

nav1, nav2 = st.columns(2)

with nav1:
    st.page_link(
        "pages/2_📖_قصة_لطفلك.py",
        label="🎁 احصلي على هديتك المجانية",
        width="stretch"
    )

with nav2:
    st.page_link(
        "pages/3_🎴_بطاقات_تعليمية.py",
        label="🎴 احصلي على بطاقات تعليمية",
        width="stretch"
    )

# ---------- CHILD INFO ----------

st.markdown(
    '<div class="section-title">أولاً، خبريني شوي عن طفلك</div>',
    unsafe_allow_html=True
)

child_name = st.text_input(
    "اسم الطفل",
    placeholder="مثلاً: لونا"
)

age = st.number_input(
    "عمر الطفل بالسنوات",
    min_value=1,
    max_value=4,
    value=3,
    step=1
)


# ---------- NEED ----------

st.markdown(
    '<div class="section-title">شو أكتر شي شاغلك حالياً؟</div>',
    unsafe_allow_html=True
)

category = st.selectbox(
    "اختاري الأقرب",
    [
        "نوبات الغضب",
        "النوم",
        "الشاشات",
        "الأكل",
        "السلوك والمشاعر",
        "اللعب والتعلّم",
        "الاستقلالية",
        "الروتين اليومي",
        "ما بعرف بالضبط — بدي أحكي شو عم يصير"
    ]
)

situation = st.text_area(
    "احكيلي شو عم يصير",
    placeholder=(
        "مثلاً: لما امنعه عن الآيباد بيبدأ يصرخ "
        "ويضربني، وصار الموضوع يتكرر كل يوم..."
    ),
    height=140
)


# ---------- CONTEXT ----------

st.markdown(
    '<div class="section-title">حتى يكون الحل أقرب لواقعكم</div>',
    unsafe_allow_html=True
)

duration = st.selectbox(
    "من إمتى بلشت المشكلة؟",
    [
        "من كم يوم",
        "من كم أسبوع",
        "من عدة أشهر",
        "من فترة طويلة",
        "مش متأكدة"
    ]
)

tried = st.text_area(
    "شو جربتي لحد الآن؟",
    placeholder=(
        "مثلاً: حاولت أشرحله، تجاهلت الصراخ، "
        "أخذت الجهاز منه فجأة..."
    ),
    height=100
)

goal = st.text_input(
    "إذا في شي واحد بدك يتحسن، شو هو؟",
    placeholder="مثلاً: يتقبل انتهاء وقت الشاشة بدون صراخ"
)


# ---------- BUTTON ----------

st.write("")

if "lama_result" not in st.session_state:
    st.session_state.lama_result = None

if "personalized_plan_result" not in st.session_state:
    st.session_state.personalized_plan_result = None

if st.button("🌿 ساعديني يا لمى"):

    if not situation.strip():

        st.warning(
            "احكيلي شوي شو عم يصير حتى نقدر نساعدك بشكل شخصي."
        )

    else:

        with st.spinner("عم نفهم وضعكم ونحضّر لك بداية مناسبة... 🌱"):

            try:

                result = get_personalized_guidance(
                    child_name=child_name,
                    age=age,
                    category=category,
                    situation=situation,
                    duration=duration,
                    tried=tried,
                    goal=goal
                )

                st.session_state.lama_result = result

            except Exception as e:

                st.error(
                    "صار خطأ أثناء تجهيز الجواب. "
                    "جربي مرة ثانية بعد قليل."
                )

                st.caption(str(e))


# ---------- RESULT ----------

result = st.session_state.lama_result

if result:

    st.markdown("---")

    st.markdown(
        '<div class="section-title">فهمت منك 🌿</div>',
        unsafe_allow_html=True
    )

    st.write(result["summary"])


    st.markdown(
        '<div class="section-title">شو ممكن يكون عم يصير؟</div>',
        unsafe_allow_html=True
    )

    for item in result["possible_explanations"]:
        st.markdown(f"• {item}")


    st.markdown(
        '<div class="section-title">شو تعملي اليوم؟</div>',
        unsafe_allow_html=True
    )

    for i, item in enumerate(result["today_steps"], start=1):
        st.markdown(f"**{i}.** {item}")


    st.markdown(
        '<div class="section-title">خلال هالأسبوع</div>',
        unsafe_allow_html=True
    )

    for item in result["week_plan"]:
        st.markdown(f"• {item}")


    st.markdown(
        '<div class="section-title">شو نراقب؟</div>',
        unsafe_allow_html=True
    )

    for item in result["watch_for"]:
        st.markdown(f"• {item}")


    st.markdown(
        '<div class="section-title">الخطوة التالية</div>',
        unsafe_allow_html=True
    )

    next_step = result["next_step"]

    if next_step == "none":

        st.success(result["next_step_message"])

    elif next_step == "personalized_plan":

        st.info(result["next_step_message"])

        if "show_plan_form" not in st.session_state:
            st.session_state.show_plan_form = False

        if st.button("🌱 جهزيلي خطة مخصصة", key="open_plan"):

            st.session_state.show_plan_form = True


        if st.session_state.show_plan_form:

            st.markdown("---")

            st.markdown(
                '<div class="section-title">بس كم شغلة صغيرة قبل ما نجهز الخطة</div>',
                unsafe_allow_html=True
            )

            plan_time = st.selectbox(
                "قديش بتقدري تخصصي يومياً لتطبيق الخطة؟",
                [
                    "5–10 دقائق",
                    "10–20 دقيقة",
                    "20–30 دقيقة",
                    "حسب اليوم"
                ],
                key="plan_time"
            )

            plan_context = st.text_area(
                "متى أو بأي ظروف غالباً بتصير المشكلة؟",
                placeholder="مثلاً: بعد الحضانة، قبل النوم، لما نكون برا البيت...",
                key="plan_context"
            )

            plan_notes = st.text_area(
                "في شي مهم لازم نراعيه بالخطة؟",
                placeholder="روتين معين، أخ أو أخت، حضانة، سفر، وقت محدود...",
                key="plan_notes"
            )

            st.caption(
                "هالمعلومات رح نستخدمها مع كل اللي حكيتيه قبل، "
                "وما رح نطلب منك تعيدي التفاصيل."
            )


            st.write("")

            if st.button("🌱 جهزي خطتي", key="generate_plan"):

                with st.spinner("عم نجهز خطة تناسبكم يوم بيوم..."):

                    try:

                        plan = create_personalized_plan(
                            child_name=child_name,
                            age=age,
                            category=category,
                            situation=situation,
                            duration=duration,
                            tried=tried,
                            goal=goal,
                            plan_time=plan_time,
                            plan_context=plan_context,
                            plan_notes=plan_notes
                        )

                        st.session_state.personalized_plan_result = plan

                    except Exception as e:

                        st.error(
                            "صار خطأ أثناء تجهيز الخطة. "
                            "جربي مرة ثانية بعد قليل."
                        )

                        st.caption(str(e))

    elif next_step == "lama_consultation":

        st.info(result["next_step_message"])

        st.button(
            "💬 احجزي جلسة مع لمى — قريباً",
            key="book_lama_consultation",
            disabled=True
        )

        if "show_consultation_plan_form" not in st.session_state:
            st.session_state.show_consultation_plan_form = False

        if st.button(
            "🌷 جهزيلي خطة مبدئية أبدأ فيها",
            key="open_consultation_plan"
        ):
            st.session_state.show_consultation_plan_form = True


        if st.session_state.show_consultation_plan_form:

            st.markdown("---")

            st.markdown(
                '<div class="section-title">خلينا نجهز لك بداية عملية لحد موعد الجلسة</div>',
                unsafe_allow_html=True
            )

            plan_time = st.selectbox(
                "قديش بتقدري تخصصي يومياً لتطبيق الخطة؟",
                [
                    "5–10 دقائق",
                    "10–20 دقيقة",
                    "20–30 دقيقة",
                    "حسب اليوم"
                ],
                key="consultation_plan_time"
            )

            plan_context = st.text_area(
                "متى أو بأي ظروف غالباً بتصير المشكلة؟",
                placeholder="مثلاً: بعد الحضانة، قبل النوم، لما نكون برا البيت...",
                key="consultation_plan_context"
            )

            plan_notes = st.text_area(
                "في شي مهم لازم نراعيه بالخطة؟",
                placeholder="روتين معين، أخ أو أخت، حضانة، سفر، وقت محدود...",
                key="consultation_plan_notes"
            )

            st.caption(
                "هاي خطة مبدئية تساعدك تبدأي بخطوات عملية، "
                "وما بتحل محل الجلسة إذا كانت الحالة بحاجة نقاش أعمق."
            )

            st.write("")

            if st.button(
                "🌷 جهزي خطتي المبدئية",
                key="generate_consultation_plan"
            ):

                with st.spinner("عم نجهز لك بداية تناسب وضعكم..."):

                    try:

                        plan = create_personalized_plan(
                            child_name=child_name,
                            age=age,
                            category=category,
                            situation=situation,
                            duration=duration,
                            tried=tried,
                            goal=goal,
                            plan_time=plan_time,
                            plan_context=plan_context,
                            plan_notes=plan_notes
                        )

                        st.session_state.personalized_plan_result = plan

                    except Exception as e:

                        st.error(
                            "صار خطأ أثناء تجهيز الخطة. "
                            "جربي مرة ثانية بعد قليل."
                        )

                        st.caption(str(e))

    elif next_step == "specialist":

        st.warning(result["next_step_message"])

    elif next_step == "urgent_help":

        st.error(result["next_step_message"])


# ---------- PERSONALIZED PLAN RESULT ----------

plan = st.session_state.personalized_plan_result

if plan:

    st.markdown("---")

    st.markdown(
        '<div class="section-title">خطتك المخصصة 🌿</div>',
        unsafe_allow_html=True
    )

    st.subheader(plan["plan_title"])
    st.write(plan["plan_goal"])

    st.markdown("### قبل ما تبلشي")

    for item in plan["before_you_start"]:
        st.markdown(f"• {item}")

    st.markdown("### خطة 7 أيام")

    for day in plan["days"]:

        with st.container(border=True):

            st.markdown(
                f"#### اليوم {day['day']} — {day['focus']}"
            )

            st.markdown("**الخطوة الرئيسية**")
            st.write(day["main_step"])

            st.markdown("**ممكن تقولي**")
            st.write(day["say_this"])

            st.markdown("**راقبي**")
            st.write(day["watch_for"])

    st.markdown("### بنهاية الأسبوع")

    st.write(plan["end_of_week"])

    st.markdown("### إذا بدنا نعدّل الخطة")

    st.write(plan["adjustment_note"])


    st.write("")

    try:
        pdf_buffer = create_plan_pdf(
            plan,
            child_name=child_name.strip() if child_name.strip() else "طفلك"
        )

        st.download_button(
            label="📄 حمّلي خطتك PDF",
            data=pdf_buffer.getvalue(),
            file_name="roots_with_lama_plan.pdf",
            mime="application/pdf",
            use_container_width=True
        )

    except Exception as e:
        st.error("ما قدرنا نجهز ملف الـPDF حالياً.")
        st.caption(str(e))


# ---------- BETA FEEDBACK ----------

if st.session_state.get("lama_result"):

    st.markdown("---")

    st.markdown(
        '<div class="section-title">قبل ما تروحي… رأيك بهمّنا 🤍</div>',
        unsafe_allow_html=True
    )

    beta_helpful = st.radio(
        "قديش حسّيتي الجواب أو الخطة مناسبين فعلاً لطفلك؟",
        [
            "كتير مناسب",
            "مناسب إلى حد ما",
            "مو مخصص كفاية"
        ],
        index=None,
        key="beta_helpful"
    )

    beta_use_again = st.radio(
        "ممكن ترجعي تستخدمي Roots مع موقف ثاني؟",
        [
            "أكيد",
            "ممكن",
            "غالباً لا"
        ],
        index=None,
        key="beta_use_again"
    )

    beta_comment = st.text_area(
        "شو الشي الوحيد اللي بتحبي نغيّره أو نضيفه؟",
        placeholder="أي ملاحظة صغيرة بتفيدنا...",
        key="beta_comment"
    )

    if st.button("💌 أرسل رأيي", key="save_beta_feedback"):

        if not beta_helpful or not beta_use_again:

            st.warning("اختاري جواب للسؤالين السريعين أولاً.")

        else:

            feedback = {
                "created_at": datetime.now().isoformat(),
                "child_age": age,
                "category": category,
                "router_decision": (
                    st.session_state.lama_result.get("next_step")
                    if st.session_state.lama_result
                    else None
                ),
                "helpful": beta_helpful,
                "use_again": beta_use_again,
                "comment": beta_comment.strip()
            }

            with open(
                "beta_feedback.jsonl",
                "a",
                encoding="utf-8"
            ) as f:
                f.write(
                    json.dumps(
                        feedback,
                        ensure_ascii=False
                    ) + "\n"
                )

            st.success(
                "شكراً 🤍 رأيك وصل، ورح يساعدنا نحسّن Roots."
            )

# ---------- FOOTER ----------

st.markdown("""
<style>
.roots-footer {
    margin-top: 90px;
    padding: 34px 20px 18px 20px;
    border-top: 1px solid #E7D8DF;
    text-align: center;
    color: #7B6570;
    font-family: "Tajawal", sans-serif;
}

.roots-footer-brand {
    font-family: "Alexandria", sans-serif;
    font-weight: 800;
    color: #624957;
    font-size: 16px;
    margin-bottom: 8px;
}

.roots-footer-copy {
    font-size: 13px;
    line-height: 1.9;
    margin-top: 18px;
    color: #927E88;
}

.roots-footer-social {
    font-size: 14px;
    margin-top: 16px;
    color: #875F75;
}
</style>

<div class="roots-footer">
    <div class="roots-footer-brand">
        ROOTS WITH LAMA · جذور مع لمى
    </div>
    <div>
        مساحة دافئة تساعدك تفهمي طفلك وتاخدي خطوات تناسب يومكم الحقيقي 🌷
    </div>
</div>
""", unsafe_allow_html=True)

footer1, footer2, footer3, footer4 = st.columns(
    4,
    gap=None
)

with footer1:
    st.page_link(
        "pages/5_🌷_من_نحن.py",
        label="من نحن؟",
        width="stretch"
    )

with footer2:
    st.page_link(
        "pages/6_الشروط_والأحكام.py",
        label="الشروط والأحكام",
        width="stretch"
    )

with footer3:
    st.page_link(
        "pages/7_سياسة_الخصوصية.py",
        label="سياسة الخصوصية",
        width="stretch"
    )

with footer4:
    st.page_link(
        "pages/8_تواصل_معنا.py",
        label="تواصل معنا",
        width="stretch"
    )

st.markdown("""
<div class="roots-footer-social">
    Instagram · TikTok · قريباً
</div>

<div class="roots-footer-copy">
    © 2026 Roots with Lama · جميع الحقوق محفوظة
</div>
""", unsafe_allow_html=True)


# ---------- FINAL HOME NAV SIZE FIX ----------

st.markdown("""
<style>

/* Make every home navigation card fill its entire available column */
div[data-testid="stPageLink"] {
    width: 100% !important;
}

div[data-testid="stPageLink"] > a {
    width: 100% !important;
    min-height: 86px !important;

    display: flex !important;
    align-items: center !important;
    justify-content: center !important;

    box-sizing: border-box !important;

    border-radius: 24px !important;
    padding: 20px 24px !important;

    text-align: center !important;
}

/* Mobile */
@media (max-width: 700px) {
    div[data-testid="stPageLink"] > a {
        min-height: 72px !important;
        padding: 16px 12px !important;
        font-size: 14px !important;
    }
}

</style>
""", unsafe_allow_html=True)

