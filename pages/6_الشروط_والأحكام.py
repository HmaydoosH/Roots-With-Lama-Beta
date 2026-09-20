import streamlit as st

st.set_page_config(
    page_title="الشروط والأحكام",
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
<div class="legal-title">الشروط والأحكام</div>

<p>
باستخدامك لموقع Roots with Lama فإنك توافق على الشروط التالية.
إذا كنت لا توافق على أي جزء منها، يرجى عدم استخدام الخدمة.
</p>

<h2>1. طبيعة الخدمة</h2>

<p>
يوفّر Roots with Lama محتوى وإرشاداً عاماً ومخصصاً للأهل، بما في ذلك الخطط،
القصص، الأدوات التعليمية والخدمات المرتبطة بالتربية والحياة اليومية مع الأطفال.
</p>

<h2>2. المحتوى المُنشأ بالذكاء الاصطناعي</h2>

<p>
قد يتم إنشاء أو مساعدة بعض المحتوى باستخدام تقنيات الذكاء الاصطناعي.
ورغم بذل الجهد لجعل النتائج مفيدة ومناسبة، قد تحتوي النتائج أحياناً على أخطاء
أو معلومات غير مناسبة لحالة محددة.
</p>

<p>
يبقى القرار النهائي في تطبيق أي اقتراح مسؤولية ولي الأمر.
</p>

<h2>3. ليس بديلاً عن الرعاية المتخصصة</h2>

<p>
المحتوى الموجود في Roots with Lama لا يشكل تشخيصاً طبياً أو نفسياً أو علاجياً،
ولا يحل محل الطبيب أو الأخصائي أو خدمات الطوارئ.
</p>

<p>
في الحالات التي تتضمن خطراً فورياً أو مشكلة صحية أو نفسية مقلقة،
ينبغي التواصل مع الجهة المختصة المناسبة.
</p>

<h2>4. دقة المعلومات</h2>

<p>
تعتمد جودة التخصيص على المعلومات التي يقدمها المستخدم.
المستخدم مسؤول عن تقديم معلومات صحيحة بقدر الإمكان عن الحالة التي يريد المساعدة فيها.
</p>

<h2>5. استخدام الصور</h2>

<p>
قد يكون رفع صورة الطفل اختيارياً في بعض الخدمات مثل القصص المخصصة.
تستخدم الصورة لإنشاء المحتوى المطلوب وفق ما هو موضح في سياسة الخصوصية.
</p>

<h2>6. الاستخدام المقبول</h2>

<p>
لا يجوز استخدام الموقع أو محتواه لأغراض غير قانونية، مسيئة، احتيالية،
أو بطريقة تنتهك حقوق الآخرين أو خصوصيتهم.
</p>

<h2>7. الملكية الفكرية</h2>

<p>
تصميم الموقع، الهوية البصرية، النصوص الأصلية والأدوات الخاصة بـ Roots with Lama
محمية بحقوق أصحابها.
</p>

<p>
المحتوى الشخصي الذي يتم إنشاؤه للمستخدم، مثل الخطة أو القصة، مخصص للاستخدام
الشخصي والعائلي ما لم يتم الاتفاق على غير ذلك.
</p>

<h2>8. الخدمات الخارجية</h2>

<p>
قد يعتمد الموقع على مزودي خدمات تقنيين مثل الاستضافة أو خدمات الذكاء الاصطناعي.
قد يخضع استخدام هذه الخدمات لسياسات وشروط مقدميها.
</p>

<h2>9. توفر الخدمة</h2>

<p>
نسعى إلى إبقاء الخدمة متاحة ومستقرة، لكن لا نضمن عدم وجود توقفات مؤقتة،
تحديثات أو أخطاء تقنية.
</p>

<h2>10. المنتجات المدفوعة</h2>

<p>
عند توفير خدمات أو منتجات مدفوعة مستقبلاً، سيتم عرض السعر والشروط المطبقة
وسياسة الإلغاء أو الاسترداد قبل إتمام عملية الشراء.
</p>

<h2>11. تحديد المسؤولية</h2>

<p>
يتم تقديم الخدمة بهدف الدعم والمساعدة. لا يتحمل Roots with Lama مسؤولية القرارات
التي يتم اتخاذها اعتماداً على المحتوى دون مراعاة ظروف الطفل والأسرة أو الحاجة
إلى رأي متخصص.
</p>

<h2>12. تعديل الشروط</h2>

<p>
قد يتم تحديث هذه الشروط من وقت لآخر مع تطور الخدمة.
استمرار استخدام الموقع بعد التحديث يعني قبول النسخة الجديدة من الشروط.
</p>

<p><strong>آخر تحديث: سبتمبر 2026</strong></p>

</div>
""", unsafe_allow_html=True)
