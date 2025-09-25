
import React from 'react';
import { DASHBOARD_STATS } from '../constants';
import StatCard from './StatCard';

const Dashboard: React.FC = () => {
  return (
    <div>
      <h2 className="text-2xl font-bold text-slate-800 mb-4">Clinic Overview</h2>
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
        {DASHBOARD_STATS.map((stat, index) => (
          <StatCard key={index} stat={stat} />
        ))}
      </div>
    </div>
  );
};

export default Dashboard;
