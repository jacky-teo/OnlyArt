FROM python:3-slim
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN python -m pip install --no-cache-dir -r requirements.txt
COPY ./post_content.py ./ invokes.py ./ amqp_setup.py ./ telebot.py ./ firebase.py ./
CMD [ "python", "./post_content.py" ]