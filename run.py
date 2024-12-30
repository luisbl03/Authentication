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
            return True
        print(f'El contenedor {name} no esta en ejecucion')
        #borramos el contenedor
        return False
    except docker.errors.NotFound:
        print(f'El contenedor {name} no existe')
        return False

def run_container(name_image:str, name_container:str) -> int:
    """Funcion que inicia un contenedor"""
    if not check_container(name_container):
        print(f'Iniciando contenedor {name_container}')
        client.containers.run(name_image,
                              name=name_container, detach=True,
                              auto_remove=True, mem_limit='2g', cpu_quota=100000, cpu_period=100000)
        print(f'Contenedor {name_container} iniciado')
        return 0
    return 1

if __name__ == '__main__':
    run_container('authsrv', 'authsrv')
