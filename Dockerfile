FROM python:3.13-slim-bookworm

RUN apt update -y && apt install awscli -y
WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt
RUN pip install --upgrade accelerate
RUN pip uninstall -y transformers accelerate
RUN pip install transformers accelerate

CMD ["python3", "app.py"]

#Summary flow of your Dockerfile:

#Use Python 3.13.2 slim base.
#Install AWS CLI.
#Set working directory to /app.
#Copy project files into container.
#Install dependencies.
#Force latest transformers + accelerate.
#Run app.py when container starts.