"""Modulo para gestionar contenedores Docker"""
import docker

client = docker.from_env()

def check_container(name: str) -> bool:
    """Funcion que verifica si un contenedor esta en ejecucion"""
    try:
        container = client.containers.get(name)
        if container.status == 'running':
            print(f'El contenedor {name} esta en ejecucion')
            return True
        print(f'El contenedor {name} no esta en ejecucion')
        return False
    except docker.errors.NotFound:
        print(f'El contenedor {name} no existe')
        return False

def run_container(name_image: str, name_container: str) -> int:
    """Funcion que inicia un contenedor"""
    if not check_container(name_container):
        print(f'Iniciando contenedor {name_container}')
        try:
            client.containers.run(
                name_image,
                name=name_container,
                detach=True,
                auto_remove=True,
                mem_limit='2g',
                cpu_quota=100000,
                cpu_period=100000
            )
            print(f'Contenedor {name_container} iniciado')
            return 0
        except docker.errors.ImageNotFound:
            print(f'La imagen {name_image} no se encuentra')
            return 1
        except docker.errors.APIError as e:
            print(f'Error al iniciar el contenedor: {e}')
            return 1
    return 1

if __name__ == '__main__':
    run_container('authsrv', 'authsrv_container')