
import React from 'react';
import { StatCardData } from '../types';
import { ArrowUpIcon, ArrowDownIcon } from './icons/HeroIcons';

interface StatCardProps {
  stat: StatCardData;
}

const StatCard: React.FC<StatCardProps> = ({ stat }) => {
  const Icon = stat.icon;
  const isPositive = stat.isPositive;

  return (
    <div className="bg-white p-5 rounded-xl shadow-sm hover:shadow-lg transition-shadow duration-300 border border-slate-100">
      <div className="flex items-center justify-between">
        <div className="p-2.5 bg-blue-100 rounded-lg">
          <Icon className="w-6 h-6 text-blue-500" />
        </div>
        <div
          className={`flex items-center text-sm font-semibold ${
            isPositive ? 'text-green-500' : 'text-red-500'
          }`}
        >
          {isPositive ? (
            <ArrowUpIcon className="w-4 h-4" />
          ) : (
            <ArrowDownIcon className="w-4 h-4" />
          )}
          <span>{stat.change}</span>
        </div>
      </div>
      <div className="mt-4">
        <h3 className="text-3xl font-bold text-slate-800">{stat.value}</h3>
        <p className="text-slate-500 font-medium">{stat.title}</p>
        <p className="text-sm text-slate-400 mt-1">{stat.description}</p>
      </div>
    </div>
  );
};

export default StatCard;
