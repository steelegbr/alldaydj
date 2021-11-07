FROM python:3.9
WORKDIR /opt/alldaydj

RUN apt update
RUN apt install -y ffmpeg

COPY ./backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install gunicorn

COPY  ./backend/ .
RUN chmod +x launch.sh
CMD ["./launch.sh"]