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

```bash
```

```bash
```

```bash
```
