PYTEST_ARGS?=-p no:cacheprovider
REQUIREMENTS_TXT=tests/requirements.txt
SED?=sed


CLEANUP_FILES=Makefile.venv
CLEANUP_DIRS=.hypothesis


test: deps venv
	$(VENV)/pytest $(PYTEST_ARGS)


lint:
	@shellcheck --version
	shellcheck --color=always bash_completion


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


# Override default venv packages for older Python versions
# https://github.com/pypa/get-pip/pull/46/files
ifeq (True,$(shell $(PY) -c "import sys; print(sys.version_info < (3,5))"))
$(VENV):
	$(PY) -m venv $(VENVDIR)
	$(VENV)/python -m pip install --upgrade "pip<19.2" "setuptools<44.0" "wheel<0.34"
endif
