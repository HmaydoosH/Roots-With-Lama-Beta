import os
import urllib.parse
import urllib.request

import streamlit as st
from dotenv import load_dotenv


st.set_page_config(
    page_title="تواصل معنا",
    page_icon="💌",
    layout="centered"
)

load_dotenv()

if not os.getenv("FORMSPREE_ENDPOINT"):
    try:
        os.environ["FORMSPREE_ENDPOINT"] = st.secrets["FORMSPREE_ENDPOINT"]
    except Exception:
        pass


st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Alexandria:wght@500;600;700;800&family=Tajawal:wght@400;500;700&display=swap');

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

.block-container {
    max-width: 820px;
    padding-top: 7rem;
    padding-bottom: 7rem;
}

.contact-card {
    background: linear-gradient(135deg, #FFF4F4 0%, #F4EAF7 100%);
    border: 1px solid #E3D0DC;
    border-radius: 34px;
    padding: 34px 38px;
    margin-bottom: 28px;
    box-shadow: 0 22px 60px rgba(112,73,91,.10);
}

.contact-title {
    font-family: "Alexandria", sans-serif;
    color: #624957;
    font-size: 32px;
    font-weight: 800;
    margin-bottom: 12px;
}

.contact-text {
    font-family: "Tajawal", sans-serif;
    color: #69545F;
    font-size: 16px;
    line-height: 2;
}

.stApp,
input,
textarea,
button,
label {
    font-family: "Tajawal", sans-serif !important;
}

label p {
    direction: rtl !important;
    text-align: right !important;
    color: #654F5A !important;
    font-weight: 700 !important;
}

input, textarea {
    background: rgba(255,253,251,.95) !important;
    border: 1px solid #E3D2DA !important;
    border-radius: 16px !important;
}

.stButton > button,
div[data-testid="stFormSubmitButton"] > button {
    width: 100% !important;
    min-height: 54px !important;
    border: 0 !important;
    border-radius: 18px !important;
    background: linear-gradient(135deg, #875F75 0%, #9C748E 55%, #8B7198 100%) !important;
    color: white !important;
    font-weight: 800 !important;
    font-size: 16px !important;
}

.roots-home-button {
    position: fixed;
    top: 18px;
    left: 20px;
    z-index: 999999;
    padding: 10px 16px;
    border-radius: 18px;
    background: rgba(255,249,247,.95);
    border: 1px solid #E4CFDA;
    color: #704F61 !important;
    text-decoration: none !important;
    font-family: "Tajawal", sans-serif;
    font-weight: 800;
    box-shadow: 0 8px 24px rgba(112,73,91,.13);
}

@media (max-width:700px) {
    .contact-card {
        padding: 28px 22px;
        border-radius: 27px;
    }

    .contact-title {
        font-size: 27px;
    }

    .roots-home-button {
        top: 12px;
        left: 12px;
        font-size: 12px;
        padding: 8px 12px;
    }
}

/* FINAL RTL ALIGNMENT */
.legal-card,
.legal-title,
.legal-card h2,
.legal-card p,
.legal-card li,
.contact-card,
.contact-title,
.contact-text,
div[data-testid="stMarkdownContainer"],
div[data-testid="stMarkdownContainer"] h1,
div[data-testid="stMarkdownContainer"] h2,
div[data-testid="stMarkdownContainer"] h3,
label,
label p {
    direction: rtl !important;
    text-align: right !important;
}

</style>

<a class="roots-home-button" href="/" target="_self">
← الرجوع للصفحة الرئيسية
</a>

<div class="contact-card">
    <div class="contact-title">احكي معنا 💌</div>
    <div class="contact-text">
        عندك سؤال، اقتراح، ملاحظة أو تجربة حابة تشاركينا ياها؟
        اكتبي لنا هون، ورسالتك رح توصل لفريق Roots with Lama مباشرة.
    </div>
</div>
""", unsafe_allow_html=True)


with st.form("contact_form", clear_on_submit=True):

    name = st.text_input(
        "الاسم",
        placeholder="اسمك"
    )

    email = st.text_input(
        "الإيميل",
        placeholder="name@example.com"
    )

    message = st.text_area(
        "رسالتك",
        placeholder="اكتبي كل اللي حابة تقوليه...",
        height=190
    )

    submitted = st.form_submit_button(
        "💌 إرسال الرسالة"
    )


if submitted:

    if not email.strip():
        st.warning("اكتبي إيميلك حتى نقدر نتواصل معك.")

    elif "@" not in email:
        st.warning("تأكدي إن الإيميل مكتوب بشكل صحيح.")

    elif not message.strip():
        st.warning("اكتبي رسالتك أولاً.")

    else:

        endpoint = os.getenv("FORMSPREE_ENDPOINT")

        if not endpoint:
            st.error("خدمة التواصل غير مفعّلة حالياً.")

        else:
            try:
                data = urllib.parse.urlencode({
                    "name": name.strip(),
                    "email": email.strip(),
                    "message": message.strip(),
                    "_subject": "رسالة جديدة من Roots with Lama"
                }).encode("utf-8")

                request = urllib.request.Request(
                    endpoint,
                    data=data,
                    method="POST",
                    headers={
                        "Accept": "application/json",
                        "Content-Type": "application/x-www-form-urlencoded"
                    }
                )

                with urllib.request.urlopen(
                    request,
                    timeout=20
                ) as response:
                    status = response.status

                if 200 <= status < 300:
                    st.success(
                        "وصلتنا رسالتك 🤍 شكراً إلك، ومنرجعلك بأقرب وقت."
                    )
                else:
                    st.error(
                        "ما قدرنا نبعت الرسالة حالياً. جربي مرة ثانية."
                    )

            except Exception as error:
                st.error(
                    "صار خطأ أثناء إرسال الرسالة. جربي مرة ثانية بعد شوي."
                )
