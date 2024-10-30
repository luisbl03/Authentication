# Authentication
## Descripción
Servicio de autenticación de usuarios, verifica la existencia de un usuario y su contraseña

## Dudas
¿En la primera entrega tengo que tener la comunicacion con el servicio de token? -> un mock que va a pasar el profesor

## librerias recomendadas
secrets para los id de usuario

## otras dudas
- is authorized lo que hace es verificar si el token es valido, y se obtiene un hash
- comunicacion con token es la capa de dominio


## cosas que hacer
- eliminar los id, son innecesarios
- tener en cuenta que cuando hago peticion a token, este me devuelve mi usuario, lo que yo introduzco en el path no es necesariamente mi usuario
- si el usuario es user, solo puede cambiar lo relacionado con su usuario en la base de datos
