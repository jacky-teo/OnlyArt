FROM python:3-slim
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN python -m pip install --no-cache-dir -r requirements.txt
COPY ./payment_log.py ./ invokes.py ./ amqp_setup.py ./  
CMD [ "python", "./payment_log.py" ]