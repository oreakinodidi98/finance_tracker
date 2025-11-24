import { useState, useEffect } from "react";

const GoalForm = ({ existingGoal={}, updateCallback }) => {
  // form state for each field
const [name, setName] = useState(existingGoal?.name || "");
const [description, setDescription] = useState(existingGoal?.description || "");
const [targetAmount, setTargetAmount] = useState(existingGoal?.target_amount || "");
const [currentAmount, setCurrentAmount] = useState(existingGoal?.current_amount || "");
const [deadline, setDeadline] = useState(existingGoal?.deadline || "");
const [priority, setPriority] = useState(existingGoal?.priority || "");
const [status, setStatus] = useState(existingGoal?.status || "");
//const [categoryId, setCategoryId] = useState(existingTransaction?.category_id || "");

  // Populate form with existing goal data when editing
  useEffect(() => {
    if (existingGoal) {
      setName(existingGoal.name || "");
      setDescription(existingGoal.description || "");
      setTargetAmount(existingGoal.target_amount || "");
      setCurrentAmount(existingGoal.current_amount || "");
      setDeadline(existingGoal.deadline || "");
      setPriority(existingGoal.priority || "");
      setStatus(existingGoal.status || "");
    } else {
      // Reset form for new goal
      setName("");
      setDescription("");
      setTargetAmount("");
      setCurrentAmount("");
      setDeadline("");
      setPriority("");
      setStatus("in_progress");
    }
  }, [existingGoal]);

  // check if we are updating an existing goal. If you pass an object that has at least 1 key, we consider it an update
  const updating = existingGoal && Object.entries(existingGoal).length !== 0;

  // on form submit
  const handleSubmit = async (e) => {
    e.preventDefault();

    // Validate form data
    if (!name || !targetAmount || !deadline) {
      alert('Please fill in all required fields');
      return;
    }

    // define data to send
    const data = {
      user_id: 1, // Hardcoded for now
      name,
      description,
      target_amount: parseFloat(targetAmount),
      current_amount: parseFloat(currentAmount) || 0,
      deadline,
      priority: parseInt(priority),
      status
    };

    console.log('Sending data:', data);

    // Choose endpoint based on whether we're editing or creating
    const isEditing = existingGoal && existingGoal.id;
    const url = isEditing 
      ? `/api/update_goal/${existingGoal.id}`
      : '/api/create_goal';

    const options = {
        method: isEditing ? 'PATCH' : 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
    };

    try {
        // setting the request
        const response = await fetch(url, options)
        console.log('Response status:', response.status);
        
        // check if request was successful
        if (response.status !== 201 && response.status !== 200) {
            const errorData = await response.json();
            alert(errorData.message || 'Error creating savings goal');
        } else {
            const responseData = await response.json();
        console.log('Response data:', responseData);

        alert(isEditing ? 'Savings goal updated successfully!' : 'Savings goal created successfully!');

        if (updateCallback) {
          updateCallback(responseData);
        }
      }
    } catch (error) {
        console.error('Error:', error);
        alert('Failed to create savings goal');
    }
  };
  return (
    <form onSubmit={handleSubmit}>
      <div className="input-group">
        <label>Goal Name</label>
        <input
          type="text"
          placeholder="Enter goal name"
          value={name}
          onChange={(e) => setName(e.target.value)}
          required
        />
      </div>

      <div className="input-group">
        <label>Description</label>
        <textarea
          placeholder="Describe your goal"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          rows={3}
        />
      </div>

      <div className="input-group">
        <label>Target Amount (£)</label>
        <input
          type="number"
          step="0.01"
          placeholder="0.00"
          value={targetAmount}
          onChange={(e) => setTargetAmount(e.target.value)}
          required
        />
      </div>

      <div className="input-group">
        <label>Current Amount (£)</label>
        <input
          type="number"
          step="0.01"
          placeholder="0.00"
          value={currentAmount}
          onChange={(e) => setCurrentAmount(e.target.value)}
        />
      </div>

      <div className="input-group">
        <label>Deadline</label>
        <input
          type="date"
          value={deadline}
          onChange={(e) => setDeadline(e.target.value)}
          required
        />
      </div>

      <div className="input-group">
        <label>Priority</label>
        <select value={priority} onChange={(e) => setPriority(e.target.value)}>
          <option value={1}>🔥 High</option>
          <option value={2}>🟡 Medium</option>
          <option value={3}>🟢 Low</option>
        </select>
      </div>

      <div className="input-group">
        <label>Status</label>
        <select value={status} onChange={(e) => setStatus(e.target.value)}>
          <option value="in_progress">🔄 In Progress</option>
          <option value="completed">✅ Completed</option>
          <option value="on_hold">⏸️ On Hold</option>
        </select>
      </div>

      <button type="submit">
        {(existingGoal && existingGoal.id) ? '💾 Update Goal' : '➕ Add Goal'}
      </button>
    </form>
  );
};

export default GoalForm;
