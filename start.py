from kubernetes import config, client



def start():
    """
    Create a deployment from scratch and add to cluster using K8s Python API.
    """
    # Load kubernetes config from .kube file
    config.load_kube_config()
    
    # Set user_id and image statically for now
    user_id = 12345
    image = "python:3.10"
    
    # Define the container specification
    container = client.V1Container(
        name=f"{user_id}-container",
        image=image,
        ports=[client.V1ContainerPort(container_port=8888)]
    )
    
    # Define the Pod template specification
    template = client.V1PodTemplateSpec(
        metadata=client.V1ObjectMeta(labels={"app": f"{user_id}-environment"}),
        spec=client.V1PodSpec(containers=[container])
    )
    
    # Define the Deployment specification
    spec = client.V1DeploymentSpec(
        replicas=1,  # Each user gets one replica
        template=template,
        selector={'matchLabels': {'app': f"{user_id}-environment"}}
    )
    
    # Create the Deployment object
    deployment = client.V1Deployment(
        api_version="apps/v1",
        kind="Deployment",
        metadata=client.V1ObjectMeta(name=f"{user_id}-deployment"),
        spec=spec
    )
    
    # Create an API client for the AppsV1Api
    apps_api = client.AppsV1Api()
    
    # Create the Deployment in the default namespace
    namespace = "default"
    response = apps_api.create_namespaced_deployment(
        body=deployment,
        namespace=namespace
    )
    
    print(f"Status: {response.status}")

if __name__ == "__main__":
    start()