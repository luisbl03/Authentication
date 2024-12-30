# SERVICIO DE AUTENTICACION

## Descripción
Este servicio se encarga de la autenticacion y gestion de los usuarios del sistema. Se comunica con un servicio de tokens de usuario para dar el acceso a los usuarios.

## Instalacion
Este servicio se encuentra dentro de un contenedor docker, para ejecutarlo, se ha creado un script que automatiza esto. Para ejecutarlo, se debe ejecutar el siguiente comando:
```bash
./build.sh
```

La persistencia se encuentra dentro del contenedor.

## Ejecucion
Para ejecutar el servicio, se debe ejecutar el siguiente comando:
```bash
python3 run.py
```

El contenedor se arranca en segundo plano, por lo que se puede seguir utilizando la terminal.

## Detener
Para detener el servicio, se debe ejecutar el siguiente comando:
```bash
python3 stop.py
```