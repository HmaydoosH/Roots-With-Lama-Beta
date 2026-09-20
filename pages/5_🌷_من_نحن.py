import streamlit as st

st.set_page_config(
    page_title="من نحن؟",
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
    padding-bottom: 7rem;
}

.legal-card {
    background: rgba(255,253,251,.88);
    border: 1px solid #E6D6DE;
    border-radius: 34px;
    padding: 42px 44px;
    box-shadow: 0 22px 60px rgba(112,73,91,.10);
}

.legal-title {
    font-family: "Alexandria", sans-serif;
    color: #624957;
    font-size: 32px;
    font-weight: 800;
    margin-bottom: 28px;
}

.legal-card h2 {
    font-family: "Alexandria", sans-serif;
    color: #765669;
    font-size: 19px;
    margin-top: 30px;
}

.legal-card p,
.legal-card li {
    font-family: "Tajawal", sans-serif;
    color: #64515B;
    font-size: 16px;
    line-height: 2;
}

.legal-card ul {
    padding-right: 22px;
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
    .legal-card {
        padding: 30px 23px;
        border-radius: 27px;
    }

    .legal-title {
        font-size: 26px;
    }

    .roots-home-button {
        top:12px;
        left:12px;
        font-size:12px;
        padding:8px 12px;
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

<div class="legal-card">
<div class="legal-title">من نحن؟</div>

<p>
Roots with Lama · جذور مع لمى هي مساحة عربية مصممة لتساعد الأهل على فهم أطفالهم
بطريقة أقرب لواقع الحياة اليومية.
</p>

<p>
الفكرة بسيطة: بدل النصائح العامة والوصفات الجاهزة، نحاول نفهم الموقف الذي يمر فيه
طفلك، عمره، روتينه وما جربتموه سابقاً، ثم نحول هذه التفاصيل إلى خطوات عملية قابلة للتطبيق.
</p>

<h2>شو منقدّم؟</h2>

<ul>
<li>إرشاد شخصي للمواقف اليومية مع الطفل.</li>
<li>خطط مخصصة تساعد الأسرة تبدأ بخطوات صغيرة وواضحة.</li>
<li>قصص شخصية يكون الطفل بطلها.</li>
<li>بطاقات وأدوات تعليمية للعائلة.</li>
<li>استشارات شخصية مع لمى عند الحاجة.</li>
</ul>

<h2>فلسفتنا</h2>

<p>
ما في طفلين متشابهين تماماً، وما في طريقة واحدة مناسبة لكل العائلات.
هدفنا هو القرب والفهم والتخصيص، بدون أحكام وبدون وعود سحرية.
</p>

<p>
Roots with Lama لا يستبدل التقييم الطبي أو النفسي أو التخصصي عند الحاجة،
وإنما يقدّم دعماً وإرشاداً عملياً للأهل في الحياة اليومية.
</p>

</div>
""", unsafe_allow_html=True)
