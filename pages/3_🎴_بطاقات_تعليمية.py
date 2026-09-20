import streamlit as st

st.set_page_config(
    page_title="🎴 احصلي على بطاقات تعليمية",
    page_icon="🌷",
    layout="centered"
)

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
    max-width: 900px;
    padding-top: 7rem;
}

.placeholder-card {
    background: linear-gradient(135deg, #F8D9D7 0%, #F2D9E5 45%, #E3D5F1 100%);
    border-radius: 36px;
    padding: 48px 42px;
    border: 1px solid rgba(255,255,255,.85);
    box-shadow: 0 28px 70px rgba(112,73,91,.13);
    text-align: right;
}

.placeholder-title {
    font-family: "Alexandria", sans-serif;
    color: #624957;
    font-size: 34px;
    font-weight: 800;
    margin-bottom: 16px;
}

.placeholder-text {
    font-family: "Tajawal", sans-serif;
    color: #69545F;
    font-size: 18px;
    line-height: 2;
}

.coming {
    display: inline-block;
    margin-top: 24px;
    padding: 9px 16px;
    border-radius: 16px;
    background: rgba(255,255,255,.65);
    color: #875F75;
    font-family: "Tajawal", sans-serif;
    font-weight: 700;
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

@media (max-width: 700px) {
    .placeholder-card {
        padding: 34px 24px;
        border-radius: 28px;
    }

    .placeholder-title {
        font-size: 27px;
    }

    .roots-home-button {
        top: 12px;
        left: 12px;
        font-size: 12px;
        padding: 8px 12px;
    }
}
</style>

<a class="roots-home-button" href="/" target="_self">
← الرجوع للصفحة الرئيسية
</a>

<div class="placeholder-card">
    <div class="placeholder-title">🎴 احصلي على بطاقات تعليمية</div>
    <div class="placeholder-text">بطاقات مصممة لتدعم التعلّم والروتين اليومي بطريقة بسيطة وقريبة من عالم طفلك.</div>
    <div class="coming">قريباً 🌷</div>
</div>
""", unsafe_allow_html=True)
