from kubernetes import client, config


# Print pods and deployments.
# Modifies webapp-deployment to increase replica count and automatically create new web-app pod.


# Load .kube config file from local machine
config.load_kube_config()

# CoreV1Api client provides access to the core API group (v1) of Kubernetes. 
# This API group includes the fundamental resources required to run a Kubernetes cluster
# [pods, services, configmaps, secrets, namespaces, persistant_volumes, replication_controllers, nodes]
core_v1 = client.CoreV1Api()

# AppsV1Api client provides access to the apps API group (v1) of Kubernetes. 
# This API group includes higher-level application management resources that provide more sophisticated deployment capabilities
# [deployments, replicasets, statefulsets, daemonsets, jobs, cronjobs]
apps_v1 = client.AppsV1Api()

namespace = 'default'

pods = core_v1.list_namespaced_pod(namespace=namespace)
deployments = apps_v1.list_namespaced_deployment(namespace=namespace)

for pod in pods.items:
    print(f"Pod name: {pod.metadata.name}")

for deployment in deployments.items:
    print(f"Deployment name: {deployment.metadata.name}")
    # Update webapp-deployment replica count to 2
    if deployment.metadata.name == 'webapp-deployment':
        deployment.spec.replicas = 3
        # Must pass modified deployment as a response through api
        response = apps_v1.patch_namespaced_deployment(
            name=deployment.metadata.name,
            namespace=namespace,
            body=deployment
        )
        print(f"Deployment updated. Status={response.status}")
    print("\n")
    

