# 1. BASE IMAGE: Start with a reliable, lightweight Python environment
FROM python:3.10-slim

# 2. WORKING DIRECTORY: Set the default folder inside the container
WORKDIR /app

# 3. DEPENDENCIES: Copy the requirements file and install packages
COPY requirements.txt .

# *** CRITICAL FIX: Add system dependencies for building packages from source ***
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc libpq-dev && \
    rm -rf /var/lib/apt/lists/*

# Install Python packages
RUN pip install --no-cache-dir -r requirements.txt
# ******************************************************************************

# 4. APPLICATION CODE: Copy the rest of your project files
# This includes app.py, your model.pkl, etc.
COPY . .

# 5. PORT: Inform the container runtime which port the app will listen on
EXPOSE 8080

# 6. RUN COMMAND: Execute the production server (Gunicorn) when the container starts
# CRITICAL FIX: Use app:app
CMD exec gunicorn --bind :8080 --workers 2 --threads 4 app:app