FROM --platform=linux/amd64 python:3.10-slim
LABEL authors="egorgrekov"

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["pyhton main.py"]