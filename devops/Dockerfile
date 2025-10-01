FROM python:3.12-bullseye

WORKDIR /app

# NOTE - If we copy and install the requirements first, we can take advantage of Docker caching
# to avoid re-installing packages if only the application code changes.
# This is especially useful in development.
COPY devops/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the important bits of code into the container
COPY Makefile .
COPY src/ ./src
COPY csc_dbt/ ./csc_dbt
COPY service_accounts/ ./service_accounts

# Run our pipeline and exit
CMD ["make", "elt"]