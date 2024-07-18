from kubernetes import client, config

config.load_kube_config()
apps_v1 = client.AppsV1Api()
core_v1 = client.CoreV1Api()

def list_and_delete_resources(namespace, label_selector):
    # List and delete Deployments
    deployments = apps_v1.list_namespaced_deployment(namespace, label_selector=label_selector)
    for dep in deployments.items:
        print(f"Deleting Deployment: {dep.metadata.name}")
        apps_v1.delete_namespaced_deployment(dep.metadata.name, namespace)

    # List and delete ReplicaSets
    replicasets = apps_v1.list_namespaced_replica_set(namespace, label_selector=label_selector)
    for rs in replicasets.items:
        print(f"Deleting ReplicaSet: {rs.metadata.name}")
        apps_v1.delete_namespaced_replica_set(rs.metadata.name, namespace)

    # List and delete StatefulSets
    statefulsets = apps_v1.list_namespaced_stateful_set(namespace, label_selector=label_selector)
    for sts in statefulsets.items:
        print(f"Deleting StatefulSet: {sts.metadata.name}")
        apps_v1.delete_namespaced_stateful_set(sts.metadata.name, namespace)

    # List and delete Pods (although this shouldn't be necessary if controllers are deleted)
    pods = core_v1.list_namespaced_pod(namespace, label_selector=label_selector)
    for pod in pods.items:
        print(f"Deleting Pod: {pod.metadata.name}")
        core_v1.delete_namespaced_pod(pod.metadata.name, namespace)

# Example usage
namespace = 'default'
label_selector = 'app=sample-app'  # Replace with your app's label

list_and_delete_resources(namespace, label_selector)