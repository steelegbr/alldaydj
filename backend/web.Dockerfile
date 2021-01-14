FROM python:3
WORKDIR /opt/alldaydj

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
RUN apt update
RUN apt install libmp3lame-dev ffmpeg

COPY  . .
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]