import streamlit as st
import json
from datetime import datetime, timedelta
import random
import math

# Page configuration
st.set_page_config(
    page_title="Wii Habit Tracker",
    page_icon="🎮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============== WII-STYLE CSS ==============
def load_wii_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800&display=swap');

    /* Main Wii Theme */
    :root {
        --wii-blue: #009EDB;
        --wii-light-blue: #7DD3FC;
        --wii-white: #FFFFFF;
        --wii-gray: #E8E8E8;
        --wii-dark: #1A1A2E;
        --wii-orange: #FF6B35;
        --wii-green: #4ADE80;
        --wii-purple: #A855F7;
        --wii-yellow: #FCD34D;
        --wii-pink: #F472B6;
    }

    /* Global styles */
    .stApp {
        background: linear-gradient(180deg, #E0F2FE 0%, #BAE6FD 50%, #7DD3FC 100%);
        font-family: 'Nunito', sans-serif;
    }

    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Wii Channel Card */
    .wii-channel {
        background: linear-gradient(145deg, #FFFFFF 0%, #F0F9FF 100%);
        border-radius: 20px;
        padding: 20px;
        margin: 10px 0;
        box-shadow:
            0 8px 32px rgba(0, 158, 219, 0.2),
            inset 0 2px 4px rgba(255, 255, 255, 0.8),
            0 4px 6px rgba(0, 0, 0, 0.1);
        border: 3px solid rgba(255, 255, 255, 0.8);
        transition: all 0.3s ease;
        cursor: pointer;
    }

    .wii-channel:hover {
        transform: scale(1.02) translateY(-5px);
        box-shadow:
            0 12px 40px rgba(0, 158, 219, 0.3),
            inset 0 2px 4px rgba(255, 255, 255, 0.9),
            0 8px 12px rgba(0, 0, 0, 0.15);
    }

    /* Wii Button */
    .wii-button {
        background: linear-gradient(180deg, #FFFFFF 0%, #E8E8E8 100%);
        border: 3px solid #CCCCCC;
        border-radius: 25px;
        padding: 12px 30px;
        font-family: 'Nunito', sans-serif;
        font-weight: 700;
        font-size: 16px;
        color: #333;
        cursor: pointer;
        transition: all 0.2s ease;
        box-shadow:
            0 4px 8px rgba(0, 0, 0, 0.1),
            inset 0 2px 4px rgba(255, 255, 255, 0.8);
    }

    .wii-button:hover {
        background: linear-gradient(180deg, #7DD3FC 0%, #009EDB 100%);
        color: white;
        border-color: #0284C7;
        transform: scale(1.05);
    }

    .wii-button-primary {
        background: linear-gradient(180deg, #7DD3FC 0%, #009EDB 100%);
        border-color: #0284C7;
        color: white;
    }

    /* Mii Avatar */
    .mii-avatar {
        width: 100px;
        height: 100px;
        border-radius: 50%;
        background: linear-gradient(145deg, #FFE4C4 0%, #FFDAB9 100%);
        border: 4px solid white;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 50px;
        margin: 0 auto;
    }

    /* Progress Bar Wii Style */
    .wii-progress-container {
        background: linear-gradient(180deg, #E8E8E8 0%, #D4D4D4 100%);
        border-radius: 15px;
        padding: 4px;
        box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.2);
        margin: 10px 0;
    }

    .wii-progress-bar {
        background: linear-gradient(180deg, #4ADE80 0%, #22C55E 100%);
        border-radius: 12px;
        height: 24px;
        transition: width 0.5s ease-out;
        box-shadow:
            inset 0 2px 4px rgba(255, 255, 255, 0.4),
            0 2px 4px rgba(0, 0, 0, 0.1);
    }

    /* XP Bar */
    .xp-bar {
        background: linear-gradient(180deg, #FCD34D 0%, #F59E0B 100%);
    }

    /* Streak Fire */
    .streak-badge {
        background: linear-gradient(145deg, #FF6B35 0%, #DC2626 100%);
        color: white;
        padding: 8px 16px;
        border-radius: 20px;
        font-weight: 700;
        display: inline-flex;
        align-items: center;
        gap: 8px;
        box-shadow: 0 4px 12px rgba(255, 107, 53, 0.4);
        animation: pulse 2s infinite;
    }

    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.05); }
    }

    /* Achievement Badge */
    .achievement-badge {
        background: linear-gradient(145deg, #A855F7 0%, #7C3AED 100%);
        color: white;
        padding: 15px;
        border-radius: 15px;
        text-align: center;
        box-shadow: 0 4px 12px rgba(168, 85, 247, 0.4);
        transition: all 0.3s ease;
    }

    .achievement-badge:hover {
        transform: scale(1.1) rotate(5deg);
    }

    .achievement-locked {
        background: linear-gradient(145deg, #9CA3AF 0%, #6B7280 100%);
        opacity: 0.6;
    }

    /* Level Badge */
    .level-badge {
        background: linear-gradient(145deg, #009EDB 0%, #0369A1 100%);
        color: white;
        padding: 10px 20px;
        border-radius: 25px;
        font-size: 18px;
        font-weight: 800;
        box-shadow:
            0 4px 12px rgba(0, 158, 219, 0.4),
            inset 0 2px 4px rgba(255, 255, 255, 0.3);
    }

    /* Habit Card */
    .habit-card {
        background: linear-gradient(145deg, #FFFFFF 0%, #F0F9FF 100%);
        border-radius: 20px;
        padding: 20px;
        margin: 15px 0;
        border-left: 6px solid var(--wii-blue);
        box-shadow:
            0 4px 16px rgba(0, 158, 219, 0.15),
            inset 0 2px 4px rgba(255, 255, 255, 0.8);
        transition: all 0.3s ease;
    }

    .habit-card:hover {
        transform: translateX(10px);
        box-shadow:
            0 8px 24px rgba(0, 158, 219, 0.25),
            inset 0 2px 4px rgba(255, 255, 255, 0.9);
    }

    .habit-card.completed {
        border-left-color: var(--wii-green);
        background: linear-gradient(145deg, #F0FDF4 0%, #DCFCE7 100%);
    }

    /* Stats Card */
    .stats-card {
        background: linear-gradient(145deg, rgba(255,255,255,0.9) 0%, rgba(240,249,255,0.9) 100%);
        border-radius: 20px;
        padding: 25px;
        text-align: center;
        box-shadow: 0 8px 32px rgba(0, 158, 219, 0.2);
        border: 2px solid rgba(255, 255, 255, 0.8);
    }

    .stats-number {
        font-size: 48px;
        font-weight: 800;
        background: linear-gradient(180deg, #009EDB 0%, #0369A1 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }

    /* Title styling */
    .wii-title {
        font-family: 'Nunito', sans-serif;
        font-weight: 800;
        font-size: 42px;
        background: linear-gradient(180deg, #009EDB 0%, #0369A1 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-align: center;
        margin-bottom: 10px;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.1);
    }

    .wii-subtitle {
        font-family: 'Nunito', sans-serif;
        font-weight: 600;
        font-size: 18px;
        color: #0369A1;
        text-align: center;
        margin-bottom: 30px;
    }

    /* Notification popup */
    .notification-popup {
        position: fixed;
        top: 20px;
        right: 20px;
        background: linear-gradient(145deg, #4ADE80 0%, #22C55E 100%);
        color: white;
        padding: 20px 30px;
        border-radius: 20px;
        font-weight: 700;
        box-shadow: 0 8px 32px rgba(34, 197, 94, 0.4);
        animation: slideIn 0.5s ease, fadeOut 0.5s ease 2.5s forwards;
        z-index: 1000;
    }

    @keyframes slideIn {
        from { transform: translateX(100%); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }

    @keyframes fadeOut {
        from { opacity: 1; }
        to { opacity: 0; }
    }

    /* Daily Quest Card */
    .quest-card {
        background: linear-gradient(145deg, #FEF3C7 0%, #FDE68A 100%);
        border-radius: 20px;
        padding: 20px;
        margin: 10px 0;
        border: 3px solid #F59E0B;
        box-shadow: 0 4px 16px rgba(245, 158, 11, 0.3);
    }

    /* Wii Remote pointer animation */
    .wii-pointer {
        animation: wobble 0.5s ease infinite;
    }

    @keyframes wobble {
        0%, 100% { transform: rotate(-2deg); }
        50% { transform: rotate(2deg); }
    }

    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1E3A5F 0%, #0F172A 100%);
    }

    [data-testid="stSidebar"] * {
        color: white !important;
    }

    /* Button overrides */
    .stButton > button {
        background: linear-gradient(180deg, #FFFFFF 0%, #E8E8E8 100%);
        border: 3px solid #CCCCCC;
        border-radius: 25px;
        padding: 12px 30px;
        font-family: 'Nunito', sans-serif;
        font-weight: 700;
        font-size: 16px;
        color: #333;
        transition: all 0.2s ease;
        box-shadow:
            0 4px 8px rgba(0, 0, 0, 0.1),
            inset 0 2px 4px rgba(255, 255, 255, 0.8);
    }

    .stButton > button:hover {
        background: linear-gradient(180deg, #7DD3FC 0%, #009EDB 100%);
        color: white;
        border-color: #0284C7;
        transform: scale(1.05);
    }

    /* Checkbox styling */
    .stCheckbox > label {
        font-family: 'Nunito', sans-serif;
        font-weight: 600;
    }

    /* Input styling */
    .stTextInput > div > div > input {
        border-radius: 15px;
        border: 2px solid #CCCCCC;
        font-family: 'Nunito', sans-serif;
    }

    .stTextInput > div > div > input:focus {
        border-color: #009EDB;
        box-shadow: 0 0 0 3px rgba(0, 158, 219, 0.2);
    }

    /* Select box */
    .stSelectbox > div > div {
        border-radius: 15px;
    }

    /* Confetti animation */
    .confetti {
        position: fixed;
        width: 10px;
        height: 10px;
        background-color: #f00;
        animation: confetti-fall 3s linear forwards;
    }

    @keyframes confetti-fall {
        0% { transform: translateY(-100vh) rotate(0deg); opacity: 1; }
        100% { transform: translateY(100vh) rotate(720deg); opacity: 0; }
    }
    </style>
    """, unsafe_allow_html=True)

# ============== DATA MANAGEMENT ==============
def init_session_state():
    """Initialize all session state variables"""
    if 'habits' not in st.session_state:
        st.session_state.habits = []

    if 'user_data' not in st.session_state:
        st.session_state.user_data = {
            'name': 'Player 1',
            'avatar': '😊',
            'xp': 0,
            'level': 1,
            'total_completions': 0,
            'current_streak': 0,
            'best_streak': 0,
            'coins': 0,
            'achievements': [],
            'daily_quests_completed': 0,
            'last_login': str(datetime.now().date())
        }

    if 'achievements_list' not in st.session_state:
        st.session_state.achievements_list = [
            {'id': 'first_habit', 'name': 'Getting Started', 'desc': 'Create your first habit', 'icon': '🌟', 'xp': 50, 'unlocked': False},
            {'id': 'streak_3', 'name': 'On Fire!', 'desc': 'Reach a 3-day streak', 'icon': '🔥', 'xp': 100, 'unlocked': False},
            {'id': 'streak_7', 'name': 'Week Warrior', 'desc': 'Reach a 7-day streak', 'icon': '⚔️', 'xp': 250, 'unlocked': False},
            {'id': 'streak_30', 'name': 'Monthly Master', 'desc': 'Reach a 30-day streak', 'icon': '👑', 'xp': 1000, 'unlocked': False},
            {'id': 'complete_5', 'name': 'High Five!', 'desc': 'Complete 5 habits total', 'icon': '🖐️', 'xp': 75, 'unlocked': False},
            {'id': 'complete_25', 'name': 'Quarter Century', 'desc': 'Complete 25 habits total', 'icon': '🎯', 'xp': 200, 'unlocked': False},
            {'id': 'complete_100', 'name': 'Century Club', 'desc': 'Complete 100 habits total', 'icon': '💯', 'xp': 500, 'unlocked': False},
            {'id': 'level_5', 'name': 'Level Up Pro', 'desc': 'Reach level 5', 'icon': '📈', 'xp': 150, 'unlocked': False},
            {'id': 'level_10', 'name': 'Double Digits', 'desc': 'Reach level 10', 'icon': '🏆', 'xp': 300, 'unlocked': False},
            {'id': 'early_bird', 'name': 'Early Bird', 'desc': 'Complete a habit before 9 AM', 'icon': '🐦', 'xp': 100, 'unlocked': False},
            {'id': 'night_owl', 'name': 'Night Owl', 'desc': 'Complete a habit after 10 PM', 'icon': '🦉', 'xp': 100, 'unlocked': False},
            {'id': 'perfectionist', 'name': 'Perfectionist', 'desc': 'Complete all habits in a day', 'icon': '✨', 'xp': 200, 'unlocked': False},
        ]

    if 'daily_quests' not in st.session_state:
        generate_daily_quests()

    if 'notifications' not in st.session_state:
        st.session_state.notifications = []

def generate_daily_quests():
    """Generate random daily quests"""
    quest_templates = [
        {'name': 'Complete 3 habits today', 'target': 3, 'type': 'completions', 'reward_xp': 75, 'reward_coins': 25},
        {'name': 'Start a new streak', 'target': 1, 'type': 'streak', 'reward_xp': 50, 'reward_coins': 15},
        {'name': 'Check in on all habits', 'target': 1, 'type': 'check_all', 'reward_xp': 60, 'reward_coins': 20},
        {'name': 'Complete a habit 2 times', 'target': 2, 'type': 'completions', 'reward_xp': 40, 'reward_coins': 10},
    ]
    st.session_state.daily_quests = random.sample(quest_templates, min(2, len(quest_templates)))
    for quest in st.session_state.daily_quests:
        quest['progress'] = 0
        quest['completed'] = False

def calculate_level(xp):
    """Calculate level from XP using a curve"""
    # Level formula: xp needed for level n = 100 * n^1.5
    level = 1
    xp_needed = 100
    remaining_xp = xp

    while remaining_xp >= xp_needed:
        remaining_xp -= xp_needed
        level += 1
        xp_needed = int(100 * (level ** 1.5))

    return level, remaining_xp, xp_needed

def add_xp(amount, reason=""):
    """Add XP to user and check for level up"""
    st.session_state.user_data['xp'] += amount
    old_level = st.session_state.user_data['level']
    new_level, _, _ = calculate_level(st.session_state.user_data['xp'])

    if new_level > old_level:
        st.session_state.user_data['level'] = new_level
        st.session_state.notifications.append(f"🎉 LEVEL UP! You are now Level {new_level}!")
        st.session_state.user_data['coins'] += new_level * 10
        check_achievements()

def check_achievements():
    """Check and unlock achievements"""
    user = st.session_state.user_data

    for achievement in st.session_state.achievements_list:
        if achievement['unlocked']:
            continue

        unlocked = False

        if achievement['id'] == 'first_habit' and len(st.session_state.habits) >= 1:
            unlocked = True
        elif achievement['id'] == 'streak_3' and user['current_streak'] >= 3:
            unlocked = True
        elif achievement['id'] == 'streak_7' and user['current_streak'] >= 7:
            unlocked = True
        elif achievement['id'] == 'streak_30' and user['current_streak'] >= 30:
            unlocked = True
        elif achievement['id'] == 'complete_5' and user['total_completions'] >= 5:
            unlocked = True
        elif achievement['id'] == 'complete_25' and user['total_completions'] >= 25:
            unlocked = True
        elif achievement['id'] == 'complete_100' and user['total_completions'] >= 100:
            unlocked = True
        elif achievement['id'] == 'level_5' and user['level'] >= 5:
            unlocked = True
        elif achievement['id'] == 'level_10' and user['level'] >= 10:
            unlocked = True
        elif achievement['id'] == 'early_bird':
            hour = datetime.now().hour
            if hour < 9:
                unlocked = True
        elif achievement['id'] == 'night_owl':
            hour = datetime.now().hour
            if hour >= 22:
                unlocked = True

        if unlocked:
            achievement['unlocked'] = True
            user['achievements'].append(achievement['id'])
            add_xp(achievement['xp'])
            st.session_state.notifications.append(
                f"🏆 Achievement Unlocked: {achievement['name']}! (+{achievement['xp']} XP)"
            )

def complete_habit(habit_index):
    """Mark a habit as complete for today"""
    today = str(datetime.now().date())
    habit = st.session_state.habits[habit_index]

    if today not in habit['completed_dates']:
        habit['completed_dates'].append(today)
        habit['streak'] += 1

        # Update user stats
        st.session_state.user_data['total_completions'] += 1

        # Update streak
        if habit['streak'] > st.session_state.user_data['current_streak']:
            st.session_state.user_data['current_streak'] = habit['streak']
        if habit['streak'] > st.session_state.user_data['best_streak']:
            st.session_state.user_data['best_streak'] = habit['streak']

        # Calculate XP reward
        base_xp = 25
        streak_bonus = min(habit['streak'] * 5, 50)  # Max 50 bonus from streak
        total_xp = base_xp + streak_bonus

        add_xp(total_xp, f"Completed: {habit['name']}")
        st.session_state.user_data['coins'] += 5 + (habit['streak'] // 3)

        # Update daily quest progress
        for quest in st.session_state.daily_quests:
            if quest['type'] == 'completions' and not quest['completed']:
                quest['progress'] += 1
                if quest['progress'] >= quest['target']:
                    quest['completed'] = True
                    add_xp(quest['reward_xp'])
                    st.session_state.user_data['coins'] += quest['reward_coins']
                    st.session_state.notifications.append(
                        f"✅ Daily Quest Complete: {quest['name']}!"
                    )

        st.session_state.notifications.append(
            f"✨ +{total_xp} XP for completing {habit['name']}!"
        )

        check_achievements()

        # Check perfectionist achievement
        all_complete = all(
            today in h['completed_dates']
            for h in st.session_state.habits
        )
        if all_complete and len(st.session_state.habits) > 0:
            for achievement in st.session_state.achievements_list:
                if achievement['id'] == 'perfectionist' and not achievement['unlocked']:
                    achievement['unlocked'] = True
                    add_xp(achievement['xp'])
                    st.session_state.notifications.append(
                        f"🏆 Achievement Unlocked: {achievement['name']}!"
                    )

# ============== UI COMPONENTS ==============
def render_header():
    """Render the Wii-style header"""
    st.markdown('<h1 class="wii-title">🎮 Wii Habit Tracker</h1>', unsafe_allow_html=True)
    st.markdown('<p class="wii-subtitle">Level up your life, one habit at a time!</p>', unsafe_allow_html=True)

def render_user_stats():
    """Render user stats panel"""
    user = st.session_state.user_data
    level, current_xp, xp_needed = calculate_level(user['xp'])
    xp_percentage = (current_xp / xp_needed) * 100

    st.markdown(f"""
    <div class="wii-channel" style="text-align: center;">
        <div class="mii-avatar">{user['avatar']}</div>
        <h2 style="margin: 15px 0 5px 0; color: #0369A1;">{user['name']}</h2>
        <span class="level-badge">Level {level}</span>

        <div style="margin-top: 20px;">
            <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                <span style="font-weight: 600; color: #666;">XP Progress</span>
                <span style="font-weight: 700; color: #F59E0B;">{current_xp}/{xp_needed}</span>
            </div>
            <div class="wii-progress-container">
                <div class="wii-progress-bar xp-bar" style="width: {xp_percentage}%;"></div>
            </div>
        </div>

        <div style="display: flex; justify-content: space-around; margin-top: 20px;">
            <div>
                <div class="streak-badge">🔥 {user['current_streak']}</div>
                <p style="font-size: 12px; color: #666; margin-top: 5px;">Current Streak</p>
            </div>
            <div>
                <span style="font-size: 24px; font-weight: 800; color: #F59E0B;">🪙 {user['coins']}</span>
                <p style="font-size: 12px; color: #666; margin-top: 5px;">Coins</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_daily_quests():
    """Render daily quests panel"""
    st.markdown("### 📋 Daily Quests")

    for quest in st.session_state.daily_quests:
        status = "✅" if quest['completed'] else f"{quest['progress']}/{quest['target']}"
        bg_color = "#DCFCE7" if quest['completed'] else "#FEF3C7"
        border_color = "#22C55E" if quest['completed'] else "#F59E0B"

        st.markdown(f"""
        <div class="quest-card" style="background: linear-gradient(145deg, {bg_color} 0%, {bg_color} 100%); border-color: {border_color};">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <strong>{quest['name']}</strong>
                    <p style="margin: 5px 0; color: #666; font-size: 14px;">
                        Reward: +{quest['reward_xp']} XP, +{quest['reward_coins']} 🪙
                    </p>
                </div>
                <span style="font-size: 20px; font-weight: 700;">{status}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

def render_habits():
    """Render the habits list"""
    today = str(datetime.now().date())

    if not st.session_state.habits:
        st.markdown("""
        <div class="wii-channel" style="text-align: center; padding: 40px;">
            <span style="font-size: 60px;">🎯</span>
            <h3 style="color: #0369A1; margin: 20px 0;">No habits yet!</h3>
            <p style="color: #666;">Create your first habit to start your journey!</p>
        </div>
        """, unsafe_allow_html=True)
        return

    for i, habit in enumerate(st.session_state.habits):
        is_completed = today in habit['completed_dates']
        card_class = "habit-card completed" if is_completed else "habit-card"

        # Calculate progress percentage for the week
        week_progress = min(habit['streak'] / 7 * 100, 100)

        col1, col2 = st.columns([4, 1])

        with col1:
            st.markdown(f"""
            <div class="{card_class}">
                <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                    <div>
                        <span style="font-size: 30px;">{habit['icon']}</span>
                        <h3 style="margin: 5px 0; color: #0369A1;">{habit['name']}</h3>
                        <p style="color: #666; margin: 0;">{habit.get('description', '')}</p>
                    </div>
                    <div style="text-align: right;">
                        <div class="streak-badge" style="{'opacity: 0.5;' if not is_completed else ''}">
                            🔥 {habit['streak']} day{'s' if habit['streak'] != 1 else ''}
                        </div>
                    </div>
                </div>
                <div style="margin-top: 15px;">
                    <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                        <span style="font-size: 12px; color: #666;">Weekly Progress</span>
                        <span style="font-size: 12px; font-weight: 600; color: #22C55E;">{habit['streak']}/7 days</span>
                    </div>
                    <div class="wii-progress-container">
                        <div class="wii-progress-bar" style="width: {week_progress}%;"></div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            if not is_completed:
                if st.button("✓ Done", key=f"complete_{i}", use_container_width=True):
                    complete_habit(i)
                    st.rerun()
            else:
                st.markdown("""
                <div style="text-align: center; padding: 20px;">
                    <span style="font-size: 40px;">✅</span>
                    <p style="color: #22C55E; font-weight: 700;">Done!</p>
                </div>
                """, unsafe_allow_html=True)

def render_achievements():
    """Render achievements panel"""
    st.markdown("### 🏆 Achievements")

    cols = st.columns(4)
    for i, achievement in enumerate(st.session_state.achievements_list):
        with cols[i % 4]:
            locked_class = "" if achievement['unlocked'] else "achievement-locked"
            st.markdown(f"""
            <div class="achievement-badge {locked_class}">
                <span style="font-size: 32px;">{achievement['icon']}</span>
                <h4 style="margin: 10px 0 5px 0;">{achievement['name']}</h4>
                <p style="font-size: 12px; margin: 0;">{achievement['desc']}</p>
                <p style="font-size: 11px; margin-top: 5px; opacity: 0.8;">+{achievement['xp']} XP</p>
            </div>
            """, unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)

def render_stats_dashboard():
    """Render statistics dashboard"""
    user = st.session_state.user_data

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(f"""
        <div class="stats-card">
            <span style="font-size: 40px;">📊</span>
            <div class="stats-number">{user['total_completions']}</div>
            <p style="color: #666; margin: 0;">Total Completions</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="stats-card">
            <span style="font-size: 40px;">🔥</span>
            <div class="stats-number">{user['best_streak']}</div>
            <p style="color: #666; margin: 0;">Best Streak</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="stats-card">
            <span style="font-size: 40px;">⭐</span>
            <div class="stats-number">{user['xp']}</div>
            <p style="color: #666; margin: 0;">Total XP</p>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        unlocked = len([a for a in st.session_state.achievements_list if a['unlocked']])
        total = len(st.session_state.achievements_list)
        st.markdown(f"""
        <div class="stats-card">
            <span style="font-size: 40px;">🏆</span>
            <div class="stats-number">{unlocked}/{total}</div>
            <p style="color: #666; margin: 0;">Achievements</p>
        </div>
        """, unsafe_allow_html=True)

def render_notifications():
    """Render any pending notifications"""
    for notification in st.session_state.notifications:
        st.toast(notification, icon="🎮")
    st.session_state.notifications = []

def render_add_habit_form():
    """Render the add habit form"""
    st.markdown("### ➕ Create New Habit")

    with st.form("add_habit_form", clear_on_submit=True):
        col1, col2 = st.columns([3, 1])

        with col1:
            habit_name = st.text_input("Habit Name", placeholder="e.g., Exercise for 30 minutes")
            habit_desc = st.text_input("Description (optional)", placeholder="e.g., Any form of physical activity")

        with col2:
            icons = ["🏃", "📚", "💪", "🧘", "💧", "🥗", "😴", "🎯", "✍️", "🎨", "🎵", "🧹", "💰", "🌱", "❤️"]
            habit_icon = st.selectbox("Icon", icons)

        submitted = st.form_submit_button("Create Habit", use_container_width=True)

        if submitted and habit_name:
            new_habit = {
                'name': habit_name,
                'description': habit_desc,
                'icon': habit_icon,
                'created_date': str(datetime.now().date()),
                'completed_dates': [],
                'streak': 0
            }
            st.session_state.habits.append(new_habit)
            st.session_state.notifications.append(f"🎉 New habit created: {habit_name}!")
            check_achievements()
            st.rerun()

def render_settings():
    """Render settings panel"""
    st.markdown("### ⚙️ Settings")

    with st.form("settings_form"):
        new_name = st.text_input("Your Name", value=st.session_state.user_data['name'])

        avatars = ["😊", "😎", "🤓", "😄", "🥳", "🤗", "😇", "🦸", "🧙", "👨‍🚀", "👩‍💻", "🐱", "🐶", "🦊", "🐼"]
        current_avatar = st.session_state.user_data['avatar']
        avatar_index = avatars.index(current_avatar) if current_avatar in avatars else 0
        new_avatar = st.selectbox("Avatar", avatars, index=avatar_index)

        if st.form_submit_button("Save Settings", use_container_width=True):
            st.session_state.user_data['name'] = new_name
            st.session_state.user_data['avatar'] = new_avatar
            st.success("Settings saved!")
            st.rerun()

    st.markdown("---")
    st.markdown("### 🗑️ Manage Habits")

    if st.session_state.habits:
        habit_to_delete = st.selectbox(
            "Select habit to delete",
            options=range(len(st.session_state.habits)),
            format_func=lambda x: f"{st.session_state.habits[x]['icon']} {st.session_state.habits[x]['name']}"
        )

        if st.button("Delete Habit", type="secondary"):
            deleted_habit = st.session_state.habits.pop(habit_to_delete)
            st.warning(f"Deleted: {deleted_habit['name']}")
            st.rerun()
    else:
        st.info("No habits to manage.")

    st.markdown("---")

    if st.button("🔄 Reset All Data", type="secondary"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.success("All data has been reset!")
        st.rerun()

# ============== MAIN APP ==============
def main():
    load_wii_css()
    init_session_state()

    # Sidebar
    with st.sidebar:
        st.markdown("""
        <div style="text-align: center; padding: 20px;">
            <span style="font-size: 60px;">🎮</span>
            <h2 style="color: white; margin: 10px 0;">Wii Habits</h2>
        </div>
        """, unsafe_allow_html=True)

        render_user_stats()

        st.markdown("<br>", unsafe_allow_html=True)
        render_daily_quests()

    # Main content
    render_header()
    render_notifications()

    # Navigation tabs
    tab1, tab2, tab3, tab4 = st.tabs(["🏠 My Habits", "➕ Add Habit", "🏆 Achievements", "⚙️ Settings"])

    with tab1:
        render_stats_dashboard()
        st.markdown("<br>", unsafe_allow_html=True)
        render_habits()

    with tab2:
        render_add_habit_form()

        # Show preview of habit cards
        st.markdown("### 💡 Tips for Good Habits")
        tips = [
            ("🎯", "Start Small", "Begin with habits that take less than 5 minutes"),
            ("⏰", "Be Specific", "Set a specific time and place for your habit"),
            ("🔗", "Stack Habits", "Link new habits to existing routines"),
            ("🎉", "Celebrate Wins", "Reward yourself for completing habits"),
        ]

        cols = st.columns(4)
        for i, (icon, title, desc) in enumerate(tips):
            with cols[i]:
                st.markdown(f"""
                <div class="wii-channel" style="text-align: center; height: 150px;">
                    <span style="font-size: 36px;">{icon}</span>
                    <h4 style="color: #0369A1; margin: 10px 0 5px 0;">{title}</h4>
                    <p style="font-size: 12px; color: #666;">{desc}</p>
                </div>
                """, unsafe_allow_html=True)

    with tab3:
        render_achievements()

        # Achievement progress
        unlocked = len([a for a in st.session_state.achievements_list if a['unlocked']])
        total = len(st.session_state.achievements_list)
        progress = (unlocked / total) * 100

        st.markdown(f"""
        <div class="wii-channel" style="margin-top: 20px;">
            <h3 style="color: #0369A1; margin-bottom: 15px;">Achievement Progress</h3>
            <div class="wii-progress-container">
                <div class="wii-progress-bar" style="width: {progress}%; background: linear-gradient(180deg, #A855F7 0%, #7C3AED 100%);"></div>
            </div>
            <p style="text-align: center; color: #666; margin-top: 10px;">{unlocked} of {total} achievements unlocked</p>
        </div>
        """, unsafe_allow_html=True)

    with tab4:
        render_settings()

if __name__ == "__main__":
    main()
