.PHONY: compile sync help

help:
	@echo " compile  - Compile requirements"
	@echo " sync     - Sync development requirements"

compile:
	rm -rf requirements/requirements*.txt
	pip-compile requirements/requirements.in
	pip-compile requirements/requirements-dev.in

sync:
	pip-sync requirements/requirements-dev.txt