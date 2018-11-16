# algo-notas-bot

Bot de Telegram para notificar cambios en el sistema de notas.

## Pasos para ejecutar el programa

- Instalar las dependencias: `pip install -r requirements.txt`
- Variables de entorno:
	- `DATABASE_URL`: URI de PostgreSQL, con formato `
	postgres://user:password@host:port/database`
	- `TOKEN_TELEGRAM_BOT`: El token del bot de Telegram.
- `python main.py`
	- Junto a las variables de entorno: `DATABASE_URL=<url> TOKEN_TELEGRAM_BOT=<token> python main.py`

## Base de datos

Los datos se guardan en una instancia de PostgreSQL, con una única tabla:
```sql
CREATE TABLE public.users (
    id integer NOT NULL,
    chat integer,
    link character varying(150),
    previous_data json
);
```
Alternativamente, el módulo `database.py` se puede reemplazar con cualquier otro sistema para guardar los datos, con tal de que sus funciones sepan guardar/eliminar/actualizar los datos del usuario. Las funciones de búsqueda retornan un diccionario:
```
{
	id: <id del usuario en el sistema>,
	chat: <id del chat en Telegram con el usuario dado>,
	link: <link de la página del sistema de notas>,
	previous_data: <diccionario con las últimas notas guardadas>
}
```