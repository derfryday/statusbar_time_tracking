VENV = .venv
MAIN = src/statusbar_time_tracker/app.py
#NUITKA = $(VENV)/bin/nuitka3
NUITKA_OPTIONS = --standalone --onefile --macos-create-app-bundle --macos-app-name=StatusbarTimeTracker --macos-signed-app-name='dev.derfryday.StatusbarTimeTracker' --output-filename=StatusbarTimeTracker --include-data-dir=src/statusbar_time_tracker/resources=statusbar_time_tracker/resources --product-name=StatusbarTimeTracker

BUILD:
	poetry install
	$(VENV)/bin/nuitka3 $(NUITKA_OPTIONS) $(MAIN)
