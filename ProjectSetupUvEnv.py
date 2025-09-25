# Final ProjectSetupUvEnv.py
# Platform support ( Linux )

import os
import json
import pandas as pd
from dotenv import load_dotenv, set_key
from dataclasses import dataclass
from typing import Dict, Any

@dataclass
class ProjectConfig:
    """Base configuration class handling common project properties"""
    project_dir: str = os.path.dirname(__file__)
    project_name: str = os.path.basename(project_dir).strip()
    
    def __post_init__(self):
        """Initialize derived properties and create folders"""
        self.project_env = os.path.join(self.project_dir, 'project.env')
        self.project_csv = os.path.join(self.project_dir, 'project_metadata.csv')

        # Required project subfolders
        self.required_folders = ["app", "docs", "features", "scripts"]
        for folder in self.required_folders:
            os.makedirs(os.path.join(self.project_dir, folder), exist_ok=True)

        self._setup_env_vars()
        
    def _setup_env_vars(self):
        """Initialize core environment variables"""
        os.environ.update({
            'ProjectName': self.project_name,
            'ProjectDir': self.project_dir,
            'ProjectEnv': self.project_env,
            'ProjectCsv': self.project_csv,
        })
        
    def save_config(self):
        """Persist configuration to environment file"""
        load_dotenv(self.project_env)
        for key in os.environ.keys():
            if key.startswith("Project"):
                set_key(self.project_env, key, os.environ[key])


class VSCodeConfigurator(ProjectConfig):
    """Handles VS Code workspace configuration"""
    def __init__(self):
        super().__init__()
        self.subfolders = [f.path for f in os.scandir(self.project_dir) if f.is_dir()]
        self.workspace_file = None
        
        # Define venv paths for Unix-like OS
        self.venv_bin_dir = os.path.join(self.project_dir, '.venv', 'bin')
        self.python_executable = os.path.join(self.venv_bin_dir, 'python')
        self.pytest_executable = os.path.join(self.venv_bin_dir, 'pytest')
        
    def configure_python_path(self):
        """Configure Python module search path"""
        os.environ['PYTHONPATH'] = self.project_dir
        set_key(self.project_env, "PYTHONPATH", self.project_dir)
        
    def create_debug_config(self) -> Dict[str, Any]:
        """Generate debug configuration for VS Code"""
        return {
            "name": f"Python: Module: {self.project_name}",
            "type": "debugpy",
            "request": "launch",
            "module": self.project_name,
            "env": {"PYTHONPATH": self.project_dir},
            "console": "integratedTerminal"
        }

    # --- New Task Generators ---

    def create_uv_project_task(self) -> Dict[str, Any]:
        return {
            "label": "create_uv_project",
            "type": "shell",
            "linux": {"command": "./scripts/create_uv_project_task.sh"},
            "windows": {"command": ".\\scripts\\create_uv_project_task.cmd"},
            "args": [],
            "options": {"cwd": "${workspaceFolder}"},
            "problemMatcher": [],
            "presentation": {"reveal": "always", "panel": "new"},
            "group": "build"
        }

 
    def build_workspace(self):
        """Create and configure VS Code workspace file"""
        config = {
            "folders": [],
            "settings": {
                # keep all defaults from original file
                "terminal.integrated.env.windows": {"PATH": "${env:anaconda_environment};"},
                "terminal.integrated.env.linux": {"PATH": f"{self.venv_bin_dir}:${{env:PATH}}"},
                "terminal.integrated.cwd": self.project_dir,
                "workbench.editor.languageDetection": True,
                "files.autoSave": "afterDelay",
                "diffEditor.renderSideBySide": True,
                "breadcrumbs.enabled": True,
                "editor.minimap.enabled": True,

                # Python defaults
                "python.defaultInterpreterPath": self.python_executable,
                "python.envFile": self.project_env,
                "python.experiments.enabled": True,
                "python.experiments.optInto": [],
                "python.experiments.optOutFrom": [],
                "python.globalModuleInstallation": False,
                "python.analysis.aiCodeActions": {"enabled": True},
                "python.analysis.include": [self.project_dir],
                "python.analysis.extraPaths": [
                    os.path.join(self.project_dir, 'app'),
                    os.path.join(self.project_dir, 'features'),
                    os.path.join(self.project_dir, 'docs'),
                    os.path.join(self.project_dir, 'scripts'),
                    os.path.join(self.project_dir, 'app/tests'),
                ],
                "python.testing.pytestPath": self.pytest_executable,
                "python.testing.pytestEnabled": True,
                "python.testing.unittestEnabled": False,
                "python.testing.pytestArgs": [
                    "--maxfail=3",
                    "-v",
                    "--tb=short",
                    "-k", "run_test"
                ],

                # Project Manager defaults
                "projectManager": {
                    "any": {"baseFolders": [self.project_dir]},
                    "git": {"baseFolders": [self.project_dir]},
                    "vscode": {"baseFolders": [self.project_dir]},
                    "tags": [
                        "Integration Project",
                        "Data Science",
                        "Web Development",
                        "Google SDK Python",
                        "Databases",
                        "Industrial Automation",
                        "Industrial Control",
                        "Industrial Instrumentation",
                        "Industrial Application",
                        "IOT"
                    ]
                },
                "python.analysis.enableTroubleshootMissingImports": True,
                "python.analysis.importFormat": "absolute",
                "python-envs.pythonProjects": [],
            },
            "launch": {"configurations": []},
            "tasks": {"version": "2.0.0", "tasks": []}
        }
        
        # Add debug configuration
        config["launch"]["configurations"].append(self.create_debug_config())
        # Add task configurations
        config["tasks"]["tasks"].extend([
            self.create_uv_project_task()
        ])
        
        # Filter folders (exclude .git, .pytest_cache)
        self.workspace_subfolders = [
            f for f in self.subfolders if os.path.basename(f) not in [".git", ".pytest_cache"]
        ]
        config["folders"] = [{"path": os.path.basename(f)} for f in self.workspace_subfolders]
        
        # Save workspace file
        vscode_dir = os.path.join(self.project_dir, '.vscode')
        os.makedirs(vscode_dir, exist_ok=True)
        
        self.workspace_file = os.path.join(vscode_dir, f'{self.project_name}.code-workspace')
        with open(self.workspace_file, 'w', encoding="utf-8") as f:
            json.dump(config, f, indent=4)
            
        os.environ['vscode_workspace'] = self.workspace_file
        set_key(self.project_env, "vscode_workspace", self.workspace_file)


class CommentHandler(ProjectConfig):
    """Handles insertion of documentation comments in workspace file"""
    COMMENT_TEMPLATE = {
        "settings": "// Controls the settings that apply to all profiles (editor, python, project manager)",
        "launch": "// Add debugging configurations to project (debugging Python modules)",
        "tasks": "// Automate project tasks\n"
                 "// - Group 'todo': handles quick to-do task generation\n"
                 "// - Group 'uv-tasks': manages uv project setup and virtual environment creation"
    }

    def __init__(self):
        super().__init__()
        self.workspace_file = os.getenv("vscode_workspace")

    def add_comments(self):
        """Insert documentation comments at appropriate locations in workspace file"""
        try:
            with open(self.workspace_file, 'r+', encoding='utf-8') as f:
                content = f.read()
                
                # Insert comments before each section
                for section, comment in self.COMMENT_TEMPLATE.items():
                    insert_pos = content.find(f'"{section}":')
                    if insert_pos != -1:
                        content = content[:insert_pos] + f'{comment}\n' + content[insert_pos:]

                # Write updated content back to file
                f.seek(0)
                f.write(content)
                f.truncate()

        except (OSError, FileNotFoundError) as e:
            print(f"Error updating workspace comments: {str(e)}")


class ProjectMetadataHandler(ProjectConfig):
    """Handles project metadata generation and documentation export"""

    DEFAULT_DATA = [
        {"attributes": "ProjectName", "value": "name", "general": 1, "documentation": 1},
        {"attributes": "ProjectRepo", "value": "https://github.com/account/name", "general": 1, "documentation": 1},
        {"attributes": "ImageName", "value": "CodeProjectTemplate.png", "general": 1, "documentation": 0},
        {"attributes": "LinkImageRepo", "value": "https://github.com/account/name/docs/media", "general": 1, "documentation": 0},
        {"attributes": "Category", "value": "Python", "general": 1, "documentation": 0},
        {"attributes": "ProjectAbout", "value": "A python project to delivery a task or a value", "general": 1, "documentation": 1},
        {"attributes": "WhyProject", "value": "To satisfy an On-brand or On-product demand", "general": 0, "documentation": 1},
        {"attributes": "medialink_1", "value": "https://github.com/account/name/docs/media/screenshot-1.png", "general": 0, "documentation": 1},
        {"attributes": "medialink_2", "value": "https://github.com/account/name/docs/media/screenshot-2.png", "general": 0, "documentation": 1},
        {"attributes": "medialink_3", "value": "https://github.com/account/name/docs/media/screenshot-3.png", "general": 0, "documentation": 1},
        {"attributes": "feature_1", "value": "Best feature option 1", "general": 0, "documentation": 1},
        {"attributes": "feature_2", "value": "Best feature option 2", "general": 0, "documentation": 1},
        {"attributes": "feature_3", "value": "Bilingual documentation (Spanish and English).", "general": 0, "documentation": 1},
        {"attributes": "email", "value": "my.mail@gmail.com", "general": 0, "documentation": 1},
        {"attributes": "LicenceName", "value": "license", "general": 0, "documentation": 1},
    ]

    def __init__(self):
        super().__init__()
        self.df = pd.DataFrame(self.DEFAULT_DATA)

    def generate_metadata(self):
        """Generate metadata and documentation CSV files"""
        if not os.path.exists(self.project_csv):
            self.df.to_csv(self.project_csv, index=False)
            set_key(self.project_env, "ProjectCsv", self.project_csv)

        # Create documentation_data.csv (only rows with documentation == 1)
        docs_dir = os.path.join(self.project_dir, "docs")
        os.makedirs(docs_dir, exist_ok=True)
        docs_csv = os.path.join(docs_dir, "documentation_data.csv")
        doc_df = self.df[self.df["documentation"] == 1]
        doc_df.to_csv(docs_csv, index=False)


if __name__ == "__main__":
    # Initialize configuration
    config = ProjectConfig()
    config.save_config()

    # Configure VS Code workspace
    vs_config = VSCodeConfigurator()
    vs_config.configure_python_path()
    vs_config.build_workspace()

    # Add documentation comments
    comment_handler = CommentHandler()
    comment_handler.add_comments()

    # Generate project metadata + documentation
    metadata_handler = ProjectMetadataHandler()
    metadata_handler.generate_metadata()
