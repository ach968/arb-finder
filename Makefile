.PHONY: frontend backend database all

all: frontend backend database

frontend:
	@echo "starting frontend..."
	@gnome-terminal -- bash -c "cd frontend && npm run dev; exec bash" 

backend:
	@echo "starting backend..."
	@gnome-terminal -- bash -c "cd backend && npm start; exec bash"

database:
	@echo "starting database..."
	@gnome-terminal -- bash -c "cd database && python3 app_init.py; exec bash"


