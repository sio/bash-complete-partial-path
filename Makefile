PYTEST_ARGS?=-p no:cacheprovider
REQUIREMENTS_TXT=tests/requirements.txt
SED?=sed


test: deps venv
	$(VENV)/pytest $(PYTEST_ARGS)


.PHONY: deps
deps:
	$(MAKE) --version
	$(PY) --version
	$(SED) --version
	bash --version


include Makefile.venv
Makefile.venv:
	curl \
		-o Makefile.fetched \
		-L "https://github.com/sio/Makefile.venv/raw/v2019.11.22/Makefile.venv"
	echo "048c4a1b9265231db97b4903bb2e835b01e0d84a5b7435d4bb8d5926c99aa7f7 *Makefile.fetched" \
		| sha256sum --check - \
		&& mv Makefile.fetched Makefile.venv
