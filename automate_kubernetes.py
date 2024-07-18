from kubernetes import client, config
from kubernetes.stream import stream
import random
import time

def create_deployment(name, image, port):
    container = client.V1Container(
        name=name,
        image=image,
        ports=[client.V1ContainerPort(container_port=port)]
    )
    
    template = client.V1PodTemplateSpec(
        metadata=client.V1ObjectMeta(labels={"app": name}),
        spec=client.V1PodSpec(containers=[container])
    )
    
    spec = client.V1DeploymentSpec(
        replicas=1,
        selector=client.V1LabelSelector(match_labels={"app": name}),
        template=template
    )
    
    deployment = client.V1Deployment(
        api_version="apps/v1",
        kind="Deployment",
        metadata=client.V1ObjectMeta(name=name),
        spec=spec
    )
    
    apps_v1.create_namespaced_deployment(namespace="default", body=deployment)

def create_service(name, port):
    service = client.V1Service(
        api_version="v1",
        kind="Service",
        metadata=client.V1ObjectMeta(name=name),
        spec=client.V1ServiceSpec(
            selector={"app": name},
            ports=[client.V1ServicePort(port=port, target_port=port)]
        )
    )
    
    v1.create_namespaced_service(namespace="default", body=service)

def assign_port():
    services = v1.list_namespaced_service(namespace="default")
    used_ports = set(service.spec.ports[0].port for service in services.items)
    return 30000
    # while True:
    #     port = random.randint(30000, 32767)  # Use NodePort range
    #     if port not in used_ports:
    #         return port

def create_and_assign_application(name, image):
    port = assign_port()
    create_deployment(name, image, port)
    create_service(name, port)
    print(f"Application '{name}' created and assigned to port {port}")
    return port

def get_pod(namespace, label_selector):
    pods = v1.list_namespaced_pod(namespace, label_selector=label_selector)
    if not pods.items:
        print(f"No pods found with label selector: {label_selector}")
        return None
    return pods.items[0]

def exec_command_on_pod(pod, container, command):
    exec_command = [
        '/bin/sh',
        '-c',
        command
    ]
    
    resp = stream(v1.connect_get_namespaced_pod_exec,
                  pod.metadata.name,
                  pod.metadata.namespace,
                  container=container,
                  command=exec_command,
                  stderr=True, stdin=False,
                  stdout=True, tty=False)
    
    print(f"Command output:\n{resp}")

def create_app_and_run_command(name, image, command):
    # Create the application
    port = create_and_assign_application(name, image)
    
    # Wait for the pod to be ready
    print("Waiting for pod to be ready...")
    time.sleep(20)  # Adjust this delay as needed
    
    # Get the pod
    pod = get_pod("default", f"app={name}")
    
    if pod:
        # Run the command on the pod
        exec_command_on_pod(pod, name, command)
    else:
        print(f"Failed to find pod for application '{name}'")


if __name__ == "__main__":
    # Load Kubernetes configuration
    config.load_kube_config()

    # Create Kubernetes API clients
    api_client = client.ApiClient()
    v1 = client.CoreV1Api(api_client)
    apps_v1 = client.AppsV1Api(api_client)

    # Example usage
    app_name = "sample-app"
    app_image = "pureblank/run_user_program"
    command_to_run = "echo 'Hello from the newly created pod!'"

    create_app_and_run_command(app_name, app_image, command_to_run)