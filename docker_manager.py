"""modulo docker"""
import docker

def stop_container(name: str) -> bool:
    """Detiene un contenedor si está en ejecución."""
    client = docker.from_env()
    try:
        container = client.containers.get(name)
        if container.status == 'running':
            print(f'El contenedor {name} está en ejecución. Deteniéndolo...')
            container.stop()
            print(f'El contenedor {name} ha sido detenido.')
            return True
        else:
            print(f'El contenedor {name} no está en ejecución.')
            return False
    except docker.errors.NotFound:
        print(f'El contenedor {name} no existe.')
        return False

def run_container(name_image: str, name_container: str) -> int:
    """Inicia un contenedor con una imagen específica si no está en ejecución."""
    client = docker.from_env()
    try:
        container = client.containers.get(name_container)
        if container.status == 'running':
            print(f'El contenedor {name_container} ya está en ejecución.')
            return 0
    except docker.errors.NotFound:
        print(f'El contenedor {name_container} no existe. Intentando iniciarlo...')

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
        print(f'Contenedor {name_container} iniciado exitosamente.')
        return 0
    except docker.errors.ImageNotFound:
        print(f'La imagen {name_image} no se encuentra.')
        return 1
    except docker.errors.APIError as e:
        print(f'Error al iniciar el contenedor: {e}')
        return 1

if __name__ == '__main__':
    # Ejemplo de uso
    print('****Manejador del contenedor Authsrv****\n')
    print('¿Desea iniciar o detener el contenedor?. Ingrese "iniciar" o "detener"')
    action = input()
    if action == 'iniciar':
        run_container('authsrv', 'authsrv_container')
    elif action == 'detener':
        stop_container('authsrv_container')
    else:
        print('Opción inválida. Saliendo...')
