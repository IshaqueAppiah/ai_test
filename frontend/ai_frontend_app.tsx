import React, { useState, useRef, useEffect } from 'react';
import { Send, Upload, Zap, Brain, Search, Settings, Menu, X, Loader, Copy, Check } from 'lucide-react';

const AIApp = () => {
  const [activeTab, setActiveTab] = useState('chat');
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [aiModel, setAiModel] = useState('openai');
  const [streamMode, setStreamMode] = useState(false);
  const [uploadedFile, setUploadedFile] = useState(null);
  const [vectorStoreId, setVectorStoreId] = useState(null);
  const [menuOpen, setMenuOpen] = useState(false);
  const [copiedId, setCopiedId] = useState(null);
  const messagesEndRef = useRef(null);
  const fileInputRef = useRef(null);

  const API_URL = 'http://localhost:8000';

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const sendMessage = async () => {
    if (!input.trim()) return;

    const userMessage = { role: 'user', content: input };
    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setLoading(true);

    try {
      let endpoint = '/chat';
      if (activeTab === 'chat') {
        if (aiModel === 'gemini') {
          endpoint = '/chat_with_gemini';
        } else if (aiModel === 'ollama') {
          endpoint = '/chat/ollama';
        } else if (streamMode) {
          endpoint = '/chat/stream';
        }
      } else if (activeTab === 'reasoning') {
        endpoint = '/chat/reasoning';
      } else if (activeTab === 'search') {
        endpoint = '/search_store';
      }

      if (streamMode && activeTab === 'chat' && aiModel === 'openai') {
        await handleStreamResponse(endpoint);
      } else if (activeTab === 'reasoning') {
        await handleReasoningStream(endpoint);
      } else {
        const response = await fetch(`${API_URL}${endpoint}`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ message: input }),
        });

        if (!response.ok) throw new Error('Failed to get response');

        const data = await response.json();
        const assistantMessage = {
          role: 'assistant',
          content: data.response || data.content || JSON.stringify(data),
        };
        setMessages(prev => [...prev, assistantMessage]);
      }
    } catch (error) {
      const errorMessage = {
        role: 'assistant',
        content: `Error: ${error.message}`,
        isError: true,
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setLoading(false);
    }
  };

  const handleStreamResponse = async (endpoint) => {
    const response = await fetch(`${API_URL}${endpoint}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message: input }),
    });

    if (!response.ok) throw new Error('Failed to stream response');

    const reader = response.body.getReader();
    const decoder = new TextDecoder();
    let fullResponse = '';

    setMessages(prev => [
      ...prev,
      { role: 'assistant', content: '', isStreaming: true },
    ]);

    while (true) {
      const { done, value } = await reader.read();
      if (done) break;

      const chunk = decoder.decode(value);
      const lines = chunk.split('\n');

      for (const line of lines) {
        if (line.startsWith('data: ')) {
          fullResponse += line.slice(6);
          setMessages(prev => {
            const updated = [...prev];
            updated[updated.length - 1].content = fullResponse;
            return updated;
          });
        }
      }
    }

    setMessages(prev => {
      const updated = [...prev];
      updated[updated.length - 1].isStreaming = false;
      return updated;
    });
  };

  const handleReasoningStream = async (endpoint) => {
    const response = await fetch(`${API_URL}${endpoint}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message: input }),
    });

    if (!response.ok) throw new Error('Failed to stream response');

    const reader = response.body.getReader();
    const decoder = new TextDecoder();
    let reasoning = '';
    let output = '';

    setMessages(prev => [
      ...prev,
      { role: 'assistant', content: '', reasoning: '', isStreaming: true },
    ]);

    while (true) {
      const { done, value } = await reader.read();
      if (done) break;

      const chunk = decoder.decode(value);
      const lines = chunk.split('\n');

      for (const line of lines) {
        if (line.includes('event: reasoning')) {
          const data = lines[lines.indexOf(line) + 1]?.slice(6) || '';
          reasoning += data;
        } else if (line.includes('event: output')) {
          const data = lines[lines.indexOf(line) + 1]?.slice(6) || '';
          output += data;
        }
      }

      setMessages(prev => {
        const updated = [...prev];
        updated[updated.length - 1].reasoning = reasoning;
        updated[updated.length - 1].content = output;
        return updated;
      });
    }

    setMessages(prev => {
      const updated = [...prev];
      updated[updated.length - 1].isStreaming = false;
      return updated;
    });
  };

  const handleFileUpload = async (e) => {
    const file = e.target.files?.[0];
    if (!file) return;

    const formData = new FormData();
    formData.append('file', file);

    try {
      setLoading(true);
      const response = await fetch(`${API_URL}/upload`, {
        method: 'POST',
        body: formData,
      });

      const data = await response.json();
      setUploadedFile(file.name);
      setVectorStoreId(data.message.includes('ID:') ? data.message.split('ID: ')[1].split(')')[0] : null);
      setMessages(prev => [
        ...prev,
        { role: 'assistant', content: data.message, isSystem: true },
      ]);
    } catch (error) {
      setMessages(prev => [
        ...prev,
        { role: 'assistant', content: `Upload error: ${error.message}`, isError: true },
      ]);
    } finally {
      setLoading(false);
    }
  };

  const copyToClipboard = (text, id) => {
    navigator.clipboard.writeText(text);
    setCopiedId(id);
    setTimeout(() => setCopiedId(null), 2000);
  };

  return (
    <div className="flex h-screen bg-gradient-to-br from-slate-950 via-slate-900 to-slate-950 text-white">
      {/* Sidebar */}
      <div className={`${menuOpen ? 'w-64' : 'w-0 md:w-64'} transition-all duration-300 bg-slate-900 border-r border-slate-800 flex flex-col p-4 overflow-hidden`}>
        <div className="flex items-center gap-2 mb-8">
          <Brain className="w-6 h-6 text-blue-500" />
          <span className="font-bold text-lg hidden md:inline">AI Labs</span>
        </div>

        <nav className="space-y-2 flex-1">
          {[
            { id: 'chat', label: 'Chat', icon: Send },
            { id: 'reasoning', label: 'Reasoning', icon: Zap },
            { id: 'search', label: 'Document Search', icon: Search },
          ].map(({ id, label, icon: Icon }) => (
            <button
              key={id}
              onClick={() => {
                setActiveTab(id);
                setMenuOpen(false);
              }}
              className={`w-full flex items-center gap-3 px-4 py-3 rounded-lg transition-all ${
                activeTab === id
                  ? 'bg-blue-600 text-white'
                  : 'text-slate-400 hover:bg-slate-800'
              }`}
            >
              <Icon className="w-5 h-5" />
              <span className="hidden md:inline">{label}</span>
            </button>
          ))}
        </nav>

        <div className="space-y-2 pt-4 border-t border-slate-800">
          <div className="text-xs font-semibold text-slate-500 px-4 py-2">Settings</div>
          {activeTab === 'chat' && (
            <>
              <label className="flex items-center gap-3 px-4 py-2 text-sm cursor-pointer hover:bg-slate-800 rounded-lg transition-colors">
                <input
                  type="checkbox"
                  checked={streamMode}
                  onChange={(e) => setStreamMode(e.target.checked)}
                  className="rounded"
                />
                <span>Stream Mode</span>
              </label>
              <select
                value={aiModel}
                onChange={(e) => setAiModel(e.target.value)}
                className="w-full px-3 py-2 bg-slate-800 border border-slate-700 rounded-lg text-sm text-white hover:border-blue-500 transition-colors"
              >
                <option value="openai">OpenAI</option>
                <option value="gemini">Gemini</option>
                <option value="ollama">Ollama</option>
              </select>
            </>
          )}
        </div>
      </div>

      {/* Main Content */}
      <div className="flex-1 flex flex-col">
        {/* Header */}
        <div className="bg-slate-900 border-b border-slate-800 p-4 flex items-center justify-between">
          <button
            onClick={() => setMenuOpen(!menuOpen)}
            className="md:hidden p-2 hover:bg-slate-800 rounded-lg"
          >
            {menuOpen ? <X /> : <Menu />}
          </button>
          <div className="text-center flex-1">
            <h1 className="text-xl font-bold">
              {activeTab === 'chat' && 'AI Chat'}
              {activeTab === 'reasoning' && 'Extended Reasoning'}
              {activeTab === 'search' && 'Document Search'}
            </h1>
          </div>
          <Settings className="w-5 h-5 text-slate-500" />
        </div>

        {/* Messages Area */}
        <div className="flex-1 overflow-y-auto p-4 space-y-4">
          {messages.length === 0 ? (
            <div className="h-full flex items-center justify-center text-center">
              <div>
                <Brain className="w-16 h-16 text-blue-500 mx-auto mb-4 opacity-50" />
                <p className="text-slate-400 text-lg">Start a conversation</p>
              </div>
            </div>
          ) : (
            messages.map((msg, idx) => (
              <div
                key={idx}
                className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
              >
                <div
                  className={`max-w-2xl px-4 py-3 rounded-lg transition-all ${
                    msg.role === 'user'
                      ? 'bg-blue-600 text-white rounded-br-none'
                      : msg.isError
                      ? 'bg-red-900 text-red-100 rounded-bl-none'
                      : 'bg-slate-800 text-slate-100 rounded-bl-none'
                  }`}
                >
                  {msg.reasoning && (
                    <div className="mb-3 pb-3 border-b border-slate-600">
                      <p className="text-xs font-semibold text-slate-400 mb-2">Reasoning:</p>
                      <p className="text-sm text-slate-300">{msg.reasoning}</p>
                    </div>
                  )}
                  <p className="break-words">{msg.content}</p>
                  {msg.role === 'assistant' && !msg.isError && (
                    <button
                      onClick={() => copyToClipboard(msg.content, idx)}
                      className="mt-2 text-xs text-slate-400 hover:text-slate-200 flex items-center gap-1"
                    >
                      {copiedId === idx ? (
                        <>
                          <Check className="w-4 h-4" />
                          Copied
                        </>
                      ) : (
                        <>
                          <Copy className="w-4 h-4" />
                          Copy
                        </>
                      )}
                    </button>
                  )}
                </div>
              </div>
            ))
          )}
          <div ref={messagesEndRef} />
        </div>

        {/* Input Area */}
        <div className="bg-slate-900 border-t border-slate-800 p-4">
          {activeTab === 'search' && !uploadedFile && (
            <button
              onClick={() => fileInputRef.current?.click()}
              className="w-full mb-4 flex items-center justify-center gap-2 px-4 py-3 bg-gradient-to-r from-blue-600 to-blue-500 hover:from-blue-700 hover:to-blue-600 rounded-lg transition-all"
            >
              <Upload className="w-5 h-5" />
              Upload Document
            </button>
          )}
          {uploadedFile && (
            <div className="mb-3 text-sm text-slate-400">
              📄 {uploadedFile}
            </div>
          )}
          <div className="flex gap-3">
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && !loading && sendMessage()}
              placeholder="Type your message..."
              className="flex-1 bg-slate-800 border border-slate-700 rounded-lg px-4 py-3 text-white placeholder-slate-500 focus:outline-none focus:border-blue-500 transition-colors"
            />
            <button
              onClick={sendMessage}
              disabled={loading || !input.trim()}
              className="bg-gradient-to-r from-blue-600 to-blue-500 hover:from-blue-700 hover:to-blue-600 disabled:opacity-50 disabled:cursor-not-allowed px-6 py-3 rounded-lg transition-all flex items-center gap-2"
            >
              {loading ? <Loader className="w-5 h-5 animate-spin" /> : <Send className="w-5 h-5" />}
            </button>
          </div>
        </div>
      </div>

      <input
        ref={fileInputRef}
        type="file"
        onChange={handleFileUpload}
        className="hidden"
        accept=".pdf,.txt,.doc,.docx"
      />
    </div>
  );
};

export default AIApp;