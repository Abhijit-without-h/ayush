
import React, { useEffect, useState } from 'react';
import { InformationCircleIcon, CheckCircleIcon } from './icons/HeroIcons';

interface NotificationProps {
  message: string;
}

const Notification: React.FC<NotificationProps> = ({ message }) => {
  const [visible, setVisible] = useState(false);

  useEffect(() => {
    if (message) {
      setVisible(true);
      const timer = setTimeout(() => {
        setVisible(false);
      }, 4500); // Notification will auto-hide
      return () => clearTimeout(timer);
    }
  }, [message]);

  const isListening = message === 'Listening...';

  return (
    <div
      className={`fixed top-5 right-5 z-50 flex items-center p-4 rounded-lg shadow-lg bg-white border-l-4 transition-transform duration-300 ease-in-out ${
        visible ? 'translate-x-0 opacity-100' : 'translate-x-full opacity-0'
      } ${
        isListening ? 'border-blue-500' : 'border-green-500'
      }`}
    >
      {isListening ? (
        <InformationCircleIcon className="w-6 h-6 text-blue-500 animate-spin" />
      ) : (
        <CheckCircleIcon className="w-6 h-6 text-green-500" />
      )}
      <p className="ml-3 font-medium text-slate-700">{message}</p>
    </div>
  );
};

export default Notification;
