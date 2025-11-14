FROM selenium/standalone-chrome:latest

WORKDIR /app
COPY . /app

# Change ownership to seluser
USER root
RUN chown -R seluser:seluser /app
USER seluser

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# CMD
CMD ["python", "sora.py"]
