# Use an official Python runtime as a parent image
FROM python:3

# Set the working directory to /CountBoxes
WORKDIR /CountBoxes

# Copy the current directory contents into the container at /app
COPY . /CountBoxes

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Run smart_course_tagging_compiled.py when the container launches
CMD ["python", "count_boxes.py"]