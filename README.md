# k8s-containers

### Precursor
* Clone the Repository

1) To get started running a kubernetes cluster using minikube, download minikube
  * https://minikube.sigs.k8s.io/docs/start/?arch=%2Fmacos%2Fx86-64%2Fstable%2Fbinary+download

2) Run `minikube start` to create a local Kubernetes environment
3) Run `minikube status` to check the current status of your envionment
```
❯ minikube status
minikube
type: Control Plane
host: Running
kubelet: Running
apiserver: Running
kubeconfig: Configured
```
4) There should be no pods found
```
❯ kubectl get pod
No resources found in default namespace.
```
5) Next, apply the yaml files in the correct order
```
❯ kubectl apply -f mongo-config.yaml
configmap/mongo-config created
❯ kubectl apply -f mongo-secret.yaml
secret/mongo-secret created
❯ kubectl apply -f mongo.yaml
deployment.apps/mongo-deployment created
service/mongo-service created
❯ kubectl apply -f webapp.yaml
deployment.apps/webapp-deployment created
service/webapp-service created
```

6) Running `kubectl get pod` should output
```
❯ kubectl get pod
NAME                                READY   STATUS              RESTARTS   AGE
mongo-deployment-5cd59c6ff5-sfskv   0/1     ContainerCreating   0          16s
webapp-deployment-bd7557f5c-kjs5z   0/1     ContainerCreating   0          14s
```
7) Run `minikube service webapp-service`
* __Purpose__: This command opens a web browser or provides a URL that directly accesses your webapp-service via Minikube's internal DNS and networking setup.
* __How It Works__: Minikube manages a local Kubernetes cluster, and when you run minikube service webapp-service, it essentially sets up port forwarding and DNS resolution so that you can access the service as if it were running on your local machine.

8) The web application should automatically run and you should be able to see it on your local browser

Notes: To stop the cluster, run `minikube delete`