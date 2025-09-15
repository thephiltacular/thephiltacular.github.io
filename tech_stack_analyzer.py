#!/usr/bin/env python3
"""
GitHub Tech Stack Analyzer
Automatically detects and updates technology stacks for projects on the portfolio website.
"""

import json
import re
import requests
from typing import Dict, List, Set
import os
from pathlib import Path

class TechStackAnalyzer:
    def __init__(self, github_token=None):
        self.github_token = github_token
        self.headers = {'Authorization': f'token {github_token}'} if github_token else {}
        self.base_url = 'https://api.github.com'

        # Technology detection patterns
        self.tech_patterns = {
            'Python': [
                r'requirements\.txt',
                r'setup\.py',
                r'pyproject\.toml',
                r'Pipfile',
                r'poetry\.lock',
                r'\.py$'
            ],
            'JavaScript': [
                r'package\.json',
                r'yarn\.lock',
                r'package-lock\.json',
                r'\.js$',
                r'\.jsx$',
                r'\.ts$',
                r'\.tsx$'
            ],
            'TypeScript': [
                r'tsconfig\.json',
                r'\.ts$',
                r'\.tsx$'
            ],
            'Go': [
                r'go\.mod',
                r'go\.sum',
                r'\.go$'
            ],
            'Rust': [
                r'Cargo\.toml',
                r'Cargo\.lock',
                r'\.rs$'
            ],
            'Docker': [
                r'Dockerfile',
                r'docker-compose\.yml',
                r'\.dockerignore'
            ],
            'Kubernetes': [
                r'.*\.yaml$',
                r'.*\.yml$',
                r'k8s',
                r'kubernetes'
            ],
            'React': [
                r'react',
                r'jsx',
                r'tsx'
            ],
            'Node.js': [
                r'package\.json',
                r'node_modules'
            ],
            'FastAPI': [
                r'fastapi',
                r'uvicorn'
            ],
            'Flask': [
                r'flask'
            ],
            'Django': [
                r'django'
            ],
            'TensorFlow': [
                r'tensorflow',
                r'tf\.'
            ],
            'PyTorch': [
                r'torch',
                r'pytorch'
            ],
            'Pandas': [
                r'pandas',
                r'pd\.'
            ],
            'NumPy': [
                r'numpy',
                r'np\.'
            ],
            'Scikit-learn': [
                r'sklearn',
                r'scikit'
            ],
            'PostgreSQL': [
                r'postgresql',
                r'postgres'
            ],
            'MongoDB': [
                r'mongodb',
                r'mongo'
            ],
            'Redis': [
                r'redis'
            ],
            'AWS': [
                r'boto3',
                r'aws',
                r's3',
                r'lambda',
                r'cloudformation'
            ],
            'Google Cloud': [
                r'google-cloud',
                r'gcp',
                r'firebase'
            ],
            'Azure': [
                r'azure',
                r'azurerm'
            ]
        }

    def get_repo_contents(self, owner: str, repo: str, path='') -> List[Dict]:
        """Fetch repository contents from GitHub API."""
        url = f'{self.base_url}/repos/{owner}/{repo}/contents/{path}'
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Error fetching {owner}/{repo}: {e}")
            return []

    def analyze_file_content(self, owner: str, repo: str, file_path: str) -> Set[str]:
        """Analyze a specific file for technology detection."""
        detected_tech = set()

        try:
            url = f'{self.base_url}/repos/{owner}/{repo}/contents/{file_path}'
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()

            file_data = response.json()
            if 'content' in file_data:
                import base64
                content = base64.b64decode(file_data['content']).decode('utf-8', errors='ignore')

                # Check for technology patterns in file content
                for tech, patterns in self.tech_patterns.items():
                    for pattern in patterns:
                        if re.search(pattern, content, re.IGNORECASE):
                            detected_tech.add(tech)
                            break

        except Exception as e:
            print(f"Error analyzing {file_path}: {e}")

        return detected_tech

    def analyze_repository(self, owner: str, repo: str) -> Set[str]:
        """Analyze a GitHub repository for technologies used."""
        detected_tech = set()

        print(f"Analyzing {owner}/{repo}...")

        # Get repository contents
        contents = self.get_repo_contents(owner, repo)

        # Analyze key files
        key_files = [
            'package.json', 'requirements.txt', 'setup.py', 'pyproject.toml',
            'Cargo.toml', 'go.mod', 'Dockerfile', 'docker-compose.yml',
            'Pipfile', 'poetry.lock', 'yarn.lock', 'package-lock.json',
            'tsconfig.json', 'go.sum', 'Cargo.lock'
        ]

        for item in contents:
            if item['name'] in key_files:
                file_tech = self.analyze_file_content(owner, repo, item['name'])
                detected_tech.update(file_tech)

        # Analyze file extensions in the root directory
        for item in contents:
            if item['type'] == 'file':
                file_name = item['name']
                for tech, patterns in self.tech_patterns.items():
                    for pattern in patterns:
                        if re.search(pattern, file_name, re.IGNORECASE):
                            detected_tech.add(tech)
                            break

        # Add language detection based on GitHub API
        try:
            url = f'{self.base_url}/repos/{owner}/{repo}/languages'
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            languages = response.json()

            # Map GitHub languages to our tech tags
            language_mapping = {
                'Python': 'Python',
                'JavaScript': 'JavaScript',
                'TypeScript': 'TypeScript',
                'Go': 'Go',
                'Rust': 'Rust',
                'HTML': 'HTML',
                'CSS': 'CSS',
                'Shell': 'Shell',
                'Dockerfile': 'Docker',
                'Makefile': 'Make'
            }

            for lang in languages.keys():
                if lang in language_mapping:
                    detected_tech.add(language_mapping[lang])

        except Exception as e:
            print(f"Error fetching languages for {owner}/{repo}: {e}")

        return detected_tech

    def get_readme_content(self, owner: str, repo: str) -> str:
        """Fetch README content from GitHub repository."""
        readme_files = ['README.md', 'readme.md', 'README.txt', 'readme.txt']

        for readme_file in readme_files:
            try:
                url = f'{self.base_url}/repos/{owner}/{repo}/contents/{readme_file}'
                response = requests.get(url, headers=self.headers)
                response.raise_for_status()

                file_data = response.json()
                if 'content' in file_data:
                    import base64
                    content = base64.b64decode(file_data['content']).decode('utf-8', errors='ignore')
                    return content
            except:
                continue

        return ""

    def extract_description_from_readme(self, readme_content: str) -> str:
        """Extract project description from README content."""
        if not readme_content:
            return ""

        # Remove markdown headers and code blocks for cleaner text
        content = re.sub(r'^#.*$', '', readme_content, flags=re.MULTILINE)
        content = re.sub(r'```[\s\S]*?```', '', content)
        content = re.sub(r'`[^`]*`', '', content)

        # Look for common description patterns
        lines = [line.strip() for line in content.split('\n') if line.strip()]

        # Try to find the first meaningful paragraph
        for line in lines:
            # Skip empty lines, links, badges, etc.
            if (len(line) > 50 and  # Substantial length
                not line.startswith('[') and  # Not a markdown link/badge
                not line.startswith('!') and  # Not an image
                not line.startswith('-') and  # Not a list item
                not re.match(r'^[^\w]*$', line) and  # Not just symbols
                'http' not in line.lower()):  # No URLs

                # Clean up the description
                description = re.sub(r'<[^>]+>', '', line)  # Remove HTML tags
                description = re.sub(r'\s+', ' ', description)  # Normalize whitespace

                # Truncate if too long (aim for 150-200 characters)
                if len(description) > 200:
                    description = description[:197] + "..."

                return description

        return ""

    def analyze_repository_description(self, owner: str, repo: str) -> str:
        """Analyze repository and extract description from README."""
        print(f"Fetching description for {owner}/{repo}...")

        readme_content = self.get_readme_content(owner, repo)
        if readme_content:
            description = self.extract_description_from_readme(readme_content)
            if description:
                return description

        return ""
        return ""

    def analyze_repository_description(self, owner: str, repo: str) -> str:
        """Analyze repository and extract description from README."""
        print(f"Fetching description for {owner}/{repo}...")

        readme_content = self.get_readme_content(owner, repo)
        if readme_content:
            description = self.extract_description_from_readme(readme_content)
            if description:
                return description

        return ""

    def update_html_tech_tags(self, html_file: str, projects: Dict[str, Set[str]]):
        """Update HTML file with detected tech stacks."""
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()

        for project_name, tech_stack in projects.items():
            # Find the project section in HTML
            project_pattern = rf'(<div class="project-card">.*?<h3>{re.escape(project_name)}</h3>.*?<div class="project-tech">).*?(</div>)'
            match = re.search(project_pattern, content, re.DOTALL)

            if match:
                # Generate new tech tags HTML
                tech_tags_html = '\n'.join([
                    f'                                <span class="tech-tag">{tech}</span>'
                    for tech in sorted(tech_stack)
                ])

                # Replace the existing tech tags
                old_tech_section = match.group(0)
                new_tech_section = match.group(1) + tech_tags_html + '\n                            ' + match.group(2)

                content = content.replace(old_tech_section, new_tech_section)
                print(f"Updated tech tags for {project_name}")

        # Write updated content back to file
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(content)

        print("HTML file updated successfully!")

    def update_html_descriptions(self, html_file: str, descriptions: Dict[str, str]):
        """Update HTML file with project descriptions from GitHub READMEs."""
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()

        for project_name, description in descriptions.items():
            if description:
                # Find the project description section in HTML
                project_pattern = rf'(<div class="project-card">.*?<h3>{re.escape(project_name)}</h3>.*?<p class="project-description">).*?(</p>)'
                match = re.search(project_pattern, content, re.DOTALL)

                if match:
                    # Replace the existing description
                    old_desc_section = match.group(0)
                    new_desc_section = match.group(1) + description + match.group(2)

                    content = content.replace(old_desc_section, new_desc_section)
                    print(f"Updated description for {project_name}")

        # Write updated content back to file
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(content)

        print("Project descriptions updated successfully!")

def main():
    # Project configurations
    projects = {
        'Voice AI Pipeline': {
            'owner': 'thephiltacular',
            'repo': 'voice-ai-pipeline'
        },
        'Open Trading Algorithm': {
            'owner': 'thephiltacular',
            'repo': 'open_trading_algo'
        },
        'CRUD IAM Playground': {
            'owner': 'thephiltacular',
            'repo': 'crud-iam-playground'
        }
    }

    # Initialize analyzer
    analyzer = TechStackAnalyzer()

    # Analyze all projects for tech stacks
    detected_tech_stacks = {}
    for project_name, config in projects.items():
        tech_stack = analyzer.analyze_repository(config['owner'], config['repo'])
        detected_tech_stacks[project_name] = tech_stack
        print(f"{project_name}: {', '.join(sorted(tech_stack))}")

    # Analyze all projects for descriptions
    detected_descriptions = {}
    for project_name, config in projects.items():
        description = analyzer.analyze_repository_description(config['owner'], config['repo'])
        detected_descriptions[project_name] = description
        if description:
            print(f"{project_name} description: {description}")

    # Update HTML file
    html_file = 'index.html'
    if os.path.exists(html_file):
        analyzer.update_html_tech_tags(html_file, detected_tech_stacks)
        analyzer.update_html_descriptions(html_file, detected_descriptions)
    else:
        print(f"HTML file '{html_file}' not found!")

if __name__ == '__main__':
    main()