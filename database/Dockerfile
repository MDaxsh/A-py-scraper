FROM postgres:15-alpine

# Copy initialization scripts
COPY scripts/ /docker-entrypoint-initdb.d/

EXPOSE 5432
