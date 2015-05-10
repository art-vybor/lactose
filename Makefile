PREFIX ?= /usr/local
BIN_DIR = $(PREFIX)/bin
LIB_DIR = $(PREFIX)/lib/python2.7/dist-packages


INSTALL_TARGETS = install-dir install-package clean

install: $(INSTALL_TARGETS)

install-dir:
	install -d $(PREFIX) $(BIN_DIR) $(LIB_DIR)

install-package: install-dir
	PYTHONPATH=$(LIB_DIR) python setup.py -q install --prefix=$(PREFIX)


clean: install-package
	rm -rf build
	rm -rf dist
	rm -rf lactose.egg-info