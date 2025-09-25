@echo off
setlocal
echo ==========================================
echo create_uv_project_task.cmd - Setup a uv project
echo ==========================================

REM 1. Create environment in current directory
echo 🔧 Creating environment with uv...
uv venv

REM 2. Activate environment
echo 📦 Activating environment...
call .venv\Scripts\activate.bat

REM 3. Initialize a uv project
echo 🚀 Initializing uv project...
uv init

REM 4. Handle requirements.txt
if not exist requirements.txt (
    echo ⚠️ No requirements.txt found, creating an empty one.
    type nul > requirements.txt
)

echo 📦 Installing dependencies from requirements.txt...
uv add -r requirements.txt

REM 5. List all installed packages with versions
echo 📝 Listing installed packages...
uv pip list > packages_version.txt

echo ✅ UV project setup completed. See packages_version.txt for package list.
endlocal
