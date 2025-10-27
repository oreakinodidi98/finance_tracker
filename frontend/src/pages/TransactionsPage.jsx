import { useState, useEffect } from 'react'
import '../App.css'
import TransactionList from "../components/TransactionList.jsx";
import TransactionForm from '../components/TransactionForm.jsx';

function TransactionsPage() {
  // state to store transactions
  const [transactions, setTransactions] = useState([])
  //modal component
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [currentTransaction, setCurrentTransaction] = useState(null);

  // call this once using useEffect to fetch transactions on component mount
  useEffect(() => {
    fetchTransactions()
  }, [])

  // Function to fetch transactions from backend
  const fetchTransactions = async () => {
    try {
      const response = await fetch('http://localhost:5000/transactions')
      const data = await response.json()
      setTransactions(data.transactions || [])
      console.log(data.transactions)
      console.log('Full response:', data)
      console.log('Transactions array:', data.transactions)
      console.log('Array length:', data.transactions ? data.transactions.length : 'undefined')
    } catch (error) {
      console.error('Error fetching transactions:', error)
      // Set some mock data for testing when backend is not available
      setTransactions([
        {
          id: 1,
          description: 'Sample transaction',
          amount: 100,
          transaction_type: 'expense',
          transaction_date: new Date().toISOString(),
          category_id: 1
        },
        {
          id: 2,
          description: 'Another transaction',
          amount: 50,
          transaction_type: 'income',
          transaction_date: new Date().toISOString(),
          category_id: 2
        }
      ])
    }
  };

  // function to toggle modal
  const closeModal = () => {
    setIsModalOpen(false);
    setCurrentTransaction(null);
  };
  const openCreateModal = () => {
    if (!isModalOpen) {
      setIsModalOpen(true);
    }
  };
  // open modal for editing
  const openEditModal = (transaction) =>
  {
  console.log('Opening edit modal for:', transaction);
  setCurrentTransaction(transaction);
  setIsModalOpen(true);
}
  // Delete function
  const deleteTransaction = async (transactionId) => {
    if (window.confirm('Are you sure you want to delete this transaction?')) {
      try {
        const response = await fetch(`http://localhost:5000/delete_transaction/${transactionId}`, {
          method: 'DELETE'
        });
        
        if (response.ok) {
          fetchTransactions(); // Refresh the list
          alert('Transaction deleted successfully!');
        } else {
          alert('Error deleting transaction');
        }
      } catch (error) {
        console.error('Error deleting transaction:', error);
        alert('Error deleting transaction');
      }
    }
  };
  // callback function after transaction is created/updated
const onUpdateTransaction = () => {
  closeModal();
  fetchTransactions();
};

  return (
  //   <>
  //   <TransactionList transactions={transactions} />
  //   < button onClick={openCreateModal}>Add Transaction</button>
  //   {isModalOpen && <div className="Modal">
  //     <div className="ModalContent">
  //       <span className="CloseButton" onClick={closeModal}>&times;</span>
  //       <TransactionForm />
  //     </div>
  //   </div>}
  //   </>
  // );
  <div className="App">
      <h1>💰 Finance Tracker</h1>

      <TransactionList transactions={transactions} onEdit={openEditModal} onDelete={deleteTransaction} updateCallback={onUpdateTransaction} />

      <button
        className="add-transaction-btn"
        onClick={openCreateModal}
      >
        ➕ Add Transaction
      </button>
      
      {isModalOpen && (
        <div className="Modal">
          <div className="ModalContent">
            <span className="CloseButton" onClick={closeModal}>&times;</span>
            <h2>{currentTransaction ? "Edit Transaction" : "Add New Transaction"}</h2>
            <TransactionForm existingTransaction={currentTransaction} updateCallback={onUpdateTransaction} />
          </div>
        </div>
      )}
    </div>
  );
}

export default TransactionsPage