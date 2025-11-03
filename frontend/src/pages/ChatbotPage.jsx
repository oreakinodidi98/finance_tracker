import React, { useState, useRef, useEffect } from 'react';
import '../styles/ChatbotPage.css';

const ChatbotPage = () => {
  const [messages, setMessages] = useState([
    {
      id: 1,
      text: "Hello! I'm your Finance Assistant. I can help you with budgeting tips, expense analysis, and financial advice. How can I help you today?",
      sender: 'bot',
      timestamp: new Date()
    }
  ]);
  const [inputMessage, setInputMessage] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const generateBotResponse = (userMessage) => {
    const message = userMessage.toLowerCase();
    
    // Simple rule-based responses for finance-related queries
    if (message.includes('budget') || message.includes('budgeting')) {
      return "Great question about budgeting! Here are some tips: 1) Track all your expenses 2) Use the 50/30/20 rule (50% needs, 30% wants, 20% savings) 3) Review your budget monthly. Would you like me to help you analyze your current spending?";
    } else if (message.includes('save') || message.includes('saving')) {
      return "Saving money is crucial for financial health! Start with an emergency fund covering 3-6 months of expenses. Then consider: automatic transfers to savings, high-yield savings accounts, and investment options. What's your current savings goal?";
    } else if (message.includes('expense') || message.includes('spending')) {
      return "Let's talk about expenses! I can see you have transaction data in this app. The key is categorizing expenses into needs vs wants. Would you like me to suggest some expense categories or help analyze your spending patterns?";
    } else if (message.includes('investment') || message.includes('invest')) {
      return "Investing is a great way to grow wealth! Consider: 1) Diversified index funds 2) Emergency fund first 3) Your risk tolerance 4) Time horizon. Remember, I'm an AI assistant - always consult with a financial advisor for personalized investment advice.";
    } else if (message.includes('debt') || message.includes('loan')) {
      return "Managing debt is important! Try these strategies: 1) List all debts with balances and interest rates 2) Consider debt avalanche (highest interest first) or snowball method (smallest balance first) 3) Avoid new debt while paying off existing ones.";
    } else if (message.includes('goal') || message.includes('goals')) {
      return "Financial goals are the foundation of good money management! Set SMART goals (Specific, Measurable, Achievable, Relevant, Time-bound). I see this app has a Goals section - have you set any financial goals there yet?";
    } else if (message.includes('help') || message.includes('hi') || message.includes('hello')) {
      return "I'm here to help with your finances! I can assist with: budgeting advice, saving strategies, expense tracking tips, debt management, goal setting, and general financial guidance. What would you like to explore?";
    } else {
      return "That's an interesting question! While I focus on financial topics, I can help you with budgeting, saving, investing basics, expense tracking, and financial goal setting. Could you ask me something about your finances?";
    }
  };

  const handleSendMessage = async (e) => {
    e.preventDefault();
    if (!inputMessage.trim()) return;

    const newMessage = {
      id: Date.now(),
      text: inputMessage,
      sender: 'user',
      timestamp: new Date()
    };

    setMessages(prev => [...prev, newMessage]);
    setInputMessage('');
    setIsTyping(true);

    // Simulate typing delay
    setTimeout(() => {
      const botResponse = {
        id: Date.now() + 1,
        text: generateBotResponse(inputMessage),
        sender: 'bot',
        timestamp: new Date()
      };
      
      setMessages(prev => [...prev, botResponse]);
      setIsTyping(false);
    }, 1500);
  };

  const formatTime = (timestamp) => {
    return timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  };

  const clearChat = () => {
    setMessages([
      {
        id: 1,
        text: "Hello! I'm your Finance Assistant. I can help you with budgeting tips, expense analysis, and financial advice. How can I help you today?",
        sender: 'bot',
        timestamp: new Date()
      }
    ]);
  };

  return (
    <div className="chatbot-page">
      <div className="chat-header">
        <div className="chat-title">
          <h1>🤖 Finance Assistant</h1>
          <p>Your AI-powered financial advisor</p>
        </div>
        <button className="clear-chat-btn" onClick={clearChat}>
          🗑️ Clear Chat
        </button>
      </div>

      <div className="chat-container">
        <div className="messages-container">
          {messages.map((message) => (
            <div
              key={message.id}
              className={`message ${message.sender === 'user' ? 'user-message' : 'bot-message'}`}
            >
              <div className="message-content">
                <p>{message.text}</p>
                <span className="message-time">{formatTime(message.timestamp)}</span>
              </div>
            </div>
          ))}
          
          {isTyping && (
            <div className="message bot-message">
              <div className="message-content">
                <div className="typing-indicator">
                  <span></span>
                  <span></span>
                  <span></span>
                </div>
              </div>
            </div>
          )}
          
          <div ref={messagesEndRef} />
        </div>

        <form className="message-input-form" onSubmit={handleSendMessage}>
          <div className="input-container">
            <input
              type="text"
              value={inputMessage}
              onChange={(e) => setInputMessage(e.target.value)}
              placeholder="Ask me about budgeting, saving, expenses..."
              className="message-input"
            />
            <button type="submit" className="send-button" disabled={!inputMessage.trim()}>
              ➤
            </button>
          </div>
        </form>
      </div>

      <div className="quick-questions">
        <h3>Quick Questions:</h3>
        <div className="quick-buttons">
          <button onClick={() => setInputMessage("How can I create a budget?")}>
            💰 Budgeting Tips
          </button>
          <button onClick={() => setInputMessage("How do I save more money?")}>
            🏦 Saving Strategies
          </button>
          <button onClick={() => setInputMessage("Help me track my expenses")}>
            📊 Expense Tracking
          </button>
          <button onClick={() => setInputMessage("What are good financial goals?")}>
            🎯 Financial Goals
          </button>
        </div>
      </div>
    </div>
  );
};

export default ChatbotPage;