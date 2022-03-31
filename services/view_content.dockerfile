FROM python:3-slim
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN python -m pip install --no-cache-dir -r requirements.txt
COPY ./view_content.py ./ amqp_setup.py ./ invokes.py ./
CMD [ "python", "./view_content.py" ]