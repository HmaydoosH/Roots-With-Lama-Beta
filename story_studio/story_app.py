import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI
import json
import base64
import os
import tempfile
import io
import zipfile
import arabic_reshaper
from bidi.algorithm import get_display
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader

st.set_page_config(
    page_title="My Story",
    page_icon="📖",
    layout="centered"
)

load_dotenv()

st.markdown("""
<style>

/* Hide Streamlit sidebar on Story Studio */
section[data-testid="stSidebar"] {
    display: none !important;
}

div[data-testid="stSidebarCollapsedControl"] {
    display: none !important;
}

/* Permanent back-to-home button */
.roots-home-button {
    position: fixed;
    top: 18px;
    left: 20px;
    z-index: 999999;

    display: inline-flex;
    align-items: center;
    justify-content: center;

    padding: 10px 16px;
    border-radius: 18px;

    background: rgba(255, 249, 247, .94);
    border: 1px solid #E4CFDA;

    color: #704F61 !important;
    text-decoration: none !important;

    font-family: "Tajawal", sans-serif;
    font-weight: 800;
    font-size: 14px;

    box-shadow: 0 8px 24px rgba(112, 73, 91, .13);
    backdrop-filter: blur(12px);
}

.roots-home-button:hover {
    background: #F7EAF1;
    color: #624957 !important;
}

@media (max-width: 700px) {
    .roots-home-button {
        top: 12px;
        left: 12px;
        padding: 8px 12px;
        font-size: 12px;
        border-radius: 15px;
    }
}

</style>

<a class="roots-home-button" href="/" target="_self">
    ← الرجوع للصفحة الرئيسية
</a>
""", unsafe_allow_html=True)


if not os.getenv("OPENAI_API_KEY"):
    try:
        os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]
    except Exception:
        pass

client = OpenAI()


st.markdown("""
<style>

.storybook-page {
    position: relative;
    overflow: hidden;
    background:
        radial-gradient(
            circle at 92% 8%,
            rgba(255, 220, 170, 0.28),
            transparent 22%
        ),
        #FFFDF8 !important;

    border: 2px solid #EADFCC !important;
    border-radius: 34px !important;
    padding: 26px !important;
    margin-bottom: 48px !important;

    box-shadow:
        0 14px 35px rgba(73, 54, 35, 0.08),
        0 2px 0 rgba(255,255,255,0.8) inset !important;
}

.storybook-page::before {
    content: "✦";
    position: absolute;
    top: 18px;
    left: 24px;
    font-size: 22px;
    color: #E4C99E;
    opacity: 0.8;
}

.storybook-page::after {
    content: "☾";
    position: absolute;
    bottom: 22px;
    left: 26px;
    font-size: 24px;
    color: #C8D7E8;
    opacity: 0.55;
}

.page-number {
    display: inline-flex;
    align-items: center;
    gap: 7px;

    background: #F3E5CC;
    color: #6A5846 !important;

    padding: 7px 13px;
    border-radius: 999px;

    font-size: 12px !important;
    font-weight: 700 !important;

    margin-bottom: 16px !important;
}

.page-number span {
    color: #C99552;
}

.storybook-page img {
    border-radius: 24px !important;
    box-shadow: 0 8px 24px rgba(56, 43, 31, 0.10);
}

.page-text {
    position: relative;

    background: #FFF8ED;
    border-radius: 22px;

    margin-top: 18px;
    padding: 22px 24px 24px 24px !important;

    font-size: 20px !important;
    line-height: 2.15 !important;

    color: #3D342C !important;
    text-align: right;

    border: 1px solid #F0E3D1;
}

.page-text::before {
    content: "❋";
    display: block;
    color: #D6AD72;
    font-size: 18px;
    margin-bottom: 5px;
}

.book-kicker {
    display: inline-block;
    background: #EEDFC5;
    padding: 10px 20px;
    border-radius: 999px;
}

@media (max-width: 700px) {

    .storybook-page {
        padding: 16px !important;
        border-radius: 26px !important;
    }

    .page-text {
        font-size: 18px !important;
        padding: 18px !important;
    }
}

</style>
""", unsafe_allow_html=True)



st.markdown("""
<style>

html, body {
    direction: rtl;
}

[data-testid="stAppViewContainer"] {
    background: #F5EFE6 !important;
}

[data-testid="stHeader"] {
    background: transparent !important;
}

.block-container {
    max-width: 900px !important;
    padding-top: 2rem !important;
}

.hero {
    direction: rtl;
    text-align: right;
    background: #241F1A;
    border-radius: 32px;
    padding: 48px 48px 42px 48px;
    margin-bottom: 36px;
    box-shadow: 0 18px 50px rgba(55, 44, 33, 0.12);
}

.hero-badge {
    display: inline-block;
    background: #EAD8BB;
    color: #3B3026;
    padding: 7px 14px;
    border-radius: 999px;
    font-size: 14px;
    font-weight: 700;
    margin-bottom: 20px;
}

.hero h1 {
    color: #FFF9F0 !important;
    font-size: 48px !important;
    line-height: 1.35 !important;
    margin: 0 0 12px 0 !important;
}

.hero p {
    color: #DCCFC0 !important;
    font-size: 18px !important;
    line-height: 1.9 !important;
    max-width: 650px;
}

[data-testid="stTextInput"],
[data-testid="stTextArea"],
[data-testid="stNumberInput"],
[data-testid="stSelectbox"],
[data-testid="stFileUploader"] {
    background: rgba(255,255,255,0.65);
    padding: 14px;
    border-radius: 18px;
    margin-bottom: 8px;
}

.stButton > button {
    background: #241F1A !important;
    color: white !important;
    border: none !important;
    border-radius: 999px !important;
    min-height: 52px;
    padding: 0 28px !important;
    font-size: 16px !important;
    font-weight: 700 !important;
}

.stButton > button:hover {
    background: #44382D !important;
    color: white !important;
    transform: translateY(-2px);
}

.stDownloadButton > button {
    background: #FFFFFF !important;
    color: #241F1A !important;
    border: 1px solid #CFC1B0 !important;
}

h1, h2, h3 {
    color: #241F1A !important;
}


.book-title {
    text-align: center;
    margin: 40px 0 28px 0;
}

.book-kicker {
    font-size: 28px;
    font-weight: 700;
    color: #241F1A;
}

.storybook-page {
    background: #FFFDF8;
    border: 1px solid #E8DDCF;
    border-radius: 28px;
    padding: 24px;
    margin: 0 0 40px 0;
    box-shadow: 0 12px 30px rgba(60, 45, 30, 0.08);
    direction: rtl;
}

.storybook-page img {
    border-radius: 20px !important;
    margin-bottom: 18px;
}

.page-number {
    font-size: 13px;
    color: #A28F7C;
    margin-bottom: 12px;
    font-weight: 600;
}

.page-text {
    font-size: 20px;
    line-height: 2;
    color: #332D28;
    text-align: right;
    padding: 6px 4px 10px 4px;
}

@media (max-width: 700px) {
    .storybook-page {
        padding: 16px;
        border-radius: 22px;
    }

    .page-text {
        font-size: 18px;
        line-height: 1.9;
    }
}

</style>
""", unsafe_allow_html=True)


st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Noto+Kufi+Arabic:wght@400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Noto Kufi Arabic', sans-serif;
}

.stApp {
    background:
        linear-gradient(
            180deg,
            #FAF7F2 0%,
            #FFFFFF 45%,
            #F8F5F0 100%
        );
}

.block-container {
    max-width: 920px;
    padding-top: 3rem;
    padding-bottom: 5rem;
}

h1, h2, h3 {
    font-family: 'Noto Kufi Arabic', sans-serif;
    color: #292724;
    letter-spacing: -0.03em;
}

p, label {
    color: #4B4742;
    line-height: 1.9;
}

div[data-testid="stTextInput"] input,
div[data-testid="stTextArea"] textarea,
div[data-testid="stNumberInput"] input {
    border-radius: 14px;
}

div[data-baseweb="select"] > div {
    border-radius: 14px;
}

.stButton > button,
.stDownloadButton > button {
    border-radius: 999px;
    padding: 0.7rem 1.3rem;
    font-weight: 600;
    border: 1px solid #D8D1C7;
    background: #FFFFFF;
    transition: all 0.2s ease;
}

.stButton > button:hover,
.stDownloadButton > button:hover {
    border-color: #9D8B72;
    transform: translateY(-1px);
}

div[data-testid="stFileUploader"] {
    border-radius: 18px;
}

hr {
    margin-top: 3rem !important;
    margin-bottom: 3rem !important;
}

</style>
""", unsafe_allow_html=True)

if "story" not in st.session_state:
    st.session_state.story = None

if "page_images" not in st.session_state:
    st.session_state.page_images = {}


if "story_settings" not in st.session_state:
    st.session_state.story_settings = {}


def prepare_arabic(text):
    reshaped = arabic_reshaper.reshape(text)
    return get_display(reshaped)


def wrap_arabic_text(text, font_name, font_size, max_width):
    words = text.split()
    lines = []
    current = ""

    for word in words:
        test = word if not current else current + " " + word
        shaped_test = prepare_arabic(test)

        if pdfmetrics.stringWidth(
            shaped_test,
            font_name,
            font_size
        ) <= max_width:
            current = test

        else:
            if current:
                lines.append(current)
            current = word

    if current:
        lines.append(current)

    return lines


def create_story_pdf(story, page_images):

    buffer = io.BytesIO()

    width, height = A4

    font_candidates = [
        os.path.expanduser("~/Library/Fonts/NotoKufiArabic[wght].ttf"),
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/noto/NotoKufiArabic-Regular.ttf",
        "/usr/share/fonts/opentype/noto/NotoKufiArabic-Regular.ttf",
    ]

    font_path = next(
        (p for p in font_candidates if os.path.exists(p)),
        None
    )

    if not font_path:
        for root, dirs, files in os.walk("/usr/share/fonts"):
            for file in files:
                if file.startswith("NotoKufiArabic") and file.endswith(".ttf"):
                    font_path = os.path.join(root, file)
                    break
            if font_path:
                break

    if not font_path:
        raise FileNotFoundError("Noto Kufi Arabic font not found")

    font_name = "NotoKufiArabic"

    if font_name not in pdfmetrics.getRegisteredFontNames():
        pdfmetrics.registerFont(
            TTFont(font_name, font_path)
        )

    c = canvas.Canvas(
        buffer,
        pagesize=A4
    )

    # ------------------
    # COVER
    # ------------------

    c.setFillColorRGB(
        0.96,
        0.93,
        0.88
    )

    c.rect(
        0,
        0,
        width,
        height,
        fill=1,
        stroke=0
    )

    first_image = page_images.get(1)

    if first_image:

        image = ImageReader(
            io.BytesIO(first_image)
        )

        cover_size = width * 0.72

        c.drawImage(
            image,
            (width - cover_size) / 2,
            height * 0.37,
            cover_size,
            cover_size,
            preserveAspectRatio=True,
            mask="auto"
        )

    title = prepare_arabic(
        story["title"]
    )

    c.setFillColorRGB(
        0.15,
        0.12,
        0.10
    )

    c.setFont(
        font_name,
        25
    )

    c.drawCentredString(
        width / 2,
        height * 0.25,
        title
    )

    c.setFont(
        font_name,
        11
    )

    c.setFillColorRGB(
        0.45,
        0.38,
        0.31
    )

    c.drawCentredString(
        width / 2,
        height * 0.18,
        prepare_arabic(
            "قصة صنعت خصيصاً لطفلك"
        )
    )

    c.showPage()

    # ------------------
    # STORY PAGES
    # ------------------

    for page in story["pages"]:

        page_number = page["page_number"]

        c.setFillColorRGB(
            1,
            0.99,
            0.97
        )

        c.rect(
            0,
            0,
            width,
            height,
            fill=1,
            stroke=0
        )

        image_bytes = page_images.get(
            page_number
        )

        if image_bytes:

            image = ImageReader(
                io.BytesIO(image_bytes)
            )

            image_width = width - 70
            image_height = height * 0.58

            c.drawImage(
                image,
                35,
                height - image_height - 45,
                image_width,
                image_height,
                preserveAspectRatio=True,
                anchor="c",
                mask="auto"
            )

        # Page number
        c.setFont(
            font_name,
            9
        )

        c.setFillColorRGB(
            0.62,
            0.53,
            0.44
        )

        c.drawRightString(
            width - 45,
            height * 0.31,
            prepare_arabic(
                f"الصفحة {page_number}"
            )
        )

        # Story text
        font_size = 14
        max_text_width = width - 90

        lines = wrap_arabic_text(
            page["text"],
            font_name,
            font_size,
            max_text_width
        )

        y = height * 0.27

        c.setFont(
            font_name,
            font_size
        )

        c.setFillColorRGB(
            0.22,
            0.18,
            0.15
        )

        for line in lines:

            c.drawRightString(
                width - 45,
                y,
                prepare_arabic(line)
            )

            y -= 27

        c.showPage()

    c.save()

    buffer.seek(0)

    return buffer.getvalue()





st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Alexandria:wght@400;500;600;700;800&family=Tajawal:wght@400;500;700;800&display=swap');

/* ROOTS WITH LAMA — STORY STUDIO */

html, body {
    direction: rtl;
}

.stApp {
    background:
        radial-gradient(circle at 90% 8%, rgba(214,177,211,.20), transparent 25%),
        radial-gradient(circle at 8% 18%, rgba(236,184,179,.18), transparent 25%),
        linear-gradient(180deg, #FFF9F5 0%, #FAF4F0 52%, #F8F3EE 100%);
    color: #4B3B42;
}

header[data-testid="stHeader"] {
    background: transparent;
}

.block-container {
    max-width: 920px;
    padding-top: 2rem;
    padding-bottom: 7rem;
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

h1, h2, h3, h4,
.story-title {
    font-family: "Alexandria", sans-serif !important;
    color: #624957 !important;
}

div[data-testid="stMarkdownContainer"],
div[data-testid="stMarkdownContainer"] p,
label,
label p {
    direction: rtl !important;
    text-align: right !important;
}

/* STORY INTRO */
.story-intro {
    position: relative;
    overflow: hidden;
    padding: 38px 42px;
    margin: 18px 0 38px 0;
    border-radius: 38px;
    background:
        linear-gradient(
            135deg,
            #F8D9D7 0%,
            #F2D9E5 45%,
            #E3D5F1 100%
        );
    border: 1px solid rgba(255,255,255,.85);
    box-shadow:
        0 28px 70px rgba(112,73,91,.13),
        inset 0 1px 0 rgba(255,255,255,.85);
}

.story-intro:before {
    content: "";
    position: absolute;
    width: 220px;
    height: 220px;
    border-radius: 50%;
    left: -90px;
    bottom: -120px;
    background: rgba(255,255,255,.23);
}

.story-brand {
    position: relative;
    color: #875F75;
    font-weight: 800;
    font-size: 12px;
    letter-spacing: 1.3px;
    margin-bottom: 14px;
}

.story-title {
    position: relative;
    font-size: 34px;
    font-weight: 800;
    line-height: 1.5;
    margin-bottom: 10px;
}

.story-subtitle {
    position: relative;
    color: #69545F;
    font-size: 17px;
    line-height: 2;
    max-width: 680px;
}

/* INPUTS */
div[data-testid="stTextInput"] input,
div[data-testid="stNumberInput"] input,
textarea {
    background: rgba(255,253,251,.92) !important;
    border: 1px solid #E8D8D7 !important;
    border-radius: 16px !important;
    color: #4B3B42 !important;
}

div[data-baseweb="select"] > div {
    background: rgba(255,253,251,.92) !important;
    border-color: #E8D8D7 !important;
    border-radius: 16px !important;
}

label p {
    color: #654F5A !important;
    font-weight: 700 !important;
}

/* FILE UPLOAD */
div[data-testid="stFileUploader"] {
    background: rgba(255,253,251,.72);
    border: 1px solid #E4D4DF;
    border-radius: 22px;
    padding: 10px;
}

div[data-testid="stFileUploaderDropzone"] {
    background: #FFFDFC !important;
    border: 1.5px dashed #CEB5C8 !important;
    border-radius: 18px !important;
}

/* BUTTONS */
.stButton > button {
    width: 100%;
    min-height: 54px;
    border: 0 !important;
    border-radius: 18px !important;
    background:
        linear-gradient(135deg, #875F75 0%, #9C748E 55%, #8B7198 100%) !important;
    color: white !important;
    font-size: 16px !important;
    font-weight: 800 !important;
    box-shadow: 0 14px 30px rgba(112,73,91,.20);
    transition: all .2s ease;
}

.stButton > button:hover {
    transform: translateY(-1px);
    box-shadow: 0 18px 34px rgba(112,73,91,.24);
}

/* DOWNLOAD BUTTONS */
div[data-testid="stDownloadButton"] > button {
    border-radius: 18px !important;
    border: 1px solid #D9C2D4 !important;
    background: #FFF9F8 !important;
    color: #704F61 !important;
    font-weight: 800 !important;
}

/* MESSAGES */
div[data-testid="stAlert"] {
    border-radius: 18px !important;
}

/* SIDEBAR */
section[data-testid="stSidebar"] {
    background:
        linear-gradient(180deg, #FFF9F7 0%, #F7EDF3 100%);
}

@media (max-width: 700px) {
    .story-intro {
        padding: 28px 24px;
        border-radius: 28px;
    }

    .story-title {
        font-size: 27px;
    }

    .story-subtitle {
        font-size: 15px;
    }
}
</style>

<div class="story-intro">
    <div class="story-brand">ROOTS WITH LAMA · جذور مع لمى</div>
    <div class="story-title">قصة معمولة خصيصاً لطفلك 📖</div>
    <div class="story-subtitle">
        تفاصيل صغيرة من عالم طفلك… ومنحوّلها لقصة يكون هو بطلها.
        اختاري اللي بتحبيه، والباقي علينا 🤍
    </div>
</div>
""", unsafe_allow_html=True)

name = st.text_input("اسم الطفل")

age = st.number_input(
    "العمر",
    min_value=2,
    max_value=10,
    value=4
)

favorite_color = st.text_input(
    "اللون المفضل",
    value="أزرق"
)

story_type = st.selectbox(
    "نوع القصة",
    [
        "Bedtime",
        "Adventure",
        "Confidence"
    ]
)

art_style = st.selectbox(
    "الستايل الفني",
    [
        "Storybook",
        "Comic",
        "3D Storybook"
    ]
)

interests = st.text_area(
    "شو الأشياء اللي بيحبها الطفل؟",
    placeholder="مثلاً: الديناصورات، السيارات، البحر..."
)

core_message = st.text_input(
    "شو بتحب القصة توصله للطفل؟",
    placeholder="مثلاً: الصبر، الشجاعة، الثقة بالنفس..."
)

st.markdown("""
<div style="
    background: linear-gradient(135deg, #FFF4F4 0%, #F7EDF8 100%);
    border: 1px solid #E7D2DF;
    border-radius: 22px;
    padding: 18px 20px;
    margin: 12px 0 14px 0;
    color: #604B57;
    line-height: 1.9;
">
    <div style="font-family: Alexandria, sans-serif; font-weight: 800; margin-bottom: 6px;">
        📷 صورة الطفل — اختيارية
    </div>
    <div style="font-size: 14px;">
        إذا رفعتي صورة، منستخدمها كمرجع أثناء إنشاء الرسومات فقط،
        وما منخزنها كملف دائم داخل التطبيق.
        <br>
        وإذا ما رفعتي صورة، منبتكر لطفلك شخصية تخيّلية خاصة بالقصة ✨
    </div>
</div>
""", unsafe_allow_html=True)

child_photo = st.file_uploader(
    "اختاري صورة إذا بتحبي",
    type=["jpg", "jpeg", "png"],
    label_visibility="collapsed"
)


if st.button("✨ اصنع قصتي"):

    if not name:
        st.warning("اكتب اسم الطفل أولاً.")

    else:

        prompt = f"""
You are a professional children's storybook author.

Write an original personalized 6-page children's story in Arabic.

CHILD INFORMATION

Name: {name}
Age: {age}
Favorite color: {favorite_color}
Story type: {story_type}
Preferred illustration style: {art_style}
Interests: {interests}
Emotional or developmental goal: {core_message}

IMPORTANT WRITING PRINCIPLES

Before writing the story, silently invent one original story premise.
Do not expose this planning step.

The story must feel like a real children's book written by a talented human author.

TITLE RULES

The title should feel like the title of a real children's book.

Do NOT automatically begin the title with the child's name.

Use the child's name in the title only when it genuinely makes the title
more charming, memorable, or important to the story.

Prefer imaginative titles that create curiosity.

Good title directions:
- a mysterious place
- a strange event
- a beautiful image
- an unusual object
- a small question
- a poetic moment from the story

Examples of the right feeling:
"حين نامت النجوم"
"سر الباب الصغير"
"ثلاث خطوات إلى القمر"
"آخر ديناصور قبل النوم"

Do not copy these examples.
Invent an original title for each story.

Avoid repetitive patterns such as:
"[child name] and the..."
"[child name] on the..."
"[child name] and the secret..."


Do not mechanically combine the user's inputs.

At least one interest of the child must meaningfully affect the plot.

If the user provides only one interest,
that interest MUST appear meaningfully in the story.

Do not replace the child's interest with something unrelated.

Do not mechanically put the interest in the title.

Never infer ethnicity, skin tone, hair color,
eye color, or physical appearance from the child's name,
language, or location.

Use the favorite color only as a subtle visual detail.

The emotional or developmental goal must be communicated
through events and actions.

Do not explain the lesson directly.

The child must be the hero.
The child should make decisions and move the story forward.

Respect the selected story type.

If the story type is Bedtime,
keep the rhythm gentle
and make the final two pages progressively calmer.

Avoid preachy language.
Avoid generic AI-style writing.
Avoid excessive moral explanation.

Write natural, warm Arabic suitable for a child aged {age}.

STORY STRUCTURE

Page 1:
Natural setup.

Page 2:
Discovery or invitation.

Page 3:
A small challenge.

Page 4:
An attempt that does not immediately work.

Page 5:
The child finds a way forward.

Page 6:
Warm emotional resolution.

Each page should be short enough for a real illustrated children's book.

ILLUSTRATION RULES

Every image prompt must use this art style:
{art_style}

Do not invent specific physical traits for the child.

Describe:
- scene
- action
- environment
- lighting
- emotion

No written words or captions inside illustrations.

Write the final story in Arabic.
"""

        with st.spinner("عم نكتب القصة... ✨"):

            try:

                response = client.responses.create(
                    model="gpt-5.6-luna",
                    input=prompt,
                    text={
                        "format": {
                            "type": "json_schema",
                            "name": "storybook",
                            "strict": True,
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "title": {
                                        "type": "string"
                                    },
                                    "pages": {
                                        "type": "array",
                                        "minItems": 6,
                                        "maxItems": 6,
                                        "items": {
                                            "type": "object",
                                            "properties": {
                                                "page_number": {
                                                    "type": "integer"
                                                },
                                                "text": {
                                                    "type": "string"
                                                },
                                                "image_prompt": {
                                                    "type": "string"
                                                }
                                            },
                                            "required": [
                                                "page_number",
                                                "text",
                                                "image_prompt"
                                            ],
                                            "additionalProperties": False
                                        }
                                    }
                                },
                                "required": [
                                    "title",
                                    "pages"
                                ],
                                "additionalProperties": False
                            }
                        }
                    }
                )

                st.session_state.story = json.loads(
                    response.output_text
                )

                st.session_state.page_images = {}

                st.session_state.story_settings = {
                    "name": name,
                    "age": age,
                    "art_style": art_style
                }

                st.success("القصة جاهزة! 🎉")

            except Exception as error:
                st.error("صار خطأ أثناء إنشاء القصة.")
                st.code(str(error))


if st.session_state.story is not None:

    story = st.session_state.story

    st.divider()

    st.header(story["title"])

    st.info(
        "إذا رغبتِ، يمكنك رفع صورة الطفل لنستخدمها كمرجع بصري. وإذا تركتِ الحقل فارغاً، سننشئ رسومات القصة بشخصية تخيّلية مناسبة."
    )

    if st.button("🎨 ولّد الكتاب كامل"):

        temp_path = None

        progress = st.progress(0)

        status = st.empty()

        try:

            st.session_state.page_images = {}

            if child_photo is not None:

                suffix = (
                    ".png"
                    if child_photo.type == "image/png"
                    else ".jpg"
                )

                with tempfile.NamedTemporaryFile(
                    delete=False,
                    suffix=suffix
                ) as temp_file:

                    temp_file.write(
                        child_photo.getvalue()
                    )

                    temp_path = temp_file.name

            for index, page in enumerate(story["pages"]):

                page_number = page["page_number"]

                status.write(
                    f"🎨 عم نرسم الصفحة {page_number} من 6..."
                )

                if child_photo is not None:

                    image_prompt = f"""
Use the uploaded photo as the strict identity reference.

Create one illustration for a premium personalized children's storybook.

This is PAGE {page_number}.

IMPORTANT IDENTITY RULES:

The person in the uploaded reference photo must remain
recognizably the same person in every illustration.

Preserve:
- facial structure
- eyes
- nose
- mouth
- hairstyle
- natural skin tone
- recognizable identity

The person is the hero of the story scene.

Ignore any generic physical description in the scene prompt
if it conflicts with the uploaded reference photo.

SCENE:

{page["image_prompt"]}

No written words.
No captions.
No letters.
No text inside the illustration.
"""

                    with open(
                        temp_path,
                        "rb"
                    ) as reference_image:

                        image_result = client.images.edit(
                            model="gpt-image-2.5-sunburst",
                            image=reference_image,
                            prompt=image_prompt,
                            size="1024x1024",
                            quality="medium",
                            output_format="png"
                        )

                else:

                    image_prompt = f"""
Create one illustration for a premium personalized children's storybook.

This is PAGE {page_number}.

The child is the hero of the story scene.

IMPORTANT CHARACTER RULES:

- Invent a warm, appealing child character appropriate for a child aged {age}.
- Do not base the child on a real uploaded person.
- Keep the same overall child identity, age feeling, hairstyle, outfit palette, and illustration style consistently across all pages of the same book.
- Use touches of the favorite color "{favorite_color}" in clothing or visual details when appropriate.
- Respect the selected illustration style: {art_style}.

SCENE:

{page["image_prompt"]}

No written words.
No captions.
No letters.
No text inside the illustration.
"""

                    image_result = client.images.generate(
                        model="gpt-image-2.5-sunburst",
                        prompt=image_prompt,
                        size="1024x1024",
                        quality="medium",
                        output_format="png"
                    )

                image_bytes = base64.b64decode(
                    image_result.data[0].b64_json
                )

                st.session_state.page_images[
                    page_number
                ] = image_bytes

                progress.progress(
                    (index + 1) / 6
                )

            status.success(
                "📖 الكتاب صار جاهز!"
            )

        except Exception as error:

            st.error(
                "صار خطأ أثناء إنشاء الرسومات."
            )

            st.code(
                str(error)
            )

        finally:

            if temp_path and os.path.exists(temp_path):
                os.remove(temp_path)




    if len(st.session_state.page_images) == 6:

        st.divider()

        st.markdown("""
        <div class="book-title">
            <div class="book-kicker">📖 قصتك</div>
        </div>
        """, unsafe_allow_html=True)

        for page in story["pages"]:

            page_number = page["page_number"]

            image_bytes = st.session_state.page_images[
                page_number
            ]

            st.markdown(
                f"""
                <div class="storybook-page">
                    <div class="page-number">الصفحة {page_number}</div>
                """,
                unsafe_allow_html=True
            )

            st.image(
                image_bytes,
                use_container_width=True
            )

            st.markdown(
                f"""
                    <div class="page-text">
                        {page["text"]}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

    else:

        st.caption(
            "بعد توليد الرسومات رح يظهر الكتاب هون كصفحات كاملة."
        )


    st.divider()
    st.subheader("⬇️ تحميل القصة")

    # Download story JSON
    story_json = json.dumps(
        story,
        ensure_ascii=False,
        indent=2
    ).encode("utf-8")

    st.download_button(
        label="📄 تحميل القصة JSON",
        data=story_json,
        file_name="story.json",
        mime="application/json"
    )

    # Download all generated images as ZIP
    if len(st.session_state.page_images) > 0:

        zip_buffer = io.BytesIO()

        with zipfile.ZipFile(
            zip_buffer,
            "w",
            zipfile.ZIP_DEFLATED
        ) as zip_file:

            for page_number, image_bytes in st.session_state.page_images.items():

                zip_file.writestr(
                    f"page_{page_number}.png",
                    image_bytes
                )

        zip_buffer.seek(0)

        st.download_button(
            label="🖼️ تحميل كل الصور ZIP",
            data=zip_buffer,
            file_name="story_images.zip",
            mime="application/zip"
        )

        if len(st.session_state.page_images) == 6:

            try:

                pdf_bytes = create_story_pdf(
                    story,
                    st.session_state.page_images
                )

                st.download_button(
                    label="📖 تحميل الكتاب PDF",
                    data=pdf_bytes,
                    file_name="my_story.pdf",
                    mime="application/pdf"
                )

            except Exception as pdf_error:

                st.error(
                    "صار خطأ أثناء تجهيز ملف PDF."
                )

                st.code(
                    str(pdf_error)
                )
