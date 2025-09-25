import React, { useState, useEffect } from 'react';
import Sidebar from './components/Sidebar';
import Header from './components/Header';
import Dashboard from './components/Dashboard';
import PatientDataTable from './components/PatientDataTable';
import ReportGeneration from './components/ReportGeneration';
import { NAV_LINKS } from './constants';
import Notification from './components/Notification';
import LoginPage from './components/LoginPage';

const App: React.FC = () => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [isSidebarOpen, setSidebarOpen] = useState(false);
  const [activeView, setActiveView] = useState('Dashboard');
  const [voiceStatus, setVoiceStatus] = useState<string | null>(null);
  const [isListening, setIsListening] = useState(false);
  const [recognizedCommand, setRecognizedCommand] = useState<string | null>(null);

  const handleLogin = () => {
    setIsAuthenticated(true);
  };

  const handleLogout = () => {
    setIsAuthenticated(false);
    setActiveView('Dashboard'); // Reset to default view on logout
  };

  // Simulate voice command processing
  const handleVoiceCommand = () => {
    if (isListening) {
      setIsListening(false);
      setVoiceStatus('Voice command cancelled.');
      setTimeout(() => setVoiceStatus(null), 3000);
      return;
    }

    setIsListening(true);
    setVoiceStatus('Listening...');
    setRecognizedCommand(null); // Clear previous command
    
    // Context-aware commands
    const commands = activeView === 'Report Generation' 
      ? [
          "Set patient to Priya Sharma",
          "Chief complaint is persistent headaches",
          "Add to findings: Patient shows positive response to Panchakarma therapy.",
          "Set report type to Monthly Summary",
        ]
      : [
          "Search for Priya Sharma",
          "Show appointments for today",
          "Look up ICD code for Migraine",
        ];
    
    const commandToRecognize = commands[Math.floor(Math.random() * commands.length)];

    setTimeout(() => {
      setVoiceStatus(`Recognized: "${commandToRecognize}"`);
      setRecognizedCommand(commandToRecognize);
    }, 2500);

    setTimeout(() => {
      setIsListening(false);
      setVoiceStatus(null);
    }, 5000);
  };

  const renderActiveView = () => {
    switch (activeView) {
      case 'Dashboard':
        return (
          <>
            <Dashboard />
            <div className="mt-8">
              <PatientDataTable />
            </div>
          </>
        );
      case 'Report Generation':
        return <ReportGeneration recognizedCommand={recognizedCommand} />;
      default:
        return (
          <div className="flex items-center justify-center h-full">
            <div className="text-center p-8 bg-white rounded-lg shadow-md">
              <h2 className="text-2xl font-bold text-slate-700">{activeView}</h2>
              <p className="mt-2 text-slate-500">This section is under development.</p>
            </div>
          </div>
        );
    }
  };

  const currentPage = NAV_LINKS.flatMap(section => section.links).find(link => link.name === activeView);
  const pageTitle = currentPage ? currentPage.name : 'Dashboard';

  if (!isAuthenticated) {
    return <LoginPage onLogin={handleLogin} />;
  }

  return (
    <div className="flex h-screen bg-slate-50">
      <Sidebar 
        isSidebarOpen={isSidebarOpen} 
        setSidebarOpen={setSidebarOpen} 
        activeView={activeView} 
        setActiveView={setActiveView}
        onLogout={handleLogout}
      />

      <div className="flex-1 flex flex-col overflow-hidden">
        <Header 
          pageTitle={pageTitle} 
          onMenuClick={() => setSidebarOpen(true)}
          isListening={isListening}
          onVoiceCommand={handleVoiceCommand}
        />
        
        <main className="flex-1 overflow-x-hidden overflow-y-auto bg-slate-50 p-6">
          {renderActiveView()}
        </main>
      </div>
      
      {voiceStatus && <Notification message={voiceStatus} />}
    </div>
  );
};

export default App;