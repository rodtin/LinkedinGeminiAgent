FROM python:3.11-slim

WORKDIR /app

# Install dependencies (system)
# RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

# Copy dependency definition first (if we had requirements.txt, but here we run pip direct)
RUN pip install --no-cache-dir google-generativeai tavily-python python-telegram-bot schedule python-dotenv requests openai

# Copy the entire workspace
# Note: We rely on .dockerignore to skip .venv / .git if present, 
# but ignoring them here manually via COPY scope is harder without .dockerignore file.
# We will just copy everything for simplicity.
COPY . /app/

# Set Python path to include root
ENV PYTHONPATH=/app

CMD ["python", "Automation/bot.py"]
