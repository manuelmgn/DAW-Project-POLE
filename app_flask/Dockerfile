# Imaxe de Python
FROM python:3.9

# Etiqueta do mantedor do Docker
LABEL mantainer "Manuel Magán <a22manuelma@iessanclemente.net>"

# Diretorio de traballo dentro do contedor
WORKDIR /app_flask

# Copia o requirements.txt dentro do contedor
COPY requirements.txt requirements.txt

# Instala as dependencias
RUN pip3 install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copia todo o contido da carpeta app_flask no contedor
COPY . .

# Expón o porto 5000 para Flask. Non debe cambiar, mesmo se o porto co que Flask sae ao exterior é outro.
EXPOSE 5000

# Comando para correr a aplicación Flask. O porto non debe cambiar, mesmo se o porto co que Flask sae ao exterior é outro.
CMD ["python3", "src/app.py"]
#CMD ["gunicorn", "src.app:app", "-b", "0.0.0.0:5000"]