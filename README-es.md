# Paso 17: Producción

[Volver al paso 16](https://gitlab.com/FedeG/django-react-workshop/tree/step16_add_redux)

Este paso es importante a la hora de poner en producción tu aplicación.
Para enterder este paso primero tenemos que tener en mente como funciona este proyecto con Django y React.

Para producción solo vamos a tener a Django trabajando, ya que el js generado con React se va a usar como archivos estaticos.

## Configuración de produccion de Django

#### Nuevas dependencias

Vamos a agregar dos dependencias nuevas:

En el `requirements.txt` vamos a agregar:

```conf
asgi-redis==1.4.3
psycopg2-binary==2.7.6.1
```

- **asgi-redis**: para poder usar `redis` para encolar tareas

- **psycopg2-binary**: para poder usar `postgres` como base de datos

#### Crear un nuevo settings para produción

Para esto vamos a crear un archivo de settings nuevo: `settings_prod.py` en la carpeta `workshop/workshop` (la misma que el `settings.py` que usamos en desarrollo)

En ese archivos vamos a poner las configuraciones de producción a partir de las configuraciones que ya tenemos, es decir importando el `settings.py`:

```python
import os
import socket
import asgi_redis

# Import dev settings
from workshop.settings import *

DEBUG = False
TEMPLATE_DEBUG = False

SECRET_KEY = os.getenv(
    'SECRET_KEY',
    'kl*@mt86$rdllg+$d633#ijwkkc49^k-hw5yxfsbtn*rdq1=l)')

ALLOWED_HOSTS = [os.getenv('APP_DNS', 'localhost'), socket.gethostname()]

WEBPACK_LOADER = {
    'DEFAULT': {
        'BUNDLE_DIR_NAME': 'bundles/prod/',  # end with slash
        'STATS_FILE': os.path.join(
            BASE_DIR, 'front', 'webpack-stats-prod.json'),
    }
}

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.getenv('POSTGRES_DB', 'workshop'),
        'USER': os.getenv('POSTGRES_USER', 'workshop'),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD', 'secret'),
        'HOST': os.getenv('POSTGRES_HOST', 'localhost'),
        'PORT': os.getenv('POSTGRES_PORT', '5432'),
        'OPTIONS': {
            'sslmode': os.environ.get("POSTGRES_OPTIONS_SSL", "prefer"),
        },
    }
}

REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': (
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
        'django_filters.rest_framework.DjangoFilterBackend',
    ),
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly'
    ],
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    )
}

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'asgi_redis.RedisChannelLayer',
        'CONFIG': {
            'hosts': [(
                os.getenv('REDIS_HOST', 'redis'),
                int(os.getenv('REDIS_PORT', '6379')),
            )],
        },
        'ROUTING': 'workshop.routing.channel_routing',
    }
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
        'logservices': {
            'format': '[%(asctime)s] [%(levelname)s] %(message)s'
        }
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.getenv(
                'LOG_FILE',
                '/var/log/workshop/workshop.log'
            ),
            'maxBytes': 1024*1024*10,
            'backupCount': 10,
            'formatter': 'logservices'
        }
    },
    'loggers': {
        'workshop': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True
        },
        'django.channels': {
            'handlers': ['file'],
            'level': 'WARNING',
            'propagate': True
        },
        'django.request': {
            'handlers': ['file'],
            'level': 'WARNING',
            'propagate': True
        },
        'django': {
            'handlers': ['console'],
            'level': 'WARNING',
            'propagate': True
        }
    }
}
```

##### Cosas importantes a destacar de este archivo:

- **DEBUG** y **DEBUG_TEMPLATES**: van a estar en false ya que en producción no se hace debug del codigo
- **os.getenv**: usaremos variables de entorno para poder configurar medienta un archivo `.env` o variables de nuestra consola
- **ALLOWED_HOSTS**: especificamos desde que dominio se puede acceder a esta aplicación
- **WEBPACK_LOADER**: usamos el stats de producción de webpack
- **DATABASES**: usamos una base de datos (en este caso postgres)
- **REST_FRAMEWORK**: la api solo va a ser accesible en modo lectura para usuario no logeados y va a responder JSON de forma predeterminada
- **CHANNEL_LAYERS**: para `django-channels` vamos a usar un `redis`
- **LOGGING**; usaremos una configuracion de logs acorde a producción

#### ¿Como usar ese settings?

Para usar el `settings_prod.py` que armamos, primero tenemos que armar un archivo `asgi.py` ya que vamos a estar usando `redis` para poder disparar acciones y encolar tareas.

En el archivo `workshop/workshop/asgi.py` vamos a poner:

```python
import os

from channels.asgi import get_channel_layer

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "workshop.settings")

channel_layer = get_channel_layer()
```

En este caso vamos a dejar como valor predeterminado de `DJANGO_SETTINGS_MODULE` el `settings.py` original ya que podria usarse y cuando pensemos usar la aplicación en modo producción solamente tenemos que configurar esa variable de entorno con el valor `workshop.settings_prod`.

## Generar los archivos js de React para usar en el servidor productivo

Si vemos los archivos que tenemos en la carpeta `workshop/front` podemos ver uno que es `webpack.prod.config.js`.
Este archivo esta armado para generar los bundles finales de js que se van a utilizar en producción.

Para crear estos bundles vamos a hacer:

```javascript
cd workshop/front
webpack --config webpack.prod.config.js
```

Este comando igual lo hace el `Dockerfile` que ya tenemos, por ende no es necesario correrlo a mano a menos de que no uses **docker**.

## Servidor completo

Para empezar hay que comprender que si bien este taller da una forma, hay muchas formas distintas de hacerlo.
En este caso vamos a usar `docker-compose` que nos permite controlar varios servicios y enlazarlos entre si.


#### Infraestructura

Antes de detallar el codigo y archivos, vamos a hablar sobre la infraestrutura que vamos a usar:

- 2 containers con python, uno va a escuchar las peticiones de la web y otro va a realizar las tareas (para esto vamos a usar una herramienta llamada `daphne`).

- 2 containers con nginx, podria simplemente usarse uno pero para hacer mas facil la implementación del dominio y puertos, vamos a usar uno con un nginx configurado por nosotros y otro con `nginx-proxy` que es una herramienta que nos permite trabajar facilmente con el tema dominios y puertos.

- 1 container con postgres, esta es la base de datos que vamos a utilizar

- 1 container con redis

También para garantizar que los datos esten guardados vamos a usar volumenes, lo cuales son:

- **/srv/deploys/workshopdata/static**: para los archivos estaticos de nuestra aplicación

- **/srv/deploys/workshopdata/postgres**: para los archivos de la base de datos

#### Archivos base:

Vamos a crear archivos para el deploy dentro de la carpeta `deploy/docker`.

En esta carpeta vamos a crear dos carpetas: `nginx` y `scripts`

#### Scripts

Esta carpeta va a tener los scripts que vamos a utilizar en nuestro `docker-compose`.

Uno va a ser el script de arranque de la aplicación y otro va a ser un script que sirve para esperar que la base de datos este andando antes de correr el otro script.

En el archivo `deploy/docker/scripts/wait-for-it.sh`:

```bash
#!/usr/bin/env bash
#   Use this script to test if a given TCP host/port are available

cmdname=$(basename $0)

echoerr() { if [[ $QUIET -ne 1 ]]; then echo "$@" 1>&2; fi }

usage()
{
    cat << USAGE >&2
Usage:
    $cmdname host:port [-s] [-t timeout] [-- command args]
    -h HOST | --host=HOST       Host or IP under test
    -p PORT | --port=PORT       TCP port under test
                                Alternatively, you specify the host and port as host:port
    -s | --strict               Only execute subcommand if the test succeeds
    -q | --quiet                Don't output any status messages
    -t TIMEOUT | --timeout=TIMEOUT
                                Timeout in seconds, zero for no timeout
    -- COMMAND ARGS             Execute command with args after the test finishes
USAGE
    exit 1
}

wait_for()
{
    if [[ $TIMEOUT -gt 0 ]]; then
        echoerr "$cmdname: waiting $TIMEOUT seconds for $HOST:$PORT"
    else
        echoerr "$cmdname: waiting for $HOST:$PORT without a timeout"
    fi
    start_ts=$(date +%s)
    while :
    do
        if [[ $ISBUSY -eq 1 ]]; then
            nc -z $HOST $PORT
            result=$?
        else
            (echo > /dev/tcp/$HOST/$PORT) >/dev/null 2>&1
            result=$?
        fi
        if [[ $result -eq 0 ]]; then
            end_ts=$(date +%s)
            echoerr "$cmdname: $HOST:$PORT is available after $((end_ts - start_ts)) seconds"
            break
        fi
        sleep 1
    done
    return $result
}

wait_for_wrapper()
{
    # In order to support SIGINT during timeout: http://unix.stackexchange.com/a/57692
    if [[ $QUIET -eq 1 ]]; then
        timeout $BUSYTIMEFLAG $TIMEOUT $0 --quiet --child --host=$HOST --port=$PORT --timeout=$TIMEOUT &
    else
        timeout $BUSYTIMEFLAG $TIMEOUT $0 --child --host=$HOST --port=$PORT --timeout=$TIMEOUT &
    fi
    PID=$!
    trap "kill -INT -$PID" INT
    wait $PID
    RESULT=$?
    if [[ $RESULT -ne 0 ]]; then
        echoerr "$cmdname: timeout occurred after waiting $TIMEOUT seconds for $HOST:$PORT"
    fi
    return $RESULT
}

# process arguments
while [[ $# -gt 0 ]]
do
    case "$1" in
        *:* )
        hostport=(${1//:/ })
        HOST=${hostport[0]}
        PORT=${hostport[1]}
        shift 1
        ;;
        --child)
        CHILD=1
        shift 1
        ;;
        -q | --quiet)
        QUIET=1
        shift 1
        ;;
        -s | --strict)
        STRICT=1
        shift 1
        ;;
        -h)
        HOST="$2"
        if [[ $HOST == "" ]]; then break; fi
        shift 2
        ;;
        --host=*)
        HOST="${1#*=}"
        shift 1
        ;;
        -p)
        PORT="$2"
        if [[ $PORT == "" ]]; then break; fi
        shift 2
        ;;
        --port=*)
        PORT="${1#*=}"
        shift 1
        ;;
        -t)
        TIMEOUT="$2"
        if [[ $TIMEOUT == "" ]]; then break; fi
        shift 2
        ;;
        --timeout=*)
        TIMEOUT="${1#*=}"
        shift 1
        ;;
        --)
        shift
        CLI="$@"
        break
        ;;
        --help)
        usage
        ;;
        *)
        echoerr "Unknown argument: $1"
        usage
        ;;
    esac
done

if [[ "$HOST" == "" || "$PORT" == "" ]]; then
    echoerr "Error: you need to provide a host and port to test."
    usage
fi

TIMEOUT=${TIMEOUT:-15}
STRICT=${STRICT:-0}
CHILD=${CHILD:-0}
QUIET=${QUIET:-0}

# check to see if timeout is from busybox?
# check to see if timeout is from busybox?
TIMEOUT_PATH=$(realpath $(which timeout))
if [[ $TIMEOUT_PATH =~ "busybox" ]]; then
        ISBUSY=1
        BUSYTIMEFLAG="-t"
else
        ISBUSY=0
        BUSYTIMEFLAG=""
fi

if [[ $CHILD -gt 0 ]]; then
    wait_for
    RESULT=$?
    exit $RESULT
else
    if [[ $TIMEOUT -gt 0 ]]; then
        wait_for_wrapper
        RESULT=$?
    else
        wait_for
        RESULT=$?
    fi
fi

if [[ $CLI != "" ]]; then
    if [[ $RESULT -ne 0 && $STRICT -eq 1 ]]; then
        echoerr "$cmdname: strict mode, refusing to execute subprocess"
        exit $RESULT
    fi
    exec $CLI
else
    exit $RESULT
fi
```

NOTA: este archivo si quieren pueden revisarlo para entenderlo en mas detalle, pero en resumen lo que hace es esperar que en un host y puerto este corriendo algo para despues ejecutar un script que se le envia por parametro

En el archivo `deploy/docker/scripts/start_workshop.sh`:

```bash
#!/bin/bash

set -e
set -x

if [ -e ./workshop.deployed ] || [ "$LOAD_INITIAL_DATA" = 'false' ]
then
  echo "Workshop is deployed"
else
  cd /usr/src/app/front
  webpack --config webpack.prod.config.js
  cd -

  python manage.py makemigrations links --noinput
  python manage.py migrate --noinput
  python manage.py collectstatic --noinput
  python manage.py loaddata data/users.json
  python manage.py loaddata data/links.json

  touch ./workshop.deployed
  export LOAD_INITIAL_DATA=false
fi
python manage.py runworker
```

En este script vamos a poner los comandos que queremos que se corrar para iniciar el container.

```bash
```

```bash
```

```bash
```
