#!/usr/bin/env bash
set -e

# create_conda_project_task.sh - Setup Conda project in WSL/Linux

# 1. Create environment if not exists
if [ ! -d ".conda_env" ]; then
  echo "🔧 Creating Conda environment in .conda_env"
  conda create -y -p .conda_env python=3.10
else
  echo "📦 Conda environment already exists in .conda_env"
fi

# 2. Activate environment
echo "📦 Activating environment..."
source "$(conda info --base)/etc/profile.d/conda.sh"
conda activate ./\.conda_env

# 3. Initialize a "conda project" (basic scaffold)
if [ ! -d "app" ]; then
  mkdir -p app
  echo "print('Hello from Conda project')" > app/main.py
  touch app/__init__.py
fi
echo "🚀 Conda project initialized in app/"

# 4. Handle requirements.txt
if [ ! -f "requirements.txt" ]; then
  echo "⚠️ No requirements.txt found, creating an empty one."
  touch requirements.txt
fi

echo "📦 Installing dependencies from requirements.txt..."
conda install -y --file requirements.txt || pip install -r requirements.txt

# 5. List installed packages
echo "📝 Listing installed packages..."
conda list > packages_version.txt

echo "✅ Conda project setup completed. See packages_version.txt for package list."
