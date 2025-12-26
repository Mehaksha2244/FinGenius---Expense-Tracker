# 💰 Personal Expense Tracker - Gen Z Edition

A modern, aesthetic, and feature-rich personal expense tracking web application built with Flask, designed specifically for the Gen Z generation. Track your spending, achieve financial goals, and build better money habits with style! 🚀

![Expense Tracker Demo](https://via.placeholder.com/800x400/FFD1DC/AEEEEE?text=Modern+Expense+Tracker)

## ✨ Features

### 🎯 Core Features
- **📊 Interactive Dashboard** - Beautiful charts and analytics with Chart.js
- **💰 Expense Tracking** - Add, edit, and manage expenses with mood tracking
- **🧠 AI-Powered Insights** - Smart spending analysis and recommendations
- **🎯 Gamified Goals** - Set and track financial goals with progress bars
- **📅 Calendar View** - Visual spending heatmap with date filtering
- **👥 Group Expenses** - Split costs with friends and track who owes what
- **📸 Receipt Scanning** - OCR-powered receipt processing with pytesseract
- **💾 Browser LocalStorage** - All data persists in your browser, works offline!

### 🎨 Design Features
- **🌸 Modern Pastel Theme** - Beautiful pastel gradients and glass morphism
- **🌙 Dark Mode** - Sleek dark theme for night owls
- **⚡ Neon Mode** - Vibrant neon theme for the bold
- **📱 Responsive Design** - Perfect on desktop, tablet, and mobile
- **🎭 Smooth Animations** - Delightful micro-interactions and transitions

### 🚀 Advanced Features
- **😊 Mood Tracking** - Track how you feel about each expense
- **💳 Budget Management** - Set limits and get alerts
- **📈 Spending Analytics** - Category breakdowns and trends
- **🎮 Achievement System** - Unlock badges for financial milestones
- **📊 Export Data** - Download your data in CSV, JSON, or PDF
- **🔔 Smart Notifications** - Budget alerts and spending insights
- **🔄 Data Persistence** - Browser-based storage with import/export capabilities

## 🛠️ Technology Stack

- **Backend**: Python Flask
- **Database**: SQLite3
- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **Charts**: Chart.js
- **OCR**: pytesseract + OpenCV
- **Styling**: Custom CSS with CSS Variables
- **Icons**: Emoji-based (Gen Z friendly! 😊)

## 📦 Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Tesseract OCR (for receipt scanning)

### Step 1: Clone the Repository
```bash
git clone https://github.com/yourusername/expense-tracker-genz.git
cd expense-tracker-genz
```

### Step 2: Install Tesseract OCR

#### Windows
1. Download Tesseract from [GitHub releases](https://github.com/UB-Mannheim/tesseract/wiki)
2. Install and add to PATH
3. Update the path in `ocr_processor.py` if needed:
```python
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
```

#### macOS
```bash
brew install tesseract
```

#### Linux (Ubuntu/Debian)
```bash
sudo apt-get install tesseract-ocr
```

### Step 3: Install Python Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Run the Application
```bash
python app.py
```

### Step 5: Open in Browser
Navigate to `http://localhost:5000` in your web browser.

## 🚀 Quick Start Guide

### 1. First Time Setup
1. Open the app in your browser
2. The database will be created automatically
3. Start adding your first expense!

### 2. Adding Expenses
1. Click "➕ Add Expense" in the navigation
2. Fill in the details or upload a receipt for automatic processing
3. Select your mood 😊
4. Click "💰 Add Expense"

### 3. Setting Goals
1. Go to "🎯 Goals" page
2. Click "🎯 Create New Goal"
3. Set your target amount and deadline
4. Track your progress with beautiful progress bars

### 4. Viewing Insights
1. Visit "🧠 Insights" for AI-generated spending analysis
2. Check out your spending patterns and get recommendations
3. See your financial health score

## 📁 Project Structure

```
ExpenseTrackerWeb/
├── app.py                      # Main Flask application
├── database.py                 # Database management
├── ocr_processor.py           # Receipt OCR processing
├── requirements.txt           # Python dependencies
├── README.md                  # This file
├── LOCALSTORAGE_GUIDE.md      # LocalStorage documentation
├── .gitignore                 # Git ignore rules
│
├── static/
│   ├── style.css              # Modern CSS with themes
│   ├── dashboard.js           # Interactive JavaScript
│   ├── localStorage.js        # Browser storage utilities
│   ├── dashboardIntegration.js # UI-storage synchronization
│   └── receipts/              # Uploaded receipt images
│
└── templates/
    ├── base.html              # Base template with scripts
    ├── index.html             # Main dashboard
    ├── add.html               # Add expense page
    ├── add_income.html        # Add income page
    ├── edit.html              # Edit expense page
    ├── insights.html          # AI insights page
    ├── goals.html             # Financial goals page
    ├── calendar.html          # Calendar view
    ├── group.html             # Group expenses
    ├── scan_receipt.html      # Receipt scanner
    └── settings.html          # User settings
```

## 🎨 Customization

### Themes
The app supports three built-in themes:
- **🌸 Pastel** (Default) - Soft pastel colors
- **🌙 Dark** - Dark mode for night usage
- **⚡ Neon** - Vibrant neon colors

### Adding Custom Themes
1. Edit `static/style.css`
2. Add new theme variables in `:root` section
3. Create new `[data-theme="your-theme"]` section
4. Update theme toggle in `dashboard.js`

### Custom Categories
1. Go to Settings page
2. Add new budget categories
3. Set monthly limits
4. Categories will appear in expense forms

## 🔧 Configuration

### Environment Variables
Create a `.env` file for configuration:
```env
FLASK_ENV=development
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///expenses.db
TESSERACT_CMD=/usr/bin/tesseract
```

### Database Configuration
The app uses SQLite by default. For production, consider:
- PostgreSQL
- MySQL
- SQLite (for small to medium usage)

### 💾 LocalStorage Feature

FinTrack now includes **browser-based localStorage** for client-side data persistence! This means:

✅ **Works Offline** - No server required for basic functionality
✅ **Instant Sync** - Changes saved immediately to your browser
✅ **Privacy First** - Your data stays on your device
✅ **Easy Backup** - Export/import your data as JSON

#### How It Works
All expenses, income, goals, and settings are automatically saved to your browser's localStorage. Data persists across:
- Page refreshes
- Browser restarts
- Tab closures

#### Storage Keys
- `fintrack_expenses` - All expense transactions
- `fintrack_income` - Income entries
- `fintrack_goals` - Savings goals
- `fintrack_settings` - User preferences
- `fintrack_budget_categories` - Budget limits
- `fintrack_group_expenses` - Shared expenses

#### Using LocalStorage
```javascript
// Access the storage API
const expenses = window.FinTrackStorage.getExpenses();
const settings = window.FinTrackStorage.getSettings();

// Export all data
const backup = window.FinTrackStorage.exportAllData();
console.log(JSON.stringify(backup, null, 2));

// Clear all data
window.FinTrackStorage.clearLocalStorageData();
```

For detailed documentation, see [LOCALSTORAGE_GUIDE.md](LOCALSTORAGE_GUIDE.md)

## 📱 Mobile Support

The app is fully responsive and works great on:
- 📱 Mobile phones (iOS/Android)
- 📱 Tablets (iPad/Android tablets)
- 💻 Desktop computers
- 🖥️ Large screens

## 🧪 Testing

Run the test suite:
```bash
pytest tests/
```

## 🚀 Deployment

### Heroku
1. Create a `Procfile`:
```
web: gunicorn app:app
```
2. Deploy to Heroku:
```bash
git push heroku main
```

### Docker
1. Create `Dockerfile`:
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["gunicorn", "app:app"]
```

### VPS/Cloud
1. Install dependencies
2. Set up reverse proxy (Nginx)
3. Use Gunicorn as WSGI server
4. Set up SSL certificate

## 🤝 Contributing

We welcome contributions! Here's how to get started:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit your changes: `git commit -m 'Add amazing feature'`
4. Push to the branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

### Development Setup
1. Clone your fork
2. Create virtual environment: `python -m venv venv`
3. Activate it: `source venv/bin/activate` (Linux/Mac) or `venv\Scripts\activate` (Windows)
4. Install dependencies: `pip install -r requirements.txt`
5. Run the app: `python app.py`

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Chart.js** for beautiful charts
- **pytesseract** for OCR functionality
- **OpenCV** for image processing
- **Flask** for the web framework
- **Gen Z** for the inspiration! 🎉

## 📞 Support

- 📧 Email: support@expensetracker.com
- 💬 Discord: [Join our server](https://discord.gg/expensetracker)
- 🐛 Issues: [GitHub Issues](https://github.com/yourusername/expense-tracker-genz/issues)
- 📖 Docs: [Full Documentation](https://docs.expensetracker.com)

## 🎯 Roadmap

### Version 2.0
- [ ] Mobile app (React Native)
- [ ] Bank account integration
- [ ] Investment tracking
- [ ] Bill reminders
- [ ] Social features

### Version 2.1
- [ ] Machine learning insights
- [ ] Voice input
- [ ] AR receipt scanning
- [ ] Cryptocurrency support

## 💡 Tips for Gen Z Users

1. **📸 Use Receipt Scanning** - Take photos of receipts for automatic data entry
2. **😊 Track Your Mood** - See how your emotions affect your spending
3. **🎯 Set Micro-Goals** - Start small and build momentum
4. **👥 Split with Friends** - Use group expenses for shared costs
5. **📊 Check Insights Daily** - Stay aware of your spending patterns
6. **🎨 Customize Your Theme** - Make it yours with different color schemes

---

**Made with ❤️ for the Gen Z generation by developers who understand the struggle! 💸✨**

*"Track your coins, not your vibes!"* 🚀
