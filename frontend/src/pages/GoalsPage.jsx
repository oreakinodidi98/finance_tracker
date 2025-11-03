import { useState, useEffect } from 'react'
import '../App.css'
import GoalList from "../components/SavingsList.jsx";
import GoalForm from '../components/SavingsForm.jsx';

function GoalsPage() {
  // state to store goals
  const [goals, setGoals] = useState([])
  //modal component
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [currentGoal, setCurrentGoal] = useState(null);
  // call this once using useEffect to fetch goals on component mount
  useEffect(() => {
    fetchGoals();
  }, []);

   // Function to fetch goals from backend
  const fetchGoals = async () => {
    try {
      const response = await fetch('http://localhost:5000/goals')
      const data = await response.json()
      setGoals(data.goals || [])
      console.log(data.goals)
      console.log('Full response:', data)
      console.log('Goals array:', data.goals)
      console.log('Array length:', data.goals ? data.goals.length : 'undefined')
    } catch (error) {
      console.error('Error fetching goals:', error)
      // Set some mock data for testing when backend is not available
      setGoals([
        {
          id: 1,
          name: 'Emergency Fund',
          description: 'Build up 6 months of expenses',
          target_amount: 10000,
          current_amount: 2500,
          deadline: '2025-11-03',
          priority: 1,
          status: 'in_progress'
        },
        {
          id: 2,
          name: 'Holiday Fund',
          description: 'Save for vacation',
          target_amount: 3000,
          current_amount: 500,
          deadline: '2025-07-15',
          priority: 2,
          status: 'in_progress'
        }
      ])
    }
  };

  // function to toggle modal
  const closeModal = () => {
    setIsModalOpen(false);
    setCurrentGoal(null);
  };
  const openCreateModal = () => {
    if (!isModalOpen) {
      setIsModalOpen(true);
    }
  };
  // open modal for editing
  const openEditModal = (goal) => {
    console.log('Opening edit modal for:', goal);
    setCurrentGoal(goal);
    setIsModalOpen(true);
  }

  // Delete function
  const deleteGoal = async (goalId) => {
    if (window.confirm('Are you sure you want to delete this goal?')) {
      try {
        const response = await fetch(`http://localhost:5000/delete_goal/${goalId}`, {
          method: 'DELETE'
        });
        
        if (response.ok) {
          fetchGoals(); // Refresh the list
          alert('Goal deleted successfully!');
        } else {
          alert('Error deleting savings goal');
        }
      } catch (error) {
        console.error('Error deleting goal:', error);
        alert('Error deleting savings goal');
      }
    }
  };

  // callback function after goal is created/updated
  const onUpdateGoal = () => {
    closeModal();
    fetchGoals();
  };

  const calculateProgress = (current, target) => {
    return Math.min((current / target) * 100, 100);
  };

  const formatCurrency = (amount) => {
    return new Intl.NumberFormat('en-GB', {
      style: 'currency',
      currency: 'GBP'
    }).format(amount);
  };

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('en-GB');
  };

  const getDaysRemaining = (deadline) => {
    const today = new Date();
    const deadlineDate = new Date(deadline);
    const diffTime = deadlineDate - today;
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
    return diffDays;
  };

  const getPriorityText = (priority) => {
    switch(priority) {
      case 1: return { text: 'High', emoji: '🔥', class: 'high' };
      case 2: return { text: 'Medium', emoji: '🟡', class: 'medium' };
      case 3: return { text: 'Low', emoji: '🟢', class: 'low' };
      default: return { text: 'Unknown', emoji: '❓', class: 'unknown' };
    }
  };

  const getStatusEmoji = (status) => {
    switch(status) {
      case 'completed': return '✅';
      case 'in_progress': return '🔄';
      case 'on_hold': return '⏸️';
      default: return '❓';
    }
  };

  return (
    <div className="App">
      <h1>🎯 Goals Tracker</h1>

      <GoalList goals={goals} onEdit={openEditModal} onDelete={deleteGoal} updateCallback={onUpdateGoal} />

      <button
        className="add-transaction-btn"
        onClick={openCreateModal}
      >
        ➕ Add Goal
      </button>
      
      {isModalOpen && (
        <div className="Modal">
          <div className="ModalContent">
            <span className="CloseButton" onClick={closeModal}>&times;</span>
            <h2>{currentGoal ? "Edit Goal" : "Add New Goal"}</h2>
            <GoalForm existingGoal={currentGoal} updateCallback={onUpdateGoal} />
          </div>
        </div>
      )}
    </div>
  );
}

export default GoalsPage