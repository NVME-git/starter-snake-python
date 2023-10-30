build:
	docker build -t battlesnake .
start:
	docker run -p 80:8000 --rm battlesnake
forward:
	ngrok http 80
