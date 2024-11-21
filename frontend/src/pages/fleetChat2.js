import React, { useState, useEffect } from 'react';
import { Transition } from '@headlessui/react';
import ReactMarkdown from 'react-markdown';

const Chat = () => {
  const [messages, setMessages] = useState([]);
  const [isTyping, setIsTyping] = useState(false);
  const [inputValue, setInputValue] = useState('');

  async function postMessage (message) {
    let data = {
      // message: "I need a diabetes-friendly dinner recipe. Can you find one and confirm if it aligns with my health records and medications?"
      message: message
    };
    const res = await fetch("http://localhost:8000/agent-workflow", {
        method: "POST",
        headers: {
        "Content-Type": "application/json", 
        },
            body: JSON.stringify(data),
    });
    const out = await res.json();
   return out;
  }

  const sendMessage = (message) => {
    setMessages((prev) => [...prev, { sender: 'user', content: message }]);
    setInputValue('');
    setIsTyping(true);
    const response = postMessage(message);

    setTimeout(() => {
        if (response.data) {
            setMessages((prev) => [
                ...prev,
                { sender: 'bot', content: response.data },
              ]);
        } else {
            setMessages((prev) => [
                ...prev,
                { sender: 'bot', content: "I'm sorry. Something went wrong. Please try again in some time." },
              ]);
        }
      setIsTyping(false);
    }, 100000);
  };

  return (
    <div className="h-screen flex flex-col bg-gray-100">
      <div className="flex-grow overflow-y-auto p-4">
        {messages.map((msg, idx) => (
          <div
            key={idx}
            className={`flex ${
              msg.sender === 'user' ? 'justify-end' : 'justify-start'
            } mb-2`}
          >
            <div
              className={`max-w-xs p-3 rounded-lg ${
                msg.sender === 'user'
                  ? 'bg-blue-500 text-white'
                  : 'bg-gray-200 text-black'
              }`}
            >
              <ReactMarkdown>{msg.content}</ReactMarkdown>
            </div>
          </div>
        ))}
        {isTyping && (
          <div className="flex justify-start mb-2">
            <div className="max-w-xs p-3 bg-gray-200 text-black rounded-lg">
              <div className="flex items-center space-x-2">
                <div className="w-2 h-2 bg-gray-500 rounded-full animate-pulse"></div>
                <div className="w-2 h-2 bg-gray-500 rounded-full animate-pulse delay-75"></div>
                <div className="w-2 h-2 bg-gray-500 rounded-full animate-pulse delay-150"></div>
              </div>
            </div>
          </div>
        )}
      </div>
      <div className="p-4 bg-white">
        <form
          onSubmit={(e) => {
            e.preventDefault();
            if (inputValue.trim()) sendMessage(inputValue);
          }}
        >
          <div className="flex items-center border border-gray-300 rounded-lg overflow-hidden">
            <input
              type="text"
              className="flex-grow px-4 py-2 outline-none"
              placeholder="Type a message..."
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
            />
            <button
              type="submit"
              className="px-4 py-2 bg-blue-500 text-white hover:bg-blue-600"
            >
              Send
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default Chat;
