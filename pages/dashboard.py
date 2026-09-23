import os
import streamlit as st
from dotenv import load_dotenv

from analytics import get_events

st.set_page_config(
    page_title="Roots Dashboard",
    page_icon="📊",
    layout="wide"
)

load_dotenv(dotenv_path=".env")


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


col1, col2, col3, col4 = st.columns(4)

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

col4.metric(
    "📋 الخطط المنشأة",
    len(plans_created)
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
