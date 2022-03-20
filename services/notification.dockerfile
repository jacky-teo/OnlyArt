FROM python:3-slim
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN python -m pip install --no-cache-dir -r requirements.txt
#COPY command may need to be modified based on what notification needs to run
COPY ./notification.py ./ telebot.py ./ amqp_setup.py ./  
CMD [ "python", "./notification.py" ]