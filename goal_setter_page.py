#############################################################################
# goal_setter_page.py
#
# Goal Setter page for the SDS fitness app.
# Pure Streamlit logic with st.markdown() used only for
# custom fonts, colors, and borders — same approach as teammates.
#
#############################################################################

import streamlit as st


# ── Styling (fonts, borders, colors only) ─────────────────────────────────
def inject_styles():
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif;
        }

        /* Page title */
        .goal-page-title {
            font-family: 'Inter', sans-serif;
            font-size: 28px;
            font-weight: 700;
            color: #1a1a1a;
            margin-bottom: 4px;
        }
        .goal-page-subtitle {
            font-size: 14px;
            color: #888;
            margin-bottom: 20px;
        }

        /* Section headers */
        .section-header {
            font-family: 'Inter', sans-serif;
            font-size: 16px;
            font-weight: 600;
            color: #333;
            border-left: 4px solid #43a047;
            padding-left: 10px;
            margin: 16px 0 12px 0;
        }

        /* Goal card wrapper */
        .goal-card-header {
            background: #f9fafb;
            border: 1px solid #e0e0e0;
            border-radius: 12px;
            padding: 14px 16px 8px 16px;
            margin-bottom: 4px;
        }
        .goal-card-name {
            font-size: 17px;
            font-weight: 600;
            color: #1a1a1a;
            margin-bottom: 2px;
        }
        .goal-card-meta {
            font-size: 12px;
            color: #888;
            margin-bottom: 6px;
        }
        .goal-badge {
            display: inline-block;
            font-size: 11px;
            font-weight: 600;
            padding: 2px 10px;
            border-radius: 20px;
            background: #e8f5e9;
            color: #2e7d32;
            border: 1px solid #a5d6a7;
        }

        /* Percentage display */
        .pct-big {
            font-size: 38px;
            font-weight: 700;
            color: #2e7d32;
            line-height: 1.1;
        }
        .pct-sub {
            font-size: 12px;
            color: #888;
            margin-top: 2px;
        }

        /* Activity items */
        .activity-header {
            font-size: 12px;
            font-weight: 600;
            color: #555;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 4px;
        }
        .activity-row {
            display: flex;
            align-items: center;
            gap: 8px;
            font-size: 13px;
            color: #444;
            padding: 4px 0;
            border-bottom: 1px solid #f0f0f0;
        }
        .activity-dot {
            width: 7px;
            height: 7px;
            border-radius: 50%;
            background: #43a047;
            flex-shrink: 0;
        }

        /* Log section label */
        .log-label {
            font-size: 13px;
            font-weight: 500;
            color: #444;
            margin-bottom: 4px;
        }

        /* Divider */
        .styled-divider {
            border: none;
            border-top: 1px solid #e8e8e8;
            margin: 20px 0;
        }

        /* Empty state */
        .empty-state {
            text-align: center;
            padding: 40px 20px;
            color: #bbb;
            font-size: 15px;
            border: 1px dashed #ddd;
            border-radius: 12px;
        }
    </style>
    """, unsafe_allow_html=True)


# ── Session state ──────────────────────────────────────────────────────────
def init_state():
    if "goals" not in st.session_state:
        st.session_state["goals"] = []
    if "next_id" not in st.session_state:
        st.session_state["next_id"] = 1
    if "editing_id" not in st.session_state:
        st.session_state["editing_id"] = None


# ── Goal logic ─────────────────────────────────────────────────────────────
def add_goal(workout_type, goal_name, target, unit, timeframe):
    st.session_state["goals"].append({
        "id": st.session_state["next_id"],
        "type": workout_type,
        "name": goal_name,
        "target": float(target),
        "unit": unit,
        "completed": 0.0,
        "timeframe": timeframe,
        "activity": [],
    })
    st.session_state["next_id"] += 1


def delete_goal(goal_id):
    st.session_state["goals"] = [
        g for g in st.session_state["goals"] if g["id"] != goal_id
    ]


def log_progress(goal_id, amount):
    for g in st.session_state["goals"]:
        if g["id"] == goal_id:
            g["completed"] = min(round(g["completed"] + amount, 1), g["target"])
            g["activity"].insert(0, f"+ {amount} {g['unit']} logged")
            if len(g["activity"]) > 3:
                g["activity"].pop()
            break


def save_edit(goal_id, new_name, new_target, new_unit):
    for g in st.session_state["goals"]:
        if g["id"] == goal_id:
            g["name"] = new_name
            g["target"] = float(new_target)
            g["unit"] = new_unit
            break
    st.session_state["editing_id"] = None


# ── Goal card ──────────────────────────────────────────────────────────────
def display_goal_card(goal):
    pct = int((goal["completed"] / goal["target"]) * 100) if goal["target"] > 0 else 0

    # Styled card header
    st.markdown(f"""
    <div class="goal-card-header">
        <div class="goal-card-name">{goal['name']}</div>
        <div class="goal-card-meta">Goal: {goal['target']} {goal['unit']} &nbsp;·&nbsp; {goal['timeframe']}</div>
        <span class="goal-badge">{goal['type']}</span>
    </div>
    """, unsafe_allow_html=True)

    # Percentage + progress bar
    st.markdown(f"""
    <div class="pct-big">{pct}%</div>
    <div class="pct-sub">{goal['completed']} / {goal['target']} {goal['unit']} completed</div>
    """, unsafe_allow_html=True)
    st.progress(pct / 100)

    # +/- log controls (pure Streamlit buttons)
    st.markdown('<div class="log-label">Log progress</div>', unsafe_allow_html=True)
    key_amount = f"log_amount_{goal['id']}"
    if key_amount not in st.session_state:
        st.session_state[key_amount] = 0.5

    col_minus, col_val, col_plus, col_log = st.columns([1, 1, 1, 3])
    with col_minus:
        if st.button("−", key=f"minus_{goal['id']}"):
            st.session_state[key_amount] = max(0.5, round(st.session_state[key_amount] - 0.5, 1))
            st.rerun()
    with col_val:
        st.markdown(f"**{st.session_state[key_amount]}**")
    with col_plus:
        if st.button("+", key=f"plus_{goal['id']}"):
            st.session_state[key_amount] = round(st.session_state[key_amount] + 0.5, 1)
            st.rerun()
    with col_log:
        if st.button("Log it", key=f"log_{goal['id']}"):
            log_progress(goal["id"], st.session_state[key_amount])
            st.session_state[key_amount] = 0.5
            st.rerun()

    # Quick text note
    quick_val = st.text_input(
        "Quick note",
        placeholder="e.g. Run 5 miles",
        key=f"quick_{goal['id']}",
        label_visibility="collapsed"
    )
    if st.button("+ Add note", key=f"quick_btn_{goal['id']}"):
        if quick_val.strip():
            goal["activity"].insert(0, f"+ {quick_val.strip()}")
            if len(goal["activity"]) > 3:
                goal["activity"].pop()
            st.rerun()

    # Recent activity (styled)
    if goal["activity"]:
        st.markdown('<div class="activity-header">Recent activity</div>', unsafe_allow_html=True)
        rows = "".join(
            f'<div class="activity-row"><span class="activity-dot"></span>{item}</div>'
            for item in goal["activity"]
        )
        st.markdown(rows, unsafe_allow_html=True)

    # Edit / Delete buttons
    col_edit, col_del, _ = st.columns([1, 1, 4])
    with col_edit:
        if st.button("✏️ Edit", key=f"edit_{goal['id']}"):
            st.session_state["editing_id"] = goal["id"]
            st.rerun()
    with col_del:
        if st.button("🗑️ Delete", key=f"del_{goal['id']}"):
            delete_goal(goal["id"])
            st.rerun()

    st.markdown('<hr class="styled-divider">', unsafe_allow_html=True)


# ── Edit form ──────────────────────────────────────────────────────────────
def display_edit_form(goal):
    st.markdown('<div class="section-header">Edit goal</div>', unsafe_allow_html=True)
    with st.form(key=f"edit_form_{goal['id']}"):
        new_name = st.text_input("Goal name", value=goal["name"])
        new_target = st.number_input("Target", min_value=0.1, value=goal["target"], step=0.5)
        new_unit = st.selectbox(
            "Unit",
            ["miles", "km", "reps", "minutes", "sets"],
            index=["miles", "km", "reps", "minutes", "sets"].index(goal["unit"])
            if goal["unit"] in ["miles", "km", "reps", "minutes", "sets"] else 0,
        )
        col_save, col_cancel = st.columns(2)
        with col_save:
            if st.form_submit_button("Save changes", use_container_width=True):
                if new_name.strip():
                    save_edit(goal["id"], new_name.strip(), new_target, new_unit)
                    st.rerun()
                else:
                    st.warning("Goal name cannot be empty.")
        with col_cancel:
            if st.form_submit_button("Cancel", use_container_width=True):
                st.session_state["editing_id"] = None
                st.rerun()
    st.markdown('<hr class="styled-divider">', unsafe_allow_html=True)


# ── Main page ──────────────────────────────────────────────────────────────
def display_goal_setter_page():
    inject_styles()
    init_state()

    st.markdown('<div class="goal-page-title">🎯 Goal Setter</div>', unsafe_allow_html=True)
    st.markdown('<div class="goal-page-subtitle">Set workout goals, track your progress, and stay on target.</div>', unsafe_allow_html=True)
    st.markdown('<hr class="styled-divider">', unsafe_allow_html=True)

    # Edit mode
    if st.session_state["editing_id"] is not None:
        goal = next((g for g in st.session_state["goals"] if g["id"] == st.session_state["editing_id"]), None)
        if goal:
            display_edit_form(goal)

    # Create goal form
    st.markdown('<div class="section-header">Create a new goal</div>', unsafe_allow_html=True)
    with st.form("create_goal_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            workout_type = st.selectbox(
                "Type of workout",
                ["Cardio", "Strength", "Flexibility", "HIIT", "Cycling", "Swimming"],
            )
            goal_name = st.text_input("Goal", placeholder="e.g. Run 5 miles")
        with col2:
            target = st.number_input("Target", min_value=0.1, value=5.0, step=0.5)
            unit = st.selectbox("Unit", ["miles", "km", "reps", "minutes", "sets"])
            timeframe = st.radio("Timeframe", ["Daily", "Weekly"], horizontal=True)

        if st.form_submit_button("💾 Save Goal", use_container_width=True):
            if not goal_name.strip():
                st.warning("Please enter a goal name.")
            else:
                add_goal(workout_type, goal_name.strip(), target, unit, timeframe)
                st.success(f"Goal '{goal_name}' saved!")
                st.rerun()

    st.markdown('<hr class="styled-divider">', unsafe_allow_html=True)

    # Active goals list
    st.markdown('<div class="section-header">Your active goals</div>', unsafe_allow_html=True)

    if not st.session_state["goals"]:
        st.markdown('<div class="empty-state">No goals yet — create one above to get started!</div>', unsafe_allow_html=True)
    else:
        for goal in st.session_state["goals"]:
            display_goal_card(goal)
