PYTEST_ARGS?=-p no:cacheprovider
REQUIREMENTS_TXT=tests/requirements.txt
SED?=sed


CLEANUP_FILES=Makefile.venv
CLEANUP_DIRS=.hypothesis


test: deps venv
	$(VENV)/pytest $(PYTEST_ARGS)


lint:
	shellcheck --version
	shellcheck bash_completion


clean: clean-venv
	-$(RM) $(CLEANUP_FILES)
	-$(RM) -r $(CLEANUP_DIRS)


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
		-L "https://github.com/sio/Makefile.venv/raw/v2019.12.05/Makefile.venv"
	echo "1b0a2f89b322ea86958d63ed4ae718846ccaaf939e5e24180524f28dede238ba *Makefile.fetched" \
		| sha256sum --check - \
		&& mv Makefile.fetched Makefile.venv
