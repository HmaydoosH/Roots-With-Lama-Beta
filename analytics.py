import json
import os
import urllib.request
import uuid

from dotenv import load_dotenv

load_dotenv(dotenv_path=".env")


def _load_cloud_secrets():
    if os.getenv("SUPABASE_URL") and os.getenv("SUPABASE_SECRET_KEY"):
        return

    try:
        import streamlit as st

        if "SUPABASE_URL" in st.secrets:
            os.environ["SUPABASE_URL"] = st.secrets["SUPABASE_URL"]

        if "SUPABASE_SECRET_KEY" in st.secrets:
            os.environ["SUPABASE_SECRET_KEY"] = st.secrets["SUPABASE_SECRET_KEY"]

    except Exception:
        pass


def get_session_id():
    try:
        import streamlit as st

        if "analytics_session_id" not in st.session_state:
            st.session_state.analytics_session_id = str(uuid.uuid4())

        return st.session_state.analytics_session_id

    except Exception:
        return str(uuid.uuid4())


def track_event(
    event_name,
    page_name=None,
    metadata=None,
    session_id=None
):
    _load_cloud_secrets()

    url = os.getenv("SUPABASE_URL")
    secret = os.getenv("SUPABASE_SECRET_KEY")

    if not url or not secret:
        return False

    base_url = url.rstrip("/")

    if base_url.endswith("/rest/v1"):
        endpoint = f"{base_url}/analytics_events"
    else:
        endpoint = f"{base_url}/rest/v1/analytics_events"

    payload = {
        "session_id": session_id or get_session_id(),
        "event_name": event_name,
        "page_name": page_name,
        "metadata": metadata or {},
    }

    request = urllib.request.Request(
        endpoint,
        data=json.dumps(payload).encode("utf-8"),
        method="POST",
        headers={
            "apikey": secret,
            "Content-Type": "application/json",
            "Prefer": "return=minimal",
        },
    )

    try:
        with urllib.request.urlopen(
            request,
            timeout=10
        ) as response:
            return 200 <= response.status < 300

    except Exception as error:
        print("Analytics error:", error)
        return False


def get_events(limit=1000):
    _load_cloud_secrets()

    url = os.getenv("SUPABASE_URL")
    secret = os.getenv("SUPABASE_SECRET_KEY")

    if not url or not secret:
        return []

    try:
        limit = max(1, min(int(limit), 10000))
    except Exception:
        limit = 1000

    base_url = url.rstrip("/")

    if base_url.endswith("/rest/v1"):
        endpoint = f"{base_url}/analytics_events"
    else:
        endpoint = f"{base_url}/rest/v1/analytics_events"

    endpoint += (
        "?select=id,session_id,event_name,page_name,metadata,created_at"
        f"&order=created_at.desc&limit={limit}"
    )

    request = urllib.request.Request(
        endpoint,
        method="GET",
        headers={
            "apikey": secret,
            "Accept": "application/json",
        },
    )

    try:
        with urllib.request.urlopen(request, timeout=10) as response:
            return json.loads(response.read().decode("utf-8"))

    except Exception as error:
        print("Analytics read error:", error)
        return []
