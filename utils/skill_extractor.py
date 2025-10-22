import re
from typing import List, Dict, Set
from collections import Counter

class SkillExtractor:
    def __init__(self):
        # Comprehensive skill databases
        self.programming_languages = {
            'python', 'java', 'javascript', 'typescript', 'c++', 'c#', 'c', 'go', 'rust', 'kotlin',
            'swift', 'php', 'ruby', 'scala', 'r', 'matlab', 'perl', 'haskell', 'clojure', 'erlang',
            'dart', 'lua', 'bash', 'powershell', 'sql', 'html', 'css', 'xml', 'json', 'yaml'
        }
        
        self.frameworks_libraries = {
            'react', 'angular', 'vue', 'node.js', 'express', 'django', 'flask', 'fastapi', 'spring',
            'laravel', 'rails', 'asp.net', 'jquery', 'bootstrap', 'tailwind', 'sass', 'less',
            'webpack', 'babel', 'gulp', 'grunt', 'npm', 'yarn', 'pip', 'maven', 'gradle',
            'tensorflow', 'pytorch', 'keras', 'scikit-learn', 'pandas', 'numpy', 'matplotlib',
            'seaborn', 'plotly', 'd3.js', 'chart.js', 'lodash', 'moment.js', 'axios'
        }
        
        self.databases = {
            'mysql', 'postgresql', 'mongodb', 'redis', 'elasticsearch', 'cassandra', 'dynamodb',
            'sqlite', 'oracle', 'sql server', 'mariadb', 'neo4j', 'influxdb', 'couchdb',
            'firebase', 'supabase', 'planetscale', 'cockroachdb'
        }
        
        self.cloud_platforms = {
            'aws', 'azure', 'gcp', 'google cloud', 'heroku', 'vercel', 'netlify', 'digital ocean',
            'linode', 'vultr', 'cloudflare', 'amazon web services', 'microsoft azure'
        }
        
        self.tools_technologies = {
            'docker', 'kubernetes', 'jenkins', 'git', 'github', 'gitlab', 'bitbucket', 'jira',
            'confluence', 'slack', 'trello', 'asana', 'figma', 'sketch', 'adobe', 'photoshop',
            'illustrator', 'vscode', 'intellij', 'eclipse', 'vim', 'emacs', 'postman', 'insomnia',
            'swagger', 'openapi', 'graphql', 'rest', 'api', 'microservices', 'ci/cd', 'devops',
            'agile', 'scrum', 'kanban', 'tdd', 'bdd', 'unit testing', 'integration testing'
        }
        
        self.soft_skills = {
            'leadership', 'communication', 'teamwork', 'problem solving', 'critical thinking',
            'time management', 'project management', 'mentoring', 'collaboration', 'adaptability',
            'creativity', 'analytical', 'detail oriented', 'self motivated', 'multitasking'
        }
        
        # Combine all skills for comprehensive matching
        self.all_skills = (
            self.programming_languages | 
            self.frameworks_libraries | 
            self.databases | 
            self.cloud_platforms | 
            self.tools_technologies | 
            self.soft_skills
        )
        
        # Common skill section headers
        self.skill_headers = [
            'skills', 'technical skills', 'core competencies', 'technologies', 'tools',
            'programming languages', 'frameworks', 'technologies used', 'expertise',
            'technical expertise', 'key skills', 'competencies', 'proficiencies'
        ]

    def extract_skills_from_text(self, text: str) -> Dict[str, List[str]]:
        """
        Extract skills from resume text using multiple methods
        """
        text_lower = text.lower()
        
        # Method 1: Direct keyword matching
        direct_matches = self._extract_direct_matches(text_lower)
        
        # Method 2: Context-aware extraction (look for skill sections)
        context_matches = self._extract_from_context(text)
        
        # Method 3: Pattern-based extraction
        pattern_matches = self._extract_with_patterns(text)
        
        # Combine and deduplicate results
        all_found_skills = set()
        all_found_skills.update(direct_matches)
        all_found_skills.update(context_matches)
        all_found_skills.update(pattern_matches)
        
        # Categorize skills
        categorized_skills = self._categorize_skills(list(all_found_skills))
        
        return categorized_skills

    def _extract_direct_matches(self, text_lower: str) -> Set[str]:
        """Extract skills using direct keyword matching"""
        found_skills = set()
        
        for skill in self.all_skills:
            # Handle multi-word skills
            if ' ' in skill:
                if skill in text_lower:
                    found_skills.add(skill.title())
            else:
                # Use word boundaries for single words to avoid partial matches
                pattern = r'\b' + re.escape(skill) + r'\b'
                if re.search(pattern, text_lower):
                    found_skills.add(skill.title())
        
        return found_skills

    def _extract_from_context(self, text: str) -> Set[str]:
        """Extract skills from dedicated skill sections"""
        found_skills = set()
        text_lower = text.lower()
        
        # Look for skill section headers
        for header in self.skill_headers:
            pattern = rf'{re.escape(header)}[:\s]*([^\n]*(?:\n[^\n]*)*?)(?:\n\n|\n[A-Z]|\n\d|$)'
            matches = re.finditer(pattern, text_lower, re.IGNORECASE | re.MULTILINE)
            
            for match in matches:
                skill_section = match.group(1)
                # Extract skills from this section
                section_skills = self._extract_skills_from_section(skill_section)
                found_skills.update(section_skills)
        
        return found_skills

    def _extract_skills_from_section(self, section_text: str) -> Set[str]:
        """Extract skills from a specific section of text"""
        found_skills = set()
        
        # Split by common separators
        separators = [',', ';', '|', '\n', '\t', '•', '-', '–']
        for sep in separators:
            if sep in section_text:
                items = [item.strip() for item in section_text.split(sep)]
                for item in items:
                    item_clean = re.sub(r'[^\w\s]', '', item.lower()).strip()
                    if item_clean in self.all_skills:
                        found_skills.add(item_clean.title())
        
        return found_skills

    def _extract_with_patterns(self, text: str) -> Set[str]:
        """Extract skills using regex patterns"""
        found_skills = set()
        
        # Pattern for "X years of experience with Y"
        experience_pattern = r'(\d+)\+?\s*years?\s*(?:of\s*)?experience\s*(?:with|in)\s*([^,\n]+)'
        matches = re.finditer(experience_pattern, text.lower())
        for match in matches:
            skill_phrase = match.group(2).strip()
            skill_clean = re.sub(r'[^\w\s]', '', skill_phrase).strip()
            if skill_clean in self.all_skills:
                found_skills.add(skill_clean.title())
        
        # Pattern for "Proficient in X, Y, Z"
        proficient_pattern = r'proficient\s*(?:in|with)\s*([^.\n]+)'
        matches = re.finditer(proficient_pattern, text.lower())
        for match in matches:
            skills_text = match.group(1)
            skills = self._extract_skills_from_section(skills_text)
            found_skills.update(skills)
        
        return found_skills

    def _categorize_skills(self, skills: List[str]) -> Dict[str, List[str]]:
        """Categorize skills into different types"""
        categorized = {
            'programming_languages': [],
            'frameworks_libraries': [],
            'databases': [],
            'cloud_platforms': [],
            'tools_technologies': [],
            'soft_skills': [],
            'other': []
        }
        
        for skill in skills:
            skill_lower = skill.lower()
            categorized_flag = False
            
            if skill_lower in self.programming_languages:
                categorized['programming_languages'].append(skill)
                categorized_flag = True
            elif skill_lower in self.frameworks_libraries:
                categorized['frameworks_libraries'].append(skill)
                categorized_flag = True
            elif skill_lower in self.databases:
                categorized['databases'].append(skill)
                categorized_flag = True
            elif skill_lower in self.cloud_platforms:
                categorized['cloud_platforms'].append(skill)
                categorized_flag = True
            elif skill_lower in self.tools_technologies:
                categorized['tools_technologies'].append(skill)
                categorized_flag = True
            elif skill_lower in self.soft_skills:
                categorized['soft_skills'].append(skill)
                categorized_flag = True
            
            if not categorized_flag:
                categorized['other'].append(skill)
        
        # Remove empty categories
        return {k: v for k, v in categorized.items() if v}

    def get_skill_summary(self, categorized_skills: Dict[str, List[str]]) -> Dict[str, any]:
        """Generate a summary of extracted skills"""
        total_skills = sum(len(skills) for skills in categorized_skills.values())
        
        return {
            'total_skills_found': total_skills,
            'categories': list(categorized_skills.keys()),
            'skill_count_by_category': {k: len(v) for k, v in categorized_skills.items()},
            'top_skills': self._get_top_skills(categorized_skills)
        }

    def _get_top_skills(self, categorized_skills: Dict[str, List[str]], limit: int = 10) -> List[str]:
        """Get the most important skills based on category priority"""
        priority_order = [
            'programming_languages',
            'frameworks_libraries', 
            'cloud_platforms',
            'databases',
            'tools_technologies',
            'soft_skills',
            'other'
        ]
        
        top_skills = []
        for category in priority_order:
            if category in categorized_skills:
                top_skills.extend(categorized_skills[category][:3])  # Take top 3 from each category
                if len(top_skills) >= limit:
                    break
        
        return top_skills[:limit]
