import hmac
import html
import os
from collections import Counter, defaultdict
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

import streamlit as st
from dotenv import load_dotenv

from analytics import get_events


st.set_page_config(
    page_title="Roots Dashboard",
    page_icon="🌱",
    layout="wide",
)

load_dotenv(dotenv_path=".env")

UAE_TZ = ZoneInfo("Asia/Dubai")
NOW_UAE = datetime.now(UAE_TZ)


# --------------------------------------------------
# DESIGN
# --------------------------------------------------

st.markdown(
    """
    <style>
    html, body, [class*="css"] {
        direction: rtl;
        text-align: right;
    }

    .stApp {
        background:
            radial-gradient(circle at 12% 0%, rgba(245, 228, 239, 0.78), transparent 30%),
            radial-gradient(circle at 92% 4%, rgba(232, 226, 247, 0.78), transparent 28%),
            #fffaf6;
        color: #52364f;
    }

    [data-testid="stMainBlockContainer"] {
        direction: rtl !important;
        text-align: right !important;
        max-width: 1240px;
        padding-top: 1.7rem;
        padding-bottom: 4rem;
    }

    [data-testid="stMarkdownContainer"],
    [data-testid="stHeading"],
    [data-testid="stWidgetLabel"],
    h1, h2, h3, p {
        direction: rtl !important;
        text-align: right !important;
    }

    [data-testid="stHorizontalBlock"] {
        direction: rtl !important;
    }

    h1, h2, h3 {
        color: #633a62;
    }

    .roots-hero {
        background: linear-gradient(135deg, rgba(255, 244, 239, 0.96), rgba(242, 234, 250, 0.96));
        border: 1px solid #eaddea;
        border-radius: 28px;
        padding: 28px 30px;
        margin-bottom: 20px;
        box-shadow: 0 10px 35px rgba(99, 58, 98, 0.06);
    }

    .roots-hero-title {
        font-size: 2rem;
        font-weight: 800;
        color: #633a62;
        margin-bottom: 6px;
    }

    .roots-hero-subtitle {
        color: #846f7f;
        font-size: 0.98rem;
    }

    .roots-note {
        background: rgba(255, 255, 255, 0.72);
        border: 1px solid #eee1e9;
        border-radius: 18px;
        padding: 14px 16px;
        color: #735d70;
        margin: 10px 0 18px 0;
    }

    [data-testid="stMetric"] {
        background: rgba(255, 255, 255, 0.9);
        border: 1px solid #eadde8;
        border-radius: 22px;
        padding: 18px 19px;
        box-shadow: 0 8px 25px rgba(99, 58, 98, 0.055);
        direction: rtl !important;
        text-align: right !important;
        min-height: 118px;
    }

    [data-testid="stMetricLabel"],
    [data-testid="stMetricValue"],
    [data-testid="stMetricDelta"] {
        width: 100% !important;
        direction: rtl !important;
        text-align: right !important;
    }

    [data-testid="stMetricValue"] {
        color: #633a62;
    }

    .st-key-time_filter button {
        border-radius: 14px !important;
        min-height: 42px;
    }

    .roots-section-card {
        background: rgba(255,255,255,0.78);
        border: 1px solid #eee2eb;
        border-radius: 22px;
        padding: 17px 18px;
        margin: 8px 0;
    }

    .roots-funnel-row {
        background: rgba(255,255,255,0.82);
        border: 1px solid #eee2eb;
        border-radius: 16px;
        padding: 13px 15px;
        margin: 8px 0 6px 0;
    }

    .roots-funnel-title {
        font-weight: 750;
        color: #633a62;
    }

    .roots-funnel-meta {
        color: #80697b;
        font-size: 0.91rem;
        margin-top: 4px;
    }

    .roots-activity {
        background: rgba(255,255,255,0.76);
        border: 1px solid #efe4ec;
        border-radius: 16px;
        padding: 12px 14px;
        margin-bottom: 8px;
    }

    .roots-activity-title {
        color: #633a62;
        font-weight: 700;
    }

    .roots-activity-meta {
        color: #8d7988;
        font-size: 0.86rem;
        margin-top: 2px;
    }

    .roots-mini-label {
        color: #846f7f;
        font-size: 0.85rem;
    }

    .roots-mini-value {
        color: #633a62;
        font-weight: 800;
        font-size: 1.35rem;
    }

    div[data-testid="stProgress"] > div > div > div > div {
        border-radius: 999px;
    }

    .stButton button,
    .stDownloadButton button {
        border-radius: 14px !important;
    }

    @media (max-width: 700px) {
        .roots-hero {
            padding: 22px 20px;
        }

        .roots-hero-title {
            font-size: 1.6rem;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# --------------------------------------------------
# PASSWORD
# --------------------------------------------------


def get_secret(name):
    value = os.getenv(name)
    if value:
        return value

    try:
        return st.secrets[name]
    except Exception:
        return None


dashboard_password = get_secret("DASHBOARD_PASSWORD")

if not dashboard_password:
    st.error("Dashboard password is not configured.")
    st.stop()

if "dashboard_authenticated" not in st.session_state:
    st.session_state.dashboard_authenticated = False

if not st.session_state.dashboard_authenticated:
    st.markdown(
        """
        <div class="roots-hero">
            <div class="roots-hero-title">🌱 Roots Dashboard</div>
            <div class="roots-hero-subtitle">لوحة الإدارة الخاصة بـ Roots with Lama</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    password_input = st.text_input("كلمة السر", type="password")

    if st.button("دخول", type="primary", use_container_width=True):
        if hmac.compare_digest(password_input, dashboard_password):
            st.session_state.dashboard_authenticated = True
            st.rerun()
        else:
            st.error("كلمة السر غير صحيحة.")

    st.stop()


# --------------------------------------------------
# HELPERS
# --------------------------------------------------


def event_datetime(event):
    raw = event.get("created_at")
    if not raw:
        return None

    try:
        dt = datetime.fromisoformat(str(raw).replace("Z", "+00:00"))
        return dt.astimezone(UAE_TZ)
    except Exception:
        return None


def unique_sessions(items):
    return {
        event.get("session_id")
        for event in items
        if event.get("session_id")
    }


def percentage(part, total):
    if not total:
        return 0.0
    return round((part / total) * 100, 1)


def safe_text(value):
    return html.escape(str(value))


def format_time(dt):
    if not dt:
        return "وقت غير معروف"

    value = dt.strftime("%d/%m/%Y · %I:%M %p")
    return value.replace("AM", "ص").replace("PM", "م")


def page_label(page_name):
    labels = {
        "home": "الصفحة الرئيسية",
        "story_studio": "استوديو القصة",
        "consultation": "الاستشارة",
        "cards": "البطاقات التعليمية",
        "about": "من نحن",
        "contact": "تواصل معنا",
    }
    return labels.get(page_name, page_name or "—")


def event_label(event_name):
    labels = {
        "page_view": "👀 زيارة صفحة",
        "lama_request": "🌿 طلب مساعدة من لمى",
        "lama_response": "💡 استجابة لمى",
        "plan_created": "📋 إنشاء خطة",
        "plan_pdf_ready": "📄 تجهيز PDF للخطة",
        "story_created": "📖 إنشاء قصة",
        "story_images_generated": "🎨 إنشاء كتاب مصوّر",
        "story_pdf_ready": "📚 تجهيز PDF للقصة",
        "consultation_click": "💬 اهتمام بالاستشارة",
        "cards_click": "🎴 اهتمام بالبطاقات",
        "feedback_submitted": "💜 إرسال ملاحظة",
        "contact_submitted": "✉️ إرسال رسالة",
    }
    return labels.get(event_name, event_name or "—")


def filter_events(all_events, choice):
    if choice == "كل الوقت":
        return all_events

    output = []

    for event in all_events:
        dt = event_datetime(event)
        if dt is None:
            continue

        if choice == "اليوم" and dt.date() == NOW_UAE.date():
            output.append(event)
        elif choice == "آخر 7 أيام" and dt >= NOW_UAE - timedelta(days=7):
            output.append(event)
        elif choice == "آخر 30 يوم" and dt >= NOW_UAE - timedelta(days=30):
            output.append(event)

    return output


def events_named(items, name):
    return [event for event in items if event.get("event_name") == name]


# --------------------------------------------------
# DATA
# --------------------------------------------------

raw_events = get_events(limit=10000)

# Keep manual smoke tests out of product analytics.
raw_events = [
    event
    for event in raw_events
    if event.get("event_name") != "test_event"
]

st.markdown(
    f"""
    <div class="roots-hero">
        <div class="roots-hero-title">🌱 Roots Dashboard</div>
        <div class="roots-hero-subtitle">
            قراءة سريعة لاستخدام النسخة التجريبية · آخر تحديث {safe_text(format_time(NOW_UAE))}
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

if "dashboard_time_filter" not in st.session_state:
    st.session_state.dashboard_time_filter = "كل الوقت"

st.markdown("**الفترة**")

with st.container(key="time_filter"):
    f1, f2, f3, f4 = st.columns(4, gap="small")

    filter_buttons = [
        (f1, "اليوم"),
        (f2, "آخر 7 أيام"),
        (f3, "آخر 30 يوم"),
        (f4, "كل الوقت"),
    ]

    for column, label in filter_buttons:
        if column.button(
            label,
            use_container_width=True,
            type=(
                "primary"
                if st.session_state.dashboard_time_filter == label
                else "secondary"
            ),
        ):
            st.session_state.dashboard_time_filter = label
            st.rerun()

filter_choice = st.session_state.dashboard_time_filter
events = filter_events(raw_events, filter_choice)

if not raw_events:
    st.info("لسا ما في أي أحداث Analytics محفوظة في Supabase.")

if not events:
    st.info("ما في نشاط ضمن الفترة المختارة.")


# --------------------------------------------------
# CORE EVENT GROUPS
# --------------------------------------------------

page_views = events_named(events, "page_view")
lama_requests = events_named(events, "lama_request")
plans_created = events_named(events, "plan_created")
stories_created = events_named(events, "story_created")
books_generated = events_named(events, "story_images_generated")

sessions = unique_sessions(events)
home_sessions = unique_sessions(
    [
        event
        for event in page_views
        if event.get("page_name") == "home"
    ]
)
lama_sessions = unique_sessions(lama_requests)
plan_sessions = unique_sessions(plans_created)
story_sessions = unique_sessions(stories_created)
book_sessions = unique_sessions(books_generated)


# --------------------------------------------------
# MAIN METRICS
# --------------------------------------------------

m1, m2, m3 = st.columns(3)
m1.metric("👩‍👧 الجلسات", len(sessions))
m2.metric("👀 مشاهدات الصفحات", len(page_views))
m3.metric("🌿 طلبات لمى", len(lama_requests))

m4, m5, m6 = st.columns(3)
m4.metric("📋 الخطط المنشأة", len(plans_created))
m5.metric("📖 القصص المنشأة", len(stories_created))
m6.metric("🎨 الكتب المصوّرة", len(books_generated))


# --------------------------------------------------
# PRODUCT SNAPSHOT
# --------------------------------------------------

st.divider()
st.subheader("لمحة سريعة")

home_count = len(home_sessions)
lama_rate = percentage(len(lama_sessions), home_count)
plan_from_lama_rate = percentage(len(plan_sessions), len(lama_sessions))
story_from_home_rate = percentage(len(story_sessions), home_count)

s1, s2, s3 = st.columns(3)
s1.metric("استخدام لمى من زوار الرئيسية", f"{lama_rate}%")
s2.metric("الخطة بعد استخدام لمى", f"{plan_from_lama_rate}%")
s3.metric("إنشاء قصة من زوار الرئيسية", f"{story_from_home_rate}%")

st.markdown(
    """
    <div class="roots-note">
        هاي النسب للنسخة التجريبية وبتصير أصدق كل ما كبر عدد الجلسات. ما عم نخزّن نص المشكلة أو اسم الطفل ضمن Analytics.
    </div>
    """,
    unsafe_allow_html=True,
)


# --------------------------------------------------
# FUNNEL
# --------------------------------------------------

st.divider()
st.subheader("مسار الاستخدام")

funnel_steps = [
    ("🏠 دخلوا الصفحة الرئيسية", len(home_sessions)),
    ("🌿 استخدموا لمى", len(lama_sessions)),
    ("📋 أنشأوا خطة", len(plan_sessions)),
    ("📖 أنشأوا قصة", len(story_sessions)),
    ("🎨 ولّدوا كتاباً مصوّراً", len(book_sessions)),
]

for index, (label, count) in enumerate(funnel_steps):
    previous_count = funnel_steps[index - 1][1] if index > 0 else count
    overall_rate = percentage(count, home_count) if index > 0 else 100.0
    step_rate = percentage(count, previous_count) if index > 0 else 100.0

    if index == 0:
        meta = f"العدد: {count}"
    else:
        meta = (
            f"العدد: {count}   |   من المرحلة السابقة: {step_rate}%   |   "
            f"من زوار الرئيسية: {overall_rate}%"
        )

    st.markdown(
        f"""
        <div class="roots-funnel-row">
            <div class="roots-funnel-title">{safe_text(label)}</div>
            <div class="roots-funnel-meta">{safe_text(meta)}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    progress_value = 0 if home_count == 0 else min(count / home_count, 1.0)
    st.progress(progress_value)


# --------------------------------------------------
# DAILY ACTIVITY
# --------------------------------------------------

st.divider()
st.subheader("النشاط عبر الأيام")

daily_counts = defaultdict(
    lambda: {
        "الجلسات": set(),
        "طلبات لمى": 0,
        "الخطط": 0,
        "القصص": 0,
        "الكتب": 0,
    }
)

for event in events:
    dt = event_datetime(event)
    if not dt:
        continue

    day_key = dt.strftime("%d/%m")
    session_id = event.get("session_id")

    if session_id:
        daily_counts[day_key]["الجلسات"].add(session_id)

    name = event.get("event_name")
    if name == "lama_request":
        daily_counts[day_key]["طلبات لمى"] += 1
    elif name == "plan_created":
        daily_counts[day_key]["الخطط"] += 1
    elif name == "story_created":
        daily_counts[day_key]["القصص"] += 1
    elif name == "story_images_generated":
        daily_counts[day_key]["الكتب"] += 1

if daily_counts:
    ordered_days = []
    seen_days = set()

    for event in sorted(
        events,
        key=lambda item: event_datetime(item)
        or datetime.min.replace(tzinfo=UAE_TZ),
    ):
        dt = event_datetime(event)
        if not dt:
            continue

        key = dt.strftime("%d/%m")
        if key not in seen_days:
            seen_days.add(key)
            ordered_days.append(key)

    for day in ordered_days[-10:]:
        values = daily_counts[day]
        total_sessions = len(values["الجلسات"])

        st.markdown(
            f"**{day}** — جلسات: **{total_sessions}** · طلبات لمى: **{values['طلبات لمى']}** · "
            f"خطط: **{values['الخطط']}** · قصص: **{values['القصص']}** · كتب: **{values['الكتب']}**"
        )
else:
    st.caption("لسا ما في بيانات كافية لعرض النشاط اليومي.")


# --------------------------------------------------
# TOP CATEGORIES + PLAN TYPES
# --------------------------------------------------

st.divider()
left, right = st.columns(2)

with left:
    st.subheader("🌿 أكثر المواضيع طلباً")

    category_counts = Counter()

    for event in lama_requests:
        metadata = event.get("metadata") or {}
        category = metadata.get("category")
        if category:
            category_counts[str(category)] += 1

    if category_counts:
        total_category_events = sum(category_counts.values())

        for category, count in category_counts.most_common(8):
            share = percentage(count, total_category_events)
            st.markdown(f"**{safe_text(category)}** — {count} طلب · {share}%")
            st.progress(min(count / total_category_events, 1.0))
    else:
        st.caption("لسا ما في بيانات كافية عن المواضيع.")

with right:
    st.subheader("📋 أنواع الخطط")

    plan_type_counts = Counter()

    for event in plans_created:
        metadata = event.get("metadata") or {}
        plan_type = metadata.get("plan_type") or "غير محدد"
        plan_type_counts[str(plan_type)] += 1

    plan_type_labels = {
        "personalized": "خطة شخصية",
        "consultation_starter": "خطة مبدئية للاستشارة",
        "غير محدد": "غير محدد",
    }

    if plan_type_counts:
        total_plans = sum(plan_type_counts.values())

        for plan_type, count in plan_type_counts.most_common():
            label = plan_type_labels.get(plan_type, plan_type)
            share = percentage(count, total_plans)
            st.markdown(f"**{safe_text(label)}** — {count} · {share}%")
            st.progress(min(count / total_plans, 1.0))
    else:
        st.caption("لسا ما في خطط مسجلة ضمن الفترة.")


# --------------------------------------------------
# STORY STUDIO
# --------------------------------------------------

st.divider()
st.subheader("📖 Story Studio")

photo_used = 0
imaginary_character = 0

for event in books_generated:
    metadata = event.get("metadata") or {}

    if metadata.get("used_uploaded_photo") is True:
        photo_used += 1
    else:
        imaginary_character += 1

story_conversion = percentage(len(book_sessions), len(story_sessions))

sc1, sc2, sc3, sc4 = st.columns(4)
sc1.metric("📖 القصص", len(stories_created))
sc2.metric("🎨 الكتب المصوّرة", len(books_generated))
sc3.metric("🖼️ مع صورة طفل", photo_used)
sc4.metric("✨ شخصية تخيّلية", imaginary_character)

st.markdown(
    f"""
    <div class="roots-note">
        نسبة تحويل القصة إلى كتاب مصوّر: <strong>{story_conversion}%</strong>
    </div>
    """,
    unsafe_allow_html=True,
)


# --------------------------------------------------
# ACTIVITY + SYSTEM STATUS
# --------------------------------------------------

st.divider()
left_activity, right_status = st.columns([1.55, 0.75])

with left_activity:
    st.subheader("🕒 آخر النشاطات")

    recent_events = sorted(
        events,
        key=lambda event: event_datetime(event)
        or datetime.min.replace(tzinfo=UAE_TZ),
        reverse=True,
    )[:20]

    if not recent_events:
        st.caption("ما في نشاط ضمن الفترة المختارة.")

    for event in recent_events:
        label = event_label(event.get("event_name"))
        page = page_label(event.get("page_name"))
        dt = event_datetime(event)

        st.markdown(
            f"""
            <div class="roots-activity">
                <div class="roots-activity-title">{safe_text(label)}</div>
                <div class="roots-activity-meta">{safe_text(page)} · {safe_text(format_time(dt))}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

with right_status:
    st.subheader("حالة البيانات")

    latest_event_dt = max(
        (event_datetime(event) for event in raw_events if event_datetime(event)),
        default=None,
    )

    total_raw_sessions = len(unique_sessions(raw_events))

    st.markdown(
        f"""
        <div class="roots-section-card">
            <div class="roots-mini-label">كل الأحداث المسجلة</div>
            <div class="roots-mini-value">{len(raw_events)}</div>
        </div>
        <div class="roots-section-card">
            <div class="roots-mini-label">كل الجلسات المسجلة</div>
            <div class="roots-mini-value">{total_raw_sessions}</div>
        </div>
        <div class="roots-section-card">
            <div class="roots-mini-label">آخر حدث</div>
            <div style="color:#633a62;font-weight:700;margin-top:5px;">{safe_text(format_time(latest_event_dt))}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# --------------------------------------------------
# CONTROLS
# --------------------------------------------------

st.divider()
logout_col, refresh_col = st.columns(2)

with refresh_col:
    if st.button("🔄 تحديث البيانات", use_container_width=True):
        st.rerun()

with logout_col:
    if st.button("تسجيل الخروج", use_container_width=True):
        st.session_state.dashboard_authenticated = False
        st.rerun()
