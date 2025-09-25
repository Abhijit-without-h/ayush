
import { Patient, PatientStatus, TreatmentType, NavSection, StatCardData } from './types';
import { 
  ChartBarIcon, UserGroupIcon, DocumentTextIcon, CalendarIcon, BeakerIcon, Squares2X2Icon, Cog8ToothIcon, ArchiveBoxIcon, DocumentArrowDownIcon
} from './components/icons/HeroIcons';

export const NAV_LINKS: NavSection[] = [
  {
    title: 'Clinical',
    links: [
      { name: 'Dashboard', icon: Squares2X2Icon },
      { name: 'Patients', icon: UserGroupIcon },
      { name: 'Appointments', icon: CalendarIcon },
      { name: 'Medical Records', icon: DocumentTextIcon },
      { name: 'Prescriptions', icon: BeakerIcon },
    ],
  },
  {
    title: 'Management',
    links: [
      { name: 'Inventory', icon: ArchiveBoxIcon },
      { name: 'Billing', icon: ChartBarIcon },
      { name: 'Report Generation', icon: DocumentArrowDownIcon },
    ],
  },
  {
    title: 'Settings',
    links: [
      { name: 'System', icon: Cog8ToothIcon },
    ],
  },
];

export const SAMPLE_PATIENTS: Patient[] = [
  {
    id: '#PAT2024001',
    name: 'Rajesh Kumar',
    diagnosis: 'Chronic Back Pain',
    ayushDiagnosis: 'Kati Shoola',
    treatmentType: TreatmentType.Combined,
    icd11Code: 'MG30.02',
    status: PatientStatus.InTreatment,
    progress: 75,
    lastVisit: '2024-07-15',
    avatar: 'https://picsum.photos/seed/rajesh/40/40',
  },
  {
    id: '#PAT2024002',
    name: 'Priya Sharma',
    diagnosis: 'Migraine',
    ayushDiagnosis: 'Shirahshool',
    treatmentType: TreatmentType.Ayurvedic,
    icd11Code: '8A80.1',
    status: PatientStatus.Pending,
    progress: 10,
    lastVisit: '2024-07-18',
    avatar: 'https://picsum.photos/seed/priya/40/40',
  },
  {
    id: '#PAT2024003',
    name: 'Mohammad Ali',
    diagnosis: 'Diabetes',
    ayushDiagnosis: 'Prameha',
    treatmentType: TreatmentType.Combined,
    icd11Code: '5A11',
    status: PatientStatus.Complete,
    progress: 100,
    lastVisit: '2024-06-20',
    avatar: 'https://picsum.photos/seed/mohammad/40/40',
  },
  {
    id: '#PAT2024004',
    name: 'Sarah Johnson',
    diagnosis: 'Anxiety',
    ayushDiagnosis: 'Chittodvega',
    treatmentType: TreatmentType.YogaHomeopathy,
    icd11Code: '6B00',
    status: PatientStatus.InTreatment,
    progress: 50,
    lastVisit: '2024-07-12',
    avatar: 'https://picsum.photos/seed/sarah/40/40',
  },
  {
    id: '#PAT2024005',
    name: 'Anjali Singh',
    diagnosis: 'Arthritis',
    ayushDiagnosis: 'Amavata',
    treatmentType: TreatmentType.Panchakarma,
    icd11Code: 'FA20.0',
    status: PatientStatus.Partial,
    progress: 30,
    lastVisit: '2024-07-19',
    avatar: 'https://picsum.photos/seed/anjali/40/40',
  },
];

export const DASHBOARD_STATS: StatCardData[] = [
  {
    title: 'Total Patients',
    value: '1,284',
    change: '+12.5%',
    isPositive: true,
    icon: UserGroupIcon,
    description: 'Active medical records'
  },
  {
    title: "Today's Appointments",
    value: '36',
    change: '-5.2%',
    isPositive: false,
    icon: CalendarIcon,
    description: 'Scheduled consultations'
  },
  {
    title: 'Prescriptions (Monthly)',
    value: '452',
    change: '+8.1%',
    isPositive: true,
    icon: BeakerIcon,
    description: 'AYUSH vs Modern'
  },
  {
    title: 'Lab Results Pending',
    value: '14',
    change: '+2',
    isPositive: false,
    icon: DocumentTextIcon,
    description: 'Awaiting review'
  },
];