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

```bash
```

```bash
```

```bash
```
