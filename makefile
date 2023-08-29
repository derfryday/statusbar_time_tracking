VENV = .venv
MAIN = src/statusbar_time_tracker/app.py
#NUITKA = $(VENV)/bin/nuitka3
NUITKA_OPTIONS = --static-libpython=no --macos-app-mode=background --disable-console --noinclude-pytest-mode=nofollow --noinclude-setuptools-mode=nofollow --standalone --onefile --macos-create-app-bundle --macos-app-name=StatusbarTimeTracker --macos-signed-app-name='dev.derfryday.StatusbarTimeTracker' --output-filename=StatusbarTimeTracker --include-data-dir=src/statusbar_time_tracker/resources=statusbar_time_tracker/resources --include-data-files=Info.plist=Info.plist --product-name=StatusbarTimeTracker

BUILD:
	poetry install --without dev
	$(VENV)/bin/nuitka3 $(NUITKA_OPTIONS) $(MAIN)
