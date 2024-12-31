"""funcion para detener el contenedor de authsrv"""
from docker_manager import stop_container

stop_container('authsrv_container')
