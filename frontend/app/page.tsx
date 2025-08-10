'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import ChatInterface from '@/components/chat-interface';
import ConversationSidebar from '@/components/conversation-sidebar';
import { Button } from '@/components/ui/button';
import { LogOut, User } from 'lucide-react';
import { useConversationStore } from '@/lib/conversation-store';
import { useChatStore } from '@/lib/chat-store';

export default function HomePage() {
  const [user, setUser] = useState<{ user_id: number; username: string; emailaddress: string } | null>(null);
  const [loading, setLoading] = useState(true);
  const [refreshTrigger, setRefreshTrigger] = useState(0);
  const router = useRouter();

  // Zustand stores
  const { currentConversationId, setCurrentConversation, clearMessages } = useChatStore();
  const { refreshConversations } = useConversationStore();

  useEffect(() => {
    // Check if user is logged in
    const userData = localStorage.getItem('user');
    if (userData) {
      setUser(JSON.parse(userData));
    } else {
      router.push('/login');
    }
    setLoading(false);
  }, [router]);

  const handleLogout = () => {
    localStorage.removeItem('user');
    localStorage.removeItem('access_token');
    // Clear all conversation histories
    Object.keys(localStorage).forEach(key => {
      if (key.startsWith('chatHistory-')) {
        localStorage.removeItem(key);
      }
    });
    router.push('/login');
  };

  const handleSelectConversation = (conversationId: number | null) => {
    console.log('Page: Selecting conversation:', conversationId);
    setCurrentConversation(conversationId);
  };

  const handleNewConversation = () => {
    setCurrentConversation(null);
    clearMessages();
  };

  const handleConversationCreated = (conversationId: number) => {
    setCurrentConversation(conversationId);
    setRefreshTrigger(prev => prev + 1); // Trigger refresh
    refreshConversations(); // Also refresh store
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  if (!user) {
    return null;
  }

  return (
    <div className="flex h-screen bg-gray-50">
      {/* Sidebar */}
      <ConversationSidebar
        currentConversationId={currentConversationId}
        onSelectConversation={handleSelectConversation}
        onNewConversation={handleNewConversation}
        refreshTrigger={refreshTrigger}
      />

      {/* Main Content */}
      <div className="flex-1 flex flex-col">
        {/* Header */}
        <header className="bg-white border-b border-gray-200 px-4 py-3">
          <div className="flex items-center justify-between max-w-6xl mx-auto">
            <div className="flex items-center space-x-3">
              <div className="w-8 h-8 bg-blue-600 rounded-lg flex items-center justify-center">
                <span className="text-white font-bold text-sm">AI</span>
              </div>
              <h1 className="text-xl font-semibold text-gray-900">Healthcare Chatbot</h1>
            </div>
            
            <div className="flex items-center space-x-4">
              <div className="flex items-center space-x-2 text-sm text-gray-600">
                <User className="w-4 h-4" />
                <span>{user.username}</span>
              </div>
              <Button
                variant="outline"
                size="sm"
                onClick={handleLogout}
                className="flex items-center space-x-2"
              >
                <LogOut className="w-4 h-4" />
                <span>Logout</span>
              </Button>
            </div>
          </div>
        </header>

        {/* Chat Interface */}
        <main className="flex-1 overflow-hidden">
          <ChatInterface 
            user={user} 
            conversationId={currentConversationId}
            onConversationCreated={handleConversationCreated}
          />
        </main>
      </div>
    </div>
  );
}
