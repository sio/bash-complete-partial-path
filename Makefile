PYTEST_ARGS?=-p no:cacheprovider
REQUIREMENTS_TXT=tests/requirements.txt
SED?=sed


test: deps venv
	$(VENV)/pytest $(PYTEST_ARGS)


lint:
	shellcheck --version
	shellcheck bash_completion


clean: clean-venv


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
		-L "https://github.com/sio/Makefile.venv/raw/v2019.12.04/Makefile.venv"
	echo "8951aeb17406548c6f50c2b7eb1142d16d1939cc40297977ea6a53731470b525 *Makefile.fetched" \
		| sha256sum --check - \
		&& mv Makefile.fetched Makefile.venv
