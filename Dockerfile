FROM python:3
ENV PYTHONUNBUFFERED=1
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip3 install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
COPY . /app
ENV FLASK_APP=app.py
ENV FLASK_ENV=development
ENV FLASK_DEBUG=true
EXPOSE 5000
CMD ["sh", "-c", "sleep 5 && python -m flask run --host=0.0.0.0"]