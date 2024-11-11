# SERVICIO DE AUTENTICACION


## Preparacion
Para el primer lanzamiento del servicio, es necesario tener la base de datos creada, para ello, se ha creado un archivo python llamado bootstrap.py, el cual se ejecuta con el siguiente comando:

```bash
python bootstrap.py
```

Este archivo creara la base de datos y añadira el usuario administrador para empezar a trabajar con el servicio.

## Instalación
Para instalar la aplicacion de servicio, es necesario disponer de un entorno virtual de python. Una vez se tenga se ejecuta el siguiente comando:

```bash
pip install .
```

## Ejecución
Para ejecutar el servicio, se debe ejecutar el siguiente comando:

```bash
authService
```

## Testing
Los test se ejcutan desde un script llamado starts_test.sh, el cual se ejecuta con el siguiente comando:

```bash
./start_tests.sh
```
Acto seguido cuando se ejecuten se abrira automaticamente el navegador con la cobertura de los test realizados.

Para borrar los tests se ejecuta el siguiente comando:

```bash
./delete_test.sh
```