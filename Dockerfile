# 1. BASE IMAGE: Start with the required Python version
FROM python:3.11-slim

# 2. WORKING DIRECTORY: Set the default folder inside the container
WORKDIR /app

# 3. DEPENDENCIES: Copy the requirements files
COPY requirements.txt .
COPY ta_requirements.txt .

# CRITICAL FIX: Add system dependencies (kept for safety)
# This installs tools like GCC to allow Python packages to compile from source.
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc libpq-dev && \
    rm -rf /var/lib/apt/lists/*

# Install all main dependencies first (easier to install)
RUN pip install --no-cache-dir -r requirements.txt

# Install the problematic package separately (Final fix for dependency conflict)
RUN pip install --no-cache-dir -r ta_requirements.txt

# 4. APPLICATION CODE: Copy the rest of your project files (including app.py and .pkl files)
COPY . .

# 5. PORT: Inform the container runtime which port the app will listen on
EXPOSE 8080

# 6. RUN COMMAND: Execute the production server (Gunicorn)
# The format is [Python_File_Name]:[Flask_App_Instance_Name]
CMD exec gunicorn --bind :8080 --workers 2 --threads 4 app:app