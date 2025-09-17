FROM python:3.12-bullseye

WORKDIR /app

COPY devops/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY Makefile .
COPY src/ ./src
COPY csc_dbt/ ./csc_dbt
COPY service_accounts/ ./service_accounts

CMD ["make", "elt"]