import React from 'react';
import { NAV_LINKS } from '../constants';
import { NavSection } from '../types';
import { XMarkIcon, HeartIcon, ArrowLeftOnRectangleIcon } from './icons/HeroIcons';

interface SidebarProps {
  isSidebarOpen: boolean;
  setSidebarOpen: (isOpen: boolean) => void;
  activeView: string;
  setActiveView: (view: string) => void;
  onLogout: () => void;
}

const NavItem: React.FC<{ link: any; isActive: boolean; onClick: () => void }> = ({ link, isActive, onClick }) => {
  const Icon = link.icon;
  return (
    <li>
      <a
        href="#"
        onClick={(e) => {
          e.preventDefault();
          onClick();
        }}
        className={`flex items-center p-2 rounded-lg transition-colors duration-200 ${
          isActive
            ? 'bg-blue-500 text-white shadow-md'
            : 'text-slate-600 hover:bg-blue-100 hover:text-blue-600'
        }`}
      >
        <Icon className="w-6 h-6" />
        <span className="ml-3 font-medium">{link.name}</span>
      </a>
    </li>
  );
};

const Sidebar: React.FC<SidebarProps> = ({ isSidebarOpen, setSidebarOpen, activeView, setActiveView, onLogout }) => {
  const handleNavClick = (view: string) => {
    setActiveView(view);
    if (window.innerWidth < 1024) { // Close sidebar on mobile after click
        setSidebarOpen(false);
    }
  };
    
  const renderNavSection = (section: NavSection) => (
    <div key={section.title}>
      <h3 className="px-2 text-xs font-semibold text-slate-400 uppercase tracking-wider">
        {section.title}
      </h3>
      <ul className="mt-2 space-y-1">
        {section.links.map((link) => (
          <NavItem
            key={link.name}
            link={link}
            isActive={activeView === link.name}
            onClick={() => handleNavClick(link.name)}
          />
        ))}
      </ul>
    </div>
  );

  return (
    <>
      {/* Overlay for mobile */}
      <div
        className={`fixed inset-0 bg-black bg-opacity-50 z-20 lg:hidden transition-opacity ${
          isSidebarOpen ? 'opacity-100' : 'opacity-0 pointer-events-none'
        }`}
        onClick={() => setSidebarOpen(false)}
      ></div>

      {/* Sidebar */}
      <aside
        className={`fixed top-0 left-0 h-full w-64 bg-white border-r border-slate-200 z-30 transform transition-transform duration-300 ease-in-out lg:translate-x-0 lg:static lg:w-[260px] flex-shrink-0 ${
          isSidebarOpen ? 'translate-x-0' : '-translate-x-full'
        }`}
      >
        <div className="flex flex-col h-full">
          <div className="flex items-center justify-between px-4 h-16 border-b border-slate-200">
            <div className="flex items-center">
              <HeartIcon className="h-8 w-8 text-blue-500" />
              <span className="ml-2 text-xl font-bold text-slate-800">AYUSH EMR</span>
            </div>
            <button
              onClick={() => setSidebarOpen(false)}
              className="lg:hidden text-slate-500 hover:text-slate-800"
            >
              <XMarkIcon className="w-6 h-6" />
            </button>
          </div>

          <div className="px-4 py-4 border-b border-slate-200">
            <h4 className="font-bold text-slate-800">AYUSH Wellness Clinic</h4>
            <p className="text-sm text-slate-500">123 Health St, Svastha, IN</p>
          </div>

          <nav className="flex-1 px-4 py-4 space-y-6 overflow-y-auto">
            {NAV_LINKS.map(renderNavSection)}
          </nav>

          <div className="px-4 py-4 border-t border-slate-200">
            <a
              href="#"
              onClick={(e) => {
                  e.preventDefault();
                  onLogout();
              }}
              className="flex items-center p-2 rounded-lg text-slate-600 hover:bg-red-100 hover:text-red-600 transition-colors duration-200"
              >
              <ArrowLeftOnRectangleIcon className="w-6 h-6" />
              <span className="ml-3 font-medium">Logout</span>
            </a>
          </div>
        </div>
      </aside>
    </>
  );
};

export default Sidebar;