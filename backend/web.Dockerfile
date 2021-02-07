FROM python:3
WORKDIR /opt/alldaydj

RUN apt update
RUN apt install -y libmp3lame-dev ffmpeg

COPY ./backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY  ./backend/ .
RUN chmod +x launch.sh
CMD ["./launch.sh"]