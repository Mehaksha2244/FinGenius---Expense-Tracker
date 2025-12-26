# FinTrack LocalStorage - Quick Reference

## 🚀 Quick Start

### Basic Usage

```javascript
// Get all expenses
const expenses = window.FinTrackStorage.getExpenses();

// Add new expense
window.FinTrackStorage.addExpense({
  date: "2025-12-25",
  category: "Food & Dining",
  description: "Lunch",
  amount: -500,
  mood: "😊"
});

// Update expense
window.FinTrackStorage.updateExpense(expenseId, {
  amount: -600,
  description: "Updated lunch"
});

// Delete expense
window.FinTrackStorage.deleteExpense(expenseId);
```

## 📊 Common Operations

### Get Current Month Spending
```javascript
const total = window.FinTrackStorage.getCurrentMonthTotal();
console.log(`This month: ₹${total}`);
```

### Get Spending by Category
```javascript
const categoryData = window.FinTrackStorage.getSpendingByCategory();
categoryData.forEach(item => {
  console.log(`${item.category}: ₹${item.total}`);
});
```

### Get Monthly Trends
```javascript
const trends = window.FinTrackStorage.getMonthlyTrends(6); // Last 6 months
console.table(trends);
```

## 💾 Backup & Restore

### Export All Data
```javascript
const backup = window.FinTrackStorage.exportAllData();
const json = JSON.stringify(backup, null, 2);

// Download as file
const blob = new Blob([json], { type: 'application/json' });
const url = URL.createObjectURL(blob);
const a = document.createElement('a');
a.href = url;
a.download = `fintrack-backup-${new Date().toISOString().split('T')[0]}.json`;
a.click();
```

### Import Data
```javascript
// From file input
document.getElementById('import-file').addEventListener('change', function(e) {
  const file = e.target.files[0];
  const reader = new FileReader();
  
  reader.onload = function(event) {
    const data = JSON.parse(event.target.result);
    window.FinTrackStorage.importAllData(data);
    alert('Data imported successfully!');
    location.reload();
  };
  
  reader.readAsText(file);
});
```

## 🎯 Goals Management

```javascript
// Add goal
window.FinTrackStorage.addGoal({
  title: "Vacation Fund",
  target_amount: 100000,
  deadline: "2026-06-30",
  category: "Travel"
});

// Update goal progress
window.FinTrackStorage.updateGoalProgress(goalId, 5000); // Add ₹5000

// Get all goals
const goals = window.FinTrackStorage.getGoals();
```

## ⚙️ Settings

```javascript
// Get settings
const settings = window.FinTrackStorage.getSettings();

// Update settings
window.FinTrackStorage.updateSettings({
  theme: "dark",
  currency: "$",
  budget_alerts: true
});
```

## 🧹 Clear Data

```javascript
// Clear all FinTrack data
if (confirm('Are you sure you want to clear all data?')) {
  window.FinTrackStorage.clearLocalStorageData();
  location.reload();
}
```

## 🔍 Debugging

### View Storage Size
```javascript
const data = window.FinTrackStorage.exportAllData();
const size = new Blob([JSON.stringify(data)]).size;
console.log(`Storage size: ${(size / 1024).toFixed(2)} KB`);
```

### View All Data in Console
```javascript
console.log('Expenses:', window.FinTrackStorage.getExpenses());
console.log('Income:', window.FinTrackStorage.getIncome());
console.log('Goals:', window.FinTrackStorage.getGoals());
console.log('Settings:', window.FinTrackStorage.getSettings());
```

### Check if localStorage is Available
```javascript
if (window.FinTrackStorage.isLocalStorageAvailable()) {
  console.log('✅ localStorage is available');
} else {
  console.log('❌ localStorage is not available');
}
```

## 📝 Storage Keys Reference

| Key | Type | Description |
|-----|------|-------------|
| `fintrack_expenses` | Array | All expense transactions |
| `fintrack_income` | Array | All income entries |
| `fintrack_goals` | Array | Savings goals |
| `fintrack_settings` | Object | User preferences |
| `fintrack_budget_categories` | Array | Budget categories |
| `fintrack_group_expenses` | Array | Group expenses |

## 🎨 Integration Examples

### Form Submission Handler
```javascript
document.getElementById('expense-form').addEventListener('submit', function(e) {
  e.preventDefault();
  
  const formData = new FormData(e.target);
  const expense = {
    date: formData.get('date'),
    category: formData.get('category'),
    description: formData.get('description'),
    amount: -Math.abs(parseFloat(formData.get('amount'))),
    mood: formData.get('mood')
  };
  
  window.FinTrackStorage.addExpense(expense);
  alert('Expense added!');
  e.target.reset();
  location.reload();
});
```

### Update Chart with localStorage Data
```javascript
function updateExpenseChart() {
  const categoryData = window.FinTrackStorage.getSpendingByCategory();
  const labels = categoryData.map(item => item.category);
  const data = categoryData.map(item => item.total);
  
  // Update Chart.js chart
  myChart.data.labels = labels;
  myChart.data.datasets[0].data = data;
  myChart.update();
}
```

## 🚨 Error Handling

```javascript
try {
  const expense = window.FinTrackStorage.addExpense(expenseData);
  console.log('✅ Expense added:', expense);
} catch (error) {
  console.error('❌ Error adding expense:', error);
  alert('Failed to add expense. Please try again.');
}
```

## 💡 Tips

1. **Always check availability** before using localStorage
2. **Export data regularly** as backup
3. **Use console logging** for debugging
4. **Handle errors gracefully** with try-catch
5. **Reload page** after major data changes for UI sync

## 📚 Full Documentation

For complete API reference and advanced usage, see [LOCALSTORAGE_GUIDE.md](LOCALSTORAGE_GUIDE.md)

---

**Last Updated:** December 25, 2025
