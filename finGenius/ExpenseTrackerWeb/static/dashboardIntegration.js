/**
 * FinTrack Dashboard Integration
 * Syncs localStorage data with dashboard UI
 */

(function () {
    'use strict';

    // Wait for DOM and localStorage to be ready
    document.addEventListener('DOMContentLoaded', function () {
        initializeDashboard();
    });

    /**
     * Initialize dashboard with localStorage data
     */
    function initializeDashboard() {
        if (!window.FinTrackStorage) {
            console.warn('⚠️ FinTrackStorage not loaded yet');
            return;
        }

        console.log('🚀 Initializing FinTrack Dashboard with localStorage');

        // Load and render data
        loadDashboardData();

        // Set up event listeners for forms
        setupFormListeners();
    }

    /**
     * Load and render dashboard data from localStorage
     */
    function loadDashboardData() {
        const expenses = window.FinTrackStorage.getExpenses();
        const income = window.FinTrackStorage.getIncome();
        const goals = window.FinTrackStorage.getGoals();
        const settings = window.FinTrackStorage.getSettings();

        console.log(`📊 Loaded: ${expenses.length} expenses, ${income.length} income, ${goals.length} goals`);

        // Update stats
        updateDashboardStats(expenses, income, goals);

        // Update charts if on dashboard page
        updateDashboardCharts(expenses);
    }

    /**
     * Update dashboard statistics
     */
    function updateDashboardStats(expenses, income, goals) {
        // Calculate current month total
        const currentMonth = new Date().toISOString().substring(0, 7);
        const monthlyExpenses = expenses.filter(exp => exp.date.startsWith(currentMonth));
        const monthlyTotal = monthlyExpenses.reduce((sum, exp) => sum + Math.abs(exp.amount), 0);

        // Update stat cards if they exist
        const monthlyStatElement = document.querySelector('[data-stat="monthly-total"]');
        if (monthlyStatElement) {
            monthlyStatElement.textContent = formatCurrency(monthlyTotal);
        }

        const totalExpensesElement = document.querySelector('[data-stat="total-expenses"]');
        if (totalExpensesElement) {
            totalExpensesElement.textContent = expenses.length;
        }

        const activeGoalsElement = document.querySelector('[data-stat="active-goals"]');
        if (activeGoalsElement) {
            activeGoalsElement.textContent = goals.length;
        }

        // Update count-up animations with localStorage data
        updateCountUpAnimations(monthlyTotal, expenses.length, goals.length);
    }

    /**
     * Update count-up animations with real data
     */
    function updateCountUpAnimations(monthlyTotal, expenseCount, goalCount) {
        const countUpElements = document.querySelectorAll('.count-up');
        countUpElements.forEach(el => {
            const statType = el.closest('.stat-card')?.querySelector('.stat-label')?.textContent;

            if (statType && statType.includes('This Month')) {
                el.setAttribute('data-target', monthlyTotal);
            } else if (statType && statType.includes('Total Expenses')) {
                el.setAttribute('data-target', expenseCount);
            } else if (statType && statType.includes('Goals')) {
                el.setAttribute('data-target', goalCount);
            }
        });

        // Re-initialize count-up if function exists
        if (typeof window.initCountUp === 'function') {
            window.initCountUp();
        }
    }

    /**
     * Update dashboard charts with localStorage data
     */
    function updateDashboardCharts(expenses) {
        const chartCanvas = document.getElementById('expenseChart');
        if (!chartCanvas) return;

        // Get spending by category
        const categoryData = window.FinTrackStorage.getSpendingByCategory();

        if (categoryData.length === 0) {
            chartCanvas.parentElement.innerHTML =
                '<div class="text-center p-4" style="color: var(--text-muted);">No expense data available yet! 💸</div>';
            return;
        }

        const categories = categoryData.map(item => item.category);
        const amounts = categoryData.map(item => item.total);

        // Create chart
        const ctx = chartCanvas.getContext('2d');

        // Destroy existing chart if it exists
        if (window.expenseChartInstance) {
            window.expenseChartInstance.destroy();
        }

        window.expenseChartInstance = new Chart(ctx, {
            type: 'pie',
            data: {
                labels: categories,
                datasets: [{
                    data: amounts,
                    backgroundColor: [
                        '#FF6384',
                        '#36A2EB',
                        '#FFCE56',
                        '#4BC0C0',
                        '#9966FF',
                        '#FF9F40',
                        '#8AC926',
                        '#1982C4',
                        '#6A4C93',
                        '#F15BB5'
                    ],
                    hoverOffset: 4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: {
                            padding: 20,
                            usePointStyle: true
                        }
                    },
                    tooltip: {
                        callbacks: {
                            label: function (context) {
                                const label = context.label || '';
                                const value = context.raw;
                                const currency = window.FinTrackStorage.getSettings().currency || '₹';
                                return `${label}: ${currency}${value.toFixed(2)}`;
                            }
                        }
                    }
                }
            }
        });
    }

    /**
     * Set up form listeners for add/edit/delete operations
     */
    function setupFormListeners() {
        // Add Expense Form
        const addExpenseForm = document.getElementById('add-expense-form');
        if (addExpenseForm) {
            addExpenseForm.addEventListener('submit', handleAddExpense);
        }

        // Add Income Form
        const addIncomeForm = document.getElementById('add-income-form');
        if (addIncomeForm) {
            addIncomeForm.addEventListener('submit', handleAddIncome);
        }

        // Add Goal Form
        const addGoalForm = document.getElementById('add-goal-form');
        if (addGoalForm) {
            addGoalForm.addEventListener('submit', handleAddGoal);
        }

        // Delete buttons
        document.querySelectorAll('[data-action="delete-expense"]').forEach(btn => {
            btn.addEventListener('click', handleDeleteExpense);
        });

        // Settings form
        const settingsForm = document.getElementById('settings-form');
        if (settingsForm) {
            settingsForm.addEventListener('submit', handleUpdateSettings);
        }
    }

    /**
     * Handle add expense form submission
     */
    function handleAddExpense(e) {
        e.preventDefault();
        const formData = new FormData(e.target);

        const expense = {
            date: formData.get('date'),
            category: formData.get('category'),
            description: formData.get('description'),
            amount: -Math.abs(parseFloat(formData.get('amount'))), // Negative for expenses
            mood: formData.get('mood') || '😊'
        };

        const added = window.FinTrackStorage.addExpense(expense);

        if (added) {
            showNotification('Expense added successfully! 💰', 'success');
            e.target.reset();

            // Reload dashboard data
            setTimeout(() => {
                window.location.reload();
            }, 1000);
        } else {
            showNotification('Error adding expense', 'error');
        }
    }

    /**
     * Handle add income form submission
     */
    function handleAddIncome(e) {
        e.preventDefault();
        const formData = new FormData(e.target);

        const income = {
            date: formData.get('date'),
            category: formData.get('category'),
            description: formData.get('description'),
            amount: Math.abs(parseFloat(formData.get('amount'))) // Positive for income
        };

        const added = window.FinTrackStorage.addIncome(income);

        if (added) {
            showNotification('Income added successfully! 💰', 'success');
            e.target.reset();

            setTimeout(() => {
                window.location.reload();
            }, 1000);
        } else {
            showNotification('Error adding income', 'error');
        }
    }

    /**
     * Handle add goal form submission
     */
    function handleAddGoal(e) {
        e.preventDefault();
        const formData = new FormData(e.target);

        const goal = {
            title: formData.get('title'),
            target_amount: parseFloat(formData.get('target_amount')),
            deadline: formData.get('deadline'),
            category: formData.get('category') || 'General'
        };

        const added = window.FinTrackStorage.addGoal(goal);

        if (added) {
            showNotification(`Goal "${goal.title}" created successfully! 🎯`, 'success');
            e.target.reset();

            setTimeout(() => {
                window.location.reload();
            }, 1000);
        } else {
            showNotification('Error creating goal', 'error');
        }
    }

    /**
     * Handle delete expense
     */
    function handleDeleteExpense(e) {
        const expenseId = parseInt(e.target.dataset.expenseId);

        if (confirm('Are you sure you want to delete this expense?')) {
            const deleted = window.FinTrackStorage.deleteExpense(expenseId);

            if (deleted) {
                showNotification('Expense deleted successfully! 🗑️', 'success');

                setTimeout(() => {
                    window.location.reload();
                }, 1000);
            } else {
                showNotification('Error deleting expense', 'error');
            }
        }
    }

    /**
     * Handle settings update
     */
    function handleUpdateSettings(e) {
        e.preventDefault();
        const formData = new FormData(e.target);

        const settings = {
            theme: formData.get('theme'),
            currency: formData.get('currency'),
            budget_alerts: formData.has('budget_alerts'),
            insights_enabled: formData.has('insights_enabled')
        };

        const updated = window.FinTrackStorage.updateSettings(settings);

        if (updated) {
            showNotification('Settings updated successfully! ⚙️', 'success');

            // Apply theme immediately
            if (settings.theme) {
                applyTheme(settings.theme);
            }
        } else {
            showNotification('Error updating settings', 'error');
        }
    }

    /**
     * Format currency
     */
    function formatCurrency(amount) {
        const settings = window.FinTrackStorage.getSettings();
        const currency = settings.currency || '₹';
        return `${currency}${parseFloat(amount).toFixed(2)}`;
    }

    /**
     * Show notification (uses existing function if available)
     */
    function showNotification(message, type) {
        if (typeof window.showNotification === 'function') {
            window.showNotification(message, type);
        } else {
            alert(message);
        }
    }

})();
