import os
from collections import Counter
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
import streamlit as st
from dotenv import load_dotenv

from analytics import get_events

st.set_page_config(
    page_title="Roots Dashboard",
    page_icon="📊",
    layout="wide"
)


load_dotenv(dotenv_path=".env")

st.markdown("""
<style>
html, body, [class*="css"] {
    direction: rtl;
    text-align: right;
}

.stApp {
    background: #fffaf6;
    direction: rtl;
    text-align: right;
}

.block-container {
    direction: rtl;
    text-align: right;
}
.block-container {
    max-width: 1200px;
    padding-top: 2rem;
}
h1, h2, h3 {
    color: #633a62;
}
[data-testid="stMetric"] {
    background: white;
    border: 1px solid #eadde8;
    border-radius: 22px;
    padding: 18px;
    box-shadow: 0 8px 25px rgba(99,58,98,0.06);
}
[data-testid="stMetricValue"] {
    color: #633a62;
}
</style>
""", unsafe_allow_html=True)



# ---------- PASSWORD ----------
dashboard_password = os.getenv("DASHBOARD_PASSWORD")

if not dashboard_password:
    try:
        dashboard_password = st.secrets["DASHBOARD_PASSWORD"]
    except Exception:
        dashboard_password = None


if not dashboard_password:
    st.error("Dashboard password is not configured.")
    st.stop()


if "dashboard_authenticated" not in st.session_state:
    st.session_state.dashboard_authenticated = False


if not st.session_state.dashboard_authenticated:
    st.title("📊 Roots Dashboard")
    st.caption("لوحة داخلية خاصة بإدارة Roots with Lama")

    password_input = st.text_input(
        "كلمة السر",
        type="password"
    )

    if st.button("دخول"):
        if password_input == dashboard_password:
            st.session_state.dashboard_authenticated = True
            st.rerun()
        else:
            st.error("كلمة السر غير صحيحة.")

    st.stop()


# ---------- DASHBOARD ----------
st.title("📊 Roots Dashboard")
st.caption("متابعة استخدام النسخة التجريبية")

events = get_events(limit=10000)

# Remove manual test events
events = [
    event for event in events
    if event.get("event_name") != "test_event"
]

UAE_TZ = ZoneInfo("Asia/Dubai")
now_uae = datetime.now(UAE_TZ)

if "dashboard_time_filter" not in st.session_state:
    st.session_state.dashboard_time_filter = "كل الوقت"

st.markdown("**الفترة**")

with st.container(key="time_filter"):
    f1, f2, f3, f4 = st.columns(4, gap="small")

    if f1.button(
        "اليوم",
        use_container_width=True,
        type="primary" if st.session_state.dashboard_time_filter == "اليوم" else "secondary"
    ):
        st.session_state.dashboard_time_filter = "اليوم"
        st.rerun()

    if f2.button(
        "آخر 7 أيام",
        use_container_width=True,
        type="primary" if st.session_state.dashboard_time_filter == "آخر 7 أيام" else "secondary"
    ):
        st.session_state.dashboard_time_filter = "آخر 7 أيام"
        st.rerun()

    if f3.button(
        "آخر 30 يوم",
        use_container_width=True,
        type="primary" if st.session_state.dashboard_time_filter == "آخر 30 يوم" else "secondary"
    ):
        st.session_state.dashboard_time_filter = "آخر 30 يوم"
        st.rerun()

    if f4.button(
        "كل الوقت",
        use_container_width=True,
        type="primary" if st.session_state.dashboard_time_filter == "كل الوقت" else "secondary"
    ):
        st.session_state.dashboard_time_filter = "كل الوقت"
        st.rerun()

filter_choice = st.session_state.dashboard_time_filter

def event_datetime(event):
    raw = event.get("created_at")
    if not raw:
        return None

    try:
        dt = datetime.fromisoformat(raw.replace("Z", "+00:00"))
        return dt.astimezone(UAE_TZ)
    except Exception:
        return None

filtered_events = []

for event in events:
    dt = event_datetime(event)

    if filter_choice == "كل الوقت":
        filtered_events.append(event)

    elif dt is None:
        continue

    elif filter_choice == "اليوم":
        if dt.date() == now_uae.date():
            filtered_events.append(event)

    elif filter_choice == "آخر 7 أيام":
        if dt >= now_uae - timedelta(days=7):
            filtered_events.append(event)

    elif filter_choice == "آخر 30 يوم":
        if dt >= now_uae - timedelta(days=30):
            filtered_events.append(event)

events = filtered_events


if not events:
    st.info("ما في بيانات مسجلة حتى الآن.")
    st.stop()


page_views = [
    event for event in events
    if event.get("event_name") == "page_view"
]

sessions = {
    event.get("session_id")
    for event in events
    if event.get("session_id")
}

lama_requests = [
    event for event in events
    if event.get("event_name") == "lama_request"
]

plans_created = [
    event for event in events
    if event.get("event_name") == "plan_created"
]

stories_created = [
    event for event in events
    if event.get("event_name") == "story_created"
]

books_generated = [
    event for event in events
    if event.get("event_name") == "story_images_generated"
]


# ---------- MAIN METRICS ----------

col1, col2, col3 = st.columns(3)

col1.metric(
    "👀 مشاهدات الصفحات",
    len(page_views)
)

col2.metric(
    "👩‍👧 الجلسات",
    len(sessions)
)

col3.metric(
    "🌿 طلبات لمى",
    len(lama_requests)
)

col4, col5, col6 = st.columns(3)

col4.metric(
    "📋 الخطط المنشأة",
    len(plans_created)
)

col5.metric(
    "📖 القصص المنشأة",
    len(stories_created)
)

col6.metric(
    "🎨 الكتب المصوّرة",
    len(books_generated)
)


# ---------- FUNNEL ----------

st.divider()
st.subheader("مسار الاستخدام")

home_sessions = {
    event.get("session_id")
    for event in events
    if event.get("event_name") == "page_view"
    and event.get("page_name") == "home"
    and event.get("session_id")
}

lama_sessions = {
    event.get("session_id")
    for event in lama_requests
    if event.get("session_id")
}

plan_sessions = {
    event.get("session_id")
    for event in plans_created
    if event.get("session_id")
}

story_sessions = {
    event.get("session_id")
    for event in stories_created
    if event.get("session_id")
}

book_sessions = {
    event.get("session_id")
    for event in books_generated
    if event.get("session_id")
}


def conversion(count, base):
    if not base:
        return 0
    return round((count / base) * 100, 1)


base = len(home_sessions)

funnel_steps = [
    ("🏠 دخلوا الصفحة الرئيسية", len(home_sessions)),
    ("🌿 استخدموا لمى", len(lama_sessions)),
    ("📋 أنشأوا خطة", len(plan_sessions)),
    ("📖 أنشأوا قصة", len(story_sessions)),
    ("🎨 ولّدوا كتاباً مصوّراً", len(book_sessions)),
]

for label, count in funnel_steps:
    if label.startswith("🏠"):
        st.markdown(f"**{label}** — {count}")
    else:
        rate = conversion(count, base)
        st.markdown(
            f"**{label}** — العدد: **{count}** &nbsp;&nbsp;&nbsp; | &nbsp;&nbsp;&nbsp; "
            f"النسبة: **{rate}%** من زوار الصفحة الرئيسية",
            unsafe_allow_html=True
        )

    progress_value = 0 if base == 0 else min(count / base, 1.0)
    st.progress(progress_value)


st.divider()

st.subheader("🌿 أكثر المواضيع طلباً")

categories = []

for event in lama_requests:
    metadata = event.get("metadata") or {}
    category = metadata.get("category")

    if category:
        categories.append(category)

category_counts = Counter(categories)

if category_counts:

    for category, count in category_counts.most_common(8):
        percentage = round(
            (count / len(lama_requests)) * 100,
            1
        ) if lama_requests else 0

        st.markdown(
            f"**{category}** — {count} طلب  ·  {percentage}%"
        )

        st.progress(
            min(count / len(lama_requests), 1.0)
            if lama_requests else 0
        )

else:
    st.caption("لسا ما في بيانات كافية عن المواضيع.")

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

story_col1, story_col2, story_col3, story_col4 = st.columns(4)

story_col1.metric(
    "📖 القصص",
    len(stories_created)
)

story_col2.metric(
    "🎨 الكتب المصوّرة",
    len(books_generated)
)

story_col3.metric(
    "🖼️ مع صورة طفل",
    photo_used
)

story_col4.metric(
    "✨ شخصية تخيّلية",
    imaginary_character
)

st.divider()

st.subheader("آخر النشاطات")

recent_events = events[:20]

for event in recent_events:
    event_name = event.get("event_name", "—")
    page_name = event.get("page_name", "—")
    created_at = event.get("created_at", "—")

    st.write(
        f"**{event_name}** · {page_name} · {created_at}"
    )


st.divider()

if st.button("تسجيل الخروج"):
    st.session_state.dashboard_authenticated = False
    st.rerun()

# ---------- FORCE FULL RTL ----------
st.markdown("""
<style>

/* Main Streamlit content */
[data-testid="stMainBlockContainer"],
[data-testid="stMarkdownContainer"],
[data-testid="stHeading"],
[data-testid="stWidgetLabel"] {
    direction: rtl !important;
    text-align: right !important;
}

/* Headings and paragraphs */
h1, h2, h3, p {
    direction: rtl !important;
    text-align: right !important;
}

/* Columns run from right to left */
[data-testid="stHorizontalBlock"] {
    direction: rtl !important;
}

/* Metrics */
[data-testid="stMetric"] {
    direction: rtl !important;
    text-align: right !important;
}

[data-testid="stMetricLabel"],
[data-testid="stMetricValue"] {
    width: 100% !important;
    direction: rtl !important;
    text-align: right !important;
}

/* Segmented filter */
[data-testid="stSegmentedControl"] {
    direction: rtl !important;
}

/* Buttons */
.stButton,
.stDownloadButton {
    direction: rtl !important;
    text-align: right !important;
}

</style>
""", unsafe_allow_html=True)

# ---------- UNIFY FILTER BUTTONS ----------
st.markdown("""
<style>

[data-testid="stSegmentedControl"] button {
    border-radius: 14px !important;
    margin: 0 3px !important;
}

</style>
""", unsafe_allow_html=True)

# ---------- FORCE SHARP TIME FILTER ----------
st.markdown("""
<style>

[data-testid="stSegmentedControl"] *,
[data-testid="stSegmentedControl"] button,
[data-testid="stSegmentedControl"] [role="button"] {
    border-radius: 0 !important;
}

</style>
""", unsafe_allow_html=True)

st.markdown("""
<style>
.st-key-time_filter button {
    border-radius: 14px !important;
}
</style>
""", unsafe_allow_html=True)
