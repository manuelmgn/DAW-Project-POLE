# Documentación

- [Idea](#idea)
- [Estudo de necesidades e modelo de negocio](#estudo-de-necesidades-e-modelo-de-negocio)
  - [Posibilidades de comercialización](#posibilidades-de-comercialización)
  - [Ideas para a súa comercialización](#ideas-para-a-súa-comercialización)
- [Requirimentos do sistema](#requirimentos-do-sistema)
  - [Funcionalidades](#funcionalidades)
  - [Tipos de usuarios](#tipos-de-usuarios)
  - [Avaliación da viabilidade técnica do proxecto](#avaliación-da-viabilidade-técnica-do-proxecto)
  - [Interfaces externas](#interfaces-externas)
  - [Análise de riscos e interesados](#análise-de-riscos-e-interesados)
  - [Melloras futuras](#melloras-futuras)
- [Fase de planificación do proxecto](#fase-de-planificación-do-proxecto)
  - [Obxectivos do proxecto](#obxectivos-do-proxecto)
  - [Guía de planificación do proxecto](#guía-de-planificación-do-proxecto)
  - [Orzamento](#orzamento)
- [Fase de deseño](#fase-de-deseño)
  - [Modelo conceptual](#modelo-conceptual)
  - [Caso de uso](#caso-de-uso)
  - [Deseño de interface de usuarios (mockups)](#deseño-de-interface-de-usuarios-mockups)
  - [Diagrama de Base de Datos](#diagrama-de-base-de-datos)
- [Fase de implantación](#fase-de-implantación)
  - [Manual técnico](#manual-técnico)
  - [Xestión de incidencias](#xestión-de-incidencias)
  - [Protección de datos de carácter persoal](#protección-de-datos-de-carácter-persoal)
  - [Manual de usuario](#manual-de-usuario)

## Idea

A polinose é, tal e como a define o [Ministerio de Saúde de España](https://www.sanidad.gob.es/ciudadanos/enfLesiones/enfNoTransmisibles/alergias.htm), unha enfermidade alérxica que afecta, aproximadamente, ao 15% da poboación e que duplica a súa incidencia entre as persoas máis novas. Pese a representar unha porcentaxe tan significativa da sociedade, semella que aínda non se teñen desenvolvido ferramentas tecnoloxías realmente útiles que axuden a lidar con esta doenza no día a día.

Inspirados por unha persoa alérxica, o propósito do noso proxecto será tratar de desenvolver, de forma práctica, unha aplicación web que poida chegar a axudar ás persoas que sofren a alerxia ao pole.

Na actualidade, a maioría das aplicacións existentes, tanto as pensadas para a web como aquelas para Android ou iOS, basean a súa funcionalidade principal na medición do pole e na calidade do aire dos últimos días, mais rara vez do día presente. A pesar de que estes datos son útiles, e que adoitan ir acompañados da previsión meteorolóxica, esta información continúa a ser demasiado xeral e ambigua, xa que non todas as persoas se ven igualmente afectadas pola cantidade de partículas de pole presentes no aire ou o tempo. Por iso, consideramos que estas aplicacións poden ser melloradas.

Por un lado, as melloras poden vir da man do rexistro do nivel de alerxia de cada persoa, para que a doente poida acceder a un historial propio que lle axude a prever posíbeis síntomas futuros.

Por outro, facendo que a nosa aplicación sexa colaborativa, partiremos dos rexistros de cada usuario para agregar unha terceira capa xeral ao noso mapa de alerxias, que se sumará ao da calidade do aire e ao da previsión meteorolóxica. Grazas a saber en tempo real como están a sofrer a polinose outras persoas da mesma contorna, os usuarios terán máis pistas de como a poden sofrer eles ese día.

Para cumprir o noso propósito, tentaremos facer unha aplicación visualmente atractiva e sinxela e que poida mostrar a información máis relevante. Deseñarémola cunha idea en mente: que unha persoa alérxica, antes de saír de casa, poida ter en poucos clics a información suficiente que lle permita prever o seu nivel de alerxia dese día e, en última instancia, que sexa quen de decidir como medicarse.

Dado que non existen aplicacións como esta, consideramos que podemos encontrar unha **oportunidade de negocio** aquí, aínda que para poder comezar a funcionar con normalidade, a _app_ requiriría dunha base de usuarios sólida, polo que achamos que precisaría dunha inversión inicial. Isto, de calquera modo, ficaría como unha tarefa pendente para futuros estadios de desenvolvemento.

Durante a primeira fase, os **requisitos** que nos marcamos teñen que máis ver coa construción e o funcionamento básico. É dicir, pretendemos conseguir unha aplicación funcional, usábel e que conteña as principais características descritas, así como unha correcta xestión dos usuarios.

Para lograr isto, tal e como se explicará nos próximos apartados, o noso primeiro obxectivo será elaborar unha aplicación web, deixando pendentes para futuras fases as versións para _smartphones_. Isto conseguirase dividindo o **_backend_** en dúas partes: unha encargada de servir a aplicación web (usando o _framework_ de Python Flask) e outra destinada en exclusiva a proporcionar as APIs que se van usar nas distintas aplicacións. Para isto usaremos outro _framework_ de Python, neste caso o popular e recente FastAPI. Como **base de datos** empregaremos PostgreSQL.

O **_frontend_** da web, pola súa parte, realizarase con Javascript, HTML e CSS. Para melloralo, usaremos tamén Bootstrap, aínda que tamén desenvolveremos o noso propio CSS cando sexa máis cómodo.

## Estudo de necesidades e modelo de negocio

A **xustificación** deste proxecto reside, tal e como se explicou anteriormente, na limitación das aplicacións existentes no tocante ao seguimento das alerxias provocadas polo pole. Do noso punto de vista, crear unha comunidade na que se comparta como está sofrer cada persoa a alerxia cada día, pode ser un modo de paliar o problema. A información extraída de cada usuario, xunto con datos máis xerais –como os meteorolóxicos e as medicións de pole– e o historial persoal de cada un, pode constituír unha fonte de datos moi valiosa que pode axudar moito aos usuarios.

O noso **propósito** é limitar o uso da aplicación a persoas rexistradas, de modo que poidamos trazar con máis facilidade a orixe dos datos. Unha vez dentro da _app_, poderase valorar dentro dunha simple escala a intensidade dos síntomas da alerxia nun momento concreto. De cada rexistro obteranse tamén a data, a hora e a localización. Esta última pode provir directamente do momento do rexistro, se está habilitada a opción de compartir a localización. Do contrario, tomarase por defecto aquela que o usuario marcase como habitual durante o rexistro ou no seu panel de control.

Os datos proporcionados en cada rexistro serán analizados xunto con doutros realizados en horas e localizacións próximas, e o resultado será o que poida ver cada usuario na súa pantalla de inicio, así como outros xa mencionados e que non dependen da interacción da comunidade. Deste modo, cada persoa poderá axudar a mellorar a aplicación.

Dada a importancia da interacción dos usuarios, unha parte moi importante da metodoloxía de traballo será a consulta con doentes de polinose. Este será o único apartado da mesma na que faga falta máis dunha persoa para traballar. Neste caso, cantas máis **persoas** alérxicas poidan aconsellar e probar a app, máis beneficioso será para nós. Con todo, non podemos prever canta xente necesitaremos, nin canta teremos á nosa disposición, máis aló dunhas poucas persoas que xa se ofreceron a colaborar.

Este mencionado apartado será o único no que a **metodoloxía** poida resultar, _a priori_, distinta da maioría dos proxectos de desenvolvemento de software, xa que o noso traballo se vai centrar en programar. Así e todo, podemos trazar _grosso modo_ algunhas das fases principais do desenvolvemento da aplicación:

1. Análise e recollida de información
2. Deseño da aplicación e da súa arquitectura
3. Creación da estrutura básica da aplicación e da base de datos, e do Docker
4. Desenvolvemento e programación, comezando polo backend e aspectos fundamentais
5. Tests e probas
6. Proba con usuarios reais
7. Documentación

Por suposto, ningún dos anteriores puntos constitúe unha fase illada nin o proceso se vai realizar soamente nunha dirección. De forma constante volverase atrás e moitas das etapas mencionadas poderán acontecer á vez que outras.

O **tempo** do que dispoñemos para realizar a aplicación é moi limitado (10 semanas, aproximadamente) e, dentro deste, a dedicación diaria tamén é moi cativa. Debemos ter en conta que durante o mesmo período se estarán a realizar prácticas na empresa DistriSantiago, o que implica non poder contar con 8 horas de luns a venres, nin co tempo preciso para ir e volver desde Santiago (40 minutos cada viaxe), así como co tempo necesario para levar a cabo outras tarefas necesarias do día a día. Por isto, entendemos que o proxecto non debe ser ambicioso en exceso, e tampouco podemos garantir que todas as fases se vaian completar satisfactoriamente ou, ao menos, do modo en que o temos pensado e en que se formulan neste anteproxecto.

De todos modos, para conseguir isto, poremos a disposición uns **medios** limitados, pero achamos que suficientes: ordenadores persoais e un NAS doméstico sobre o que o poder correr permanentemente a aplicación web unha vez o seu desenvolvemento o permita.

### Posibilidades de comercialización

As posibilidades de comercialización dun proxecto de software son moi relativas e a análise corresponderíalle a unha persoa con coñecementos especializados no tema. A breve historia das aplicacións web, e a Historia en xeral, téñennos demostrado que as boas ideas e os bos proxectos non son sempre viábeis e que, mesmo se o son, as súas posibilidades de comercialización poden resultar escasas. Proba disto son numerosas aplicacións de software libre, descoñecidas para o gran público por non dispor de medios económicos cos que competir; grandes fracasos de grandes compañías, como a rede social Google+, ou outros moitos. Pese a todo, vamos analizar brevemente a **viabilidade** do proxecto e a súa competencia.

En primeiro lugar, cómpre deixar claro que, _a priori_, será posíbel dispoñer dos medios materiais e humanos necesarios para facer a aplicación xa que, tal e como se apuntou anteriormente, estes son xa de por si moi limitados. Os únicos impedimentos técnicos que se contemplan son aqueles producidos por causas inesperadas, como a posíbel avaría dos computadores, por exemplo.

En canto á **viabilidade económica**, tal e como temos dito, resúltanos imposíbel medir tal parámetro. Con todo, existen algunhas axudas ás que, dependendo da evolución do proxecto, poderíamos considerar optar. Algunhas delas son as de Enisa, como a destinada a [emprendedores menores de 40 anos](https://www.enisa.es/es/financia-tu-empresa/lineas-de-financiacion/d/jovenes-emprendedores); [Activa Startups](https://one.gob.es/es/ayudas-y-convocatorias/activa-startups); [Pyme Innova](https://www.camara.es/innovacion-y-competitividad/pyme_innova); o [EIC Accelerator](https://eic.ec.europa.eu/eic-funding-opportunities/eic-accelerator_en#who-can-apply), ou as [Ayudas Neotec](https://www.cdti.es/ayudas/ayudas-neotec-2024).

Estas subvencións e liñas de axudas poderen favorecer a **competencia** con outras apps con cometido semellante ao noso.

-   Alerta Pólen, de Protosoft. É a mellor valorada en tendas como a Play Store. Carece de aplicación web e de app para iOS.
-   Alerta Pólenes, da SEAIC (Sociedad Española de Alergología e Inmunología Clínica). Ten aplicación web, para Android e para iOS, pero nas tendas oficiais destes sistemas recibe moi malas valoracións e as apps teñen poucas descargas. A súa aplicación web é máis informativa que útil para o día a día.
-   Polen Control, de Almirall e tamén a SEAIC. Tamén con malas _reviews_.
-   Polen, da Comunidade de Madrid. Tamén con malas valoracións.
-   Pollen+, de Screencode. Semella unha aplicación interesante e con boa aceptación.
-   Polen REA, da Rede Aerobiolóxica Española. Non recibe actualizacións desde hai máis dun ano.
-   Polen Wise, de Pollen Sense LLC. Parece unha das máis interesantes.
-   xEco Polen, de Dejan Lekić. Non recibe actualizacións desde hai máis de 2 anos.
-   Poderíamos contar como competencia todas aquelas aplicacións de tempo que permiten ver tamén os niveis de pole.
-   Tamén podemos incluír neste apartado aquelas webs que inclúen mapas e nos que permiten ver, por provincias, os niveis de pole. Algunhas son de empresas, como [Rino-Ebastel](https://www.rinoebastel.com/nivel-polen/), e outras de institucións públicas estatais ou das distintas comunidades autónomas, como [REA](https://www.redespanoladeaerobiologia.com/mapa.html), [AVAIC](https://avaic.es/index.php/niveles-de-polen/), a de [Castilla y León](https://analisis.datosabiertos.jcyl.es/pages/polen/), a de [Castilla-La Mancha](https://www.polencastillalamancha.com/) ou a da [Universidad de Córdoba](https://www.uco.es/investiga/grupos/rea/?page_id=262). Todas elas moi simples en funcionalidades.

### Ideas para a súa comercialización

No curto prazo, consideramos que carece de todo sentido facer un prognóstico da comercialización do noso produto. Como xa se dixo, o tempo e os recursos son limitados, e estes deben inverterse en programar a nosa _app_. Agora ben, nun hipotético futuro no que a aplicación estivese lista, e nun pensamento a longo prazo, probabelmente decidiría facer o mesmo que a maioría de empresas: aproveitarme de redes sociais gratuítas, subir o contido xusto para que non ser penalizado polos seus algoritmos, pagar por unha publicación patrocinada de cando en vez e tentar ter presenza en actos empresariais para proxectar imaxe social.

Por motivos semellantes aos anteriores, son completamente incapaz de saber que tipo de modelo de negocio terá a miña aplicación no seu futuro. Por tanto, a miña resposta estará baseada, de novo, no que fan a maioría de empresas: ofrecerase un plano gratuíto con publicidade no que se vendan os datos das persoas a empresas de _marketing_ ou doutros sectores (como farmacéuticas), e un plano con subscrición mensual no que se respectará a privacidade.

## Requirimentos do sistema

### Funcionalidades

-   Xestión de usuarios.
-   Visión dos niveis de pole.
-   Xestión de rexistros da intensidade dos síntomas.

### Tipos de usuarios

Só haberá un tipo de usuario que poida acceder a esta aplicación (alén do administrador): aquel que se rexistre. Unha vez completen o seu rexistro, todos os usuarios terán acceso ás mesmas pantallas e mesmos permisos, que son aqueles que se veñen describindo ao longo da documentación.

Tal e como se dixo, non se permitirán os usuarios anónimos, xa que consideramos que é importante forzar o rexistro, para así, en segunda instancia, favorecer a interacción.

De cumprir coas hipóteses de apartados anteriores, quizais fose preciso diferenciar tamén entre usuarios subscritos (que pagan) e usuarios que non. Isto, de todos modos, non corresponde a este estadio do desenvolvemento.

O outro tipo de usuario é o administrador, aquel capaz de modificar, eliminar e desactivar os outros usuarios de nivel inferior.

### Avaliación da viabilidade técnica do proxecto

Tal e como se dixo anteriormente, o desenvolvemento do proxecto non require de ningún tipo de investimento en **hardware**, xa que se pode levar a cabo a través de computadores de usuario. Case calquera equipo, coa RAM e os procesadores comúns do mercado actual, serven para correr aplicacións de Docker en segundo plano e escribir programas en aplicacións como Visual Studio Code. Por iso, entendemos que os nosos propios computadores (un PC montado por pezas cunha Ryzen 5 de 2020 e 32 GB de RAM e un MacBook Air M3 con 16 GB de RAM) resultan idóneos.

A maiores, dispoñemos dun NAS doméstico da marca QNAP, cun Intel Celeron e 8 GB de RAM, que son máis que suficientes para correr de xeito permanente a aplicación nun Docker e funcionar como servidor externo para que outras persoas accedan remotamente (a través de VPN) á app.

Se estamos a pensar no hardware que necesitaremos no futuro, por suposto precisaremos de servidores con capacidade para aceptar máis conexións, con máis capas de seguridade e cuxas capacidades poidan escalar. Con todo, como viñemos dicindo, isto é unha cuestión que só se poderá valorar no futuro. O que podemos garantir agora é que eses servidores non precisarán de gran potencia para correr a nosa aplicación, polo que o investimento se poderá concentrar na súa capacidade para conectarse e resolver peticións.

En canto ao **software**, xa contamos con todo o necesario. Tal e como se esbozou, os programas específicos que se van usar son IDEs como Visual Studio Code. As tecnoloxías, librarías e frameworks necesarios para programar tamén son de acceso aberto. De cara ao futuro, de novo, sería posíbel facer que a aplicación funcionase a partir dun Docker, ao menos nun inicio.

### Interfaces externas

A nosa aplicación será accesíbel aos usuarios a través de dispositivos como ordenadores, tablets ou smartphones e, por tanto, a única interface externa necesaria que será precisa é unha pantalla.

En canto ao _software_, inicialmente os usuarios só requirirán un navegador, peza de _software_ que ven pre-instalada en todos os dispositivos de usuario. En fases posteriores, cando se poida crear unha aplicación propia, será necesario tamén que dispoñan das tendas de aplicacións que a distribúan. Con todo, como dicimos, este é un tema que deberá ser abordado dentro de moito tempo.

### Análise de riscos e interesados

En España existen certas asociacións e entidades que poden ter un impacto positivo na aplicación. Entendemos que podería ser de axuda contactalas cando a aplicación estivese lista. Con todo, tal e como se viu cando se falou da competencia, moitas destas asociacións teñen tamén os seus propios proxectos, polo que o seu impacto podería tornarse negativo.

### Melloras futuras

Entendemos que é cedo para pensar como mellorar algo que aínda non existe. Con todo, a mellora principal que se poderá desenvolver no futuro será a creación de aplicacións para smartphones. O actual proxecto, aínda que será soamente web, ten este como o seu principal obxectivo a medio-longo prazo, e con tal propósito está orientada a arquitectura do programa.

Outras posíbeis melloras a curto prazo:

-   Interface
-   Capacidades
-   Axuste de localizacións e coordenadas
-   Mellora dos mapas
-   Traducións completas

## Fase de planificación do proxecto

### Obxectivos do proxecto

-   Obxectivos xerais:
    -   Crear unha aplicación para o rexistro de alerxias
    -   Crear unha aplicación cun enfoque comunitario
    -   Crear unha aplicación pensada para traballar na web e nun smartphone, desenvolvemento agora mesmo só a parte web, e diferenciando unha capa de lóxica e outras de interface e aceso á primeira.
-   Obxectivos concretos:
    -   Aprender sobre algúns dos frameworks web de Python: FastAPI e Flask
    -   Aprender sobre a creación de APIs (FastAPI)
    -   Aprender sobre o chamado de APIs internamente (desde Flask)
    -   Aprender sobre o chamado de APIs alleas (Nominatim, Open Meteo...)
    -   Aprender a traballar con librarías externas (Leaflet.js)
    -   Desenvolver unha aplicación completa (Base de datos - Backend - Frontend) con funcionalidades e nunha linguaxe nova
    -   Aprender a crear interfaces usando Bootstrap
    -   etc.

### Guía de planificación do proxecto

#### Metodoloxía

A metodoloxía e a planificación deste proxecto están marcados por uns poucos parámetros que resultan fundamentais:

-   Falta de coñecemento e experiencia:
    1. Nunca se traballou con PostgreSQL
    2. Estase aprendendo a programar en Python
    3. Nunca se traballou con FastAPI
    4. Estase aprendendo a crear aplicacións (nas prácticas FCT) con Flask
    5. Estase aprendendo (nas prácticas FCT) a crear frontends con Bootstrap
    6. Nunca se realizou unha aplicación destas características nin desta "magnitude"
-   Limitación temporal:
    -   O horario das FCT implica saír de casa cada día ás 7:40 e volver ás 17:40. Isto provoca que só queden 6 horas diarias (+ fines de semana + 8 horas de sono) para realizar todas as tarefas restantes, entre as que se inclúe esta aplicación.
    -   O número de horas asignadas no programa á realización do proxecto é de 26h.
    -   Os meses de traballo son outubro, novembro e dúas semanas de decembro.

Para formular unha metodoloxía realista debemos contar con que se precisan semanas para aprender e familiarizarse coas tecnoloxías (escollidas dado o seu uso na empresa das FCT), debemos dar tempo ao deseño e análise da aplicación e á realización da documentación, fases que non implican directamente a escritura de código. Por iso, debe formularse unha aplicación extremadamente sinxela e fácil de programar.

_Grosso modo_, diferenciamos as seguintes fases, con cadansúas tarefas

1. Deseño, análise e formación
    1. Documentación sobre o pole e as aplicación actuais
    2. Estudo das necesidades
    3. Formación en Python e resto de tecnoloxías
2. Backend
    1. Estrutura principal da aplicación
    2. Creación de modelos para a base de datos
    3. Desenvolvemento das APIs principais e a lóxica
    4. Deseño da vista pública da aplicación
    5. Desenvolvemento das rutas que chamarán ás APIS
3. Frontend
    1. Deseño visual principal da aplicación (cores, logotipo, layout...)
    2. Primera implantación dos HTML e estilos xerais en CSS (usando Bootstrap ou código persoal)
    3. Desenvolvemento do frontend
    4. Accesibilidade
4. Probas e documentación final
5. Realización doutras tarefas:
    1. Script de instalacións
    2. Revisións
    3. Titorías
    4. Consulta de dúbidas
    5. Traballo no git

Todas estas tarefas se realizan por unha única persoa empregando os mesmos recursos de hardware e software, que xa foron mencionados.

A duración de cada unha é variábel, sendo o backend a parte que levaría máis traballo.

Sería ideal poder completar todas as tarefas, aínda que dado as limitación mencionadas non se descarta que algunhas deban ser obviadas ou recortadas.

No seguinte diagrama de Gantt pódese apreciar a calendarización das fases mencionadas. Para facilitar a comprensión e que todo puidese ser compactado nunha soa imaxe, resúmense aquí as principais tarefas:

![Diagrama Gantt](/documentacion/img/Online%20Gantt%20Dec%204%202024.png)

### Orzamento

Tal e como se dixo, as actividades e tarefas para levar a cabo a aplicación non requiren de custos específicos, máis aló dos computadores, a conexión a internet, o gasto enerxético e o valor do tempo de traballo dun programador en formación.

Dado que todas as actividades requiren dos mesmos recursos e persoas, non se elaborará o orzamento para cada unha.

Mesmo no caso de continuar adiante con este proxecto e tentar facer del unha aplicación real, moitos dos gastos serían semellantes. Practicamente non sería necesario ningún tipo de material extra (máis aló duns poucos folios e un bolígrafo para tomar algunha anotación, algo do que xa dispoñemos), tampouco habería necesidades de locais ou de contratos de subministracións, e o persoal involucrado podería ser soamente unha persoa (se esta -eu- tivese os coñecementos necesarios para facer todas as partes do proceso). Si sería preciso contratar un servidor desde o que se executase a aplicación e quizá tamén publicidade.

Con todo, continuando con esta hipótese, a aplicación debería pasar por numerosas fases até chegar o momento de contratar publicidade, xa que antes tería que estar feito o desenvolvemento completo e tería que superar unha etapa de probas internas, onde a _app_ fose empregada para un número limitado e reducido de usuarios. Para facer isto, ao inicio, bastaría con implementala no meu propio servidor e dar aceso a externos a través de VPN. Posteriormente, nunha fase onde se queira abrir a proba a máis usuarios, Pole podería despregarse nun servidor máis grande (aínda sendo pequeno) e externo, contratando o servizo con empresas como Hetzner ou outras, cun gasto de 40€ mensuais, aproximadamente. De todos modos, debemos entender isto xa como unha perspectiva a longo prazo, polo que outros escenarios maiores, nos que sexan necesarios servidores máis potentes ou contratar outras persoas, están aínda fóra de lugar.

Algo que aprendemos á hora de saber como emprender, é valorar as expectativas e as posibilidades reais de que algo prospere, e tamén a saber se o noso investimento pode ser rentábel. Actualmente, non consideramos aínda que poidamos estar traballando nunha aplicación competitiva, xa que se lle dedicaron poucas horas de traballo e aínda non foi probada por un número suficiente de persoas. Ao mesmo tempo, a día de hoxe, descoñecemos se teremos o tempo e a capacidade de facer unha aplicación que poida cumprir os requisitos mínimos para aspirar a competir con outras. Por iso descartamos facer valoración de orzamento ou partidas de inversión e gasto.

## Fase de deseño

### Modelo conceptual

![Diagrama de clases de FastAPI](/documentacion/img/app_fastapi.png)_Diagrama de clases de FastAPI_

![Diagrama de clases de Flask](/documentacion/img/app_flask.png)_Diagrama de clases de Flask_

![Diagrama de Frontend](/documentacion/img/app_flask_front.png)_Diagrama de Frontend_

### Caso de uso

![Diagrama de uso simplificado](/documentacion/img/diagrama-simple-uso.png)_Diagrama de uso simplificado_

### Deseño de interface de usuarios (mockups)

![Mockup Desktop Login](/documentacion/img/mockup_desktop_login.png)_Mockup Desktop Login_

![Mockup Desktop Inicio Anotado](/documentacion/img/mockup_desktop_inicio_anotado.png)_Mockup Desktop Inicio Anotado_

![Mockup Smartphone Inicio](/documentacion/img/mockup_iphone_inicio.png)_Mockup Smartphone Inicio_

### Diagrama de Base de Datos

![Diagrama ER](/documentacion/img/ER-Diagram-DBeaver.png)

## Fase de implantación

### Manual técnico

#### Información relativa á instalación

-   Requirimentos:
    -   A aplicación (o docker) debería poder instalarse en computadores con recursos básicos.
-   Software necesario:
    -   Docker (principalmente)
    -   Git (opcionalmente, útil para descargar a aplicación desde GitLab e/ou seguir o script de instalación)
-   Configuración inicial:
    -   Non debería ser preciso realizar ningunha configuración inicial.
-   Carga inicial de datos na base de datos:
    -   Para usar a app, non é preciso facer ningunha carga na base de datos.
    -   De todos modos, para avaliar a aplicación, recomendamos cargar a copia da base de datos que pomos á disposición neste repositorio. Este contén usuarios e rexistros, para facilitar ver como se comporta a aplicación nun escenario real.
-   Usuarios do sistema. Usuarios da aplicación.
    -   Os usuarios (cos seus datos) son indicados na guía inicial da aplicación.

#### Información relativa á administración do sistema

-   Cando o sistema estea a funcionar recoméndanse facer todo de copias de seguridade do sistema e especialmente da base de datos, xa que esta contén os rexistros dos usuarios, que son irrepetíbeis e o valor principal da aplicación.
-   Alén delas, deben contemplarse tamén:
    -   Xestión de usuarios.
    -   Xestión seguridade.
    -   Xestión de incidencias, que poden ser de dous tipos: de sistema (accesos non autorizados á BD, etc) ou de fallos no software.

#### Información relativa ao mantemento do sistema

Somos conscientes de que o sistema contén *bugs* e carece de funcionalidades. Como dicimos, isto é só unha primeira aproximación a esta aplicación, por iso, convidamos os usuarios a:

-   Comunicar e corrixir erros.
-   Propor novas funcionalidades ou, directamente, escribilas.
-   Axudar a depurar e refactorizar código.
-   Testar a aplicación en distintos escenarios de hardware e software.

### Xestión de incidencias

As incidencias deberán comunicarse a través do GitLab.

### Protección de datos de carácter persoal

Dado que aínda non existen usuarios reais e, como xa se dixo, non os haberá proximamente, non se contemplan aínda modelos de protección de datos nin políticas de privacidade. Isto, por suposto, tería que facerse no futuro.

### Manual de usuario

O funcionamento da aplicación é sinxelo. Calquera usuario debería poder usala sen problemas se está familiarizado co uso de aplicacións semellantes ou de redes sociais, xa que a estrutura segue un deseño semellante, en parte, por este motivo.
