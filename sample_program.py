from kubernetes import client, config

# Load kube config from Minikube
config.load_kube_config()

# Pod manifest
pod_manifest = {
    "apiVersion": "v1",
    "kind": "Pod",
    "metadata": {
        "name": "hello-world-pod"
    },
    "spec": {
        "containers": [
            {
                "name": "hello-world-container",
                "image": "",
                # "command":  ["python3", "infinite_program.py"]
            }
        ]
    }
}

# Create pod
api_instance = client.CoreV1Api()
namespace = 'default'
api_instance.create_namespaced_pod(
    namespace=namespace,
    body=pod_manifest
)
print("Pod created. Check the status with 'kubectl get pods'.")


# select specific pod
# copy program into that pod
# the infinite program runs that pod