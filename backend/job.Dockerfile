FROM python:3
WORKDIR /opt/alldaydj

COPY ./backend/requirements.txt .
RUN apt update
RUN apt install -y libmp3lame-dev ffmpeg
RUN pip install --no-cache-dir -r requirements.txt

COPY  ./backend/ .
CMD ["celery", "-A", "alldaydj", "worker", "-l", "INFO"]