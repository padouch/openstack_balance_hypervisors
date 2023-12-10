import os
from openstack import connection


def create_connection():
    config_file = os.path.join(os.path.dirname(__file__), 'clouds.yml')
    return connection.Connection(config_file=config_file, cloud='openstack')


def get_hypervisors(conn):
    all_hypervisors = list(conn.compute.hypervisors())
    enabled_hypervisors = [hypervisor for hypervisor in all_hypervisors if hypervisor.status == 'enabled']
    return enabled_hypervisors


def get_l3hyperviors(conn):
    active_alive_l3_agents = []
    for agent in conn.network.agents():
        if agent.agent_type == 'L3 agent' and agent.is_alive and agent.is_admin_state_up:
            active_alive_l3_agents.append(agent.host)
    return active_alive_l3_agents


def balance_hypervisor(conn):
    hypervisors = get_hypervisors(conn)
    l3nodes = get_l3hyperviors(conn)

    for hypervisor in hypervisors:
        if hypervisor.name not in l3nodes:
            overallocatio = 3
            hypervisor = conn.compute.get_hypervisor(hypervisor.id)
            print(
                f"Hypervisor {hypervisor.name} - Hypervisro state: {hypervisor.state}, Hypervisor status:{hypervisor.status}, fy CPUs {hypervisor.vcpus}, vCPUs all: {hypervisor.vcpus * overallocatio}. vCPUs Used: {hypervisor.vcpus_used}, Running VMs: {hypervisor.running_vms}")
        else:
            overallocatio = 2
            # Attempt to update or refresh the hypervisor data
            hypervisor = conn.compute.get_hypervisor(hypervisor.id)
            print(
                f"Hypervisor {hypervisor.name} - Hypervisro state: {hypervisor.state}, Hypervisor status:{hypervisor.status}, fy CPUs {hypervisor.vcpus}, vCPUs all: {hypervisor.vcpus * overallocatio}, vCPUs Used: {hypervisor.vcpus_used}, Running VMs: {hypervisor.running_vms}")


def main():
    conn = create_connection()
    balance_hypervisor(conn)


if __name__ == '__main__':
    main()
