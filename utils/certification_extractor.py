import re
from typing import List, Dict, Set, Tuple
from datetime import datetime
import json

class CertificationExtractor:
    def __init__(self):
        # Comprehensive certification database
        self.certifications = {
            # Cloud Certifications
            'aws': {
                'AWS Certified Solutions Architect', 'AWS Certified Developer', 'AWS Certified SysOps Administrator',
                'AWS Certified DevOps Engineer', 'AWS Certified Security Specialist', 'AWS Certified Data Analytics',
                'AWS Certified Machine Learning', 'AWS Certified Database', 'AWS Certified Advanced Networking',
                'AWS Certified Cloud Practitioner', 'AWS Certified Solutions Architect Associate',
                'AWS Certified Solutions Architect Professional', 'AWS Certified Developer Associate',
                'AWS Certified SysOps Administrator Associate', 'AWS Certified DevOps Engineer Professional',
                'AWS Certified Security Specialty', 'AWS Certified Data Analytics Specialty',
                'AWS Certified Machine Learning Specialty', 'AWS Certified Database Specialty',
                'AWS Certified Advanced Networking Specialty', 'AWS Certified Cloud Practitioner'
            },
            'azure': {
                'Microsoft Azure Fundamentals', 'Microsoft Azure Administrator', 'Microsoft Azure Developer',
                'Microsoft Azure Solutions Architect', 'Microsoft Azure DevOps Engineer', 'Microsoft Azure Security Engineer',
                'Microsoft Azure Data Scientist', 'Microsoft Azure Data Engineer', 'Microsoft Azure AI Engineer',
                'Microsoft Azure Fundamentals (AZ-900)', 'Microsoft Azure Administrator (AZ-104)',
                'Microsoft Azure Developer (AZ-204)', 'Microsoft Azure Solutions Architect Expert (AZ-305)',
                'Microsoft Azure DevOps Engineer Expert (AZ-400)', 'Microsoft Azure Security Engineer (AZ-500)',
                'Microsoft Azure Data Scientist (DP-100)', 'Microsoft Azure Data Engineer (DP-203)',
                'Microsoft Azure AI Engineer (AI-102)'
            },
            'gcp': {
                'Google Cloud Certified Professional Cloud Architect', 'Google Cloud Certified Professional Data Engineer',
                'Google Cloud Certified Professional Machine Learning Engineer', 'Google Cloud Certified Professional Cloud Developer',
                'Google Cloud Certified Professional Cloud DevOps Engineer', 'Google Cloud Certified Professional Security Engineer',
                'Google Cloud Certified Professional Network Engineer', 'Google Cloud Certified Professional Collaboration Engineer',
                'Google Cloud Certified Associate Cloud Engineer', 'Google Cloud Certified Professional Cloud Architect',
                'Google Cloud Certified Professional Data Engineer', 'Google Cloud Certified Professional Machine Learning Engineer',
                'Google Cloud Certified Professional Cloud Developer', 'Google Cloud Certified Professional Cloud DevOps Engineer',
                'Google Cloud Certified Professional Security Engineer', 'Google Cloud Certified Professional Network Engineer',
                'Google Cloud Certified Professional Collaboration Engineer', 'Google Cloud Certified Associate Cloud Engineer'
            },
            
            # Programming & Development
            'programming': {
                'Oracle Certified Java Programmer', 'Oracle Certified Java Developer', 'Oracle Certified Java Architect',
                'Microsoft Certified Solutions Developer', 'Microsoft Certified Professional Developer',
                'Sun Certified Java Programmer', 'Sun Certified Java Developer', 'Sun Certified Java Architect',
                'Oracle Certified Associate Java SE', 'Oracle Certified Professional Java SE',
                'Oracle Certified Master Java SE', 'Oracle Certified Expert Java EE',
                'Microsoft Certified Azure Developer Associate', 'Microsoft Certified Azure Solutions Architect Expert',
                'Microsoft Certified DevOps Engineer Expert', 'Microsoft Certified Azure Security Engineer Associate',
                'Microsoft Certified Azure Data Engineer Associate', 'Microsoft Certified Azure AI Engineer Associate',
                'Microsoft Certified Azure Administrator Associate', 'Microsoft Certified Azure Fundamentals'
            },
            
            # Project Management
            'project_management': {
                'Project Management Professional', 'Certified Associate in Project Management',
                'Program Management Professional', 'Portfolio Management Professional',
                'Agile Certified Practitioner', 'Certified ScrumMaster', 'Certified Scrum Product Owner',
                'Certified Scrum Developer', 'Professional Scrum Master', 'Professional Scrum Product Owner',
                'Professional Scrum Developer', 'Scaled Agile Framework', 'SAFe Agilist', 'SAFe Product Owner',
                'SAFe Scrum Master', 'SAFe Advanced Scrum Master', 'SAFe Product Manager', 'SAFe Release Train Engineer',
                'SAFe Program Consultant', 'SAFe Architect', 'SAFe DevOps Practitioner', 'SAFe Agile Software Engineer',
                'PMP', 'CAPM', 'PgMP', 'PfMP', 'ACP', 'CSM', 'CSPO', 'CSD', 'PSM', 'PSPO', 'PSD'
            },
            
            # Data & Analytics
            'data_analytics': {
                'Certified Analytics Professional', 'Certified Data Management Professional',
                'Microsoft Certified Azure Data Scientist', 'Microsoft Certified Azure Data Engineer',
                'Google Cloud Certified Professional Data Engineer', 'AWS Certified Data Analytics',
                'AWS Certified Machine Learning', 'Google Cloud Certified Professional Machine Learning Engineer',
                'Microsoft Certified Azure AI Engineer', 'AWS Certified Machine Learning Specialty',
                'Google Cloud Certified Professional Machine Learning Engineer', 'Microsoft Certified Azure Data Scientist',
                'Microsoft Certified Azure Data Engineer', 'AWS Certified Data Analytics Specialty',
                'Google Cloud Certified Professional Data Engineer', 'Microsoft Certified Azure AI Engineer Associate',
                'CAP', 'CDMP', 'Azure Data Scientist', 'Azure Data Engineer', 'GCP Data Engineer',
                'GCP Machine Learning Engineer', 'Azure AI Engineer', 'AWS Machine Learning Specialty',
                'AWS Data Analytics Specialty', 'GCP Data Engineer', 'GCP Machine Learning Engineer'
            },
            
            # Security
            'security': {
                'Certified Information Systems Security Professional', 'Certified Information Security Manager',
                'Certified Information Systems Auditor', 'Certified Ethical Hacker', 'CompTIA Security+',
                'Certified Information Security Manager', 'Certified Information Systems Security Professional',
                'Certified Information Systems Auditor', 'Certified Ethical Hacker', 'CompTIA Security+',
                'CISSP', 'CISM', 'CISA', 'CEH', 'Security+', 'AWS Certified Security Specialty',
                'Microsoft Certified Azure Security Engineer', 'Google Cloud Certified Professional Security Engineer',
                'Certified Cloud Security Professional', 'Certified Information Privacy Professional',
                'Certified Information Privacy Technologist', 'Certified Information Privacy Manager',
                'Certified Information Privacy Professional', 'Certified Information Privacy Technologist',
                'Certified Information Privacy Manager', 'CCSP', 'CIPP', 'CIPT', 'CIPM'
            },
            
            # Networking
            'networking': {
                'Cisco Certified Network Associate', 'Cisco Certified Network Professional',
                'Cisco Certified Internetwork Expert', 'Cisco Certified Design Associate',
                'Cisco Certified Design Professional', 'Cisco Certified Design Expert',
                'CompTIA Network+', 'CompTIA A+', 'CompTIA Linux+', 'CompTIA Cloud+',
                'CCNA', 'CCNP', 'CCIE', 'CCDA', 'CCDP', 'CCDE', 'Network+', 'A+', 'Linux+', 'Cloud+',
                'AWS Certified Advanced Networking Specialty', 'Microsoft Certified Azure Network Engineer Associate',
                'Google Cloud Certified Professional Network Engineer'
            },
            
            # Database
            'database': {
                'Oracle Database Administrator', 'Microsoft SQL Server', 'MySQL Database Administrator',
                'PostgreSQL Database Administrator', 'MongoDB Certified Developer', 'MongoDB Certified DBA',
                'Oracle Certified Professional', 'Oracle Certified Master', 'Oracle Certified Expert',
                'Microsoft Certified Azure Database Administrator Associate', 'AWS Certified Database Specialty',
                'Google Cloud Certified Professional Cloud Database Engineer', 'Oracle DBA', 'SQL Server DBA',
                'MySQL DBA', 'PostgreSQL DBA', 'MongoDB Developer', 'MongoDB DBA', 'Oracle OCP', 'Oracle OCM',
                'Oracle OCE', 'Azure Database Administrator', 'AWS Database Specialty', 'GCP Cloud Database Engineer'
            },
            
            # DevOps & Tools
            'devops': {
                'Docker Certified Associate', 'Kubernetes Certified Administrator', 'Kubernetes Certified Application Developer',
                'Red Hat Certified Engineer', 'Red Hat Certified System Administrator', 'Red Hat Certified Architect',
                'Jenkins Certified Engineer', 'GitLab Certified Associate', 'GitLab Certified Professional',
                'Terraform Associate', 'Terraform Professional', 'Ansible Certified Engineer', 'Puppet Certified Professional',
                'Chef Certified Developer', 'Docker DCA', 'Kubernetes CKA', 'Kubernetes CKAD', 'RHCE', 'RHCSA', 'RHCA',
                'Jenkins CE', 'GitLab CA', 'GitLab CP', 'Terraform Associate', 'Terraform Professional', 'Ansible CE',
                'Puppet CP', 'Chef CD'
            }
        }
        
        # Flatten all certifications for easier matching
        self.all_certifications = set()
        for category_certs in self.certifications.values():
            self.all_certifications.update(category_certs)
        
        # Common certification patterns
        self.certification_patterns = [
            r'(?:certified|certification|cert)\s+([^,\n]+)',
            r'([^,\n]+)\s+(?:certified|certification|cert)',
            r'(?:aws|azure|gcp|google cloud|microsoft|oracle|cisco|comptia|pmp|cissp|cism|cisa|ceh)\s+([^,\n]+)',
            r'([^,\n]+)\s+(?:associate|professional|expert|specialist|practitioner|master|developer|architect|engineer|administrator)',
            r'(?:certified|certification|cert)\s+([^,\n]+)\s+(?:associate|professional|expert|specialist|practitioner|master|developer|architect|engineer|administrator)',
            r'([^,\n]+)\s+(?:certified|certification|cert)\s+(?:associate|professional|expert|specialist|practitioner|master|developer|architect|engineer|administrator)'
        ]
        
        # Common certification section headers
        self.certification_headers = [
            'certifications', 'certificates', 'professional certifications', 'technical certifications',
            'industry certifications', 'vendor certifications', 'credentials', 'qualifications',
            'professional credentials', 'technical credentials', 'industry credentials', 'vendor credentials',
            'certified', 'certification', 'certificate', 'credential', 'qualification'
        ]

    def extract_certifications_from_text(self, text: str) -> Dict[str, any]:
        """
        Extract certifications from resume text using multiple methods
        """
        text_lower = text.lower()
        
        # Method 1: Direct certification matching
        direct_matches = self._extract_direct_certifications(text_lower)
        
        # Method 2: Context-aware extraction (look for certification sections)
        context_matches = self._extract_from_certification_sections(text)
        
        # Method 3: Pattern-based extraction
        pattern_matches = self._extract_with_certification_patterns(text)
        
        # Method 4: Abbreviation matching
        abbreviation_matches = self._extract_certification_abbreviations(text)
        
        # Combine and deduplicate results
        all_found_certifications = set()
        all_found_certifications.update(direct_matches)
        all_found_certifications.update(context_matches)
        all_found_certifications.update(pattern_matches)
        all_found_certifications.update(abbreviation_matches)
        
        # Categorize certifications
        categorized_certifications = self._categorize_certifications(list(all_found_certifications))
        
        # Extract certification details (dates, issuing organizations)
        certification_details = self._extract_certification_details(text, list(all_found_certifications))
        
        return {
            'certifications': categorized_certifications,
            'details': certification_details,
            'summary': self._get_certification_summary(categorized_certifications)
        }

    def _extract_direct_certifications(self, text_lower: str) -> Set[str]:
        """Extract certifications using direct keyword matching"""
        found_certifications = set()
        
        for cert in self.all_certifications:
            cert_lower = cert.lower()
            # Use word boundaries for better matching
            pattern = r'\b' + re.escape(cert_lower) + r'\b'
            if re.search(pattern, text_lower):
                found_certifications.add(cert)
        
        return found_certifications

    def _extract_from_certification_sections(self, text: str) -> Set[str]:
        """Extract certifications from dedicated certification sections"""
        found_certifications = set()
        text_lower = text.lower()
        
        # Look for certification section headers
        for header in self.certification_headers:
            pattern = rf'{re.escape(header)}[:\s]*([^\n]*(?:\n[^\n]*)*?)(?:\n\n|\n[A-Z]|\n\d|$)'
            matches = re.finditer(pattern, text_lower, re.IGNORECASE | re.MULTILINE)
            
            for match in matches:
                cert_section = match.group(1)
                # Extract certifications from this section
                section_certs = self._extract_certifications_from_section(cert_section)
                found_certifications.update(section_certs)
        
        return found_certifications

    def _extract_certifications_from_section(self, section_text: str) -> Set[str]:
        """Extract certifications from a specific section of text"""
        found_certifications = set()
        
        # Split by common separators
        separators = [',', ';', '|', '\n', '\t', '•', '-', '–']
        for sep in separators:
            if sep in section_text:
                items = [item.strip() for item in section_text.split(sep)]
                for item in items:
                    item_clean = re.sub(r'[^\w\s]', '', item.lower()).strip()
                    # Check if this item matches any certification
                    for cert in self.all_certifications:
                        if item_clean in cert.lower() or cert.lower() in item_clean:
                            found_certifications.add(cert)
                            break
        
        return found_certifications

    def _extract_with_certification_patterns(self, text: str) -> Set[str]:
        """Extract certifications using regex patterns"""
        found_certifications = set()
        
        for pattern in self.certification_patterns:
            matches = re.finditer(pattern, text.lower())
            for match in matches:
                cert_phrase = match.group(1).strip()
                cert_clean = re.sub(r'[^\w\s]', '', cert_phrase).strip()
                
                # Check if this phrase matches any certification
                for cert in self.all_certifications:
                    if cert_clean in cert.lower() or cert.lower() in cert_clean:
                        found_certifications.add(cert)
                        break
        
        return found_certifications

    def _extract_certification_abbreviations(self, text: str) -> Set[str]:
        """Extract certifications using common abbreviations"""
        found_certifications = set()
        
        # Common certification abbreviations
        abbreviations = {
            'pmp': 'Project Management Professional',
            'cissp': 'Certified Information Systems Security Professional',
            'cism': 'Certified Information Security Manager',
            'cisa': 'Certified Information Systems Auditor',
            'ceh': 'Certified Ethical Hacker',
            'ccna': 'Cisco Certified Network Associate',
            'ccnp': 'Cisco Certified Network Professional',
            'ccie': 'Cisco Certified Internetwork Expert',
            'aws': 'AWS Certified Solutions Architect',
            'azure': 'Microsoft Azure Administrator',
            'gcp': 'Google Cloud Certified Professional Cloud Architect',
            'rhce': 'Red Hat Certified Engineer',
            'rhcsa': 'Red Hat Certified System Administrator',
            'rhca': 'Red Hat Certified Architect',
            'cka': 'Kubernetes Certified Administrator',
            'ckad': 'Kubernetes Certified Application Developer',
            'dca': 'Docker Certified Associate'
        }
        
        text_lower = text.lower()
        for abbrev, full_name in abbreviations.items():
            pattern = r'\b' + re.escape(abbrev) + r'\b'
            if re.search(pattern, text_lower):
                found_certifications.add(full_name)
        
        return found_certifications

    def _categorize_certifications(self, certifications: List[str]) -> Dict[str, List[str]]:
        """Categorize certifications into different types"""
        categorized = {
            'cloud_certifications': [],
            'programming_certifications': [],
            'project_management_certifications': [],
            'data_analytics_certifications': [],
            'security_certifications': [],
            'networking_certifications': [],
            'database_certifications': [],
            'devops_certifications': [],
            'other_certifications': []
        }
        
        for cert in certifications:
            cert_lower = cert.lower()
            categorized_flag = False
            
            if cert_lower in [c.lower() for c in self.certifications['aws'] | self.certifications['azure'] | self.certifications['gcp']]:
                categorized['cloud_certifications'].append(cert)
                categorized_flag = True
            elif cert_lower in [c.lower() for c in self.certifications['programming']]:
                categorized['programming_certifications'].append(cert)
                categorized_flag = True
            elif cert_lower in [c.lower() for c in self.certifications['project_management']]:
                categorized['project_management_certifications'].append(cert)
                categorized_flag = True
            elif cert_lower in [c.lower() for c in self.certifications['data_analytics']]:
                categorized['data_analytics_certifications'].append(cert)
                categorized_flag = True
            elif cert_lower in [c.lower() for c in self.certifications['security']]:
                categorized['security_certifications'].append(cert)
                categorized_flag = True
            elif cert_lower in [c.lower() for c in self.certifications['networking']]:
                categorized['networking_certifications'].append(cert)
                categorized_flag = True
            elif cert_lower in [c.lower() for c in self.certifications['database']]:
                categorized['database_certifications'].append(cert)
                categorized_flag = True
            elif cert_lower in [c.lower() for c in self.certifications['devops']]:
                categorized['devops_certifications'].append(cert)
                categorized_flag = True
            
            if not categorized_flag:
                categorized['other_certifications'].append(cert)
        
        # Remove empty categories
        return {k: v for k, v in categorized.items() if v}

    def _extract_certification_details(self, text: str, certifications: List[str]) -> List[Dict[str, str]]:
        """Extract additional details about certifications (dates, organizations)"""
        details = []
        
        for cert in certifications:
            cert_lower = cert.lower()
            cert_details = {'certification': cert}
            
            # Look for dates near the certification
            date_pattern = r'(\d{4}|\d{1,2}/\d{1,2}/\d{4}|\d{1,2}-\d{1,2}-\d{4})'
            cert_context = self._get_certification_context(text, cert)
            
            dates = re.findall(date_pattern, cert_context)
            if dates:
                cert_details['date'] = dates[0]
            
            # Look for issuing organizations
            organizations = ['AWS', 'Microsoft', 'Google', 'Oracle', 'Cisco', 'CompTIA', 'PMI', 'ISACA', 'Red Hat']
            for org in organizations:
                if org.lower() in cert_context.lower():
                    cert_details['issuing_organization'] = org
                    break
            
            details.append(cert_details)
        
        return details

    def _get_certification_context(self, text: str, certification: str) -> str:
        """Get context around a certification mention"""
        cert_lower = certification.lower()
        text_lower = text.lower()
        
        # Find the position of the certification
        pos = text_lower.find(cert_lower)
        if pos != -1:
            # Get 200 characters before and after
            start = max(0, pos - 200)
            end = min(len(text), pos + len(certification) + 200)
            return text[start:end]
        
        return ""

    def _get_certification_summary(self, categorized_certifications: Dict[str, List[str]]) -> Dict[str, any]:
        """Generate a summary of extracted certifications"""
        total_certifications = sum(len(certs) for certs in categorized_certifications.values())
        
        return {
            'total_certifications_found': total_certifications,
            'categories': list(categorized_certifications.keys()),
            'certification_count_by_category': {k: len(v) for k, v in categorized_certifications.items()},
            'top_certifications': self._get_top_certifications(categorized_certifications)
        }

    def _get_top_certifications(self, categorized_certifications: Dict[str, List[str]], limit: int = 10) -> List[str]:
        """Get the most important certifications based on category priority"""
        priority_order = [
            'cloud_certifications',
            'security_certifications',
            'project_management_certifications',
            'data_analytics_certifications',
            'programming_certifications',
            'networking_certifications',
            'database_certifications',
            'devops_certifications',
            'other_certifications'
        ]
        
        top_certifications = []
        for category in priority_order:
            if category in categorized_certifications:
                top_certifications.extend(categorized_certifications[category][:2])  # Take top 2 from each category
                if len(top_certifications) >= limit:
                    break
        
        return top_certifications[:limit]
