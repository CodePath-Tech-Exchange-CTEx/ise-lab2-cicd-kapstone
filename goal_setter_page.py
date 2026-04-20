#############################################################################
# goal_setter_page.py
#############################################################################

import streamlit as st


def init_state():
    if "goals" not in st.session_state:
        st.session_state["goals"] = []
    if "next_id" not in st.session_state:
        st.session_state["next_id"] = 1
    if "editing_id" not in st.session_state:
        st.session_state["editing_id"] = None


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
            g["activity"].insert(0, f"+{amount} {g['unit']} logged")
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


def display_goal_card(goal):
    pct = int((goal["completed"] / goal["target"]) * 100) if goal["target"] > 0 else 0

    if pct >= 100:
        accent = "#39d98a"
        badge_bg = "rgba(57,217,138,0.12)"
    elif pct >= 50:
        accent = "#C6FF00"
        badge_bg = "rgba(198,255,0,0.10)"
    else:
        accent = "#f6a623"
        badge_bg = "rgba(246,166,35,0.12)"

    activity_html = ""
    if goal["activity"]:
        rows = "".join(
            f'<div style="display:flex;align-items:center;gap:8px;padding:4px 0;border-bottom:1px solid rgba(255,255,255,0.04);font-size:12px;color:#8a93a8;">'
            f'<span style="width:6px;height:6px;border-radius:50%;background:{accent};flex-shrink:0;"></span>{item}</div>'
            for item in goal["activity"]
        )
        activity_html = f"""
        <div style="margin-top:10px;">
            <div style="font-size:10px;text-transform:uppercase;letter-spacing:1.5px;color:#4a5568;font-weight:600;margin-bottom:4px;">Recent Activity</div>
            {rows}
        </div>
        """

    st.markdown(f"""
    <div style="background:#161b24;border:1px solid rgba(255,255,255,0.07);border-radius:16px;padding:22px 24px;margin-bottom:14px;position:relative;overflow:hidden;">
        <div style="position:absolute;top:0;left:0;right:0;height:2px;background:linear-gradient(90deg,{accent},transparent);"></div>
        <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:14px;">
            <div>
                <div style="font-family:'Barlow Condensed',sans-serif;font-size:22px;font-weight:700;color:#f0f4ff;margin-bottom:4px;">{goal['name']}</div>
                <div style="display:flex;gap:8px;align-items:center;">
                    <span style="background:{badge_bg};color:{accent};border:1px solid {accent}30;border-radius:20px;font-size:10px;font-weight:700;padding:2px 10px;text-transform:uppercase;letter-spacing:0.8px;">{goal['type']}</span>
                    <span style="font-size:11px;color:#4a5568;">{goal['timeframe']}</span>
                </div>
            </div>
            <div style="text-align:right;">
                <div style="font-family:'Barlow Condensed',sans-serif;font-size:40px;font-weight:800;color:{accent};line-height:1;">{pct}%</div>
                <div style="font-size:11px;color:#4a5568;">{goal['completed']} / {goal['target']} {goal['unit']}</div>
            </div>
        </div>
        {activity_html}
    </div>
    """, unsafe_allow_html=True)

    st.progress(pct / 100)

    col_label, col_minus, col_val, col_plus, col_log = st.columns([2, 0.5, 0.7, 0.5, 2])
    key_amount = f"log_amount_{goal['id']}"
    if key_amount not in st.session_state:
        st.session_state[key_amount] = 0.5

    with col_label:
        st.markdown('<div style="font-size:12px;color:#4a5568;padding-top:8px;font-weight:600;text-transform:uppercase;letter-spacing:1px;">Log Progress</div>', unsafe_allow_html=True)
    with col_minus:
        if st.button("−", key=f"minus_{goal['id']}"):
            st.session_state[key_amount] = max(0.5, round(st.session_state[key_amount] - 0.5, 1))
            st.rerun()
    with col_val:
        st.markdown(f'<div style="text-align:center;font-family:Barlow Condensed,sans-serif;font-size:20px;font-weight:700;padding-top:4px;color:#f0f4ff;">{st.session_state[key_amount]}</div>', unsafe_allow_html=True)
    with col_plus:
        if st.button("+", key=f"plus_{goal['id']}"):
            st.session_state[key_amount] = round(st.session_state[key_amount] + 0.5, 1)
            st.rerun()
    with col_log:
        if st.button("Log it ✓", key=f"log_{goal['id']}"):
            log_progress(goal["id"], st.session_state[key_amount])
            st.session_state[key_amount] = 0.5
            st.rerun()

    col_note, col_edit, col_del = st.columns([4, 1, 1])
    with col_note:
        quick_val = st.text_input(
            "Quick note",
            placeholder="Add a note...",
            key=f"quick_{goal['id']}",
            label_visibility="collapsed"
        )
    with col_edit:
        if st.button("✏️", key=f"edit_{goal['id']}", help="Edit goal"):
            st.session_state["editing_id"] = goal["id"]
            st.rerun()
    with col_del:
        if st.button("🗑️", key=f"del_{goal['id']}", help="Delete goal"):
            delete_goal(goal["id"])
            st.rerun()

    if quick_val and st.button("+ Add note", key=f"quick_btn_{goal['id']}"):
        if quick_val.strip():
            goal["activity"].insert(0, f"📝 {quick_val.strip()}")
            if len(goal["activity"]) > 3:
                goal["activity"].pop()
            st.rerun()

    st.markdown('<hr class="custom-divider">', unsafe_allow_html=True)


def display_edit_form(goal):
    st.markdown('<div class="section-title">Edit Goal</div>', unsafe_allow_html=True)
    with st.form(key=f"edit_form_{goal['id']}"):
        new_name = st.text_input("Goal name", value=goal["name"])
        col1, col2 = st.columns(2)
        with col1:
            new_target = st.number_input("Target", min_value=0.1, value=goal["target"], step=0.5)
        with col2:
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
    st.markdown('<hr class="custom-divider">', unsafe_allow_html=True)


def display_goal_setter_page():
    init_state()

    st.markdown("""
    <div class="page-title">GOAL SETTER</div>
    <div class="page-subtitle">Set workout goals, track your progress, and stay on target</div>
    <hr class="custom-divider">
    """, unsafe_allow_html=True)

    if st.session_state["editing_id"] is not None:
        goal = next((g for g in st.session_state["goals"] if g["id"] == st.session_state["editing_id"]), None)
        if goal:
            display_edit_form(goal)

    st.markdown('<div class="section-title">Create a New Goal</div>', unsafe_allow_html=True)
    with st.form("create_goal_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            workout_type = st.selectbox(
                "Type of workout",
                ["Cardio", "Strength", "Flexibility", "HIIT", "Cycling", "Swimming"],
            )
            goal_name = st.text_input("Goal name", placeholder="e.g. Run 5 miles this week")
        with col2:
            target = st.number_input("Target", min_value=0.1, value=5.0, step=0.5)
            unit = st.selectbox("Unit", ["miles", "km", "reps", "minutes", "sets"])
            timeframe = st.radio("Timeframe", ["Daily", "Weekly"], horizontal=True)

        if st.form_submit_button("💾 Save Goal", use_container_width=True):
            if not goal_name.strip():
                st.warning("Please enter a goal name.")
            else:
                add_goal(workout_type, goal_name.strip(), target, unit, timeframe)
                st.success(f"Goal '{goal_name}' created!")
                st.rerun()

    st.markdown('<hr class="custom-divider">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Your Active Goals</div>', unsafe_allow_html=True)

    if not st.session_state["goals"]:
        st.markdown("""
        <div style="text-align:center;padding:48px 20px;color:#2a3040;border:1px dashed rgba(255,255,255,0.07);border-radius:16px;margin-top:8px;">
            <div style="font-family:'Barlow Condensed',sans-serif;font-size:36px;font-weight:800;margin-bottom:8px;">NO GOALS YET</div>
            <div style="font-size:13px;">Create one above to get started 👆</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        for goal in st.session_state["goals"]:
            display_goal_card(goal)