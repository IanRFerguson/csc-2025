FROM python:3.12-bullseye

WORKDIR /app

COPY ./devops/requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

RUN mkdir src/ csc_dbt/ service_accounts/
COPY src/ src/
COPY csc_dbt/ csc_dbt/
COPY service_accounts/ service_accounts/
COPY Makefile .

CMD ["make", "pipeline"]