import React, { useState, useEffect } from 'react'
import {
  PieChart,
  Pie,
  Cell,
  LineChart,
  Line,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer
} from 'recharts'
import '../styles/AnalyticsPage.css'

const AnalyticsPage = () => {
  const [analyticsData, setAnalyticsData] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [period, setPeriod] = useState('30')

  useEffect(() => {
    fetchAnalytics()
  }, [period])

  const fetchAnalytics = async () => {
    try {
      setLoading(true)
      const response = await fetch(`/api/analytics?period=${period}&user_id=1`)
      
      if (!response.ok) {
        throw new Error('Failed to fetch analytics data')
      }
      
      const data = await response.json()
      setAnalyticsData(data)
      setError(null)
    } catch (err) {
      console.error('Error fetching analytics:', err)
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#8884D8', '#82ca9d', '#ffc658', '#ff7c7c']

  if (loading) {
    return (
      <div className="analytics-page">
        <div className="loading">Loading analytics...</div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="analytics-page">
        <div className="error">Error: {error}</div>
        <button onClick={fetchAnalytics}>Retry</button>
      </div>
    )
  }

  if (!analyticsData) {
    return (
      <div className="analytics-page">
        <div className="no-data">No analytics data available</div>
      </div>
    )
  }

  const { summary, spending_by_category, daily_trend, top_categories } = analyticsData

  // Prepare data for expense categories pie chart (only expenses)
  const expenseCategories = spending_by_category.filter(cat => cat.type === 'expense')
  
  // Prepare data for income vs expense comparison
  const incomeExpenseData = [
    { name: 'Income', value: summary.total_income, color: '#00C49F' },
    { name: 'Expenses', value: summary.total_expenses, color: '#FF8042' }
  ]

  return (
    <div className="analytics-page">
      <div className="analytics-header">
        <h1>📊 Financial Analytics</h1>
        <div className="period-selector">
          <label>Period: </label>
          <select value={period} onChange={(e) => setPeriod(e.target.value)}>
            <option value="7">Last 7 Days</option>
            <option value="30">Last 30 Days</option>
            <option value="90">Last 90 Days</option>
            <option value="365">Last Year</option>
          </select>
        </div>
      </div>

      {/* Summary Cards */}
      <div className="summary-cards">
        <div className="card income-card">
          <div className="card-icon">💰</div>
          <div className="card-content">
            <h3>Total Income</h3>
            <p className="amount">£{summary.total_income.toFixed(2)}</p>
          </div>
        </div>

        <div className="card expense-card">
          <div className="card-icon">💸</div>
          <div className="card-content">
            <h3>Total Expenses</h3>
            <p className="amount">£{summary.total_expenses.toFixed(2)}</p>
          </div>
        </div>

        <div className="card savings-card">
          <div className="card-icon">💎</div>
          <div className="card-content">
            <h3>Net Savings</h3>
            <p className={`amount ${summary.net_savings >= 0 ? 'positive' : 'negative'}`}>
              £{summary.net_savings.toFixed(2)}
            </p>
          </div>
        </div>

        <div className="card transaction-card">
          <div className="card-icon">📝</div>
          <div className="card-content">
            <h3>Transactions</h3>
            <p className="amount">{summary.transaction_count}</p>
            <p className="sub-text">Avg: £{summary.avg_transaction.toFixed(2)}</p>
          </div>
        </div>
      </div>

      {/* Charts Section */}
      <div className="charts-container">
        {/* Income vs Expense Pie Chart */}
        <div className="chart-card">
          <h3>Income vs Expenses</h3>
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie
                data={incomeExpenseData}
                cx="50%"
                cy="50%"
                labelLine={false}
                label={({ name, value }) => `${name}: £${value.toFixed(0)}`}
                outerRadius={80}
                fill="#8884d8"
                dataKey="value"
              >
                {incomeExpenseData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={entry.color} />
                ))}
              </Pie>
              <Tooltip formatter={(value) => `£${value.toFixed(2)}`} />
            </PieChart>
          </ResponsiveContainer>
        </div>

        {/* Spending by Category Pie Chart */}
        {expenseCategories.length > 0 && (
          <div className="chart-card">
            <h3>Spending by Category</h3>
            <ResponsiveContainer width="100%" height={300}>
              <PieChart>
                <Pie
                  data={expenseCategories}
                  cx="50%"
                  cy="50%"
                  labelLine={false}
                  label={({ category, amount }) => `${category}: £${amount.toFixed(0)}`}
                  outerRadius={80}
                  fill="#8884d8"
                  dataKey="amount"
                >
                  {expenseCategories.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip formatter={(value) => `£${value.toFixed(2)}`} />
              </PieChart>
            </ResponsiveContainer>
          </div>
        )}

        {/* Daily Trend Line Chart */}
        {daily_trend.length > 0 && (
          <div className="chart-card wide">
            <h3>Daily Income & Expense Trend</h3>
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={daily_trend}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis 
                  dataKey="date" 
                  tick={{ fontSize: 12 }}
                  angle={-45}
                  textAnchor="end"
                  height={80}
                />
                <YAxis />
                <Tooltip formatter={(value) => `£${value.toFixed(2)}`} />
                <Legend />
                <Line 
                  type="monotone" 
                  dataKey="income" 
                  stroke="#00C49F" 
                  strokeWidth={2}
                  name="Income"
                />
                <Line 
                  type="monotone" 
                  dataKey="expense" 
                  stroke="#FF8042" 
                  strokeWidth={2}
                  name="Expenses"
                />
              </LineChart>
            </ResponsiveContainer>
          </div>
        )}

        {/* Top Categories Bar Chart */}
        {top_categories.length > 0 && (
          <div className="chart-card wide">
            <h3>Top 5 Spending Categories</h3>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={top_categories}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="category" />
                <YAxis />
                <Tooltip formatter={(value) => `£${value.toFixed(2)}`} />
                <Legend />
                <Bar dataKey="amount" fill="#8884d8" name="Amount (£)">
                  {top_categories.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
        )}
      </div>

      {/* Insights Section */}
      <div className="insights-section">
        <h3>💡 Insights</h3>
        <div className="insights-cards">
          {summary.net_savings > 0 ? (
            <div className="insight-card positive">
              <p>Great job! You saved £{summary.net_savings.toFixed(2)} in the last {period} days.</p>
            </div>
          ) : (
            <div className="insight-card negative">
              <p>Your expenses exceeded income by £{Math.abs(summary.net_savings).toFixed(2)} in the last {period} days.</p>
            </div>
          )}
          
          {top_categories.length > 0 && (
            <div className="insight-card">
              <p>Your top spending category is <strong>{top_categories[0].category}</strong> at £{top_categories[0].amount.toFixed(2)}.</p>
            </div>
          )}
          
          <div className="insight-card">
            <p>You made {summary.transaction_count} transactions with an average of £{summary.avg_transaction.toFixed(2)} per transaction.</p>
          </div>
        </div>
      </div>
    </div>
  )
}

export default AnalyticsPage