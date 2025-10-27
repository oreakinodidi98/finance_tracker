import React, { useState } from 'react'
import { Link, useLocation } from 'react-router-dom'
import '../styles/Navbar.css'

const Navbar = () => {
  const [isProfileDropdownOpen, setIsProfileDropdownOpen] = useState(false)
  const location = useLocation()

  const isActive = (path) => location.pathname === path

  return (
    <nav className="navbar">
      <div className="nav-container">
        <Link to="/" className="nav-logo">
          💰 Finance Tracker
        </Link>
        
        <div className="nav-links">
          <Link 
            to="/" 
            className={`nav-link ${isActive('/') ? 'active' : ''}`}
          >
            🏠 Home
          </Link>
          <Link 
            to="/transactions" 
            className={`nav-link ${isActive('/transactions') ? 'active' : ''}`}
          >
            💳 Transactions
          </Link>
          <Link 
            to="/goals" 
            className={`nav-link ${isActive('/goals') ? 'active' : ''}`}
          >
            🎯 Goals
          </Link>
          <Link 
            to="/analytics" 
            className={`nav-link ${isActive('/analytics') ? 'active' : ''}`}
          >
            📊 Analytics
          </Link>
          <Link 
            to="/categories" 
            className={`nav-link ${isActive('/categories') ? 'active' : ''}`}
          >
            📂 Categories
          </Link>
        </div>

        <div className="profile-section">
          <button 
            className="profile-btn"
            onClick={() => setIsProfileDropdownOpen(!isProfileDropdownOpen)}
          >
            👤
          </button>
          
          {isProfileDropdownOpen && (
            <div className="profile-dropdown">
              <Link to="/profile" className="dropdown-item">
                Profile Settings
              </Link>
              <div className="dropdown-item">
                Logout
              </div>
            </div>
          )}
        </div>
      </div>
    </nav>
  )
}

export default Navbar