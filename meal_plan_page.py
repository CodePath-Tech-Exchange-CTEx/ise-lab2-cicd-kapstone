#############################################################################
# meal_plan_page.py
#
# This file contains the Meal Plan page for the app.
# It displays Breakfast, Lunch, and Dinner sections with food items,
# calorie tracking, and the ability to add food to each meal.
#############################################################################

import streamlit as st


# ── Default data 

DEFAULT_CALORIE_GOAL = 2000

DEFAULT_MEALS = {
    "Breakfast": [
        {"name": "Oatmeal", "calories": 150},
        {"name": "Banana", "calories": 90},
    ],
    "Lunch": [
        {"name": "Grilled Chicken Salad", "calories": 320},
        {"name": "Whole Wheat Roll", "calories": 110},
    ],
    "Dinner": [
        {"name": "Salmon Fillet", "calories": 400},
        {"name": "Steamed Broccoli", "calories": 55},
    ],
}


def _init_state():
    if "meal_plan" not in st.session_state:
        st.session_state["meal_plan"] = {
            meal: list(items) for meal, items in DEFAULT_MEALS.items()
        }
    if "calorie_goal" not in st.session_state:
        st.session_state["calorie_goal"] = DEFAULT_CALORIE_GOAL
    # Track which meal section is expanded  (None = all collapsed)
    if "expanded_meal" not in st.session_state:
        st.session_state["expanded_meal"] = None
    # Track which meal the "add food" form is open for
    if "adding_to_meal" not in st.session_state:
        st.session_state["adding_to_meal"] = None



def _total_calories():
    return sum(
        item["calories"]
        for items in st.session_state["meal_plan"].values()
        for item in items
    )


def _meal_calories(meal_name):
    return sum(item["calories"] for item in st.session_state["meal_plan"][meal_name])


def _render_add_food_form(meal_name):
    """Renders the 'Add food to <Meal>' form (Image 1 in the mockup)."""
    st.markdown(
        f"""
        <div style="
            border: 2px solid #111;
            border-radius: 10px;
            padding: 18px 24px;
            margin-bottom: 24px;
            text-align: center;
        ">
            <h2 style="margin: 0;">Add food to {meal_name}</h2>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col_food, col_cal = st.columns(2)
    with col_food:
        food_name = st.text_input("Type in Food", key=f"food_name_{meal_name}")
    with col_cal:
        calories = st.number_input(
            "Enter Amount Calories",
            min_value=0,
            max_value=5000,
            step=1,
            key=f"food_cal_{meal_name}",
        )

    col_add, col_cancel = st.columns([1, 3])
    with col_add:
        if st.button("Add", key=f"confirm_add_{meal_name}", use_container_width=True):
            if food_name.strip():
                st.session_state["meal_plan"][meal_name].append(
                    {"name": food_name.strip(), "calories": int(calories)}
                )
                st.session_state["adding_to_meal"] = None
                st.rerun()
            else:
                st.warning("Please enter a food name.")
    with col_cancel:
        if st.button("Cancel", key=f"cancel_add_{meal_name}"):
            st.session_state["adding_to_meal"] = None
            st.rerun()


def _render_meal_section(meal_name, expanded):
    """Renders one meal row with optional expanded details (Images 2 & 3)."""
    meal_cal = _meal_calories(meal_name)


    col_arrow, col_title, col_plus = st.columns([1, 8, 1])

    with col_arrow:
        arrow_label = "▲" if expanded else "▼"
        if st.button(arrow_label, key=f"toggle_{meal_name}"):
            st.session_state["expanded_meal"] = (
                None if expanded else meal_name
            )
            st.session_state["adding_to_meal"] = None
            st.rerun()

    with col_title:
        st.markdown(
            f"""
            <div style="
                border: 1.5px solid #333;
                border-radius: 12px;
                padding: 10px 0;
                text-align: center;
                font-weight: 700;
                font-size: 1.15rem;
                background: #fafafa;
                color: #111;
            ">
                {meal_name}
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col_plus:
        if st.button("＋", key=f"add_{meal_name}"):
            st.session_state["adding_to_meal"] = meal_name
            st.session_state["expanded_meal"] = meal_name
            st.rerun()


    if expanded:
        st.markdown(
            f"<p style='text-align:center; font-weight:600; margin-top:6px;'>"
            f"Calories: {meal_cal}</p>",
            unsafe_allow_html=True,
        )
        items = st.session_state["meal_plan"][meal_name]
        if items:
            st.markdown("**Details:**")
            for idx, item in enumerate(items):
                col_item, col_del = st.columns([10, 1])
                with col_item:
                    st.markdown(f"&nbsp;&nbsp;&nbsp;- {item['name']} ({item['calories']} cal)")
                with col_del:
                    if st.button("🗑", key=f"del_{meal_name}_{idx}"):
                        st.session_state["meal_plan"][meal_name].pop(idx)
                        st.rerun()
        else:
            st.caption("No items yet. Hit ＋ to add food!")




def display_meal_plan_page():
    """Displays the full Meal Plan page."""
    _init_state()

    st.markdown(
        """
        <div style="
            border: 2px solid #111;
            border-radius: 8px;
            padding: 10px 24px;
            max-width: 380px;
            margin: 0 auto 28px auto;
            text-align: center;
            font-size: 1.4rem;
            font-weight: 700;
        ">
            Meal Plan
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ── Calorie goal editor 
    with st.expander("⚙️ Set calorie goal", expanded=False):
        new_goal = st.number_input(
            "Daily Calorie Goal",
            min_value=500,
            max_value=10000,
            step=50,
            value=st.session_state["calorie_goal"],
            key="goal_input",
        )
        if st.button("Save Goal"):
            st.session_state["calorie_goal"] = new_goal
            st.rerun()

    # ── Calorie summary bar 
    total = _total_calories()
    goal = st.session_state["calorie_goal"]
    pct = min(total / goal, 1.0) if goal > 0 else 0
    bar_color = "#e74c3c" if total > goal else "#27ae60"

    st.markdown(
        f"""
        <div style="
            border: 1.5px solid #333;
            border-radius: 8px;
            padding: 10px 18px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 8px;
            font-weight: 600;
        ">
            <span>Total Calories: {total}</span>
            <span>Goal: {goal}</span>
        </div>
        <div style="
            height: 8px;
            background: #e0e0e0;
            border-radius: 4px;
            margin-bottom: 24px;
            overflow: hidden;
        ">
            <div style="
                width: {pct * 100:.1f}%;
                height: 100%;
                background: {bar_color};
                border-radius: 4px;
                transition: width 0.4s;
            "></div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ── Check if "add food" form is open
    adding_to = st.session_state.get("adding_to_meal")
    if adding_to:
        _render_add_food_form(adding_to)
        st.markdown("---")

    # ── Meal sections
    for meal_name in ["Breakfast", "Lunch", "Dinner"]:
        expanded = st.session_state["expanded_meal"] == meal_name
        _render_meal_section(meal_name, expanded)
        st.write("")  # spacing


if __name__ == "__main__":
    display_meal_plan_page()