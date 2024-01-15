FROM python:3.10-slim

#
LABEL maintainer="mkhaikin@yandex.ru"

#
WORKDIR /.

#
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONBUFFERED 1

#
COPY . .

#
RUN pip install --no-cache-dir --upgrade -r /requirements.txt

#
CMD ["uvicorn", "app.main:app", "--workers", "2", "--host", "0.0.0.0", "--port", "8000"]
