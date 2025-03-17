# Imaxe oficial PostgreSQL
FROM postgres:13

# Copia o arquivo SQL de inicialización banaarpeta de inicialización do contenedor
COPY init.sql /docker-entrypoint-initdb.d/

# Expón o puerto 5432 para PostgreSQL
EXPOSE 5432
