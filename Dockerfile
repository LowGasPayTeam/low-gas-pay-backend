FROM python:3.9-slim AS compile-image
RUN apt-get upgrade & \
    apt-get install -y --no-install-recommends build-essential gcc & \
    python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
COPY requirements.txt .
RUN pip install -r requirements.txt

FROM python:3.9-slim AS build-image
COPY --from=compile-image /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH" FLASK_ENV="PRD"
WORKDIR /low-gas-pay-backend
COPY . .
CMD ["gunicorn","-w","4","-b","0.0.0.0:9999","--log-level=info","run:app"]
