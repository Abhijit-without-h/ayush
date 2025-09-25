
import React, { useState } from 'react';
import { SAMPLE_PATIENTS } from '../constants';
import { Patient, PatientStatus } from '../types';

const TABS = ['Patient Records', 'Treatment Plans', 'AYUSH Protocols', 'ICD-11 Codes'];

const getStatusClasses = (status: PatientStatus): string => {
  switch (status) {
    case PatientStatus.Pending:
      return 'bg-yellow-100 text-yellow-800';
    case PatientStatus.InTreatment:
      return 'bg-blue-100 text-blue-800';
    case PatientStatus.Complete:
      return 'bg-green-100 text-green-800';
    case PatientStatus.Partial:
      return 'bg-orange-100 text-orange-800';
    default:
      return 'bg-slate-100 text-slate-800';
  }
};

const getProgressColor = (progress: number): string => {
  if (progress < 40) return 'bg-red-500';
  if (progress < 70) return 'bg-yellow-500';
  return 'bg-green-500';
};

const PatientRow: React.FC<{ patient: Patient }> = ({ patient }) => (
    <tr className="hover:bg-slate-100 transition-colors duration-200 border-b border-slate-200">
      <td className="p-4 whitespace-nowrap text-sm font-medium text-slate-800">{patient.id}</td>
      <td className="p-4 whitespace-nowrap">
        <div className="flex items-center">
          <img src={patient.avatar} alt={patient.name} className="w-8 h-8 rounded-full mr-3" />
          <span className="font-medium text-slate-800">{patient.name}</span>
        </div>
      </td>
      <td className="p-4 whitespace-nowrap text-sm text-slate-600">
        {patient.diagnosis} <span className="text-slate-400">({patient.ayushDiagnosis})</span>
      </td>
      <td className="p-4 whitespace-nowrap text-sm text-slate-600">{patient.treatmentType}</td>
      <td className="p-4 whitespace-nowrap text-sm font-mono text-slate-600">{patient.icd11Code}</td>
      <td className="p-4 whitespace-nowrap">
        <span className={`px-2.5 py-0.5 text-xs font-semibold rounded-full ${getStatusClasses(patient.status)}`}>
          {patient.status}
        </span>
      </td>
      <td className="p-4 whitespace-nowrap">
        <div className="flex items-center">
          <div className="w-24 bg-slate-200 rounded-full h-2 mr-2">
            <div className={`h-2 rounded-full ${getProgressColor(patient.progress)}`} style={{ width: `${patient.progress}%` }}></div>
          </div>
          <span className="text-sm font-medium text-slate-600">{patient.progress}%</span>
        </div>
      </td>
      <td className="p-4 whitespace-nowrap text-sm text-slate-600">{patient.lastVisit}</td>
      <td className="p-4 whitespace-nowrap text-right text-sm font-medium">
        <a href="#" className="text-blue-600 hover:text-blue-800">View Details</a>
      </td>
    </tr>
);


const PatientDataTable: React.FC = () => {
  const [activeTab, setActiveTab] = useState(TABS[0]);

  return (
    <div className="bg-white rounded-xl shadow-sm border border-slate-100 overflow-hidden">
      <div className="px-6 pt-4 border-b border-slate-200">
        <div className="flex items-center justify-between">
           <h3 className="text-lg font-bold text-slate-800">Medical Data</h3>
           <div className="flex space-x-4">
            {TABS.map((tab) => (
              <button
                key={tab}
                onClick={() => setActiveTab(tab)}
                className={`pb-2 text-sm font-medium transition-colors duration-200 border-b-2 ${
                  activeTab === tab
                    ? 'border-blue-500 text-blue-600'
                    : 'border-transparent text-slate-500 hover:text-slate-800'
                }`}
              >
                {tab}
              </button>
            ))}
          </div>
        </div>
      </div>
      
      <div className="overflow-x-auto">
        {activeTab === 'Patient Records' ? (
          <table className="min-w-full divide-y divide-slate-200">
            <thead className="bg-slate-50">
              <tr>
                <th scope="col" className="p-4 text-left text-xs font-semibold text-slate-500 uppercase tracking-wider">Patient ID</th>
                <th scope="col" className="p-4 text-left text-xs font-semibold text-slate-500 uppercase tracking-wider">Patient Name</th>
                <th scope="col" className="p-4 text-left text-xs font-semibold text-slate-500 uppercase tracking-wider">Diagnosis</th>
                <th scope="col" className="p-4 text-left text-xs font-semibold text-slate-500 uppercase tracking-wider">Treatment Type</th>
                <th scope="col" className="p-4 text-left text-xs font-semibold text-slate-500 uppercase tracking-wider">ICD-11</th>
                <th scope="col" className="p-4 text-left text-xs font-semibold text-slate-500 uppercase tracking-wider">Status</th>
                <th scope="col" className="p-4 text-left text-xs font-semibold text-slate-500 uppercase tracking-wider">Progress</th>
                <th scope="col" className="p-4 text-left text-xs font-semibold text-slate-500 uppercase tracking-wider">Last Visit</th>
                <th scope="col" className="relative p-4"><span className="sr-only">Actions</span></th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-slate-200">
              {SAMPLE_PATIENTS.map(patient => <PatientRow key={patient.id} patient={patient} />)}
            </tbody>
          </table>
        ) : (
          <div className="p-12 text-center text-slate-500">
            <h4 className="text-lg font-semibold text-slate-700">{activeTab}</h4>
            <p>Data for this section is not available yet.</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default PatientDataTable;
