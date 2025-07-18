import os
import json
import csv

# Load configuration data from CSV
config_data = {}
csv_file_path = os.path.join(os.path.dirname(__file__), 'server_configuration_data.csv')
with open(csv_file_path, mode='r') as infile:
    reader = csv.DictReader(infile)
    for row in reader:
        config_data[row['variable']] = row['value']


# Set Conda environment path
conda_prefix = os.getenv('CONDA_PREFIX', '/opt/conda')

# configuration directory to write the modular configuration files in your conda environment
#config_dir = f"{conda_prefix}/etc/jupyter/jupyter_server_config.d"

# Configuration directory to write the modular configuration files in your local directory
config_dir = os.path.dirname(__file__)

# Ensure the config directory exists
os.makedirs(config_dir, exist_ok=True)


# Open Jupyter template json file
jupyter_template_path = 'templates\\jupyterlab.json'
jupyter_file_path = f"{config_dir}\\jupyterlab.json"
with open(jupyter_template_path, 'r', encoding='utf-8') as infile:
    # load json data
    jupyterlab_json_data = json.load(infile)

# -----------------------------
# JupyterLab Application Settings
# -----------------------------
app_settings = {
    "ServerApp": {
        "ip": config_data.get("ip", "127.0.0.1"),
        "port": 9000,
        "open_browser": False,
        "allow_remote_access": True,
        "base_url": config_data.get("base_url", "/default-learning-env/"),
        "default_url": config_data.get("default_url", "/lab"),
        "shutdown_no_activity_timeout": 3600,
        "root_dir": config_data.get("root_dir", "/opt/conda/var/jupyter")
    }
}
with open(f"{config_dir}/application.json", "w") as f:
    json.dump(app_settings, f, indent=4)

# Update jupyterlab_json_data
for key in app_settings["ServerApp"].keys():
    jupyterlab_json_data["ServerApp"][key] = app_settings["ServerApp"][key]

# -----------------------------
# JupyterLab Extensions
# -----------------------------
extensions_settings = {
    "LabApp": {
        "labextensions_path": [config_data.get("custom_lab_extensions_path", "D:/custom_jupyterlab_extensions")],
        "blocked_extensions_uris": [],
        "extensions_in_dev_mode": False,
        "expose_app_in_browser": True
    }
}
with open(f"{config_dir}/extensions.json", "w") as f:
    json.dump(extensions_settings, f, indent=4)

# Update jupyterlab_json_data
for key in extensions_settings["LabApp"].keys():
    jupyterlab_json_data["LabApp"][key] = extensions_settings["LabApp"][key]

# -----------------------------
# JupyterLab Workspaces
# -----------------------------
workspaces_settings = {
    "LabApp": {
        "workspaces_dir": config_data.get("workspaces_dir", "/opt/conda/var/jupyter/workspaces"),
        "default_url": config_data.get("default_url", "/lab"),
        "workspaces_api_url": config_data.get("workspaces_api_url", "/api/workspaces")
    }
}
with open(f"{config_dir}/workspaces.json", "w") as f:
    json.dump(workspaces_settings, f, indent=4)

# Update jupyterlab_json_data
for key in workspaces_settings["LabApp"].keys():
    jupyterlab_json_data["LabApp"][key] = workspaces_settings["LabApp"][key]

# -----------------------------
# Password Identity Provider Settings
# -----------------------------
identity_provider_settings = {
    "PasswordIdentityProvider": {
        "hashed_password": "argon2:-to-be-replaced-",
    }
}
with open(f"{config_dir}/identity_provider.json", "w") as f:
    json.dump(identity_provider_settings, f, indent=4)

# Update jupyterlab_json_data
for key in identity_provider_settings["PasswordIdentityProvider"].keys():
    jupyterlab_json_data["PasswordIdentityProvider"][key] = identity_provider_settings["PasswordIdentityProvider"][key]

# -----------------------------
# Security & Authentication
# -----------------------------
security_settings = {
    "ServerApp": {
        "token": "your_secure_token_here",
        "password_required": True,
        "certfile": f"{conda_prefix}/etc/jupyter/cert.pem",
        "keyfile": f"{conda_prefix}/etc/jupyter/key.pem",
        "disable_check_xsrf": False,
        "allow_origin": "*"
    }
}
security_settings["ServerApp"]["token"] = os.getenv("JUPYTER_TOKEN", "your_secure_token_here")
with open(f"{config_dir}/security.json", "w") as f:
    json.dump(security_settings, f, indent=4)

# Update jupyterlab_json_data
for key in security_settings["ServerApp"].keys():
    jupyterlab_json_data["ServerApp"][key] = security_settings["ServerApp"][key]

# -----------------------------
# Performance & Scalability
# -----------------------------
performance_settings = {
    "ServerApp": {
        "shutdown_no_activity_timeout": 3600,
        "max_body_size": 536870912,
        "max_buffer_size": 536870912,
        "limit_rate": True,
        "tornado_settings": {
            "websocket_max_message_size": 512 * 1024 * 1024
        },
        "kernel_manager_class": "jupyter_server.services.kernels.kernelmanager.AsyncMappingKernelManager"
    }
}
with open(f"{config_dir}/performance.json", "w") as f:
    json.dump(performance_settings, f, indent=4)

# Update jupyterlab_json_data
for key in performance_settings["ServerApp"].keys():
    jupyterlab_json_data["ServerApp"][key] = performance_settings["ServerApp"][key]

# -----------------------------
# JupyterLab Theming & UI Customization
# -----------------------------
theming_settings = {
    "LabApp": {
        "theme": "JupyterLab Dark",
        "hide_sys_info": True,
        "collaborative": True,
        "custom_css": config_data.get("custom_css", "path/to/custom.css"),
        "custom_js": config_data.get("custom_js", "path/to/custom.js")
    }
}
with open(f"{config_dir}/theming.json", "w") as f:
    json.dump(theming_settings, f, indent=4)

# Update jupyterlab_json_data
for key in theming_settings["LabApp"].keys():
    jupyterlab_json_data["LabApp"][key] = theming_settings["LabApp"][key]

# Write new jupyterlab.json configuration file:
with open(jupyter_file_path, 'w', encoding='utf-8') as outfile:
    json.dump(jupyterlab_json_data, outfile, indent=4)

# Print
print(f"\nJupyter Server modular configuration files have been written to:\n{config_dir}")
