@echo off
setlocal
echo ==========================================
echo create_conda_project_task.cmd - Setup Conda project
echo ==========================================

REM 1. Check if .conda_env exists, if not create
if not exist .conda_env (
    echo 🔧 Creating Conda environment in .conda_env
    conda create -y -p .conda_env python=3.10
) else (
    echo 📦 Conda environment already exists in .conda_env
)

REM 2. Activate environment
echo 📦 Activating environment...
call conda activate .conda_env

REM 3. Initialize a "conda project" (basic scaffold)
if not exist app (
    mkdir app
    echo print("Hello from Conda project") > app\main.py
    type nul > app\__init__.py
)
echo 🚀 Conda project initialized in app\

REM 4. Handle requirements.txt
if not exist requirements.txt (
    echo ⚠️ No requirements.txt found, creating an empty one.
    type nul > requirements.txt
)

echo 📦 Installing dependencies from requirements.txt...
conda install -y --file requirements.txt || pip install -r requirements.txt

REM 5. List installed packages
echo 📝 Listing installed packages...
conda list > packages_version.txt

echo ✅ Conda project setup completed. See packages_version.txt for package list.
endlocal
