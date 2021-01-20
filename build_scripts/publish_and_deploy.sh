docker push $1/todo-app:latest
docker tag $1/todo-app:latest registry.heroku.com/cree1000-todo-app/web
docker login --username=$2 --password=$3 registry.heroku.com
docker push registry.heroku.com/cree1000-todo-app/web
heroku container:release -a cree1000-todo-app web