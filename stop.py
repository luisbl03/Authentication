"""modulo docker"""
import docker

client = docker.from_env()

#miramos si el contenedor esta en ejecucion
def check_container(name:str):
    """Funcion que detiene un contenedor si esta en ejecucion"""
    try:
        container = client.containers.get(name)
        if container.status == 'running':
            print(f'El contenedor {name} esta en ejecucion')
            container.stop()
            print(f'El contenedor {name} ha sido detenido')

        else:
            print(f'El contenedor {name} no esta en ejecucion')
            return False

    except docker.errors.NotFound:
        print(f'El contenedor {name} no existe')
        return False

    return True

if __name__ == '__main__':
    check_container('authsrv')
