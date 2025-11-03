import React from "react"

// Component to display a list of Goals
const GoalList = ({ goals, onEdit, onDelete }) => {

  // Helper function to format priority display
  const formatPriority = (priority) => {
    switch(priority) {
      case 1: return '🔥 High';
      case 2: return '🟡 Medium'; 
      case 3: return '🟢 Low';
      default: return priority;
    }
  };

  // Helper function to format status display
  const formatStatus = (status) => {
    switch(status) {
      case 'in_progress': return '🔄 In Progress';
      case 'completed': return '✅ Completed';
      case 'on_hold': return '⏸️ On Hold';
      default: return status;
    }
  };

  return (
    <div>
      <h2>Savings Goals List</h2>
      <table>
        <thead>
          <tr>
            <th>ID</th>
            <th>Name</th>
            <th>Description</th>
            <th>Target Amount</th>
            <th>Current Amount</th>
            <th>Deadline</th>
            <th>Priority</th>
            <th>Status</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {goals && goals.length > 0 ? (
            goals.map((goal) => (
              <tr key={goal.id}>
                <td>{goal.id}</td>
                <td>{goal.name}</td>
                <td>{goal.description}</td>
                <td>£{parseFloat(goal.target_amount).toFixed(2)}</td>
                <td>£{parseFloat(goal.current_amount).toFixed(2)}</td>
                <td>{new Date(goal.deadline).toLocaleDateString()}</td>
                <td className="priority">{formatPriority(goal.priority)}</td>
                <td className={`status ${goal.status}`}>{formatStatus(goal.status)}</td>
                <td>
                  <button 
                    className="edit-btn"
                    onClick={() => onEdit(goal)}
                    title="Edit Saving Goal"
                  >
                    ✏️ Edit
                  </button>
                  <button 
                    className="delete-btn"
                    onClick={() => onDelete(goal.id)}
                    title="Delete Saving Goal"
                  >
                    🗑️ Delete
                  </button>
                </td>
              </tr>
            ))
          ) : (
            <tr>
              <td colSpan="9" style={{ textAlign: 'center', padding: '20px' }}>
                No savings goals found. Add your first saving goal!
              </td>
            </tr>
          )}
        </tbody>
      </table>
    </div>
  )
}

export default GoalList;