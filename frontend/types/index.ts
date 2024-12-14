import { LucideIcon } from 'lucide-react';

export interface Service {
  icon: LucideIcon;
  title: string;
  description: string;
  slug: string;
}

export interface NavItem {
  label: string;
  href: string;
}