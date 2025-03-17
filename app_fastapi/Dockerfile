# Imaxe de Python
FROM python:3.9

# Etiqueta do mantedor do Docker
LABEL mantainer "Manuel Magán <a22manuelma@iessanclemente.net>"

# Diretorio de traballo dentro do contedor
WORKDIR /app_fastapi

# Copia o requirements.txt dentro do contedor
COPY requirements.txt .

# Instala as dependencias
RUN pip3 install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copia todo o contido da carpeta da aplicación FastAPI no contedor
COPY . .

# Expón o puerto 8000 para FastAPI
EXPOSE 8000

# Executa a aplicación
CMD ["python3", "src/main.py"]
