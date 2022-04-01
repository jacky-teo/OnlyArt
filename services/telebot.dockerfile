FROM python:3-slim
WORKDIR /usr/src/app
COPY requirements.txt ./ .env ./
RUN python -m pip install --no-cache-dir -r requirements.txt
COPY ./telebot.py ./
CMD [ "python", "./telebot.py" ]