import { useState, useEffect } from "react";

const TransactionForm = ({ existingTransaction={}, updateCallback }) => {
  // form state for each field
  const [description, setDescription] = useState(existingTransaction?.description || "");
const [amount, setAmount] = useState(existingTransaction?.amount || "");
const [transactionType, setTransactionType] = useState(existingTransaction?.transaction_type || "expense");
const [transactionDate, setTransactionDate] = useState(existingTransaction?.transaction_date || "");
const [categoryId, setCategoryId] = useState(existingTransaction?.category_id || "");

  // Populate form with existing transaction data when editing
  useEffect(() => {
    if (existingTransaction) {
      setDescription(existingTransaction.description || "");
      setAmount(existingTransaction.amount || "");
      setTransactionType(existingTransaction.transaction_type || "expense");
      
      // Format date for input field
      if (existingTransaction.transaction_date) {
        const date = new Date(existingTransaction.transaction_date);
        setTransactionDate(date.toISOString().split('T')[0]);
      }
      
      setCategoryId(existingTransaction.category_id || "");
    } else {
      // Reset form for new transaction
      setDescription("");
      setAmount("");
      setTransactionType("expense");
      setTransactionDate("");
      setCategoryId("");
    }
  }, [existingTransaction]);

  // check if we are updating an existing transaction. If you pass an object that has at least 1 key, we consider it an update
  const updating = existingTransaction && Object.entries(existingTransaction).length !== 0;

  // on form submit
  const handleSubmit = async (e) => {
    e.preventDefault();
    
    // Validate form data
    if (!amount || !transactionDate) {
        alert('Please fill in all fields');
        return;
    }
    
    // define data to send
    const data =
    {
        description,
        amount: parseFloat(amount),
        transaction_type: transactionType,
        transaction_date: transactionDate,
        category_id: parseInt(categoryId),
    }
    
    console.log('Sending data:', data);
    
    // define url endpoint and options for request
    //const url = 'http://localhost:5000/'+(updating ? `update_transaction/${existingTransaction.id}` : 'create_transaction');
    
    // Choose endpoint based on whether we're editing or creating
    const isEditing = existingTransaction && existingTransaction.id;
    const url = isEditing 
      ? `http://localhost:5000/update_transaction/${existingTransaction.id}`
      : 'http://localhost:5000/create_transaction';

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
            alert(errorData.message || 'Error creating transaction');
        } else {
            const responseData = await response.json();
        console.log('Response data:', responseData);
        
        alert(isEditing ? 'Transaction updated successfully!' : 'Transaction created successfully!');
        
        if (updateCallback) {
          updateCallback(responseData);
        }
      }
    } catch (error) {
        console.error('Error:', error);
        alert('Failed to create transaction');
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <div className="input-group">
        <label>Description</label>
        <input
          type="text"
          placeholder="Enter description"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          required
        />
      </div>

      <div className="input-group">
        <label>Amount (£)</label>
        <input
          type="number"
          step="0.01"
          placeholder="0.00"
          value={amount}
          onChange={(e) => setAmount(e.target.value)}
          required
        />
      </div>

      <div className="input-group">
        <label>Transaction Type</label>
        <select
          value={transactionType}
          onChange={(e) => setTransactionType(e.target.value)}
        >
          <option value="expense">Expense</option>
          <option value="income">Income</option>
        </select>
      </div>

      <div className="input-group">
        <label>Date</label>
        <input
          type="date"
          value={transactionDate}
          onChange={(e) => setTransactionDate(e.target.value)}
          required
        />
      </div>

      <div className="input-group">
        <label>Category ID</label>
        <input
          type="number"
          placeholder="Category ID"
          value={categoryId}
          onChange={(e) => setCategoryId(e.target.value)}
          required
          min="1"
        />
      </div>

      <button type="submit">
        {(existingTransaction && existingTransaction.id) ? '💾 Update Transaction' : '➕ Add Transaction'}
      </button>
    </form>
  );
};

export default TransactionForm;
