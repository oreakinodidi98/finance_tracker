import React from 'react'
import '../styles/HomePage.css'

const HomePage = () => {
  return (
    <div className="home-page">
      <div className="hero-section">
        <h1>Welcome to Finance Tracker</h1>
        <p>Take control of your finances with our comprehensive tracking system</p>
        <div className="stats-grid">
          <div className="stat-card">
            <h3>£0.00</h3>
            <p>Total Balance</p>
          </div>
          <div className="stat-card">
            <h3>0</h3>
            <p>This Month's Transactions</p>
          </div>
          <div className="stat-card">
            <h3>0</h3>
            <p>Active Goals</p>
          </div>
          <div className="stat-card">
            <h3>0</h3>
            <p>Categories</p>
          </div>
        </div>
      </div>
      
      <div className="quick-actions">
        <h2>Quick Actions</h2>
        <div className="action-buttons">
          <button className="action-btn">Add Transaction</button>
          <button className="action-btn">Create Goal</button>
          <button className="action-btn">View Analytics</button>
        </div>
      </div>
    </div>
  )
}

export default HomePage