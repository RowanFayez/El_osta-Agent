FROM python:3.12-slim

WORKDIR /app

# Some environments enable pip hash-checking by default; disable it for this image.
ENV PIP_REQUIRE_HASHES=0

# System deps for some Python wheels (keep minimal)
RUN apt-get update \
  && apt-get install -y --no-install-recommends gcc \
  && rm -rf /var/lib/apt/lists/*

COPY requirements.runtime.txt ./
RUN pip config unset global.require-hashes || true
RUN pip install --no-cache-dir -r requirements.runtime.txt

COPY . .

# Streamlit defaults
EXPOSE 8501

CMD ["streamlit", "run", "app/st_app.py", "--server.address=0.0.0.0", "--server.port=8501"]
