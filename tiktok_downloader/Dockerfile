# Step 1: Use the official Python image as the base
FROM python:latest

# Step 2: Set a working directory inside the container
WORKDIR /app

# Step 3: Copy the project files into the container
COPY . /app

# Step 4: Install Python dependencies
#RUN pip install --no-cache-dir yt-dlp requests beautifulsoup4
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose Flask server port
EXPOSE 5000

# Step 5: Set the command to run the program
# Use ENTRYPOINT to default to "python"
ENTRYPOINT ["python"]

# Use CMD to allow specifying which script to run
CMD ["tiktok_downloader.py"]