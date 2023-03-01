# Minimal python
FROM python:3.11.2-slim AS builder

# Add repo code & install dependencies
ADD . /app
WORKDIR /app
RUN python3 -m pip install -r requirements.txt

# Start command
ENTRYPOINT ["python3"]
CMD ["main.py"]
