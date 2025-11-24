import React, { useState, useEffect } from 'react'
import '../styles/homepage.css'

const HomePage = () => {
  const [stats, setStats] = useState({
    totalBalance: 0,
    monthlyTransactions: 0,
    activeGoals: 0,
    categories: 0
  });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    try {
      setLoading(true);
      
      // Fetch all required data in parallel
      const [transactionsRes, goalsRes, categoriesRes] = await Promise.all([
        fetch('/api/transactions'),
        fetch('/api/goals'),
        fetch('/api/categories')
      ]);

      // Check if responses are ok
      if (!transactionsRes.ok) {
        throw new Error(`Transactions API error: ${transactionsRes.status}`);
      }
      if (!goalsRes.ok) {
        throw new Error(`Goals API error: ${goalsRes.status}`);
      }

      const transactionsData = await transactionsRes.json();
      const goalsData = await goalsRes.json();
      const categoriesData = await categoriesRes.json();

      const transactions = transactionsData.transactions || [];
      const goals = goalsData.goals || [];
      const categories = categoriesData.categories || [];

      console.log('Fetched transactions:', transactions);
      console.log('Fetched goals:', goals);

      // Calculate total balance (income - expenses)
      const totalBalance = transactions.reduce((balance, transaction) => {
        const amount = parseFloat(transaction.amount) || 0;
        if (transaction.transaction_type === 'income') {
          return balance + amount;
        } else if (transaction.transaction_type === 'expense') {
          return balance - amount;
        }
        return balance;
      }, 0);
      
      console.log('Calculated total balance:', totalBalance);

      // Calculate this month's transactions
      const currentMonth = new Date().getMonth();
      const currentYear = new Date().getFullYear();
      const monthlyTransactions = transactions.filter(transaction => {
        const transactionDate = new Date(transaction.transaction_date);
        return transactionDate.getMonth() === currentMonth && 
               transactionDate.getFullYear() === currentYear;
      }).length;

      // Count active goals (not completed)
      const activeGoals = goals.filter(goal => goal.status !== 'completed').length;

      // Update stats
      setStats({
        totalBalance: totalBalance,
        monthlyTransactions: monthlyTransactions,
        activeGoals: activeGoals,
        categories: categories.length
      });

    } catch (error) {
      console.error('Error fetching dashboard data:', error);
      // Keep default values on error
    } finally {
      setLoading(false);
    }
  };

  // Helper function to format currency
  const formatCurrency = (amount) => {
    return new Intl.NumberFormat('en-GB', {
      style: 'currency',
      currency: 'GBP'
    }).format(amount);
  };

  // Helper function to determine balance color
  const getBalanceColor = (balance) => {
    if (balance > 0) return 'positive';
    if (balance < 0) return 'negative';
    return 'neutral';
  };

  return (
    <div className="home-page">
      <div className="hero-section">
        <h1>Money Talks</h1>
        <p>Take control of your finances with our comprehensive tracking system</p>
        <div className="stats-grid">
          <div className={`stat-card balance-card ${getBalanceColor(stats.totalBalance)}`}>
            <h3 className="balance-amount">
              {loading ? 'Loading...' : formatCurrency(stats.totalBalance)}
            </h3>
            <p>Total Balance</p>
            {!loading && (
              <small className="balance-indicator">
                {stats.totalBalance > 0 ? '📈 Positive' : 
                 stats.totalBalance < 0 ? '📉 Negative' : '➖ Neutral'}
              </small>
            )}
          </div>
          
          <div className="stat-card">
            <h3>{loading ? '...' : stats.monthlyTransactions}</h3>
            <p>This Month's Transactions</p>
            {!loading && <small>🗓️ {new Date().toLocaleDateString('en-GB', { month: 'long', year: 'numeric' })}</small>}
          </div>
          
          <div className="stat-card">
            <h3>{loading ? '...' : stats.activeGoals}</h3>
            <p>Active Goals</p>
            {!loading && <small>🎯 In Progress</small>}
          </div>
          
          <div className="stat-card">
            <h3>{loading ? '...' : stats.categories}</h3>
            <p>Categories</p>
            {!loading && <small>📂 Available</small>}
          </div>
        </div>
      </div>
      
      <div className="quick-actions">
        <h2>Quick Actions</h2>
        <div className="action-buttons">
          <button 
            className="action-btn"
            onClick={() => window.location.href = '/transactions'}
          >
            💰 Add Transaction
          </button>
          <button 
            className="action-btn"
            onClick={() => window.location.href = '/goals'}
          >
            🎯 Create Goal
          </button>
          <button 
            className="action-btn"
            onClick={() => window.location.href = '/analytics'}
          >
            📊 View Analytics
          </button>
        </div>
      </div>
      
      {!loading && (
        <div className="balance-summary">
          <h3>Financial Summary</h3>
          <div className="summary-details">
            <div className="summary-item">
              <span>Current Status:</span>
              <span className={getBalanceColor(stats.totalBalance)}>
                {stats.totalBalance > 0 ? 'You\'re in the green! 🟢' :
                 stats.totalBalance < 0 ? 'Consider reviewing expenses 🔴' :
                 'Breaking even 🟡'}
              </span>
            </div>
            <div className="summary-item">
              <span>This Month:</span>
              <span>{stats.monthlyTransactions} transactions recorded</span>
            </div>
            <div className="summary-item">
              <span>Goals Progress:</span>
              <span>{stats.activeGoals} goals in progress</span>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

export default HomePage