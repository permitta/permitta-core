FROM python:3.12-slim-bookworm

# Set default OPA version (can be overridden at build time)
ARG OPA_VERSION=1.7.1

# Create non-root user with UID 1000
RUN groupadd -g 1000 appuser && \
    useradd -u 1000 -g appuser -s /bin/bash -m appuser

RUN mkdir -p /app/permitta-core
WORKDIR /app/permitta-core

# Install Deps
RUN apt-get update && apt-get install -y curl libexpat1 && \
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

# Expose the port the app runs on
EXPOSE 8000

# Switch to non-root user
USER appuser

# Set the entrypoint script
ENTRYPOINT ["/app/entrypoint.sh"]

# Default command (start the server)
CMD ["start-server"]
