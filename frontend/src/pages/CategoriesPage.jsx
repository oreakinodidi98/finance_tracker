import React, { useState, useEffect } from 'react'
import '../styles/CategoriesPage.css'

const CategoriesPage = () => {
  const [categoryStats, setCategoryStats] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [period, setPeriod] = useState('30')
  const [filter, setFilter] = useState('all') // all, income, expense
  const [showCreateForm, setShowCreateForm] = useState(false)
  const [newCategory, setNewCategory] = useState({
    name: '',
    type: 'expense',
    description: ''
  })

  useEffect(() => {
    fetchCategoryStats()
  }, [period])

  const fetchCategoryStats = async () => {
    try {
      setLoading(true)
      const response = await fetch(`/api/categories/stats?period=${period}&user_id=1`)
      
      if (!response.ok) {
        throw new Error('Failed to fetch category statistics')
      }
      
      const data = await response.json()
      setCategoryStats(data.categories)
      setError(null)
    } catch (err) {
      console.error('Error fetching category stats:', err)
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  const handleSeedCategories = async () => {
    try {
      const response = await fetch('/api/categories/seed', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ user_id: 1 })
      })
      
      if (response.ok) {
        const data = await response.json()
        alert(data.message)
        fetchCategoryStats()
      }
    } catch (err) {
      console.error('Error seeding categories:', err)
      alert('Failed to create default categories')
    }
  }

  const handleCreateCategory = async (e) => {
    e.preventDefault()
    
    if (!newCategory.name.trim()) {
      alert('Please enter a category name')
      return
    }

    try {
      const response = await fetch('/api/categories/create', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          ...newCategory,
          user_id: 1
        })
      })

      if (response.ok) {
        const data = await response.json()
        alert(data.message)
        setNewCategory({ name: '', type: 'expense', description: '' })
        setShowCreateForm(false)
        fetchCategoryStats()
      } else {
        const errorData = await response.json()
        alert(errorData.error || 'Failed to create category')
      }
    } catch (err) {
      console.error('Error creating category:', err)
      alert('Failed to create category')
    }
  }

  const handleDeleteCategory = async (categoryId, categoryName) => {
    if (!window.confirm(`Are you sure you want to delete "${categoryName}"?`)) {
      return
    }

    try {
      const response = await fetch(`/api/categories/delete/${categoryId}`, {
        method: 'DELETE'
      })

      if (response.ok) {
        alert('Category deleted successfully')
        fetchCategoryStats()
      } else {
        const errorData = await response.json()
        alert(errorData.error || 'Failed to delete category')
      }
    } catch (err) {
      console.error('Error deleting category:', err)
      alert('Failed to delete category')
    }
  }

  const getCategoryIcon = (name, type) => {
    const iconMap = {
      'Groceries': '🛒',
      'Transportation': '🚗',
      'Utilities': '💡',
      'Rent/Mortgage': '🏠',
      'Healthcare': '⚕️',
      'Entertainment': '🎮',
      'Dining Out': '🍽️',
      'Shopping': '🛍️',
      'Insurance': '🛡️',
      'Education': '📚',
      'Salary': '💰',
      'Freelance': '💼',
      'Investments': '📈',
      'Other Income': '💵'
    }
    return iconMap[name] || (type === 'income' ? '💰' : '💸')
  }

  const filteredCategories = categoryStats.filter(cat => {
    if (filter === 'all') return true
    return cat.type === filter
  })

  const totalSpending = filteredCategories
    .filter(cat => cat.type === 'expense')
    .reduce((sum, cat) => sum + cat.total_spent, 0)

  const totalIncome = filteredCategories
    .filter(cat => cat.type === 'income')
    .reduce((sum, cat) => sum + cat.total_spent, 0)

  if (loading) {
    return (
      <div className="categories-page">
        <div className="loading">Loading categories...</div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="categories-page">
        <div className="error">Error: {error}</div>
        <button onClick={fetchCategoryStats}>Retry</button>
      </div>
    )
  }

  if (categoryStats.length === 0) {
    return (
      <div className="categories-page">
        <div className="empty-state">
          <h2>📂 No Categories Found</h2>
          <p>Create default categories to get started</p>
          <button className="seed-button" onClick={handleSeedCategories}>
            ➕ Create Default Categories
          </button>
        </div>
      </div>
    )
  }

  return (
    <div className="categories-page">
      <div className="categories-header">
        <h1>📂 Spending Categories</h1>
        <div className="header-controls">
          <div className="period-selector">
            <label>Period: </label>
            <select value={period} onChange={(e) => setPeriod(e.target.value)}>
              <option value="7">Last 7 Days</option>
              <option value="30">Last 30 Days</option>
              <option value="90">Last 90 Days</option>
              <option value="365">Last Year</option>
            </select>
          </div>
          <button 
            className="create-button" 
            onClick={() => setShowCreateForm(!showCreateForm)}
          >
            ➕ Create Category
          </button>
          <button className="seed-button-small" onClick={handleSeedCategories}>
            🌱 Seed Defaults
          </button>
        </div>
      </div>

      {/* Create Category Form */}
      {showCreateForm && (
        <div className="create-form-container">
          <form onSubmit={handleCreateCategory} className="create-category-form">
            <h3>Create New Category</h3>
            <div className="form-row">
              <div className="form-group">
                <label>Category Name *</label>
                <input
                  type="text"
                  placeholder="e.g., Gym Membership"
                  value={newCategory.name}
                  onChange={(e) => setNewCategory({...newCategory, name: e.target.value})}
                  required
                />
              </div>
              <div className="form-group">
                <label>Type *</label>
                <select
                  value={newCategory.type}
                  onChange={(e) => setNewCategory({...newCategory, type: e.target.value})}
                >
                  <option value="expense">Expense</option>
                  <option value="income">Income</option>
                </select>
              </div>
            </div>
            <div className="form-group">
              <label>Description (Optional)</label>
              <input
                type="text"
                placeholder="Brief description of this category"
                value={newCategory.description}
                onChange={(e) => setNewCategory({...newCategory, description: e.target.value})}
              />
            </div>
            <div className="form-actions">
              <button type="submit" className="submit-button">
                ✅ Create Category
              </button>
              <button 
                type="button" 
                className="cancel-button"
                onClick={() => {
                  setShowCreateForm(false)
                  setNewCategory({ name: '', type: 'expense', description: '' })
                }}
              >
                ❌ Cancel
              </button>
            </div>
          </form>
        </div>
      )}

      {/* Summary Stats */}
      <div className="summary-row">
        <div className="summary-card expense-summary">
          <div className="summary-icon">💸</div>
          <div className="summary-content">
            <h3>Total Expenses</h3>
            <p className="summary-amount">£{totalSpending.toFixed(2)}</p>
            <p className="summary-subtitle">
              {filteredCategories.filter(c => c.type === 'expense').length} categories
            </p>
          </div>
        </div>
        <div className="summary-card income-summary">
          <div className="summary-icon">💰</div>
          <div className="summary-content">
            <h3>Total Income</h3>
            <p className="summary-amount">£{totalIncome.toFixed(2)}</p>
            <p className="summary-subtitle">
              {filteredCategories.filter(c => c.type === 'income').length} categories
            </p>
          </div>
        </div>
      </div>

      {/* Filter Tabs */}
      <div className="filter-tabs">
        <button 
          className={filter === 'all' ? 'active' : ''}
          onClick={() => setFilter('all')}
        >
          All Categories
        </button>
        <button 
          className={filter === 'expense' ? 'active' : ''}
          onClick={() => setFilter('expense')}
        >
          Expenses
        </button>
        <button 
          className={filter === 'income' ? 'active' : ''}
          onClick={() => setFilter('income')}
        >
          Income
        </button>
      </div>

      {/* Category Cards Grid */}
      <div className="categories-grid">
        {filteredCategories.map((category) => (
          <div 
            key={category.id} 
            className={`category-card ${category.type}`}
          >
            <div className="category-header">
              <div className="category-icon">
                {getCategoryIcon(category.name, category.type)}
              </div>
              <div className="category-info">
                <h3>{category.name}</h3>
                <p className="category-description">{category.description}</p>
              </div>
              <span className={`type-badge ${category.type}`}>
                {category.type}
              </span>
            </div>

            <div className="category-stats">
              <div className="stat-item">
                <span className="stat-label">Total Spent</span>
                <span className="stat-value amount">
                  £{category.total_spent.toFixed(2)}
                </span>
              </div>
              <div className="stat-item">
                <span className="stat-label">Transactions</span>
                <span className="stat-value">{category.transaction_count}</span>
              </div>
              <div className="stat-item">
                <span className="stat-label">Average</span>
                <span className="stat-value">
                  £{category.avg_transaction.toFixed(2)}
                </span>
              </div>
            </div>

            {category.recent_transactions && category.recent_transactions.length > 0 && (
              <div className="recent-transactions">
                <h4>Recent Transactions</h4>
                <div className="transactions-list">
                  {category.recent_transactions.map((transaction, idx) => (
                    <div key={idx} className="transaction-item">
                      <span className="transaction-desc">
                        {transaction.description || 'No description'}
                      </span>
                      <span className="transaction-amount">
                        £{parseFloat(transaction.amount).toFixed(2)}
                      </span>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {category.transaction_count === 0 && (
              <div className="no-transactions">
                <p>No transactions in this period</p>
              </div>
            )}

            <button 
              className="delete-category-button"
              onClick={() => handleDeleteCategory(category.id, category.name)}
              title="Delete this category"
            >
              🗑️ Delete
            </button>
          </div>
        ))}
      </div>
    </div>
  )
}

export default CategoriesPage