# Setup Kubeflow workspace 

## I. Preresquites 

- K8s or MiniKube 

- Docker 

## II. Guidance
1. Install manifests 

- Install kustomize:
```bash
export PIPELINE_VERSION=1.8.5
kubectl apply -k "github.com/kubeflow/pipelines/manifests/kustomize/cluster-scoped-resources?ref=$PIPELINE_VERSION"
kubectl wait --for condition=established --timeout=300s crd/applications.app.k8s.io
kubectl apply -k "github.com/kubeflow/pipelines/manifests/kustomize/env/platform-agnostic-pns?ref=$PIPELINE_VERSION"
```

- Check state 

```bash 
kubectl get deploy -n kebeflow
```

- access the **ml-pupeline-ui** 

```bash
kubectl port-forward -n kubeflow svc/ml-pipeline-ui 8080:80
```




