import os
from openstack import connection

def create_connection():
    config_file = os.path.join(os.path.dirname(__file__), 'clouds.yml')
    return connection.Connection(config_file=config_file, cloud='openstack')


def get_hypervisors(conn):
    return list(conn.compute.hypervisors())

def balance_hypervisor(conn):
    hypervisors = get_hypervisors(conn)
    for hypervisor in hypervisors:
        # Attempt to update or refresh the hypervisor data
        hypervisor = conn.compute.get_hypervisor(hypervisor.id)
        print(f"Hypervisor {hypervisor.name} - Hypervisro state: {hypervisor.state}, Hypervisor status:{hypervisor.status}, vCPUs all: {hypervisor.vcpus}. vCPUs Used: {hypervisor.vcpus_used}, Running VMs: {hypervisor.running_vms}")


def main():
    conn = create_connection()
    balance_hypervisor(conn)


if __name__ == '__main__':
    main()