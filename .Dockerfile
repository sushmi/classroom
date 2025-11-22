FROM python:3.11.4-slim-bookworm

# update OS packages to pick up security fixes
RUN set -eux; \
	apt-get update && apt-get upgrade -y && apt-get install -y --no-install-recommends ca-certificates && \
	rm -rf /var/lib/apt/lists/*

WORKDIR /app

# create a non-root user for better security
RUN addgroup --system app && adduser --system --ingroup app app

# install Python dependencies in one layer without cache and avoid duplicate installs
RUN pip3 install --no-cache-dir dash pandas numpy scikit-learn "dash-bootstrap-components[pandas]" "dash[testing]"

COPY ./src/app /app

USER app

CMD ["tail", "-f", "/dev/null"]