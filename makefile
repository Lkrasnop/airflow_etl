venv:
	python3 -m venv venv
	# source venv/bin/activate   # On macOS and Linux

source: 
	source venv/bin/activate

install:
	pip install --upgrade pip &&\
	pip install -r requirements.txt

run: install
	python3 check_postgres.py

format:
	black main.py

lint: format
	pylint --disable=R,C,E0401,E0611 main2.py

remove:
	rm -rf venv

deactivate:
	deactivate

git_zero:
	git status
	git add . &&\
	git fetch origin &&\
	git merge origin/main &&\
	git commit -m "add layers of feature importance + compare between two models" &&\
	git push
# git fetch origin
# git merge origin/main

DOCKER_IMAGE_NAME = text2sql-app
DOCKER_CONTAINER_NAME = text2sql-container

.PHONY: docker-build docker-run docker-stop docker-clean docker-test

docker-build:
	docker build -t $(DOCKER_IMAGE_NAME) .

docker-run:
	docker run -d -p 5000:5000 --name $(DOCKER_CONTAINER_NAME) $(DOCKER_IMAGE_NAME)

docker-stop:
	docker stop $(DOCKER_CONTAINER_NAME)
	docker rm $(DOCKER_CONTAINER_NAME)

docker-clean: docker-stop
	docker rmi $(DOCKER_IMAGE_NAME)

docker-test:
	docker run --rm $(DOCKER_IMAGE_NAME) python -m unittest test.py

# Git commands
git:
	git status
	git add . &&\
	git commit -m "remove notebook and rename notebook 6 with notebook" &&\
	git push

# Test command (can be used for both local and Docker environments)
test:
	python -m unittest main_test.py