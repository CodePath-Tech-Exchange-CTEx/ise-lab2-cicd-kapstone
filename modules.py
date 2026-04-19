#############################################################################
# modules.py
#
# Revamped UI modules with polished styling.
#
#############################################################################

from internals import create_component
import streamlit as st


def inject_global_styles():
    """Injects global CSS styles for the app."""
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@400;600;700;800&family=DM+Sans:wght@300;400;500;600&display=swap');

    :root {
        --accent: #C6FF00;
        --accent-dim: #8fb300;
        --bg-deep: #0d0f14;
        --bg-card: #161b24;
        --bg-card2: #1e2535;
        --border: rgba(198,255,0,0.15);
        --border-subtle: rgba(255,255,255,0.07);
        --text-primary: #f0f4ff;
        --text-secondary: #8a93a8;
        --text-muted: #4a5568;
        --success: #39d98a;
        --warning: #f6a623;
        --danger: #ff5c5c;
    }

    html, body, [class*="css"] {
        font-family: 'DM Sans', sans-serif !important;
        background-color: var(--bg-deep) !important;
        color: var(--text-primary) !important;
    }

    /* Hide streamlit chrome */
    #MainMenu, footer, header { visibility: hidden; }
    .stDeployButton { display: none; }

    /* Main content area */
    .main .block-container {
        padding: 2rem 2.5rem 3rem 2.5rem !important;
        max-width: 1100px !important;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: #0d0f14 !important;
        border-right: 1px solid var(--border-subtle) !important;
    }
    section[data-testid="stSidebar"] .stSelectbox label {
        color: var(--text-secondary) !important;
        font-size: 11px !important;
        text-transform: uppercase !important;
        letter-spacing: 1.5px !important;
        font-weight: 600 !important;
    }

    /* Metric cards row */
    .metric-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 14px;
        margin: 20px 0 28px 0;
    }
    .metric-card {
        background: var(--bg-card);
        border: 1px solid var(--border-subtle);
        border-radius: 14px;
        padding: 18px 20px 16px 20px;
        position: relative;
        overflow: hidden;
        transition: border-color 0.2s, transform 0.2s;
    }
    .metric-card:hover {
        border-color: var(--border);
        transform: translateY(-2px);
    }
    .metric-card::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 2px;
        background: linear-gradient(90deg, var(--accent), transparent);
    }
    .metric-icon {
        font-size: 20px;
        margin-bottom: 8px;
        display: block;
    }
    .metric-value {
        font-family: 'Barlow Condensed', sans-serif;
        font-size: 32px;
        font-weight: 800;
        color: var(--accent);
        line-height: 1;
        margin-bottom: 4px;
    }
    .metric-label {
        font-size: 11px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
        color: var(--text-secondary);
    }

    /* Workout cards */
    .workout-card {
        background: var(--bg-card);
        border: 1px solid var(--border-subtle);
        border-radius: 16px;
        padding: 22px 24px;
        margin-bottom: 14px;
        display: grid;
        grid-template-columns: auto 1fr auto;
        gap: 16px;
        align-items: center;
        transition: border-color 0.2s;
    }
    .workout-card:hover { border-color: var(--border); }
    .workout-index {
        font-family: 'Barlow Condensed', sans-serif;
        font-size: 42px;
        font-weight: 800;
        color: var(--text-muted);
        line-height: 1;
        min-width: 40px;
    }
    .workout-meta { flex: 1; }
    .workout-time {
        font-size: 13px;
        color: var(--text-secondary);
        margin-bottom: 8px;
        display: flex;
        align-items: center;
        gap: 6px;
    }
    .workout-stats {
        display: flex;
        gap: 20px;
        flex-wrap: wrap;
    }
    .workout-stat {
        display: flex;
        flex-direction: column;
    }
    .workout-stat-val {
        font-family: 'Barlow Condensed', sans-serif;
        font-size: 20px;
        font-weight: 700;
        color: var(--text-primary);
    }
    .workout-stat-lbl {
        font-size: 10px;
        text-transform: uppercase;
        letter-spacing: 0.8px;
        color: var(--text-muted);
        font-weight: 600;
    }
    .workout-duration {
        text-align: right;
    }
    .duration-val {
        font-family: 'Barlow Condensed', sans-serif;
        font-size: 24px;
        font-weight: 700;
        color: var(--accent);
    }
    .duration-lbl {
        font-size: 10px;
        text-transform: uppercase;
        letter-spacing: 0.8px;
        color: var(--text-muted);
        font-weight: 600;
        display: block;
    }

    /* Section headers */
    .section-title {
        font-family: 'Barlow Condensed', sans-serif;
        font-size: 13px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 2.5px;
        color: var(--accent);
        margin: 32px 0 16px 0;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    .section-title::after {
        content: '';
        flex: 1;
        height: 1px;
        background: var(--border-subtle);
    }

    /* Page title */
    .page-title {
        font-family: 'Barlow Condensed', sans-serif;
        font-size: 52px;
        font-weight: 800;
        color: var(--text-primary);
        line-height: 1;
        margin-bottom: 4px;
        letter-spacing: -1px;
    }
    .page-subtitle {
        font-size: 14px;
        color: var(--text-secondary);
        margin-bottom: 0;
        font-weight: 400;
    }

    /* Post card */
    .post-card {
        background: var(--bg-card);
        border: 1px solid var(--border-subtle);
        border-radius: 16px;
        padding: 20px 22px;
        margin-bottom: 14px;
        transition: border-color 0.2s;
    }
    .post-card:hover { border-color: var(--border); }
    .post-header {
        display: flex;
        align-items: center;
        gap: 12px;
        margin-bottom: 12px;
    }
    .post-avatar {
        width: 40px; height: 40px;
        border-radius: 50%;
        background: var(--bg-card2);
        border: 2px solid var(--border);
        object-fit: cover;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 16px;
        overflow: hidden;
    }
    .post-username {
        font-weight: 600;
        font-size: 14px;
        color: var(--text-primary);
    }
    .post-time {
        font-size: 11px;
        color: var(--text-muted);
        margin-top: 1px;
    }
    .post-content {
        font-size: 14px;
        line-height: 1.6;
        color: var(--text-secondary);
    }

    /* Advice card */
    .advice-card {
        background: linear-gradient(135deg, var(--bg-card) 0%, #1a2235 100%);
        border: 1px solid var(--border);
        border-radius: 16px;
        padding: 24px 26px;
        margin: 16px 0;
        position: relative;
        overflow: hidden;
    }
    .advice-card::before {
        content: '';
        position: absolute;
        top: -40px; right: -40px;
        width: 120px; height: 120px;
        border-radius: 50%;
        background: radial-gradient(circle, rgba(198,255,0,0.12), transparent 70%);
    }
    .advice-label {
        font-family: 'Barlow Condensed', sans-serif;
        font-size: 11px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 2px;
        color: var(--accent);
        margin-bottom: 10px;
    }
    .advice-text {
        font-size: 15px;
        line-height: 1.7;
        color: var(--text-primary);
        font-weight: 400;
    }
    .advice-timestamp {
        font-size: 11px;
        color: var(--text-muted);
        margin-top: 12px;
    }

    /* Divider */
    .custom-divider {
        border: none;
        border-top: 1px solid var(--border-subtle);
        margin: 28px 0;
    }

    /* Streamlit form inputs */
    .stTextInput input, .stTextArea textarea, .stSelectbox select {
        background: var(--bg-card) !important;
        border: 1px solid var(--border-subtle) !important;
        border-radius: 10px !important;
        color: var(--text-primary) !important;
    }
    .stTextInput input:focus, .stTextArea textarea:focus {
        border-color: var(--accent) !important;
        box-shadow: 0 0 0 2px rgba(198,255,0,0.1) !important;
    }

    /* Buttons */
    .stButton button {
        background: var(--accent) !important;
        color: #0d0f14 !important;
        font-weight: 700 !important;
        font-family: 'DM Sans', sans-serif !important;
        border: none !important;
        border-radius: 10px !important;
        letter-spacing: 0.3px !important;
        transition: opacity 0.2s, transform 0.1s !important;
    }
    .stButton button:hover {
        opacity: 0.88 !important;
        transform: translateY(-1px) !important;
    }

    /* Success / warning / info boxes */
    .stSuccess {
        background: rgba(57,217,138,0.1) !important;
        border-left: 3px solid var(--success) !important;
        border-radius: 8px !important;
    }
    .stWarning {
        background: rgba(246,166,35,0.1) !important;
        border-left: 3px solid var(--warning) !important;
    }
    .stInfo {
        background: rgba(198,255,0,0.07) !important;
        border-left: 3px solid var(--accent-dim) !important;
    }

    /* Selectbox */
    .stSelectbox [data-baseweb="select"] {
        background: var(--bg-card) !important;
    }

    /* Radio buttons */
    .stRadio label { color: var(--text-secondary) !important; }

    /* File uploader */
    .stFileUploader {
        background: var(--bg-card) !important;
        border: 1px dashed var(--border-subtle) !important;
        border-radius: 10px !important;
    }

    /* Progress bar */
    .stProgress > div > div {
        background: var(--accent) !important;
        border-radius: 4px !important;
    }
    .stProgress > div {
        background: var(--bg-card2) !important;
        border-radius: 4px !important;
    }

    /* Number input */
    .stNumberInput input {
        background: var(--bg-card) !important;
        border: 1px solid var(--border-subtle) !important;
        color: var(--text-primary) !important;
        border-radius: 10px !important;
    }
    </style>
    """, unsafe_allow_html=True)


def display_my_custom_component(value):
    data = {'NAME': value}
    html_file_name = "my_custom_component"
    create_component(data, html_file_name)


def display_post(username, user_image, timestamp, content, post_image):
    """Displays a polished post card."""
    ts_str = timestamp.strftime("%b %d, %Y · %I:%M %p") if hasattr(timestamp, 'strftime') else str(timestamp)
    initial = username[0].upper() if username else "?"

    # Build avatar HTML
    if user_image and isinstance(user_image, str) and user_image.startswith('http'):
        avatar_html = f'<img src="{user_image}" style="width:40px;height:40px;border-radius:50%;object-fit:cover;border:2px solid rgba(198,255,0,0.3);">'
    elif user_image and isinstance(user_image, bytes):
        import base64
        b64 = base64.b64encode(user_image).decode()
        avatar_html = f'<img src="data:image/jpeg;base64,{b64}" style="width:40px;height:40px;border-radius:50%;object-fit:cover;border:2px solid rgba(198,255,0,0.3);">'
    else:
        avatar_html = f'<div style="width:40px;height:40px;border-radius:50%;background:#1e2535;border:2px solid rgba(198,255,0,0.3);display:flex;align-items:center;justify-content:center;font-weight:700;font-size:16px;color:#C6FF00;">{initial}</div>'

    st.markdown(f"""
    <div class="post-card">
        <div class="post-header">
            {avatar_html}
            <div>
                <div class="post-username">{username}</div>
                <div class="post-time">{ts_str}</div>
            </div>
        </div>
        <div class="post-content">{content}</div>
    </div>
    """, unsafe_allow_html=True)

    if post_image:
        if isinstance(post_image, str) and post_image.startswith('http'):
            st.image(post_image, use_container_width=True)
        elif isinstance(post_image, bytes):
            st.image(post_image, use_container_width=True)


def display_activity_summary(workouts_list):
    """Displays a polished activity summary with metric cards."""
    if not workouts_list:
        st.markdown('<div style="color:#4a5568;font-size:14px;padding:20px 0;">No workouts recorded yet.</div>', unsafe_allow_html=True)
        return None

    # Fix: handle both 'calories' and 'calories_burned' keys
    total_dist = sum(w.get('distance') or 0 for w in workouts_list)
    total_steps = sum(w.get('steps') or 0 for w in workouts_list)
    total_cals = sum((w.get('calories_burned') or w.get('calories') or 0) for w in workouts_list)
    total_workouts = len(workouts_list)

    # Calculate total duration in minutes
    total_mins = 0
    from datetime import datetime
    for w in workouts_list:
        try:
            start = datetime.strptime(str(w.get('start_timestamp', '')), '%Y-%m-%d %H:%M:%S')
            end = datetime.strptime(str(w.get('end_timestamp', '')), '%Y-%m-%d %H:%M:%S')
            total_mins += int((end - start).total_seconds() / 60)
        except Exception:
            pass

    st.markdown(f"""
    <div class="metric-grid">
        <div class="metric-card">
            <span class="metric-icon">🏋️</span>
            <div class="metric-value">{total_workouts}</div>
            <div class="metric-label">Workouts</div>
        </div>
        <div class="metric-card">
            <span class="metric-icon">📍</span>
            <div class="metric-value">{total_dist:.1f}</div>
            <div class="metric-label">Miles</div>
        </div>
        <div class="metric-card">
            <span class="metric-icon">👟</span>
            <div class="metric-value">{total_steps:,}</div>
            <div class="metric-label">Steps</div>
        </div>
        <div class="metric-card">
            <span class="metric-icon">🔥</span>
            <div class="metric-value">{total_cals:,}</div>
            <div class="metric-label">Calories</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    return None


def display_recent_workouts(workouts_list=[]):
    """Displays polished workout cards."""
    if not workouts_list:
        st.markdown('<div style="color:#4a5568;font-size:14px;padding:16px 0;">No recent workouts to show.</div>', unsafe_allow_html=True)
        return

    from datetime import datetime

    for i, workout in enumerate(workouts_list, start=1):
        start_raw = workout.get('start_timestamp', '')
        end_raw = workout.get('end_timestamp', '')
        distance = workout.get('distance')
        steps = workout.get('steps') or 0
        cals = workout.get('calories_burned') or workout.get('calories') or 0

        # Format distance
        dist_str = f"{distance:.1f} mi" if distance is not None else "—"

        # Calculate duration
        duration_str = "—"
        try:
            start_dt = datetime.strptime(str(start_raw), '%Y-%m-%d %H:%M:%S')
            end_dt = datetime.strptime(str(end_raw), '%Y-%m-%d %H:%M:%S')
            mins = int((end_dt - start_dt).total_seconds() / 60)
            duration_str = f"{mins}"
            time_label = "min"
            # Format display date
            date_str = start_dt.strftime("%b %d, %Y · %I:%M %p")
        except Exception:
            date_str = str(start_raw)
            time_label = "min"

        st.markdown(f"""
        <div class="workout-card">
            <div class="workout-index">0{i}</div>
            <div class="workout-meta">
                <div class="workout-time">📅 {date_str}</div>
                <div class="workout-stats">
                    <div class="workout-stat">
                        <span class="workout-stat-val">{dist_str}</span>
                        <span class="workout-stat-lbl">Distance</span>
                    </div>
                    <div class="workout-stat">
                        <span class="workout-stat-val">{steps:,}</span>
                        <span class="workout-stat-lbl">Steps</span>
                    </div>
                    <div class="workout-stat">
                        <span class="workout-stat-val">{cals:,}</span>
                        <span class="workout-stat-lbl">Calories</span>
                    </div>
                </div>
            </div>
            <div class="workout-duration">
                <span class="duration-val">{duration_str}</span>
                <span class="duration-lbl">{time_label}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)


def display_genai_advice(timestamp, content, image):
    """Displays a polished AI advice card."""
    st.markdown(f"""
    <div class="advice-card">
        <div class="advice-label">⚡ AI Coach · Generated {timestamp}</div>
        <div class="advice-text">{content}</div>
    </div>
    """, unsafe_allow_html=True)

    if image and isinstance(image, str) and image.startswith('http'):
        st.image(image, use_container_width=True)