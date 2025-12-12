# 1. Use a lightweight version of Python as the base
FROM python:3.11-slim

# 2. Set the working directory inside the container
WORKDIR /app

# 3. Copy the requirements file first (for better caching)
COPY requirements.txt .

# 4. Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy the rest of the application code
# We copy specific folders to keep the image clean
COPY src/ ./src/
COPY models/ ./models/

# 6. Expose the port the API runs on
EXPOSE 8000

# 7. The command to start the API when the container runs
CMD ["uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8000"]