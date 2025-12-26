# FinGenius---Expense-Tracker

🧠💰 FinGenius – AI-Powered Personal Finance Manager

FinGenius is a full-stack, AI-assisted personal finance web application designed to help users track expenses, manage income, set savings goals, and understand spending behavior through data visualization, automation, and intelligent insights.
Unlike basic expense trackers, FinGenius focuses on behavioral finance, combining receipt OCR, goal planning, mood tracking, and analytics into one seamless experience.

🌟 Key Highlights

Built using Flask + SQLite
AI-assisted receipt scanning & insights
Clean, animated dashboard for real-time understanding
Designed for learning, scalability, and real-world use

🚀 Core Features (Detailed)
💸 Expense & Income Management
Add, edit, and delete transactions
Separate income and expense flows
Categorized spending (Food, Travel, Bills, Shopping, etc.)
Optional notes and mood tagging per transaction

📊 Smart Dashboard
Live financial summary (Income, Expenses, Balance)
Interactive pie chart for category-wise spending
Monthly spending trends
Smooth UI animations for better UX

🧠 AI-Powered Insights
Detects overspending patterns
Identifies top expense categories
Generates insights like:
“You spent 35% more on Food this month than last month.”
📸 AI Receipt Scanner (OCR)
Upload a receipt image
Automatically extracts:
Amount
Merchant name
Date
Reduces manual data entry
Confidence-based extraction feedback

🎯 Goals & Budget Tracking
Create savings goals (e.g., Trip, Laptop, Emergency Fund)
Track progress visually with progress bars
Category-based budget limits
Alerts when nearing budget limits

😊 Mood-Based Spending Analysis
Attach a mood emoji to expenses
Analyze emotional spending habits
Understand correlation between mood and spending

👥 Group Expense Splitter
Add shared expenses
Auto-split among participants
Track who paid and who owes

⚙️ Personalization & Settings
Theme switching (Light / Dark / Neon)
Currency preference
Enable/disable AI insights
Budget alert settings

🛠️ Tech Stack
Frontend
HTML5
CSS3 (Glassmorphism, animations, responsive layout)
JavaScript
Chart.js
Backend
Python
Flask
Database
SQLite (persistent backend storage)
LocalStorage (client-side caching)
AI & Utilities
OCR for receipt scanning
AI logic for insights generation

📁 Project Structure
FinGenius/
│
├── app.py                # Flask app & routes
├── database.py           # Database manager (SQLite)
├── ocr_processor.py      # Receipt OCR logic
├── requirements.txt
│
├── templates/
│   ├── index.html        # Dashboard
│   ├── add.html          # Add transaction
│   ├── edit.html         # Edit transaction
│   ├── goals.html        # Savings goals
│   ├── insights.html    # AI insights
│   └── settings.html
│
├── static/
│   ├── css/style.css
│   ├── js/script.js
│   └── receipts/
│
└── README.md

📌 Future Scope
User authentication & profiles
Cloud database (PostgreSQL / Firebase)
Mobile app version
AI-based expense prediction
Voice-based expense input

👩‍💻 Author
Mehak Sharma
B.Tech – Artificial Intelligence & Data Science

🎯 Learning Outcomes
Full-stack web development
Database design & queries
AI integration in real applications
UX/UI design with animations
Data analysis & visualization

⭐ Why FinGenius?
FinGenius is not just an expense tracker —
it’s a learning-driven, AI-enhanced finance assistant built to explore how technology can improve everyday money decisions.
