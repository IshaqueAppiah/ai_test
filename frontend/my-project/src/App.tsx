import './App.css'
import React, { useState, useRef, useEffect } from 'react';
import { Send, Upload, Zap, Brain, Search, Menu, X, Loader, Copy, Check, Trash2 } from 'lucide-react';

type Message = {
  role: string;
  content: string;
  isError?: boolean;
  isSystem?: boolean;
  isStreaming?: boolean;
  reasoning?: string;
  model?: string;
};

function App() {
  const [activeTab, setActiveTab] = useState<string>('chat');
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState<string>('');
  const [loading, setLoading] = useState<boolean>(false);
  const [aiModel, setAiModel] = useState<string>('openai');
  const [streamMode, setStreamMode] = useState<boolean>(false);
  const [uploadedFile, setUploadedFile] = useState<string | null>(null);
  const [vectorStoreId, setVectorStoreId] = useState<string | null>(null);
  const [menuOpen, setMenuOpen] = useState<boolean>(false);
  const [copiedId, setCopiedId] = useState<number | null>(null);
  const [temperature, setTemperature] = useState<number>(0.7);
  const [topK, setTopK] = useState<number>(5);
  const messagesEndRef = useRef<HTMLDivElement | null>(null);
  const fileInputRef = useRef<HTMLInputElement | null>(null);
  const API_URL = 'http://localhost:8000';
    const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

    useEffect(() => {
      scrollToBottom();
    }, [messages]);

      const buildPayload = (): Record<string, unknown> => {
    const payload: Record<string, unknown> = {
      message: input.trim(),
    };

    if (activeTab === 'chat' && aiModel === 'ollama') {
      return {
        message: input.trim(),
      };
    }

    if (activeTab === 'search') {
      return {
        message: input.trim(),
        top_k: topK,
      };
    }

    payload.model = aiModel;
    return payload;
  };

  const sendMessage = async () => {
    if (!input.trim()) return;
    if (activeTab === 'search' && !vectorStoreId) {
      alert('Please upload a document first');
      return;
    }

    const userMessage = { role: 'user', content: input };
    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setLoading(true);

    try {
      let endpoint = '/chat';
      const payload = buildPayload();

      if (activeTab === 'chat') {
        if (aiModel === 'gemini') {
          endpoint = '/chat/chat_with_gemini';
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
        await handleStreamResponse(endpoint, payload);
      } else if (activeTab === 'reasoning') {
        await handleReasoningStream(endpoint, payload);
      } else {
        const response = await fetch(`${API_URL}${endpoint}`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload),
        });

        if (!response.ok) {
          const error = await response.json();
          throw new Error(error.detail || error.error || 'Failed to get response');
        }

        const data = await response.json();
        const assistantMessage = {
          role: 'assistant',
          content: data.response || data.content || JSON.stringify(data),
          model: data.model,
        };
        setMessages(prev => [...prev, assistantMessage]);
      }
    } catch (error) {
      const errorMessage = {
        role: 'assistant',
        content: `Error: ${error instanceof Error ? error.message : String(error)}`,
        isError: true,
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setLoading(false);
    }
  };

  const handleStreamResponse = async (endpoint: string, payload: Record<string, unknown>): Promise<void> => {
    const response = await fetch(`${API_URL}${endpoint}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });

    if (!response.ok) throw new Error('Failed to stream response');

    const reader = response?.body?.getReader();
    const decoder = new TextDecoder();
    let fullResponse = '';

    setMessages(prev => [
      ...prev,
      { role: 'assistant', content: '', isStreaming: true },
    ]);

    if (!reader) {
      throw new Error('Failed to get stream reader');
    }

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

  const handleReasoningStream = async (endpoint: string, payload: Record<string, unknown>): Promise<void> => {
    const response = await fetch(`${API_URL}${endpoint}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });

    if (!response.ok) throw new Error('Failed to stream response');

    const reader = response?.body?.getReader();
    const decoder = new TextDecoder();
    let reasoning = '';
    let output = '';

    setMessages(prev => [
      ...prev,
      { role: 'assistant', content: '', reasoning: '', isStreaming: true },
    ]);

    while (true) {
      const { done, value } = await reader!.read();
      if (done) break;

      const chunk = decoder.decode(value);
      const lines = chunk.split('\n');

      for (let i = 0; i < lines.length; i++) {
        if (lines[i].includes('event: reasoning')) {
          const data = lines[i + 1]?.slice(6) || '';
          reasoning += data;
        } else if (lines[i].includes('event: output')) {
          const data = lines[i + 1]?.slice(6) || '';
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

  const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>): Promise<void> => {
    const file = e.target.files?.[0] ?? null;
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
      
      const idMatch = data.message.match(/ID: ([^)]+)/);
      if (idMatch) {
        setVectorStoreId(idMatch[1]);
      }

      setMessages(prev => [
        ...prev,
        { role: 'assistant', content: data.message, isSystem: true },
      ]);
    } catch (error) {
      const errorMsg = error instanceof Error ? error.message : String(error);
      setMessages(prev => [
        ...prev,
        { role: 'assistant', content: `Upload error: ${errorMsg}`, isError: true },
      ]);
    } finally {
      setLoading(false);
    }
  };

  const copyToClipboard = (text: string, id: number | null): void => {
    if (navigator?.clipboard?.writeText) {
      navigator.clipboard.writeText(text).catch(() => {});
    }
    setCopiedId(typeof id === 'number' ? id : null);
    setTimeout(() => setCopiedId(null), 2000);
  };

  const clearChat = () => {
    setMessages([]);
    setInput('');
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

        <div className="space-y-3 pt-4 border-t border-slate-800">
          <div className="text-xs font-semibold text-slate-500 px-4">Settings</div>

          {activeTab === 'chat' && (
            <>
              <label className="flex items-center gap-3 px-4 py-2 text-sm cursor-pointer hover:bg-slate-800 rounded-lg transition-colors">
                <input
                  type="checkbox"
                  checked={streamMode && aiModel === 'openai'}
                  onChange={(e) => setStreamMode(e.target.checked)}
                  disabled={aiModel !== 'openai'}
                  className="rounded disabled:opacity-50"
                />
                <span>Stream Mode</span>
              </label>
              <div className="px-4">
                <label className="text-xs text-slate-400 mb-2 block">Model</label>
                <select
                  value={aiModel}
                  onChange={(e) => setAiModel(e.target.value)}
                  className="w-full px-3 py-2 bg-slate-800 border border-slate-700 rounded-lg text-sm text-white hover:border-blue-500 transition-colors"
                >
                  <option value="openai">OpenAI</option>
                  <option value="gemini">Gemini</option>
                  <option value="ollama">Ollama</option>
                </select>
              </div>

              {aiModel === 'ollama' && (
                <div className="px-4">
                  <label className="text-xs text-slate-400 mb-2 block">Temperature: {temperature.toFixed(1)}</label>
                  <input
                    type="range"
                    min="0"
                    max="2"
                    step="0.1"
                    value={temperature}
                    onChange={(e) => setTemperature(parseFloat(e.target.value))}
                    className="w-full"
                  />
                </div>
              )}
            </>
          )}

          {activeTab === 'search' && (
            <div className="px-4">
              <label className="text-xs text-slate-400 mb-2 block">Top K Results: {topK}</label>
              <input
                type="range"
                min="1"
                max="50"
                step="1"
                value={topK}
                onChange={(e) => setTopK(parseInt(e.target.value))}
                className="w-full"
              />
            </div>
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
              {activeTab === 'chat' && `AI Chat - ${aiModel.toUpperCase()}`}
              {activeTab === 'reasoning' && 'Extended Reasoning'}
              {activeTab === 'search' && 'Document Search'}
            </h1>
          </div>
          <button
            onClick={clearChat}
            className="p-2 hover:bg-slate-800 rounded-lg transition-colors"
            title="Clear chat"
          >
            <Trash2 className="w-5 h-5" />
          </button>
        </div>

        {/* Messages Area */}
        <div className="flex-1 overflow-y-auto p-4 space-y-4">
          {messages.length === 0 ? (
            <div className="h-full flex items-center justify-center text-center">
              <div>
                <Brain className="w-16 h-16 text-blue-500 mx-auto mb-4 opacity-50" />
                <p className="text-slate-400 text-lg">Start a conversation</p>
                <p className="text-slate-500 text-sm mt-2">
                  {activeTab === 'search' && uploadedFile === null && 'Upload a document to get started'}
                  {activeTab === 'search' && uploadedFile && 'Ask questions about your document'}
                  {activeTab !== 'search' && 'Type a message below'}
                </p>
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
                      : msg.isSystem
                      ? 'bg-slate-700 text-slate-100 rounded-bl-none'
                      : 'bg-slate-800 text-slate-100 rounded-bl-none'
                  }`}
                >
                  {msg.reasoning && (
                    <div className="mb-3 pb-3 border-b border-slate-600">
                      <p className="text-xs font-semibold text-slate-400 mb-2">Reasoning:</p>
                      <p className="text-sm text-slate-300">{msg.reasoning}</p>
                    </div>
                  )}
                  <p className="break-words whitespace-pre-wrap">{msg.content}</p>
                  {msg.model && (
                    <p className="text-xs text-slate-500 mt-2">Model: {msg.model}</p>
                  )}
                  {msg.role === 'assistant' && !msg.isError && (
                    <button
                      onClick={() => copyToClipboard(msg.content, idx)}
                      className="mt-2 text-xs text-slate-400 hover:text-slate-200 flex items-center gap-1 transition-colors"
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
              className="w-full mb-4 flex items-center justify-center gap-2 px-4 py-3 bg-gradient-to-r from-blue-600 to-blue-500 hover:from-blue-700 hover:to-blue-600 rounded-lg transition-all font-medium"
            >
              <Upload className="w-5 h-5" />
              Upload Document
            </button>
          )}
          {uploadedFile && (
            <div className="mb-3 flex items-center justify-between bg-slate-800 px-3 py-2 rounded-lg">
              <span className="text-sm text-slate-300">📄 {uploadedFile}</span>
              <button
                onClick={() => {
                  setUploadedFile(null);
                  setVectorStoreId(null);
                  setMessages([]);
                }}
                className="text-xs text-slate-400 hover:text-red-400 transition-colors"
              >
                Change
              </button>
            </div>
          )}
          <div className="flex gap-3">
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && !loading && sendMessage()}
              placeholder="Type your message..."
              className="flex-1 bg-slate-800 border border-slate-700 rounded-lg px-4 py-3 text-white placeholder-slate-500 focus:outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20 transition-all"
            />
            <button
              onClick={sendMessage}
              disabled={loading || !input.trim() || (activeTab === 'search' && !vectorStoreId)}
              className="bg-gradient-to-r from-blue-600 to-blue-500 hover:from-blue-700 hover:to-blue-600 disabled:opacity-50 disabled:cursor-not-allowed px-6 py-3 rounded-lg transition-all flex items-center gap-2 font-medium"
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
}

export default App
