PREFIX ?= /usr/local
BIN_DIR = $(PREFIX)/bin
LIB_DIR = $(PREFIX)/lib/python2.7/site-packages


INSTALL_TARGETS = install-dir install-package clean

install: $(INSTALL_TARGETS)

install-dir:
	install -d $(PREFIX) $(BIN_DIR) $(LIB_DIR)

install-package: install-dir clean
	java -jar ./lib/antlr-4.5-complete.jar -Dlanguage=Python2 ./lactose/grammar/lactose.g4
	PYTHONPATH=$(LIB_DIR) python setup.py install --prefix=$(PREFIX) test
	@echo 'Lactose successfully installed'

clean:
	@find . -name \*.pyc -delete
	@rm -rf build dist lactose.egg-info