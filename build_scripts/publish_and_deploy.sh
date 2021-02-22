echo $2 | docker login -u $1 --password-stdin registry.heroku.com
docker push registry.heroku.com/cree1000-todo-app/web
heroku container:release -a cree1000-todo-app web