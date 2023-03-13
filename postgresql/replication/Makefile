PROFILE_NAME=postgresql

cluster:
	minikube start driver=docker --nodes 3 --profile=$(PROFILE_NAME)

finalize:
	minikube delete --profile=$(PROFILE_NAME)

tunnel:
	minikube tunnel --profile=$(PROFILE_NAME)
