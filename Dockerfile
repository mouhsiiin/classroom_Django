FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Copy the dependencies file to the working directory
COPY InTouchLearn/requirments.txt .

# Install any dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the content of the local src directory to the working directory
COPY . .

# Collect the Django static files
RUN python manage.py collectstatic --no-input

# Expose the port the Django app will run on
EXPOSE 8000

# Set the command to start the Django app
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]