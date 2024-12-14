import { FileSearch, Users, BarChart2, Calendar } from 'lucide-react';
import type { Service } from '../types';

export const services: Service[] = [
  {
    icon: FileSearch,
    title: 'Market Research Snapshots',
    description: 'Comprehensive market analysis with actionable insights for your business growth.',
    slug: 'market-research',
  },
  {
    icon: Users,
    title: 'Customer Persona Development',
    description: 'Detailed buyer personas to help you understand and target your ideal customers.',
    slug: 'customer-personas',
  },
  {
    icon: BarChart2,
    title: 'Competitive Analysis Reports',
    description: 'In-depth analysis of your competitors and market positioning strategies.',
    slug: 'competitive-analysis',
  },
  {
    icon: Calendar,
    title: 'Social Media Content Calendars',
    description: 'Strategic content planning and scheduling for maximum social media impact.',
    slug: 'content-calendars',
  },
];