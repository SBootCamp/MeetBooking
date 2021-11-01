FROM python:3.9.5

WORKDIR /home/MeetBooking/

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip3 install --upgrade pip
COPY ./requirements.txt .
RUN pip3 install -r requirements.txt

COPY . .

RUN python3 manage.py collectstatic