FROM python:3-slim
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN python -m pip install --no-cache-dir -r requirements.txt
COPY ./subscription_link.py ./
CMD [ "python", "./subscription_link.py" ]