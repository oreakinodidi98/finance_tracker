import React, { useState, useRef, useEffect } from 'react';
import '../styles/ChatbotPage.css';

const ChatbotPage = () => {
  const [messages, setMessages] = useState([
    {
      id: 1,
      text: "Hello! I'm your AI-powered Finance Assistant. I can help you with budgeting tips, expense analysis, investment advice, and answer questions about your financial data. How can I help you today?",
      sender: 'bot',
      timestamp: new Date()
    }
  ]);
  const [inputMessage, setInputMessage] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const [isRagEnabled, setIsRagEnabled] = useState(true);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const generateBotResponse = async (userMessage) => {
    try {
      if (isRagEnabled) {
        // Try to use the RAG agent through the backend
        const response = await fetch('/api/chat', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ message: userMessage }),
        });

        if (response.ok) {
          const data = await response.json();
          return {
            text: data.response,
            source: data.source
          };
        } else {
          console.warn('RAG endpoint failed, falling back to simple responses');
          setIsRagEnabled(false);
        }
      }
    } catch (error) {
      console.warn('RAG request failed, falling back to simple responses:', error);
      setIsRagEnabled(false);
    }

    // Fallback to simple rule-based responses
    const message = userMessage.toLowerCase();
    
    if (message.includes('budget') || message.includes('budgeting')) {
      return {
        text: "Great question about budgeting! Here are some tips: 1) Track all your expenses 2) Use the 50/30/20 rule (50% needs, 30% wants, 20% savings) 3) Review your budget monthly. Would you like me to help you analyze your current spending?",
        source: 'fallback'
      };
    } else if (message.includes('save') || message.includes('saving')) {
      return {
        text: "Saving money is crucial for financial health! Start with an emergency fund covering 3-6 months of expenses. Then consider: automatic transfers to savings, high-yield savings accounts, and investment options. What's your current savings goal?",
        source: 'fallback'
      };
    } else if (message.includes('expense') || message.includes('spending')) {
      return {
        text: "Let's talk about expenses! I can see you have transaction data in this app. The key is categorizing expenses into needs vs wants. Would you like me to suggest some expense categories or help analyze your spending patterns?",
        source: 'fallback'
      };
    } else if (message.includes('investment') || message.includes('invest')) {
      return {
        text: "Investing is a great way to grow wealth! Consider: 1) Diversified index funds 2) Emergency fund first 3) Your risk tolerance 4) Time horizon. Remember, I'm an AI assistant - always consult with a financial advisor for personalized investment advice.",
        source: 'fallback'
      };
    } else if (message.includes('debt') || message.includes('loan')) {
      return {
        text: "Managing debt is important! Try these strategies: 1) List all debts with balances and interest rates 2) Consider debt avalanche (highest interest first) or snowball method (smallest balance first) 3) Avoid new debt while paying off existing ones.",
        source: 'fallback'
      };
    } else if (message.includes('goal') || message.includes('goals')) {
      return {
        text: "Financial goals are the foundation of good money management! Set SMART goals (Specific, Measurable, Achievable, Relevant, Time-bound). I see this app has a Goals section - have you set any financial goals there yet?",
        source: 'fallback'
      };
    } else if (message.includes('help') || message.includes('hi') || message.includes('hello')) {
      return {
        text: "I'm here to help with your finances! I can assist with: budgeting advice, saving strategies, expense tracking tips, debt management, goal setting, and general financial guidance. What would you like to explore?",
        source: 'fallback'
      };
    } else {
      return {
        text: "That's an interesting question! While I focus on financial topics, I can help you with budgeting, saving, investing basics, expense tracking, and financial goal setting. Could you ask me something about your finances?",
        source: 'fallback'
      };
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
    const currentMessage = inputMessage;
    setInputMessage('');
    setIsTyping(true);

    try {
      // Get bot response (either from RAG or fallback)
      const botResponseData = await generateBotResponse(currentMessage);
      
      const botResponse = {
        id: Date.now() + 1,
        text: botResponseData.text,
        sender: 'bot',
        timestamp: new Date(),
        source: botResponseData.source
      };
      
      setMessages(prev => [...prev, botResponse]);
    } catch (error) {
      console.error('Error generating bot response:', error);
      const errorResponse = {
        id: Date.now() + 1,
        text: "I apologize, but I'm having trouble processing your request right now. Please try again in a moment.",
        sender: 'bot',
        timestamp: new Date(),
        source: 'error'
      };
      setMessages(prev => [...prev, errorResponse]);
    } finally {
      setIsTyping(false);
    }
  };

  const formatTime = (timestamp) => {
    return timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  };

  const clearChat = () => {
    setMessages([
      {
        id: 1,
        text: "Hello! I'm your AI-powered Finance Assistant. I can help you with budgeting tips, expense analysis, investment advice, and answer questions about your financial data. How can I help you today?",
        sender: 'bot',
        timestamp: new Date()
      }
    ]);
  };

  const handleQuickQuestion = (question) => {
    setInputMessage(question);
    // Auto-submit the message
    setTimeout(() => {
      const event = { preventDefault: () => {} };
      handleSendMessage(event);
    }, 100);
  };

  return (
    <div className="chatbot-page">
      <div className="chat-header">
        <div className="chat-title">
          <h1>🤖 Finance Assistant</h1>
          <p>
            {isRagEnabled ? 
              "AI-powered financial advisor" : 
              "Financial advisor (Simple mode)"
            }
          </p>
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
                <div className="message-meta">
                  <span className="message-time">{formatTime(message.timestamp)}</span>
                  {message.source && (
                    <span className={`message-source ${message.source}`}>
                      {message.source === 'rag_agent' ? '🧠 AI' : 
                       message.source === 'fallback' ? '💡 Simple' : ''}
                    </span>
                  )}
                </div>
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
              placeholder="Ask me about budgeting, saving, expenses, or investments..."
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
          <button onClick={() => handleQuickQuestion("How can I create a budget?")}>
            💰 Budgeting Tips
          </button>
          <button onClick={() => handleQuickQuestion("How do I save more money?")}>
            🏦 Saving Strategies
          </button>
          <button onClick={() => handleQuickQuestion("Help me track my expenses")}>
            📊 Expense Tracking
          </button>
          <button onClick={() => handleQuickQuestion("What are good financial goals?")}>
            🎯 Financial Goals
          </button>
          <button onClick={() => handleQuickQuestion("How should I start investing?")}>
            📈 Investment Advice
          </button>
          <button onClick={() => handleQuickQuestion("How can I manage my debt?")}>
            💳 Debt Management
          </button>
        </div>
      </div>
    </div>
  );
};

export default ChatbotPage;