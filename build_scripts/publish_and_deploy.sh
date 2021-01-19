echo $2 | docker login -u $1 --password-stdin
docker push $1/todo-app:latest