import React from "react"

// Component to display a list of transactions
const TransactionList = ({ transactions, onEdit, onDelete }) => {

  return (
    <div>
      <h2>Transaction List</h2>
      <table>
        <thead>
          <tr>
            <th>ID</th>
            <th>Description</th>
            <th>Amount</th>
            <th>Type</th>
            <th>Date</th>
            <th>Category</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {transactions && transactions.length > 0 ? (
            transactions.map((transaction) => (
              <tr key={transaction.id}>
                <td>{transaction.id}</td>
                <td>{transaction.description}</td>
                <td>£{parseFloat(transaction.amount).toFixed(2)}</td>
                <td className={`transaction-type ${transaction.transaction_type}`}>
                  {transaction.transaction_type}
                </td>
                <td>{new Date(transaction.transaction_date).toLocaleDateString()}</td>
                <td>{transaction.category_id}</td>
                <td>
                  <button 
                    className="edit-btn"
                    onClick={() => onEdit(transaction)}
                    title="Edit Transaction"
                  >
                    ✏️ Edit
                  </button>
                  <button 
                    className="delete-btn"
                    onClick={() => onDelete(transaction.id)}
                    title="Delete Transaction"
                  >
                    🗑️ Delete
                  </button>
                </td>
              </tr>
            ))
          ) : (
            <tr>
              <td colSpan="7" style={{ textAlign: 'center', padding: '20px' }}>
                No transactions found. Add your first transaction!
              </td>
            </tr>
          )}
        </tbody>
      </table>
    </div>
  )
}

export default TransactionList