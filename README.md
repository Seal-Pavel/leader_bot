### `Kubernetes secrets`
Генерация секретов кубера из .env файлов:
```sh
kubectl create secret generic leader-bot-secret --from-env-file="./.env" --namespace=leader-bot --dry-run=client -o yaml > ./k8s/leader-bot-secret.yaml
```
Применение на сервере:
```sh
kubectl apply -f ./leader-bot-secret.yaml
```