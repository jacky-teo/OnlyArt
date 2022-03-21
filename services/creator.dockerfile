FROM python:3-slim
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN python -m pip install --no-cache-dir -r requirements.txt
COPY ./creator_account.py ./ 
CMD [ "python", "./creator_account.py" ]