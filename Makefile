
prefix=/usr/local
bindir=$(prefix)/bin
datadir=$(prefix)/share
docdir=$(datadir)/doc

DESTDIR=

INSTALL=install
INSTALL_DATA=install -m 644
INSTALL_DIR=install -d

UNINSTALL=rm
UNINSTALL_DIR=rm -r

pkg_datadir=$(datadir)/cjc
pkg_docdir=$(docdir)/cjc


VERSION=1.2.1
SNAPSHOT=

PY_DIRS=cjc cjc/ui plugins
DOCS=doc/manual.html COPYING ChangeLog README TODO

EXTRA_DIST=cjc.in cjc.py doc/manual.xml doc/Makefile cjc.spec

.PHONY: all version dist cosmetics ChangeLog

all: cjc.inst $(DOCS) version

doc/manual.html: doc/manual.xml 
	cd doc; make

version: 
	if test -d ".git" ; then \
		echo "version='$(VERSION)+git'" > cjc/version.py || : ; \
	fi

cjc.inst: cjc.in
	sed -e 's,BASE_DIR,$(pkg_datadir),' < cjc.in > cjc.inst 

ChangeLog: 
	test -d .git && make cl-stamp || :
	test -d .git && make spec || :
	
cl-stamp: .git
	git log > ChangeLog
	touch cl-stamp

cosmetics:
	./aux/cosmetics.sh
	
clean:
	-rm -f cjc.inst

spec:
	sed -i 's/\(^Version:[ \t]*\)\([0-9.A-Za-z_-]*\)/\1$(VERSION)/g' cjc.spec
	sed -i -n '1,/%changelog/p' cjc.spec
	git-log |grep -v ^commit|sed 's/ *-/-/g'|sed 's/^  */- /g'| awk '/Author/ {a=$$0;gsub("Author:","",a);next} /Date/ {d=$$2" "$$3" "$$4" "$$6; gsub("-.*","",d);print "\n* "d,a;next} /^-/ {print} '|sed 1d |grep -v '^- $$' >>cjc.spec

	#git-log |grep -v ^commit|sed 's/ *-/-/g'|sed 's/^  */- /g'| awk '/Author/ {a=$0;gsub("Author:","",a);next} /Date/ {d=$2" "$3" "$4" "$6; gsub("-.*","",d);print "\n* "d,a;next} /^-/ {print} '|sed 1d |grep -v '^- $' >>../SPECS/python26-pyxmpp.spec

install: all
	for d in $(PY_DIRS) ; do \
		$(INSTALL_DIR) $(DESTDIR)$(pkg_datadir)/$$d ; \
		$(INSTALL_DATA) $$d/*.py $(DESTDIR)$(pkg_datadir)/$$d ; \
	done
	python26 -c "import compileall; compileall.compile_dir('$(DESTDIR)$(pkg_datadir)', ddir='$(pkg_datadir)')" 
	$(INSTALL_DIR) $(DESTDIR)$(pkg_docdir)
	$(INSTALL_DATA) $(DOCS) $(DESTDIR)$(pkg_docdir)
	$(INSTALL_DIR) $(DESTDIR)$(bindir)
	$(INSTALL) cjc.inst $(DESTDIR)$(bindir)/cjc

uninstall:
	for d in $(PY_DIRS) ; do \
		$(UNINSTALL_DIR) $(DESTDIR)$(pkg_datadir)/$$d ; \
	done || :
	$(UNINSTALL_DIR) $(DESTDIR)$(pkg_datadir) || :
	$(UNINSTALL_DIR) $(DESTDIR)$(pkg_docdir) || :
	$(UNINSTALL) $(DESTDIR)$(bindir)/cjc || :

dist: all
	echo "version='$(VERSION)$(SNAPSHOT)'" > cjc/version.py ; \
	version=`python26 -c "import cjc.version; print cjc.version.version"` ; \
	distname=cjc-$$version ; \
	for d in $(PY_DIRS) ; do \
		$(INSTALL_DIR) $$distname/$$d || exit 1 ; \
		cp -a $$d/*.py $$distname/$$d || exit 1 ; \
	done || exit 1 ; \
	for f in $(DOCS) $(EXTRA_DIST) ; do \
		d=`dirname $$f` ; \
		$(INSTALL_DIR) $$distname/$$d || exit 1; \
		cp -a $$f $$distname/$$d || exit 1; \
	done ; \
	sed -e "s/^SNAPSHOT=.*/SNAPSHOT=$(SNAPSHOT)/" Makefile > $$distname/Makefile ; \
	mkdir -p dist ; \
	tar czf dist/$${distname}.tar.gz $$distname && \
	rm -r $$distname
