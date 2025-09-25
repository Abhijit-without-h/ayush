
import React from 'react';
import { Bars3Icon, ChevronLeftIcon, MagnifyingGlassIcon, MicrophoneIcon } from './icons/HeroIcons';

interface HeaderProps {
  pageTitle: string;
  onMenuClick: () => void;
  isListening: boolean;
  onVoiceCommand: () => void;
}

const Header: React.FC<HeaderProps> = ({ pageTitle, onMenuClick, isListening, onVoiceCommand }) => {
  return (
    <header className="flex-shrink-0 bg-white h-16 flex items-center justify-between px-6 border-b border-slate-200">
      {/* Left side */}
      <div className="flex items-center">
        <button onClick={onMenuClick} className="lg:hidden text-slate-500 mr-4">
          <Bars3Icon className="w-6 h-6" />
        </button>
        <button className="hidden sm:block text-slate-400 hover:text-slate-600">
            <ChevronLeftIcon className="w-6 h-6" />
        </button>
        <h1 className="text-xl font-bold text-slate-800 ml-2">{pageTitle}</h1>
      </div>

      {/* Center: Search and Voice */}
      <div className="flex-1 flex justify-center px-4 lg:px-8">
        <div className="w-full max-w-lg relative">
          <MagnifyingGlassIcon className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-400" />
          <input
            type="text"
            placeholder="Search patients, ICD-11 codes, AYUSH terms..."
            className="w-full pl-10 pr-12 py-2 border border-slate-300 rounded-full bg-slate-50 focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
          <button
            onClick={onVoiceCommand}
            className={`absolute right-1 top-1/2 -translate-y-1/2 p-2 rounded-full transition-colors duration-200 ${
              isListening
                ? 'bg-green-500 text-white pulse-animation'
                : 'bg-red-500 text-white hover:bg-red-600'
            }`}
          >
            <MicrophoneIcon className="w-5 h-5" />
          </button>
        </div>
      </div>

      {/* Right side: User Profile */}
      <div className="flex items-center">
        <div className="relative">
          <button className="flex items-center space-x-2">
            <img
              className="w-10 h-10 rounded-full"
              src="https://picsum.photos/seed/doctor/100/100"
              alt="User Avatar"
            />
            <div className="hidden md:block text-left">
              <div className="font-semibold text-slate-800">Dr. Aranya Sharma</div>
              <div className="text-sm text-slate-500">Ayurveda Specialist</div>
            </div>
          </button>
        </div>
      </div>
    </header>
  );
};

export default Header;
