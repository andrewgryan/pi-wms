FROM python:3.13-alpine
RUN apk add vim
WORKDIR /usr/src/app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["uvicorn", "--port", "8080", "--host", "0.0.0.0", "server:app"]

