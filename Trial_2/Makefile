all: build up

build:
	docker-compose build

up:
	docker-compose up -d

down:
	docker-compose down

clean:
	docker-compose down --rmi all --volumes

test:
	@echo "Testing /rep endpoint"
	@curl -s http://localhost:5000/rep
	@echo "\nTesting /home endpoint"
	@curl -s http://localhost:5000/home
	@echo "\nAdding 2 servers"
	@curl -s -X POST -H "Content-Type: application/json" -d '{"n": 2, "hostnames": ["s4", "s5"]}' http://localhost:5000/add
	@echo "\nTesting /rep after adding"
	@curl -s http://localhost:5000/rep
	@echo "\nRemoving 2 servers"
	@curl -s -X DELETE -H "Content-Type: application/json" -d '{"n": 2, "hostnames": ["s4", "s5"]}' http://localhost:5000/rm
	@echo "\nTesting /rep after removing"
	@curl -s http://localhost:5000/rep