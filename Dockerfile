FROM alpine:latest

# Install PostgreSQL
RUN apk update && \
    apk add postgresql postgresql-contrib

# Initialize the database
USER postgres
RUN /etc/init.d/postgresql setup && \
    /etc/init.d/postgresql start && \
    psql --command "CREATE USER postgres WITH SUPERUSER PASSWORD 'dummy_password';" && \
    createdb --owner=postgres airscan

# Expose the PostgreSQL port
EXPOSE 5432

# Start PostgreSQL
CMD ["postgres", "-D", "/var/lib/postgresql/data", "-c", "config_file=/etc/postgresql/postgresql.conf"]