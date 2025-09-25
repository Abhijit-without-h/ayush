
import React from 'react';

export enum PatientStatus {
  Pending = 'Pending',
  InTreatment = 'In Treatment',
  Complete = 'Complete',
  Partial = 'Partial',
}

export enum TreatmentType {
  Panchakarma = 'Panchakarma',
  Modern = 'Modern',
  Combined = 'Combined',
  Ayurvedic = 'Ayurvedic',
  YogaHomeopathy = 'Yoga + Homeopathy',
}

export interface Patient {
  id: string;
  name: string;
  diagnosis: string;
  ayushDiagnosis: string;
  treatmentType: TreatmentType;
  icd11Code: string;
  status: PatientStatus;
  progress: number;
  lastVisit: string;
  avatar: string;
}

export interface NavLink {
    name: string;
    icon: React.FC<React.SVGProps<SVGSVGElement>>;
}

export interface NavSection {
    title: string;
    links: NavLink[];
}

export interface StatCardData {
  title: string;
  value: string;
  change: string;
  isPositive: boolean;
  icon: React.FC<React.SVGProps<SVGSVGElement>>;
  description: string;
}
