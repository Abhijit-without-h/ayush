import React, { useState, useEffect } from 'react';
import { SAMPLE_PATIENTS } from '../constants';
import { DocumentArrowDownIcon } from './icons/HeroIcons';
import ConfirmationDialog from './ConfirmationDialog';

// Explicitly declare jsPDF types for window object
declare global {
  interface Window {
    jspdf: any;
  }
}

interface ReportGenerationProps {
  recognizedCommand: string | null;
}

const ReportGeneration: React.FC<ReportGenerationProps> = ({ recognizedCommand }) => {
  const [formData, setFormData] = useState({
    patientId: '',
    reportType: 'Monthly Summary',
    startDate: new Date().toISOString().split('T')[0],
    endDate: new Date().toISOString().split('T')[0],
    chiefComplaint: '',
    findings: '',
    diagnosis: '',
    treatmentPlan: ''
  });
  const [showConfirmDialog, setShowConfirmDialog] = useState(false);

  useEffect(() => {
    if (!recognizedCommand) return;

    const command = recognizedCommand.toLowerCase();

    // Helper to extract value after a keyword
    const extractValue = (keyword: string) => {
        const regex = new RegExp(`${keyword}\\s+(.*)`, 'i');
        const match = command.match(regex);
        return match ? match[1].trim() : null;
    };
    
    if (command.startsWith('set patient to')) {
        const patientName = extractValue('set patient to');
        const patient = SAMPLE_PATIENTS.find(p => p.name.toLowerCase() === patientName);
        if (patient) {
            setFormData(prev => ({ ...prev, patientId: patient.id }));
        }
    } else if (command.startsWith('set report type to')) {
        const reportType = extractValue('set report type to');
        if (reportType) {
            const capitalizedType = reportType.charAt(0).toUpperCase() + reportType.slice(1);
            const validTypes = ['Monthly Summary', 'Lab Result Analysis', 'Treatment Progress'];
            if(validTypes.some(t => t.toLowerCase() === reportType)) {
                 setFormData(prev => ({ ...prev, reportType: capitalizedType }));
            }
        }
    } else if (command.startsWith('chief complaint is')) {
        const complaint = extractValue('chief complaint is');
        if(complaint) setFormData(prev => ({ ...prev, chiefComplaint: complaint }));
    } else if (command.startsWith('add to findings')) {
        const finding = extractValue('add to findings');
        if(finding) setFormData(prev => ({ ...prev, findings: prev.findings ? `${prev.findings}\n- ${finding}` : `- ${finding}` }));
    }

  }, [recognizedCommand]);


  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleGeneratePdf = () => {
    const { jsPDF } = window.jspdf;
    const doc = new jsPDF();
    const patient = SAMPLE_PATIENTS.find(p => p.id === formData.patientId);
    
    // Header
    doc.setFontSize(20);
    doc.setFont('helvetica', 'bold');
    doc.text('AYUSH Wellness Clinic - Medical Report', 105, 20, { align: 'center' });

    doc.setFontSize(12);
    doc.setFont('helvetica', 'normal');
    doc.text(`Date: ${new Date().toLocaleDateString()}`, 190, 30, { align: 'right' });
    doc.text(`Report Type: ${formData.reportType}`, 20, 30);
    doc.line(20, 35, 190, 35); // Horizontal line

    // Patient Info
    doc.setFontSize(14);
    doc.setFont('helvetica', 'bold');
    doc.text('Patient Information', 20, 45);
    doc.setFontSize(12);
    doc.setFont('helvetica', 'normal');
    
    if (patient) {
        (doc as any).autoTable({
            startY: 50,
            head: [['Patient ID', 'Name', 'Diagnosis', 'ICD-11 Code']],
            body: [[patient.id, patient.name, `${patient.diagnosis} (${patient.ayushDiagnosis})`, patient.icd11Code]],
            theme: 'striped',
            headStyles: { fillColor: [59, 130, 246] }
        });
    } else {
        doc.text('No patient selected.', 20, 55);
    }
    
    let finalY = (doc as any).lastAutoTable.finalY || 60;

    // Report Details
    const reportContent = [
        { title: 'Report Period', content: `${formData.startDate} to ${formData.endDate}` },
        { title: 'Chief Complaint', content: formData.chiefComplaint },
        { title: 'Clinical Findings / Observations', content: formData.findings },
        { title: 'Diagnosis', content: formData.diagnosis },
        { title: 'Treatment Plan', content: formData.treatmentPlan },
    ];
    
    reportContent.forEach(section => {
        if(section.content) {
            finalY += 15;
            doc.setFontSize(14);
            doc.setFont('helvetica', 'bold');
            doc.text(section.title, 20, finalY);
            finalY += 8;
            doc.setFontSize(12);
            doc.setFont('helvetica', 'normal');
            const splitText = doc.splitTextToSize(section.content, 170);
            doc.text(splitText, 20, finalY);
            finalY += (splitText.length * 5);
        }
    });


    // Footer
    const pageCount = doc.internal.getNumberOfPages();
    for (let i = 1; i <= pageCount; i++) {
      doc.setPage(i);
      doc.line(20, 280, 190, 280);
      doc.text(`Page ${i} of ${pageCount}`, 105, 287, { align: 'center' });
      doc.text('AYUSH EMR System | Confidential', 20, 287);
    }

    doc.save(`Medical_Report_${patient?.name.replace(' ', '_') || 'Generated'}.pdf`);
  };

  const handleConfirmGeneration = () => {
    handleGeneratePdf();
    setShowConfirmDialog(false);
  };

  return (
    <div className="bg-white p-8 rounded-xl shadow-sm border border-slate-100 max-w-4xl mx-auto">
      <h2 className="text-2xl font-bold text-slate-800 mb-6">Create New Report</h2>
      
      <form onSubmit={(e) => { e.preventDefault(); setShowConfirmDialog(true); }} className="space-y-6">
        {/* Section 1: Patient and Report Type */}
        <div className="p-5 border border-slate-200 rounded-lg">
          <h3 className="text-lg font-semibold text-slate-700 mb-4">Report Setup</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label htmlFor="patientId" className="block text-sm font-medium text-slate-600 mb-1">Patient</label>
              <select id="patientId" name="patientId" value={formData.patientId} onChange={handleInputChange} className="w-full p-2 border border-slate-300 rounded-md focus:ring-blue-500 focus:border-blue-500 bg-white text-slate-900">
                <option value="">Select a patient</option>
                {SAMPLE_PATIENTS.map(p => <option key={p.id} value={p.id}>{p.name} ({p.id})</option>)}
              </select>
            </div>
            <div>
              <label htmlFor="reportType" className="block text-sm font-medium text-slate-600 mb-1">Report Type</label>
              <select id="reportType" name="reportType" value={formData.reportType} onChange={handleInputChange} className="w-full p-2 border border-slate-300 rounded-md focus:ring-blue-500 focus:border-blue-500 bg-white text-slate-900">
                <option>Monthly Summary</option>
                <option>Lab Result Analysis</option>
                <option>Treatment Progress</option>
              </select>
            </div>
            <div>
              <label htmlFor="startDate" className="block text-sm font-medium text-slate-600 mb-1">Start Date</label>
              <input type="date" id="startDate" name="startDate" value={formData.startDate} onChange={handleInputChange} className="w-full p-2 border border-slate-300 rounded-md focus:ring-blue-500 focus:border-blue-500 bg-white text-slate-900" />
            </div>
            <div>
              <label htmlFor="endDate" className="block text-sm font-medium text-slate-600 mb-1">End Date</label>
              <input type="date" id="endDate" name="endDate" value={formData.endDate} onChange={handleInputChange} className="w-full p-2 border border-slate-300 rounded-md focus:ring-blue-500 focus:border-blue-500 bg-white text-slate-900" />
            </div>
          </div>
        </div>

        {/* Section 2: Clinical Details */}
         <div className="p-5 border border-slate-200 rounded-lg">
           <h3 className="text-lg font-semibold text-slate-700 mb-4">Clinical Details</h3>
           <div className="space-y-4">
              <div>
                <label htmlFor="chiefComplaint" className="block text-sm font-medium text-slate-600 mb-1">Chief Complaint</label>
                <textarea id="chiefComplaint" name="chiefComplaint" rows={2} value={formData.chiefComplaint} onChange={handleInputChange} className="w-full p-2 border border-slate-300 rounded-md focus:ring-blue-500 focus:border-blue-500 bg-white text-slate-900" placeholder="e.g., Persistent headaches, joint pain..."></textarea>
              </div>
              <div>
                <label htmlFor="findings" className="block text-sm font-medium text-slate-600 mb-1">Clinical Findings / Observations</label>
                <textarea id="findings" name="findings" rows={5} value={formData.findings} onChange={handleInputChange} className="w-full p-2 border border-slate-300 rounded-md focus:ring-blue-500 focus:border-blue-500 bg-white text-slate-900" placeholder="Enter detailed observations..."></textarea>
              </div>
               <div>
                <label htmlFor="diagnosis" className="block text-sm font-medium text-slate-600 mb-1">Diagnosis</label>
                <textarea id="diagnosis" name="diagnosis" rows={2} value={formData.diagnosis} onChange={handleInputChange} className="w-full p-2 border border-slate-300 rounded-md focus:ring-blue-500 focus:border-blue-500 bg-white text-slate-900" placeholder="e.g., Shirahshool (Migraine) - ICD-11: 8A80.1"></textarea>
              </div>
              <div>
                <label htmlFor="treatmentPlan" className="block text-sm font-medium text-slate-600 mb-1">Treatment Plan</label>
                <textarea id="treatmentPlan" name="treatmentPlan" rows={3} value={formData.treatmentPlan} onChange={handleInputChange} className="w-full p-2 border border-slate-300 rounded-md focus:ring-blue-500 focus:border-blue-500 bg-white text-slate-900" placeholder="e.g., Prescribed Panchakarma therapy, dietary changes..."></textarea>
              </div>
           </div>
        </div>

        <div className="flex justify-end pt-4">
          <button type="submit" className="inline-flex items-center px-6 py-3 border border-transparent text-base font-medium rounded-md shadow-sm text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition-colors">
            <DocumentArrowDownIcon className="w-5 h-5 mr-2" />
            Generate PDF
          </button>
        </div>
      </form>

      <ConfirmationDialog
        isOpen={showConfirmDialog}
        onClose={() => setShowConfirmDialog(false)}
        onConfirm={handleConfirmGeneration}
        title="Confirm Report Generation"
        message="Are you sure you want to generate the PDF report with the current data? Please review all fields before proceeding."
      />
    </div>
  );
};

export default ReportGeneration;