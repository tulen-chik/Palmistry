FROM python:3.12.1
# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt /app/
RUN pip install torch --index-url https://download.pytorch.org/whl/cpu
RUN pip install -r requirements.txt

# Copy the project code into the container
COPY .. /app/
EXPOSE 10000
CMD ["python3", "bot.py"]