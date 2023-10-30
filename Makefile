run:
	python3 main.py

build:
	docker build -t battlesnake .
	
start:
	docker run -p 80:80 --rm battlesnake

forward:
	ngrok http 8000

server: build start 
	@echo "Started application server"

clean:
	@echo "Cleaning up"

.DEFAULT_GOAL := run
