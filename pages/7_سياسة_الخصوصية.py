import streamlit as st

st.set_page_config(
    page_title="سياسة الخصوصية",
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
<div class="legal-title">سياسة الخصوصية</div>

<p>
نحترم خصوصية العائلة والطفل، ونحاول جمع أقل قدر من المعلومات اللازمة
لتقديم التجربة المطلوبة.
</p>

<h2>1. المعلومات التي قد يتم إدخالها</h2>

<ul>
<li>اسم الطفل أو الاسم الذي يختاره المستخدم.</li>
<li>العمر.</li>
<li>تفاصيل عن الروتين أو الموقف الذي يواجه الأسرة.</li>
<li>اهتمامات الطفل وتفضيلاته.</li>
<li>صورة اختيارية عند استخدام خدمة القصص.</li>
<li>معلومات التواصل التي يرسلها المستخدم طوعاً.</li>
</ul>

<h2>2. لماذا نستخدم هذه المعلومات؟</h2>

<p>
تستخدم المعلومات لتخصيص المحتوى، إنشاء الخطط والقصص، تحسين التجربة،
والرد على استفسارات المستخدمين.
</p>

<h2>3. استخدام الذكاء الاصطناعي</h2>

<p>
قد تتم معالجة بعض المعلومات بواسطة مزودي خدمات ذكاء اصطناعي وتقنية
من أجل إنشاء الردود، الخطط أو الصور المطلوبة.
</p>

<p>
قد يخضع هذا النوع من المعالجة أيضاً لسياسات الخصوصية الخاصة بمزود الخدمة التقني.
</p>

<h2>4. صور الأطفال</h2>

<p>
رفع الصورة اختياري.
عند رفع صورة لإنشاء قصة شخصية، يستخدم التطبيق الصورة كمرجع أثناء عملية إنشاء الرسومات.
</p>

<p>
التطبيق لا يحتفظ بالنسخة المؤقتة من الصورة كملف دائم بعد انتهاء عملية التوليد.
وقد تتم معالجة الصورة أثناء الإنشاء بواسطة مزود الخدمة التقني المستخدم لتوليد الصور.
</p>

<h2>5. مشاركة وبيع البيانات</h2>

<p>
لا نبيع المعلومات الشخصية للمستخدمين لأغراض إعلانية.
قد تتم مشاركة البيانات التقنية اللازمة فقط مع مقدمي الخدمات الذين يعتمد عليهم الموقع
لتشغيل الوظائف المطلوبة.
</p>

<h2>6. معلومات الأطفال</h2>

<p>
Roots with Lama موجه للأهل ومقدمي الرعاية.
يجب أن يتم إدخال معلومات الطفل بواسطة شخص بالغ مخول بذلك.
</p>

<h2>7. الأمان</h2>

<p>
نستخدم وسائل تقنية معقولة لحماية المعلومات، لكن لا توجد خدمة إلكترونية يمكنها
ضمان أمان كامل بنسبة 100%.
</p>

<h2>8. السجلات التقنية</h2>

<p>
قد تقوم منصات الاستضافة والخدمات التقنية المستخدمة بتسجيل بعض البيانات الفنية
مثل عنوان الشبكة، نوع الجهاز أو سجلات الأخطاء لأغراض التشغيل والأمان.
</p>

<h2>9. طلبات الخصوصية</h2>

<p>
يمكن للمستخدم التواصل معنا بخصوص أي استفسار متعلق ببياناته أو خصوصيته
من خلال صفحة «تواصل معنا».
</p>

<h2>10. تحديث السياسة</h2>

<p>
قد يتم تحديث سياسة الخصوصية مع تطور Roots with Lama وإضافة خدمات جديدة.
</p>

<p><strong>آخر تحديث: سبتمبر 2026</strong></p>

</div>
""", unsafe_allow_html=True)
