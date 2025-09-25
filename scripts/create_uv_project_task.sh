#!/usr/bin/env bash
set -e

# create_uv_project_task.sh - Setup a uv project with environment and dependencies

# 1. Create environment in current directory
echo "🔧 Creating environment with uv..."
uv venv

echo "📦 Activating environment..."
source .venv/bin/activate

# 2. Initialize a uv project
echo "🚀 Initializing uv project..."
uv init

# 3. Handle requirements.txt
REQ_FILE="requirements.txt"
if [ ! -f "$REQ_FILE" ]; then
    echo "⚠️ No requirements.txt found, creating an empty one."
    touch "$REQ_FILE"
fi

echo "📦 Installing dependencies from $REQ_FILE..."
uv add -r "$REQ_FILE"

# 4. List all installed packages with versions
echo "📝 Listing installed packages..."
uv pip list > packages_version.txt

echo "✅ UV project setup completed. See packages_version.txt for package list."
