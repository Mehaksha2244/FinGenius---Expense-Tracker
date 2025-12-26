from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
import sqlite3
from datetime import datetime, timedelta
import os
import json
from database import DatabaseManager
from ocr_processor import ReceiptProcessor

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Change this in production

# Initialize database manager and OCR processor
db = DatabaseManager()
ocr_processor = ReceiptProcessor()

# -------------------------------
# Helper functions
# -------------------------------
def get_currency():
    """Get user's preferred currency"""
    return db.get_currency()

def format_currency(amount):
    """Format amount with user's currency"""
    currency = get_currency()
    return f"{currency}{amount:.2f}"

def get_current_month():
    """Get current month in YYYY-MM format"""
    return datetime.now().strftime('%Y-%m')

def get_month_name(month_str):
    """Convert YYYY-MM to readable month name"""
    try:
        date_obj = datetime.strptime(month_str, '%Y-%m')
        return date_obj.strftime('%B %Y')
    except:
        return month_str

# -------------------------------
# Routes
# -------------------------------

@app.route('/')
def dashboard():
    """Main dashboard with charts and insights"""
    # Get recent expenses
    expenses = db.get_expenses(limit=10)
    
    # Get spending analytics
    category_data = db.get_spending_by_category()
    monthly_trends = db.get_monthly_trends(6)
    mood_analysis = db.get_mood_analysis()
    
    # Get insights
    insights = db.generate_insights()
    
    # Get current month spending
    current_month = get_current_month()
    current_month_expenses = db.get_expenses(
        start_date=f"{current_month}-01",
        end_date=f"{current_month}-31"
    )
    current_month_total = sum(exp['amount'] for exp in current_month_expenses)
    
    # Get budget categories
    budget_categories = db.get_budget_categories()
    
    # Get expense distribution for pie chart (only negative amounts)
    expense_data = db.get_spending_by_category()
    # Filter to only include negative amounts (expenses)
    expense_categories = [item for item in expense_data if item['total'] < 0]
    categories = [item['category'] for item in expense_categories]
    amounts = [abs(item['total']) for item in expense_categories]
    
    return render_template('index.html', 
                         expenses=expenses,
                         category_data=category_data,
                         monthly_trends=monthly_trends,
                         mood_analysis=mood_analysis,
                         insights=insights,
                         current_month_total=current_month_total,
                         budget_categories=budget_categories,
                         categories=categories,
                         amounts=amounts,
                         currency=get_currency())

@app.route('/add')
def add_expense_page():
    """Add expense page with mood tracking"""
    budget_categories = db.get_budget_categories()
    return render_template('add.html', 
                         categories=[cat['category'] for cat in budget_categories],
                         currency=get_currency())

@app.route('/add_income', methods=['GET', 'POST'])
def add_income():
    """Add income transaction"""
    if request.method == 'POST':
        try:
            date = request.form['date']
            category = request.form['category']
            description = request.form['description']
            amount = float(request.form['amount'])
            
            # Add income to database (positive amount)
            db.add_expense(date, category, description, amount)
            flash(f'Income added successfully! 💰', 'success')
            return redirect(url_for('dashboard'))
        except Exception as e:
            flash(f'Error adding income: {str(e)}', 'error')
            return redirect(url_for('add_income'))
    
    return render_template('add_income.html', 
                         currency=get_currency())

@app.route('/add_expense', methods=['GET', 'POST'])
def add_expense():
    """Add expense transaction"""
    if request.method == 'POST':
        try:
            date = request.form['date']
            category = request.form['category']
            description = request.form['description']
            amount = float(request.form['amount'])
            mood = request.form.get('mood', '😊')
            
            # Add expense to database (negative amount)
            db.add_expense(date, category, description, -amount, mood)
            flash(f'Expense added successfully! 💰', 'success')
            return redirect(url_for('dashboard'))
        except Exception as e:
            flash(f'Error adding expense: {str(e)}', 'error')
            return redirect(url_for('add_expense'))
    
    budget_categories = db.get_budget_categories()
    return render_template('add.html', 
                         categories=[cat['category'] for cat in budget_categories],
                         currency=get_currency(),
                         transaction_type='expense')

# The add_expense route has been moved to the new separate routes above

@app.route('/edit/<int:expense_id>', methods=['GET', 'POST'])
def edit_expense(expense_id):
    """Edit existing expense"""
    if request.method == 'POST':
        try:
            date = request.form['date']
            category = request.form['category']
            description = request.form['description']
            amount = float(request.form['amount'])
            mood = request.form.get('mood', '😊')
            
            success = db.update_expense(expense_id, 
                                      date=date, 
                                      category=category, 
                                      description=description, 
                                      amount=amount, 
                                      mood=mood)
            
            if success:
                flash('Expense updated successfully! ✏️', 'success')
            else:
                flash('Expense not found!', 'error')
                
            return redirect(url_for('dashboard'))
            
        except Exception as e:
            flash(f'Error updating expense: {str(e)}', 'error')
            return redirect(url_for('edit_expense', expense_id=expense_id))
    
    # Get expense data for editing
    expenses = db.get_expenses()
    expense = next((exp for exp in expenses if exp['id'] == expense_id), None)
    
    if not expense:
        flash('Expense not found!', 'error')
        return redirect(url_for('dashboard'))
    
    budget_categories = db.get_budget_categories()
    return render_template('edit.html', 
                         expense=expense,
                         categories=[cat['category'] for cat in budget_categories],
                         currency=get_currency())

@app.route('/delete/<int:expense_id>')
def delete_expense(expense_id):
    """Delete expense"""
    success = db.delete_expense(expense_id)
    if success:
        flash('Expense deleted successfully! 🗑️', 'success')
    else:
        flash('Expense not found!', 'error')
    return redirect(url_for('dashboard'))

@app.route('/insights')
def insights():
    """AI-powered insights page"""
    insights = db.generate_insights()
    category_data = db.get_spending_by_category()
    monthly_trends = db.get_monthly_trends(12)
    mood_analysis = db.get_mood_analysis()
    
    return render_template('insights.html',
                         insights=insights,
                         category_data=category_data,
                         monthly_trends=monthly_trends,
                         mood_analysis=mood_analysis,
                         currency=get_currency())

@app.route('/goals')
def goals():
    """Savings goals page"""
    goals = db.get_savings_goals()
    return render_template('goals.html', 
                         goals=goals,
                         currency=get_currency())

@app.route('/goals', methods=['POST'])
def add_goal():
    """Add new savings goal"""
    try:
        title = request.form['title']
        target_amount = float(request.form['target_amount'])
        deadline = request.form.get('deadline')
        category = request.form.get('category', 'General')
        
        goal_id = db.add_savings_goal(title, target_amount, deadline, category)
        flash(f'Goal "{title}" created successfully! 🎯', 'success')
        
    except Exception as e:
        flash(f'Error creating goal: {str(e)}', 'error')
    
    return redirect(url_for('goals'))

@app.route('/goals/<int:goal_id>/update', methods=['POST'])
def update_goal_progress(goal_id):
    """Update goal progress"""
    try:
        amount = float(request.form['amount'])
        success = db.update_goal_progress(goal_id, amount)
        
        if success:
            flash(f'Added {get_currency()}{amount:.2f} to your goal! 💪', 'success')
        else:
            flash('Goal not found!', 'error')
            
    except Exception as e:
        flash(f'Error updating goal: {str(e)}', 'error')
    
    return redirect(url_for('goals'))

@app.route('/calendar')
def calendar():
    """Calendar view with spending heatmap"""
    year = request.args.get('year', datetime.now().year, type=int)
    month = request.args.get('month', datetime.now().month, type=int)
    
    daily_spending = db.get_daily_spending(year, month)
    
    return render_template('calendar.html',
                         daily_spending=daily_spending,
                         year=year,
                         month=month,
                         currency=get_currency())

@app.route('/group')
def group_expenses():
    """Group expense splitter"""
    group_expenses = db.get_group_expenses()
    return render_template('group.html',
                         group_expenses=group_expenses,
                         currency=get_currency())

@app.route('/group', methods=['POST'])
def add_group_expense():
    """Add group expense"""
    try:
        title = request.form['title']
        total_amount = float(request.form['total_amount'])
        participants = request.form['participants'].split(',')
        participants = [p.strip() for p in participants if p.strip()]
        paid_by = request.form['paid_by']
        date = request.form['date']
        description = request.form.get('description', '')
        
        if len(participants) < 2:
            flash('At least 2 participants required!', 'error')
            return redirect(url_for('group_expenses'))
        
        expense_id = db.add_group_expense(title, total_amount, participants, paid_by, date, description)
        flash(f'Group expense "{title}" created successfully! 👥', 'success')
        
    except Exception as e:
        flash(f'Error creating group expense: {str(e)}', 'error')
    
    return redirect(url_for('group_expenses'))

@app.route('/scan_receipt', methods=['GET', 'POST'])
def scan_receipt():
    """AI Receipt Scanner - Upload receipt and extract expense data"""
    if request.method == 'POST':
        try:
            if 'receipt' not in request.files:
                flash('No file provided!', 'error')
                return redirect(url_for('scan_receipt'))
            
            file = request.files['receipt']
            if file.filename == '':
                flash('No file selected!', 'error')
                return redirect(url_for('scan_receipt'))
            
            # Save temporary file
            filename = f"receipt_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{file.filename}"
            file_path = os.path.join('static', 'receipts', filename)
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            file.save(file_path)
            
            # Process with OCR
            result = ocr_processor.process_receipt(file_path)
            
            if result['success']:
                flash('Receipt processed successfully! Review and confirm the details below.', 'success')
                return render_template('scan_receipt.html', 
                                     extracted=result,
                                     file_path=file_path,
                                     currency=get_currency(),
                                     budget_categories=db.get_budget_categories())
            else:
                flash(f'Error processing receipt: {result.get("error", "Unknown error")}', 'error')
                # Clean up failed file
                try:
                    os.remove(file_path)
                except:
                    pass
                return redirect(url_for('scan_receipt'))
                
        except Exception as e:
            flash(f'Error processing receipt: {str(e)}', 'error')
            return redirect(url_for('scan_receipt'))
    
    return render_template('scan_receipt.html', 
                         currency=get_currency(),
                         budget_categories=db.get_budget_categories())


@app.route('/confirm_receipt', methods=['POST'])
def confirm_receipt():
    """Confirm receipt data and add as expense"""
    try:
        date = request.form['date']
        amount = float(request.form['amount'])
        category = request.form['category']
        description = request.form['description']
        file_path = request.form.get('file_path', '')
        
        # Add expense to database
        expense_id = db.add_expense(date, category, description, -amount, receipt_image=file_path)
        
        # Update file path to use expense ID
        if file_path and os.path.exists(file_path):
            new_filename = f"receipt_{expense_id}_{os.path.basename(file_path)}"
            new_file_path = os.path.join('static', 'receipts', new_filename)
            os.makedirs(os.path.dirname(new_file_path), exist_ok=True)
            os.rename(file_path, new_file_path)
            db.update_expense(expense_id, receipt_image=new_file_path)
        
        flash(f'Expense added successfully from receipt! 💰', 'success')
        
    except Exception as e:
        flash(f'Error adding expense: {str(e)}', 'error')
    
    return redirect(url_for('dashboard'))

# API endpoints for AJAX requests
@app.route('/api/expenses')
def api_expenses():
    """API endpoint for expenses data"""
    category = request.args.get('category')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    expenses = db.get_expenses(category=category, start_date=start_date, end_date=end_date)
    return jsonify(expenses)

@app.route('/api/insights')
def api_insights():
    """API endpoint for insights"""
    insights = db.generate_insights()
    return jsonify(insights)

@app.route('/api/charts/category')
def api_charts_category():
    """API endpoint for category spending chart"""
    data = db.get_spending_by_category()
    return jsonify(data)

@app.route('/api/charts/monthly')
def api_charts_monthly():
    """API endpoint for monthly trends chart"""
    data = db.get_monthly_trends(12)
    return jsonify(data)

@app.route('/api/calendar/<int:year>/<int:month>')
def api_calendar_data(year, month):
    """API endpoint for calendar data"""
    data = db.get_daily_spending(year, month)
    return jsonify(data)

@app.route('/settings')
def settings():
    """User settings page"""
    preferences = db.get_user_preferences()
    budget_categories = db.get_budget_categories()
    
    return render_template('settings.html',
                         preferences=preferences,
                         budget_categories=budget_categories,
                         currency=get_currency())

@app.route('/settings', methods=['POST'])
def update_settings():
    """Update user settings"""
    try:
        theme = request.form.get('theme')
        currency = request.form.get('currency')
        budget_alerts = 'budget_alerts' in request.form
        insights_enabled = 'insights_enabled' in request.form
        
        db.update_user_preferences(
            theme=theme,
            currency=currency,
            budget_alerts=budget_alerts,
            insights_enabled=insights_enabled
        )
        
        flash('Settings updated successfully! ⚙️', 'success')
        
    except Exception as e:
        flash(f'Error updating settings: {str(e)}', 'error')
    
    return redirect(url_for('settings'))

@app.route('/api/ocr/process', methods=['POST'])
def process_receipt_ocr():
    """API endpoint for processing receipt OCR"""
    try:
        if 'receipt' not in request.files:
            return jsonify({'success': False, 'error': 'No file provided'})
        
        file = request.files['receipt']
        if file.filename == '':
            return jsonify({'success': False, 'error': 'No file selected'})
        
        # Save temporary file
        filename = f"temp_receipt_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{file.filename}"
        file_path = os.path.join('static', 'receipts', filename)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        file.save(file_path)
        
        # Process with OCR
        result = ocr_processor.process_receipt(file_path)
        
        # Clean up temporary file
        try:
            os.remove(file_path)
        except:
            pass
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/budget/update', methods=['POST'])
def update_budget_limit():
    """API endpoint for updating budget limits"""
    try:
        data = request.get_json()
        category = data.get('category')
        limit = data.get('limit')
        
        if not category or limit is None:
            return jsonify({'success': False, 'error': 'Missing required fields'})
        
        success = db.update_budget_limit(category, float(limit))
        
        if success:
            return jsonify({'success': True, 'message': 'Budget limit updated'})
        else:
            return jsonify({'success': False, 'error': 'Failed to update budget limit'})
            
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)



