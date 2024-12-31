"""funcion principal para correr el contenedor de authsrv"""
from docker_manager import run_container

if __name__ == '__main__':
    run_container('authsrv', 'authsrv_container')
