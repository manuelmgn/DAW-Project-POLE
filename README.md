# POLE, proxecto de Manuel Magán

<div align="center">
    <img src="documentacion/img/logo-1.3-web.png" width="300" title="POLE logo" alt="POLE logo">
</div>

## Descrición

Aplicación destinada ao control persoal das alerxias e ao seguimento dos niveis de pole cun enfoque comunitario. Con POLE poderás rexistrar o lugar e a intensidade dos teus síntomas derivados da alerxia aos distintos tipos de pole. Esta información é empregada para analizar o nivel de pole en cada zona e dar información completa aos usuarios. Así, cando entras en POLE non ves soamente a cantidade de pole no ar e a previsión meteorolóxica (aínda que estas características tamén están presentes), senón tamén como se sinten outros usuarios na túa zona e un historial dos teus propios rexistros. Grazas a esta información poderás planificar mellor o teu día e saber como precisas protexerte do pole.

![Paseo pola aplicación](/documentacion/img/CleanShot%202024-12-10%20at%2019.14.44-converted%202.mp4) ([link para mellor calidade](https://share.cleanshot.com/2Vf7RHmy))*

## Índices

### README

- [Descrición](#descrición)
- [Índices](#índices)
  - [README](#readme)
  - [Estrutura de arquivos](#estrutura-de-arquivos)
- [Instalación e configuración](#instalación-e-configuración)
  - [Introdución](#introdución)
  - [Requisitos previos](#requisitos-previos)
  - [Instalación](#instalación)
  - [Aceso](#aceso)
  - [Configuración](#configuración)
- [Uso](#uso)
- [Sobre o autor](#sobre-o-autor)
- [Licencia](#licencia)
- [Guía de contribución](#guía-de-contribución)

### Estrutura de arquivos

-   ⚡ **[FastAPI](/app_fastapi/)** (`app_fastapi`)
    -   📂 [src](/app_fastapi/src/)
        -   📂 [auth](/app_fastapi/auth)
        -   📂 [database](/app_fastapi/database)
        -   📂 [external_apis](/app_fastapi/external_apis)
        -   📂 [user_logs](/app_fastapi/user_logs/)
        -   📂 [users](/app_fastapi/users/)
        -   🐍 config.py
        -   🐍 main.py
        -   🐍 security.py
        -   🐍 utils.py
    -   🐳 [Dockerfile](/app_fastapi/Dockerfile)
    -   📝 [requirements.txt](/app_fastapi/requirements.txt)
-   📯 **[Flask](/app_flask/)** (`app_flask`)
    -   📂 [src](/app_flask/src/)
        -   📂 [config](/app_flask/config/)
        -   📂 [forms](/app_flask/forms/)
        -   📂 [routes](/app_flask/routes/)
        -   📂 [static](/app_flask/static/)
        -   📂 [templates](/app_flask/templates/)
        -   📂 [utils](/app_flask/utils/)
        -   🐍 app.py
        -   🐍 models.py
    -   🐳 [Dockerfile](/app_flask/Dockerfile)
    -   📝 [requirements.txt](/app_flask/requirements.txt)
-   🐘 **[PostgreSQL](/db/)** (`db`)
-   🐘 **[PostgreSQL - Admin](/db_admin/)** (`db_admin`)
-   📂 **[Documentación](/documentacion/)** (documentacion)
    -   📂 [IMG](/documentacion/img/): Imaxes do proxecto, como capturas de pantalla e logotipos.
    -   📂 [Outros documentos](/documentacion/outros-documentos/): Guías e documentos de referencia, no seu estado orixinal, para a elaboración do proxecto e da súa documentación.
    -   📝 [Documentación](/documentacion/documentacion.md): Anteproxecto entregábel para a FP.
    -   📝 [Imaxe](/documentacion/imaxe.md): Documentación sobre a imaxe e o deseño da aplicación.
    -   📝 [Ligazóns de interese / Webgrafía](/documentacion/links.md).
    -   📝 [README](/documentacion/documentacion.md).
-   🐳 **[Docker compose](/docker-compose.yml)** (`docker-compose.yml`)
-   👟 **[Script de instalación](/install.sh)** (`install.sh`): Script de instalación.
-   📝 **[README.md](/README.md)**

## Instalación e configuración

### Introdución

-   A aplicación corre sobre contedores [Docker](https://www.docker.com/), polo que é preciso ter instalado este programa. É recomendábel descargar o código desde GitLab, polo que tamén é conveniente ter Git instalado.
-   Python e o resto de requirimentos da aplicación son instalados dentro do contedor.

### Requisitos previos

-   Docker
-   Docker Compose
-   Git

### Instalación

#### Opción 1: Script de instalación

1. Descargar o script `install.sh`.
2. Executalo.

    ```bash
    ./install.sh
    ```

3. Seguir os pasos.

#### Opción 2: Docker compose

1. Clonar o repositorio

    ```bash
    git clone https://gitlab.iessanclemente.net/dawd/a22manuelma.git
    cd a22manuelma
    ```

2. Construir a imaxe Docker

    ```bash
    docker compose build
    ```

3. Iniciar os contedores

    ```bash
    docker compose up
    ```

### Aceso

- PostgreSQL:
    -   URL para aceso desde aplicativos locais[`http://localhost:5533/`](http://localhost:5533)
    -   URL para aceso desde o propio Docker: `172.18.0.2:5432`.
-   PGAdmin:
    -   [`http://localhost:5534/`](http://localhost:5534)
    -   A conexión coa base de datos realízase mediante o enderezo indicado anteriormente.
    -   Os datos de acceso encóntranse no [docker-compose.yml](/docker-compose.yml).
-   FastAPI:
    -   [`http://localhost:5535/`](http://localhost:5535/)
    -   Documentación: [`http://localhost:5535/docs`](http://localhost:8000/docs)
-   Flask (vista principal):
    -   [`http://localhost:5536/`](http://localhost:5536/)

### Configuración

-   Non é necesario realizar ningún tipo de configuración nin cambios no código para usar a aplicación.
-   Recomendamos crear usuarios e realizar distintos rexistros para probala correctamente.
-   Para facilitar as probas, créase automaticamente un usuario administrador. Pode rexistrarse co nome de usuario `admin` e o contrasinal `123`. Recoméndase iniciar sesión con él, despois de ter creado usuarios e rexistros de síntomas, e facer probas. Ao iniciar sesión poderase acceder ao menú de Administración.

## Uso

-   Para usar a aplicación (como un usuario corrente) recomendamos seguir os seguintes pasos:
    -   Rexistrar un novo usuario e iniciar sesión.
    -   Crear distintos rexistros de síntomas de alerxia.
    -   Consultar o mapa, a previsión meteorolóxica, e o historial de rexistros (dentro de usuario).
-   Para testear os aspectos da app recomendamos:
    -   Crear varios usuarios.
    -   Realizar distintos tipos de rexistros, con distintas intensidade e en distintas localizacións (a maioría próximas, para ver como se comporta a aplicación).
    -   Crear un usuario administrador e tentar, por exemplo, borrar un usuario existente.

## Sobre o autor

Manuel Magán é Doutor pola Universidade de Santiago de Compostela e actualmente está a formarse como desenvolvedor web. Ten estudado distintas tecnoloxías e linguaxes de programación, mais no seu curriculum destacan **Python** e **Javascript**, as mesmas que se empregan principalmente nesta aplicación.

A orixe de POLE está na conversa entre dous amigos, un deles alérxico, sobre a necesidade de crear unha aplicación distinta ás existentes e cun enfoque comunitario, xa que, ao parecer, os datos como a cantidade de pole no aire resultan insuficientes para predicir como será a doenza cada día.

É posíbel contactar co desenvolvedor a través do correo electrónico persoal [manuel.ma@posteo.net](mailto:manuel.ma@posteo.net).

## Licencia

Este proxecto emprega unha licencia GNU GPLv3.

## Guía de contribución

Este proxecto está aberto a calquera tipo de contribución:

-   Desenvolvemento de Aplicación para Smartphones.
-   Desenvolvemento dunha Progressive Web App.
-   Desenvolvemento de Funcionalidades: Podes propor algunhas, mellorar as existentes ou desenvolver outras, como por exemplo o envío de notificación a través do navegador.
-   Corrección de erros: identifica e corrixe bugs existentes.
-   Optimización do código.
-   Probas automatizadas.
-   Mellora do frontend e da accesibilidade.
