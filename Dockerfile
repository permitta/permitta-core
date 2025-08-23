FROM python:3.12-slim-bookworm

# Set default OPA version (can be overridden at build time)
ARG OPA_VERSION=1.7.1

WORKDIR /app

# Install OPA
RUN apt-get update && apt-get install -y curl && \
    curl -L -o /usr/local/bin/opa https://github.com/open-policy-agent/opa/releases/download/v${OPA_VERSION}/opa_linux_amd64_static && \
    chmod 755 /usr/local/bin/opa && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY permitta-core/ /app/permitta-core/

# Copy the entrypoint script
COPY entrypoint.sh /app/
RUN chmod +x /app/entrypoint.sh

# Set environment variables
ENV PYTHONPATH=/app/permitta-core/src
ENV FLASK_APP=permitta-core.src.app

# Set default values for required environment variables
# These can be overridden when running the container
ENV FLASK_SECRET_KEY=default_secret_key_change_me_in_production
ENV OIDC_AUTH_PROVIDER_CLIENT_SECRET=default_client_secret_change_me_in_production

# Expose the port the app runs on
EXPOSE 8000

# Set the entrypoint script
ENTRYPOINT ["/app/entrypoint.sh"]

# Default command (start the server)
CMD ["start-server"]
