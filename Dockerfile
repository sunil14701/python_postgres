FROM python:3.9

WORKDIR /app

COPY requirement.txt .

RUN pip install -r requirement.txt

COPY app .

ENTRYPOINT [ "fastapi", "run", "main.py", "--port", "8000" ]