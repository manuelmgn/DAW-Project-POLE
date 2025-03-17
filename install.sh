#!/bin/bash

#########################
###### VARIABEIS ########
#########################

# Repo
REPO_URL="https://gitlab.iessanclemente.net/dawd/a22manuelma.git"

# Docker
CONTAINER_NAME="a22manuelma"
PSGR_CONTAINER="postgres_db"
PGAD_CONTAINER="pgadmin"
FAPI_CONTAINER="fastapi_app"
FLSK_CONTAINER="flask_app"

URL_PGA="http://localhost:5534"
URL_FASTAPI="http://localhost:5535/docs"
URL_FLASK="http://localhost:5536"

PSGR_IP=""

PGA_ok=FALSE
FastAPI_ok=FALSE
FLASK_ok=FALSE

# Outras
emojis_reloxo=("🕐" "🕑" "🕒" "🕓" "🕔" "🕕" "🕖" "🕗" "🕘" "🕙" "🕚" "🕛")

#########################
## FUNCIONS DE FORMATO ##
#########################

# Función para imprimir o texto principal
function texto_principal {
  echo -e "\033[1;35m$1\033[0m"
}

# Función para imprimir o texto secundario
function texto_secundario {
  echo -e "\033[35m$1\033[0m"
}

# Función para imprimir o texto de que todo segue ben
function texto_ok {
  echo -e "\033[33m$1\033[0m"
}

# Función para imprimir texto de erro
function texto_erro {
  echo -e "\033[31m$1\033[0m"
}

#########################
## FUNCIÓNS PRINCIPAIS ##
#########################

# Esperar e imprimir unha liña en branco
function esperar_1_e_imprimir_linha() {
  sleep 1
  echo ""
}

# Función para verificar 1 requisito
function verificar_requisito() {
  local servizo=$1
  local nome_servizo=$2

  if ! command -v $servizo &>/dev/null; then
    texto_erro "   ⛔ Erro: $nome_servizo non está instalado."
    exit 1
  fi
}

# Función para ir chamando as distintas verificacións
function verificar_requisitos() {
  texto_principal "🔍 Verificando requisitos previos..."

  verificar_requisito "docker" "Docker"
  verificar_requisito "git" "Git"

  texto_ok "   👍 Requisitos listos."
  esperar_1_e_imprimir_linha
}

# Escoller o tipo de rama que se vai clonar
function escoller_rama() {
  local resposta=""

  while [ -z "$REPO_RAMA" ]; do
    texto_principal "🌳 Que rama queres usar?"
    texto_ok "   1) 🏠 Main"
    texto_secundario "     Rama principal. Máis estábel".
    texto_ok "   2) 🏗️ Desenvolvemento"
    texto_secundario "     Rama máis inestábel e máis avanzada".
    read -p "   Selecciona una opción (1 o 2): " resposta

    case $resposta in
    1) REPO_RAMA="main" ;;
    2) REPO_RAMA="desenvolvemento" ;;
    *) texto_erro "   Debes seleccionar 1 para Main ou 2 para Desenvolvemento.\n" ;;
    esac
  done
  esperar_1_e_imprimir_linha
}

# Eliminar docker e carpetas antigas
function eliminar_vello() {
  texto_principal "🪓 Vamos eliminar contedores e a información previa!"

  # Elimino o docker
  docker compose down -v 2>/dev/null

  # Elimino a carpeta se xa existe
  if [ -d "$CONTAINER_NAME" ]; then
    # Primeiro intento: sen sudo
    if rm -rf "$CONTAINER_NAME" 2>/dev/null; then
      texto_ok "   👍 Carpeta eliminada correctamente."
    else
      texto_secundario "   🔒 Necesitamos que sexas administrador para borrar arquivos vellos"

      # Segundo intento: con sudo
      if sudo rm -rf "$CONTAINER_NAME" 2>/dev/null; then
        texto_ok "   👍 Carpeta eliminada correctamente."
      else
        texto_erro "   ❌ Non se puido borrar a carpeta $CONTAINER_NAME."
        texto_erro "      Proba a borrala manualmente."
        exit 1
      fi
    fi
  fi

  texto_ok "   👍 Todo listo, seguimos!"
  esperar_1_e_imprimir_linha
}

# Función para clonar o repositorio
function clonar_repo() {
  texto_principal "🐑 Imos clonar o repositorio da aplicación."

  # Intentar clonar
  if ! git clone -b "$REPO_RAMA" "$REPO_URL"; then
    texto_erro "   ⛔ Erro: Non se puido clonar o repositorio."
    texto_erro "      Asegúrate de que as credenciais son correctas."
    exit 1
  fi

  # Tentamos entrar na carpeta
  if ! cd "$CONTAINER_NAME"; then
    texto_erro "   ⛔ Erro: Non se puido entrar no directorio."
    exit 1
  fi

  esperar_1_e_imprimir_linha
}

# Construir a imaxe Docker
function construir_docker() {
  texto_principal "🐳 Estamos a construír o Docker..."
  texto_secundario "   Paciencia"
  docker compose build --no-cache
  esperar_1_e_imprimir_linha
}

# Comprobar se un servizo está a funcionar correctamente
function comprobar_servizo() {
  local container=$1
  local url=$2
  local varname=$3

  if curl --output /dev/null --silent --head --fail "$url"; then
    if [ "$(docker inspect -f '{{.State.Status}}' "$container")" == "running" ]; then
      eval "$varname=TRUE"
    fi
  fi
}

# Función para ir comprobando os distintos servizos
function comprobar_servizos() {
  texto_principal "🥁 Moi ben, agora imos verificar se todo funcionou..."
  echo -n "   "
  for emoji in "${emojis_reloxo[@]}"; do
    echo -n "$emoji"
    sleep 1
  done
  echo ""

  comprobar_servizo "$PGAD_CONTAINER" "$URL_PGA" "PGA_ok"
  comprobar_servizo "$FLSK_CONTAINER" "$URL_FLASK" "FLASK_ok"
  comprobar_servizo "$FAPI_CONTAINER" "$URL_FASTAPI" "FastAPI_ok"
  PSGR_IP=$(docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' "$PSGR_CONTAINER")
  
  esperar_1_e_imprimir_linha
}

# Imprimir as mensaxes dependendo do estado do servizo
function reporte_servizo() {
  local estado=$1
  local nombre=$2
  local url=$3

  if [ "$estado" == "TRUE" ]; then
    texto_ok "   ✔️ $nombre está a funcionar."
    texto_secundario "      Accede en '$url'"
  else
    texto_erro "   🚧 $nombre debería ser acesíbel desde '$url', pero non funciona."
  fi
}

# Función que vai dando o reporte final dos servizos
function reporte_servizos() {
  if [ "$PGA_ok" == "TRUE" ] && [ "$FLASK_ok" == "TRUE" ] && [ "$FastAPI_ok" == "TRUE" ]; then
    texto_principal "✅ Todo listo!"
  else
    texto_erro "😢 Parece que hai algún problema..."
    texto_erro "   Contacta co administrador ou executa manualmente a instalación"
  fi

  sleep 1

  reporte_servizo "$FastAPI_ok" "FastAPI" "$URL_FASTAPI"
  reporte_servizo "$FLASK_ok" "Flask" "$URL_FLASK"
  reporte_servizo "$PGA_ok" "PGAdmin" "$URL_PGA"

  if [ "$PGA_ok" == "TRUE" ]; then
    texto_secundario "      Podes conectalo a PostgreSQL coa IP $PSGR_IP:5432."
  fi
}

#########################
#### LÓXICA EXECUCIÓN ###
#########################

# Verificar requisitos
verificar_requisitos

# Escoller rama
escoller_rama

# Elimino arquivos e docker vello
eliminar_vello

# Clona o repo e, se algo vai mal, sae da execución
clonar_repo || exit 1

# Construir a imaxe Docker
construir_docker

# Iniciar os contedores
texto_principal "👟 Todo listo para iniciar os contedores."
docker compose up -d
esperar_1_e_imprimir_linha

# Comprobar servizos
comprobar_servizos

# Reporte final dos servizos
reporte_servizos

esperar_1_e_imprimir_linha
exit
