/**
 * FinTrack LocalStorage Manager
 * Handles all browser-based data persistence using localStorage
 * Pure JavaScript implementation - no external dependencies
 */

// LocalStorage Keys
const STORAGE_KEYS = {
    EXPENSES: 'fintrack_expenses',
    INCOME: 'fintrack_income',
    GOALS: 'fintrack_goals',
    SETTINGS: 'fintrack_settings',
    BUDGET_CATEGORIES: 'fintrack_budget_categories',
    GROUP_EXPENSES: 'fintrack_group_expenses'
};

// ========================================
// Core Utility Functions
// ========================================

/**
 * Save data to localStorage
 * @param {string} key - Storage key
 * @param {any} data - Data to store (will be JSON stringified)
 * @returns {boolean} - Success status
 */
function saveToLocalStorage(key, data) {
    try {
        const jsonData = JSON.stringify(data);
        localStorage.setItem(key, jsonData);
        console.log(`✅ Saved to localStorage: ${key}`);
        return true;
    } catch (error) {
        console.error(`❌ Error saving to localStorage (${key}):`, error);
        return false;
    }
}

/**
 * Load data from localStorage
 * @param {string} key - Storage key
 * @param {any} defaultValue - Default value if key doesn't exist
 * @returns {any} - Parsed data or default value
 */
function loadFromLocalStorage(key, defaultValue = null) {
    try {
        const jsonData = localStorage.getItem(key);
        if (jsonData === null) {
            console.log(`ℹ️ No data found for key: ${key}, using default`);
            return defaultValue;
        }
        const data = JSON.parse(jsonData);
        console.log(`✅ Loaded from localStorage: ${key}`);
        return data;
    } catch (error) {
        console.error(`❌ Error loading from localStorage (${key}):`, error);
        return defaultValue;
    }
}

/**
 * Clear all FinTrack data from localStorage
 * @returns {boolean} - Success status
 */
function clearLocalStorageData() {
    try {
        Object.values(STORAGE_KEYS).forEach(key => {
            localStorage.removeItem(key);
        });
        console.log('✅ All FinTrack data cleared from localStorage');
        return true;
    } catch (error) {
        console.error('❌ Error clearing localStorage:', error);
        return false;
    }
}

/**
 * Check if localStorage is available
 * @returns {boolean}
 */
function isLocalStorageAvailable() {
    try {
        const test = '__localStorage_test__';
        localStorage.setItem(test, test);
        localStorage.removeItem(test);
        return true;
    } catch (error) {
        console.warn('⚠️ localStorage is not available');
        return false;
    }
}

// ========================================
// Expense Management
// ========================================

/**
 * Get all expenses from localStorage
 * @returns {Array} - Array of expense objects
 */
function getExpenses() {
    return loadFromLocalStorage(STORAGE_KEYS.EXPENSES, []);
}

/**
 * Add a new expense
 * @param {Object} expense - Expense object
 * @returns {Object} - Added expense with ID
 */
function addExpense(expense) {
    const expenses = getExpenses();
    const newExpense = {
        id: generateId(),
        date: expense.date || new Date().toISOString().split('T')[0],
        category: expense.category || 'Other',
        description: expense.description || '',
        amount: parseFloat(expense.amount) || 0,
        mood: expense.mood || '😊',
        receipt_image: expense.receipt_image || null,
        created_at: new Date().toISOString()
    };
    expenses.push(newExpense);
    saveToLocalStorage(STORAGE_KEYS.EXPENSES, expenses);
    return newExpense;
}

/**
 * Update an existing expense
 * @param {number} id - Expense ID
 * @param {Object} updates - Fields to update
 * @returns {boolean} - Success status
 */
function updateExpense(id, updates) {
    const expenses = getExpenses();
    const index = expenses.findIndex(exp => exp.id === id);
    if (index === -1) {
        console.warn(`⚠️ Expense with ID ${id} not found`);
        return false;
    }
    expenses[index] = { ...expenses[index], ...updates, updated_at: new Date().toISOString() };
    saveToLocalStorage(STORAGE_KEYS.EXPENSES, expenses);
    return true;
}

/**
 * Delete an expense
 * @param {number} id - Expense ID
 * @returns {boolean} - Success status
 */
function deleteExpense(id) {
    const expenses = getExpenses();
    const filtered = expenses.filter(exp => exp.id !== id);
    if (filtered.length === expenses.length) {
        console.warn(`⚠️ Expense with ID ${id} not found`);
        return false;
    }
    saveToLocalStorage(STORAGE_KEYS.EXPENSES, filtered);
    return true;
}

// ========================================
// Income Management
// ========================================

/**
 * Get all income entries
 * @returns {Array}
 */
function getIncome() {
    return loadFromLocalStorage(STORAGE_KEYS.INCOME, []);
}

/**
 * Add income entry
 * @param {Object} income
 * @returns {Object}
 */
function addIncome(income) {
    const incomeList = getIncome();
    const newIncome = {
        id: generateId(),
        date: income.date || new Date().toISOString().split('T')[0],
        category: income.category || 'Salary',
        description: income.description || '',
        amount: parseFloat(income.amount) || 0,
        created_at: new Date().toISOString()
    };
    incomeList.push(newIncome);
    saveToLocalStorage(STORAGE_KEYS.INCOME, incomeList);
    return newIncome;
}

/**
 * Update income entry
 * @param {number} id
 * @param {Object} updates
 * @returns {boolean}
 */
function updateIncome(id, updates) {
    const incomeList = getIncome();
    const index = incomeList.findIndex(inc => inc.id === id);
    if (index === -1) return false;
    incomeList[index] = { ...incomeList[index], ...updates, updated_at: new Date().toISOString() };
    saveToLocalStorage(STORAGE_KEYS.INCOME, incomeList);
    return true;
}

/**
 * Delete income entry
 * @param {number} id
 * @returns {boolean}
 */
function deleteIncome(id) {
    const incomeList = getIncome();
    const filtered = incomeList.filter(inc => inc.id !== id);
    if (filtered.length === incomeList.length) return false;
    saveToLocalStorage(STORAGE_KEYS.INCOME, filtered);
    return true;
}

// ========================================
// Goals Management
// ========================================

/**
 * Get all goals
 * @returns {Array}
 */
function getGoals() {
    return loadFromLocalStorage(STORAGE_KEYS.GOALS, []);
}

/**
 * Add a new goal
 * @param {Object} goal
 * @returns {Object}
 */
function addGoal(goal) {
    const goals = getGoals();
    const newGoal = {
        id: generateId(),
        title: goal.title || 'New Goal',
        target_amount: parseFloat(goal.target_amount) || 0,
        current_amount: parseFloat(goal.current_amount) || 0,
        deadline: goal.deadline || null,
        category: goal.category || 'General',
        created_at: new Date().toISOString()
    };
    goals.push(newGoal);
    saveToLocalStorage(STORAGE_KEYS.GOALS, goals);
    return newGoal;
}

/**
 * Update goal
 * @param {number} id
 * @param {Object} updates
 * @returns {boolean}
 */
function updateGoal(id, updates) {
    const goals = getGoals();
    const index = goals.findIndex(g => g.id === id);
    if (index === -1) return false;
    goals[index] = { ...goals[index], ...updates, updated_at: new Date().toISOString() };
    saveToLocalStorage(STORAGE_KEYS.GOALS, goals);
    return true;
}

/**
 * Update goal progress
 * @param {number} id
 * @param {number} amount
 * @returns {boolean}
 */
function updateGoalProgress(id, amount) {
    const goals = getGoals();
    const goal = goals.find(g => g.id === id);
    if (!goal) return false;
    goal.current_amount = (goal.current_amount || 0) + parseFloat(amount);
    goal.updated_at = new Date().toISOString();
    saveToLocalStorage(STORAGE_KEYS.GOALS, goals);
    return true;
}

/**
 * Delete goal
 * @param {number} id
 * @returns {boolean}
 */
function deleteGoal(id) {
    const goals = getGoals();
    const filtered = goals.filter(g => g.id !== id);
    if (filtered.length === goals.length) return false;
    saveToLocalStorage(STORAGE_KEYS.GOALS, filtered);
    return true;
}

// ========================================
// Settings Management
// ========================================

/**
 * Get user settings
 * @returns {Object}
 */
function getSettings() {
    const defaultSettings = {
        theme: 'dark',
        currency: '₹',
        budget_alerts: true,
        insights_enabled: true,
        language: 'en'
    };
    return loadFromLocalStorage(STORAGE_KEYS.SETTINGS, defaultSettings);
}

/**
 * Update settings
 * @param {Object} updates
 * @returns {boolean}
 */
function updateSettings(updates) {
    const settings = getSettings();
    const newSettings = { ...settings, ...updates, updated_at: new Date().toISOString() };
    return saveToLocalStorage(STORAGE_KEYS.SETTINGS, newSettings);
}

// ========================================
// Budget Categories Management
// ========================================

/**
 * Get budget categories
 * @returns {Array}
 */
function getBudgetCategories() {
    const defaultCategories = [
        { category: 'Food & Dining', limit: 5000, icon: '🍔' },
        { category: 'Transportation', limit: 3000, icon: '🚗' },
        { category: 'Shopping', limit: 4000, icon: '🛍️' },
        { category: 'Entertainment', limit: 2000, icon: '🎬' },
        { category: 'Bills & Utilities', limit: 3000, icon: '💡' },
        { category: 'Healthcare', limit: 2000, icon: '🏥' },
        { category: 'Education', limit: 3000, icon: '📚' },
        { category: 'Other', limit: 2000, icon: '📦' }
    ];
    return loadFromLocalStorage(STORAGE_KEYS.BUDGET_CATEGORIES, defaultCategories);
}

/**
 * Update budget category limit
 * @param {string} category
 * @param {number} limit
 * @returns {boolean}
 */
function updateBudgetLimit(category, limit) {
    const categories = getBudgetCategories();
    const cat = categories.find(c => c.category === category);
    if (!cat) return false;
    cat.limit = parseFloat(limit);
    return saveToLocalStorage(STORAGE_KEYS.BUDGET_CATEGORIES, categories);
}

// ========================================
// Group Expenses Management
// ========================================

/**
 * Get group expenses
 * @returns {Array}
 */
function getGroupExpenses() {
    return loadFromLocalStorage(STORAGE_KEYS.GROUP_EXPENSES, []);
}

/**
 * Add group expense
 * @param {Object} groupExpense
 * @returns {Object}
 */
function addGroupExpense(groupExpense) {
    const groupExpenses = getGroupExpenses();
    const newGroupExpense = {
        id: generateId(),
        title: groupExpense.title || 'Group Expense',
        total_amount: parseFloat(groupExpense.total_amount) || 0,
        participants: groupExpense.participants || [],
        paid_by: groupExpense.paid_by || '',
        date: groupExpense.date || new Date().toISOString().split('T')[0],
        description: groupExpense.description || '',
        created_at: new Date().toISOString()
    };
    groupExpenses.push(newGroupExpense);
    saveToLocalStorage(STORAGE_KEYS.GROUP_EXPENSES, groupExpenses);
    return newGroupExpense;
}

// ========================================
// Analytics & Insights
// ========================================

/**
 * Get spending by category
 * @returns {Array}
 */
function getSpendingByCategory() {
    const expenses = getExpenses();
    const categoryTotals = {};
    
    expenses.forEach(exp => {
        const category = exp.category || 'Other';
        categoryTotals[category] = (categoryTotals[category] || 0) + Math.abs(exp.amount);
    });
    
    return Object.entries(categoryTotals).map(([category, total]) => ({
        category,
        total
    }));
}

/**
 * Get monthly spending trends
 * @param {number} months - Number of months to include
 * @returns {Array}
 */
function getMonthlyTrends(months = 6) {
    const expenses = getExpenses();
    const monthlyData = {};
    
    expenses.forEach(exp => {
        const month = exp.date.substring(0, 7); // YYYY-MM
        monthlyData[month] = (monthlyData[month] || 0) + Math.abs(exp.amount);
    });
    
    return Object.entries(monthlyData)
        .map(([month, total]) => ({ month, total }))
        .sort((a, b) => a.month.localeCompare(b.month))
        .slice(-months);
}

/**
 * Get current month total
 * @returns {number}
 */
function getCurrentMonthTotal() {
    const expenses = getExpenses();
    const currentMonth = new Date().toISOString().substring(0, 7);
    
    return expenses
        .filter(exp => exp.date.startsWith(currentMonth))
        .reduce((sum, exp) => sum + Math.abs(exp.amount), 0);
}

// ========================================
// Utility Functions
// ========================================

/**
 * Generate unique ID
 * @returns {number}
 */
function generateId() {
    return Date.now() + Math.floor(Math.random() * 1000);
}

/**
 * Export all data as JSON
 * @returns {Object}
 */
function exportAllData() {
    return {
        expenses: getExpenses(),
        income: getIncome(),
        goals: getGoals(),
        settings: getSettings(),
        budget_categories: getBudgetCategories(),
        group_expenses: getGroupExpenses(),
        exported_at: new Date().toISOString()
    };
}

/**
 * Import data from JSON
 * @param {Object} data
 * @returns {boolean}
 */
function importAllData(data) {
    try {
        if (data.expenses) saveToLocalStorage(STORAGE_KEYS.EXPENSES, data.expenses);
        if (data.income) saveToLocalStorage(STORAGE_KEYS.INCOME, data.income);
        if (data.goals) saveToLocalStorage(STORAGE_KEYS.GOALS, data.goals);
        if (data.settings) saveToLocalStorage(STORAGE_KEYS.SETTINGS, data.settings);
        if (data.budget_categories) saveToLocalStorage(STORAGE_KEYS.BUDGET_CATEGORIES, data.budget_categories);
        if (data.group_expenses) saveToLocalStorage(STORAGE_KEYS.GROUP_EXPENSES, data.group_expenses);
        console.log('✅ Data imported successfully');
        return true;
    } catch (error) {
        console.error('❌ Error importing data:', error);
        return false;
    }
}

// ========================================
// Export functions to global scope
// ========================================

window.FinTrackStorage = {
    // Core utilities
    saveToLocalStorage,
    loadFromLocalStorage,
    clearLocalStorageData,
    isLocalStorageAvailable,
    
    // Expense management
    getExpenses,
    addExpense,
    updateExpense,
    deleteExpense,
    
    // Income management
    getIncome,
    addIncome,
    updateIncome,
    deleteIncome,
    
    // Goals management
    getGoals,
    addGoal,
    updateGoal,
    updateGoalProgress,
    deleteGoal,
    
    // Settings
    getSettings,
    updateSettings,
    
    // Budget categories
    getBudgetCategories,
    updateBudgetLimit,
    
    // Group expenses
    getGroupExpenses,
    addGroupExpense,
    
    // Analytics
    getSpendingByCategory,
    getMonthlyTrends,
    getCurrentMonthTotal,
    
    // Import/Export
    exportAllData,
    importAllData,
    
    // Constants
    STORAGE_KEYS
};

// Initialize on load
document.addEventListener('DOMContentLoaded', function() {
    if (!isLocalStorageAvailable()) {
        console.warn('⚠️ localStorage is not available. Data will not persist.');
    } else {
        console.log('✅ FinTrack localStorage initialized');
    }
});
