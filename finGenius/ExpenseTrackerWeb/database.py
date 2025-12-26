"""
Enhanced Database Module for Personal Expense Tracker
Handles SQLite database connections and operations with mood tracking, goals, and insights
"""

import sqlite3
from datetime import datetime, timedelta
from typing import List, Dict, Tuple, Optional
import json

class DatabaseManager:
    def __init__(self, db_path: str = 'expenses.db'):
        self.db_path = db_path
        self.init_database()
    
    def get_connection(self):
        """Get database connection with row factory for easier data handling"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
    
    def init_database(self):
        """Initialize all database tables with enhanced schema"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Enhanced expenses table with mood tracking
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                category TEXT NOT NULL,
                description TEXT,
                amount REAL NOT NULL,
                mood TEXT DEFAULT '😊',
                receipt_image TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Savings goals table for gamification
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS savings_goals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                target_amount REAL NOT NULL,
                current_amount REAL DEFAULT 0,
                deadline TEXT,
                category TEXT,
                status TEXT DEFAULT 'active',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Group expenses for splitting functionality
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS group_expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                total_amount REAL NOT NULL,
                participants TEXT NOT NULL,
                split_amount REAL NOT NULL,
                paid_by TEXT NOT NULL,
                date TEXT NOT NULL,
                description TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # User preferences for themes and settings
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_preferences (
                id INTEGER PRIMARY KEY DEFAULT 1,
                theme TEXT DEFAULT 'pastel',
                currency TEXT DEFAULT '₹',
                budget_alerts BOOLEAN DEFAULT 1,
                insights_enabled BOOLEAN DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Budget categories with limits
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS budget_categories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                category TEXT UNIQUE NOT NULL,
                monthly_limit REAL,
                color TEXT DEFAULT '#FFD1DC',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Insert default budget categories
        default_categories = [
            ('Food & Dining', 5000, '#FFD1DC'),
            ('Transportation', 3000, '#AEEEEE'),
            ('Shopping', 4000, '#C5E1A5'),
            ('Entertainment', 2000, '#FFB6C1'),
            ('Bills & Utilities', 6000, '#DDA0DD'),
            ('Healthcare', 1500, '#98FB98'),
            ('Education', 3000, '#F0E68C'),
            ('Others', 2000, '#D3D3D3')
        ]
        
        for category, limit, color in default_categories:
            cursor.execute('''
                INSERT OR IGNORE INTO budget_categories (category, monthly_limit, color)
                VALUES (?, ?, ?)
            ''', (category, limit, color))
        
        # Insert default user preferences
        cursor.execute('''
            INSERT OR IGNORE INTO user_preferences (id, theme, currency, budget_alerts, insights_enabled)
            VALUES (1, 'pastel', '₹', 1, 1)
        ''')
        
        conn.commit()
        conn.close()
    
    # Expense operations
    def add_expense(self, date: str, category: str, description: str, amount: float, 
                   mood: str = '😊', receipt_image: str = None) -> int:
        """Add a new expense with mood tracking"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO expenses (date, category, description, amount, mood, receipt_image)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (date, category, description, amount, mood, receipt_image))
        
        expense_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return expense_id
    
    def get_expenses(self, limit: int = None, category: str = None, 
                    start_date: str = None, end_date: str = None) -> List[Dict]:
        """Get expenses with optional filtering"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        query = "SELECT * FROM expenses WHERE 1=1"
        params = []
        
        if category:
            query += " AND category = ?"
            params.append(category)
        
        if start_date:
            query += " AND date >= ?"
            params.append(start_date)
            
        if end_date:
            query += " AND date <= ?"
            params.append(end_date)
        
        query += " ORDER BY date DESC"
        
        if limit:
            query += " LIMIT ?"
            params.append(limit)
        
        cursor.execute(query, params)
        expenses = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return expenses
    
    def update_expense(self, expense_id: int, **kwargs) -> bool:
        """Update expense fields"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Build dynamic update query
        set_clauses = []
        params = []
        
        for field, value in kwargs.items():
            if field in ['date', 'category', 'description', 'amount', 'mood', 'receipt_image']:
                set_clauses.append(f"{field} = ?")
                params.append(value)
        
        if not set_clauses:
            return False
        
        params.append(expense_id)
        query = f"UPDATE expenses SET {', '.join(set_clauses)} WHERE id = ?"
        
        cursor.execute(query, params)
        success = cursor.rowcount > 0
        conn.commit()
        conn.close()
        return success
    
    def delete_expense(self, expense_id: int) -> bool:
        """Delete an expense"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
        success = cursor.rowcount > 0
        conn.commit()
        conn.close()
        return success
    
    def execute(self, query: str, params=None):
        """Execute a raw SQL query"""
        conn = self.get_connection()
        cursor = conn.cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        return cursor
    
    def commit(self):
        """Commit the current transaction"""
        # This is handled automatically in each method, but added for compatibility
        pass
    
    # Analytics and insights
    def get_spending_by_category(self, start_date: str = None, end_date: str = None) -> List[Dict]:
        """Get spending breakdown by category"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        query = '''
            SELECT category, SUM(amount) as total, COUNT(*) as count,
                   AVG(amount) as average, mood
            FROM expenses WHERE 1=1
        '''
        params = []
        
        if start_date:
            query += " AND date >= ?"
            params.append(start_date)
            
        if end_date:
            query += " AND date <= ?"
            params.append(end_date)
        
        query += " GROUP BY category ORDER BY total DESC"
        
        cursor.execute(query, params)
        results = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return results
    
    def get_monthly_trends(self, months: int = 6) -> List[Dict]:
        """Get monthly spending trends"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        query = '''
            SELECT strftime('%Y-%m', date) as month,
                   SUM(amount) as total,
                   COUNT(*) as count
            FROM expenses 
            WHERE date >= date('now', '-{} months')
            GROUP BY strftime('%Y-%m', date)
            ORDER BY month
        '''.format(months)
        
        cursor.execute(query)
        results = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return results
    
    def get_daily_spending(self, year: int, month: int) -> List[Dict]:
        """Get daily spending for calendar heatmap"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        query = '''
            SELECT date, SUM(amount) as total, COUNT(*) as count
            FROM expenses 
            WHERE strftime('%Y', date) = ? AND strftime('%m', date) = ?
            GROUP BY date
            ORDER BY date
        '''
        
        cursor.execute(query, (str(year), f"{month:02d}"))
        results = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return results
    
    def get_mood_analysis(self) -> Dict:
        """Analyze spending patterns by mood"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        query = '''
            SELECT mood, 
                   COUNT(*) as count,
                   SUM(amount) as total,
                   AVG(amount) as average
            FROM expenses 
            GROUP BY mood
            ORDER BY total DESC
        '''
        
        cursor.execute(query)
        results = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return results
    
    # AI-powered insights generation
    def generate_insights(self) -> List[str]:
        """Generate AI-like spending insights based on data patterns"""
        insights = []
        
        # Get recent spending data
        recent_expenses = self.get_expenses(limit=50)
        if not recent_expenses:
            return ["No expenses found. Start tracking to get insights! 💡"]
        
        # Category analysis
        category_data = self.get_spending_by_category()
        if category_data:
            top_category = category_data[0]
            insights.append(f"Your biggest spending category is {top_category['category']} at {top_category['total']:.0f} {self.get_currency()}")
        
        # Monthly comparison
        monthly_trends = self.get_monthly_trends(2)
        if len(monthly_trends) >= 2:
            current_month = monthly_trends[-1]['total']
            previous_month = monthly_trends[-2]['total']
            if current_month > previous_month:
                increase = ((current_month - previous_month) / previous_month) * 100
                insights.append(f"Spending increased by {increase:.1f}% compared to last month 📈")
            else:
                decrease = ((previous_month - current_month) / previous_month) * 100
                insights.append(f"Great job! Spending decreased by {decrease:.1f}% this month 🎉")
        
        # Mood analysis
        mood_data = self.get_mood_analysis()
        if mood_data:
            happy_spending = next((item for item in mood_data if '😊' in item['mood'] or '😄' in item['mood']), None)
            if happy_spending:
                insights.append(f"You spent {happy_spending['total']:.0f} {self.get_currency()} on happy moments! 😊")
        
        # Budget alerts
        budget_categories = self.get_budget_categories()
        current_month = datetime.now().strftime('%Y-%m')
        for category in budget_categories:
            if category['monthly_limit']:
                category_expenses = self.get_spending_by_category(
                    start_date=f"{current_month}-01",
                    end_date=f"{current_month}-31"
                )
                category_total = next((item['total'] for item in category_expenses if item['category'] == category['category']), 0)
                if category_total > category['monthly_limit'] * 0.8:
                    insights.append(f"⚠️ You've used {category_total/category['monthly_limit']*100:.0f}% of your {category['category']} budget!")
        
        return insights[:5]  # Return top 5 insights
    
    # Goals management
    def add_savings_goal(self, title: str, target_amount: float, deadline: str = None, 
                        category: str = None) -> int:
        """Add a new savings goal"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO savings_goals (title, target_amount, deadline, category)
            VALUES (?, ?, ?, ?)
        ''', (title, target_amount, deadline, category))
        
        goal_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return goal_id
    
    def get_savings_goals(self, status: str = 'active') -> List[Dict]:
        """Get savings goals"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM savings_goals 
            WHERE status = ? 
            ORDER BY created_at DESC
        ''', (status,))
        
        goals = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return goals
    
    def update_goal_progress(self, goal_id: int, amount: float) -> bool:
        """Update goal progress by adding amount"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE savings_goals 
            SET current_amount = current_amount + ? 
            WHERE id = ?
        ''', (amount, goal_id))
        
        success = cursor.rowcount > 0
        conn.commit()
        conn.close()
        return success
    
    # Group expenses
    def add_group_expense(self, title: str, total_amount: float, participants: List[str], 
                         paid_by: str, date: str, description: str = None) -> int:
        """Add a group expense and calculate splits"""
        split_amount = total_amount / len(participants)
        participants_json = json.dumps(participants)
        
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO group_expenses (title, total_amount, participants, split_amount, paid_by, date, description)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (title, total_amount, participants_json, split_amount, paid_by, date, description))
        
        expense_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return expense_id
    
    def get_group_expenses(self) -> List[Dict]:
        """Get all group expenses"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM group_expenses ORDER BY date DESC')
        expenses = []
        for row in cursor.fetchall():
            expense = dict(row)
            expense['participants'] = json.loads(expense['participants'])
            expenses.append(expense)
        
        conn.close()
        return expenses
    
    # Budget management
    def get_budget_categories(self) -> List[Dict]:
        """Get budget categories with limits"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM budget_categories ORDER BY category')
        categories = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return categories
    
    def update_budget_limit(self, category: str, limit: float) -> bool:
        """Update budget limit for a category"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE budget_categories 
            SET monthly_limit = ? 
            WHERE category = ?
        ''', (limit, category))
        
        success = cursor.rowcount > 0
        conn.commit()
        conn.close()
        return success
    
    # User preferences
    def get_user_preferences(self) -> Dict:
        """Get user preferences"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM user_preferences WHERE id = 1')
        result = cursor.fetchone()
        conn.close()
        
        return dict(result) if result else {}
    
    def update_user_preferences(self, **kwargs) -> bool:
        """Update user preferences"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        set_clauses = []
        params = []
        
        for field, value in kwargs.items():
            if field in ['theme', 'currency', 'budget_alerts', 'insights_enabled']:
                set_clauses.append(f"{field} = ?")
                params.append(value)
        
        if not set_clauses:
            return False
        
        query = f"UPDATE user_preferences SET {', '.join(set_clauses)} WHERE id = 1"
        cursor.execute(query, params)
        
        success = cursor.rowcount > 0
        conn.commit()
        conn.close()
        return success
    
    def get_currency(self) -> str:
        """Get user's preferred currency"""
        prefs = self.get_user_preferences()
        return prefs.get('currency', '₹')
