FROM python:3.7.0-alpine

# Copy all the code to the `app` directory
WORKDIR /usr/src/app
COPY . .

# Install dependencies
RUN pip install -r requirements.txt

# Run the app
ENTRYPOINT ["python", "app.py"]
