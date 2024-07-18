from kubernetes import config, client

def delete_deployment(apps_v1_api, deployment_name, namespace):
    resp = apps_v1_api.delete_namespaced_deployment(
        name=deployment_name,
        namespace=namespace,
        body=client.V1DeleteOptions(
            propagation_policy="Background", grace_period_seconds=1
        ),
    )
    print("\nDeployment deleted.")



if __name__ == "__main__":
    # Load kube config
    config.load_kube_config()
    # Initialize the Kubernetes API client
    apps_v1_api = client.AppsV1Api()
    
    deployment_name = "12345-deployment"
    namespace = "default"
    
    delete_deployment(apps_v1_api, deployment_name, namespace)