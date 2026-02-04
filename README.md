# Wii Habit Tracker

A gamified habit tracking application with Nintendo Wii-inspired UI design. Level up your life, one habit at a time!

## Features

### Gamification System
- **XP & Leveling**: Earn experience points for completing habits with a progressive leveling curve
- **Streak Tracking**: Build daily streaks for bonus XP and rewards
- **Achievements**: Unlock 12 unique achievements for milestones like streak goals, completion counts, and special conditions
- **Coins**: Earn coins for completing habits and leveling up
- **Daily Quests**: Random daily challenges for extra XP and coin rewards

### Wii-Style UI
- Soft blue gradient backgrounds reminiscent of the Wii Menu
- Glossy, rounded "channel" cards with hover animations
- Mii-inspired avatar selection
- Smooth progress bars with gradient fills
- Pulsing streak badges and achievement animations
- Clean, playful typography using Nunito font

### Habit Management
- Create custom habits with icons and descriptions
- Track daily completions with one-click check-ins
- View weekly progress for each habit
- Delete habits through settings

## How to Run

1. Install the requirements:
   ```
   pip install -r requirements.txt
   ```

2. Run the app:
   ```
   streamlit run streamlit_app.py
   ```

## Achievements

| Achievement | Description | XP Reward |
|-------------|-------------|-----------|
| Getting Started | Create your first habit | 50 XP |
| On Fire! | Reach a 3-day streak | 100 XP |
| Week Warrior | Reach a 7-day streak | 250 XP |
| Monthly Master | Reach a 30-day streak | 1000 XP |
| High Five! | Complete 5 habits total | 75 XP |
| Quarter Century | Complete 25 habits total | 200 XP |
| Century Club | Complete 100 habits total | 500 XP |
| Level Up Pro | Reach level 5 | 150 XP |
| Double Digits | Reach level 10 | 300 XP |
| Early Bird | Complete a habit before 9 AM | 100 XP |
| Night Owl | Complete a habit after 10 PM | 100 XP |
| Perfectionist | Complete all habits in a day | 200 XP |

## Technologies

- **Streamlit**: Web application framework
- **Python**: Backend logic
- **Custom CSS**: Wii-themed styling and animations
