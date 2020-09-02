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
		-L "https://github.com/sio/Makefile.venv/raw/v2020.08.14/Makefile.venv"
	echo "5afbcf51a82f629cd65ff23185acde90ebe4dec889ef80bbdc12562fbd0b2611 *Makefile.fetched" \
		| sha256sum --check - \
		&& mv Makefile.fetched Makefile.venv
