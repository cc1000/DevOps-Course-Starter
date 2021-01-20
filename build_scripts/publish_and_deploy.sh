docker push $1/todo-app:latest
docker tag $1/todo-app:latest registry.heroku.com/cree1000-todo-app/web
echo $3 | docker login -u $2 --password-stdin registry.heroku.com
docker push registry.heroku.com/cree1000-todo-app/web
heroku container:release -a cree1000-todo-app web