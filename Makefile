PYTEST_ARGS?=-p no:cacheprovider
REQUIREMENTS_TXT=tests/requirements.txt


test: venv
	$(VENV)/pytest $(PYTEST_ARGS)


include Makefile.venv
Makefile.venv:
	curl \
		-o Makefile.fetched \
		-L "https://github.com/sio/Makefile.venv/raw/v2019.11.08/Makefile.venv"
	echo "71133c27bf6979d10ed470e122d5207e35217fef06c37341c175057f60ecf3a7 *Makefile.fetched" \
		| sha256sum --check - \
		&& mv Makefile.fetched Makefile.venv
