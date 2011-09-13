# $Revision: 1.21 $, $Date: 2005/12/26 20:22:24 $
#
Summary:	Console Jabber Client
Summary(pl):	CJC - konsolowy klient Jabbera
Name:		cjc
Version:	1.2.1
Release:	1
Epoch:		1
License:	GPL
Group:		Applications/Communications
Source0:	http://files.jabberstudio.org/cjc/cjc-%{version}.tar.gz
#Patch1:		cjc_python26.patch
URL:		http://cjc.jabberstudio.org/
Requires:	python26-pyxmpp, dnspython26, python26, libxml2-python26
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
A Jabber client for text terminals with user interface similar to
those known from popular IRC clients.

%description -l pl
Klient Jabbera dla terminali tekstowych z interfejsem użytkownika
podobnym do tego znanego z popularnych klientów IRC.

%prep
%setup -q
#%patch1 -p1

%build
%{__make} \
	prefix=%{_prefix}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	prefix=%{_prefix} \
	DESTDIR=$RPM_BUILD_ROOT

rm -rf $RPM_BUILD_ROOT%{_prefix}/share/doc

rm -f $RPM_BUILD_ROOT%{_datadir}/%{name}/%{name}{,/ui}/*.py

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README TODO ChangeLog doc/manual.html
%attr(755,root,root) %{_bindir}/*
%dir %{_datadir}/%{name}
%dir %{_datadir}/%{name}/%{name}
%dir %{_datadir}/%{name}/%{name}/ui
%dir %{_datadir}/%{name}/plugins
%{_datadir}/%{name}/%{name}/*.pyc
%{_datadir}/%{name}/%{name}/ui/*.pyc
%{_datadir}/%{name}/plugins/*

%define date	%(echo `LC_ALL="C" date +"%a %b %d %Y"`)
%changelog
* Fri Aug 26 2011  Jacek Konieczny <jajcus@jajcus.net>
- Merge pull request #45 from flocke/master
- MUC Autojoin
- Looks good and I assume its tested.

* Fri Aug 26 2011  flocke <flocke@shadowice.org>
- replaced event 'autojoin' with 'roster updated'

* Fri Aug 26 2011  flocke <flocke@shadowice.org>
- added autojoin function to the muc plugin

* Fri Aug 26 2011  flocke <flocke@shadowice.org>
- added 'autojoin' event after loading the roster for the first time

* Sun May 8 2011  Jacek Konieczny <jajcus@jajcus.net>
- Fix plugin loading from *.pyc or *.pyo files

* Sun May 8 2011  Jacek Konieczny <jajcus@jajcus.net>
- Version: 1.2.1

* Sun May 8 2011  Jacek Konieczny <jajcus@jajcus.net>
- Backspace fix for broken terminals
- Back-space key often did not work corretly. This was because
- 'backspace' key code in the terminfo database was set to something
- else then the key actually sends. At the same time 'erase' character
- is properly set in the terminal settings, so the key works in other
- application.
- This patch implements a workaround: if there is no key binding for
- a pressed key and the key is current terminal 'erase' character, treat
- it as KEY_BACKSPACE. This should give the expected behaviour in most
- cases.
- As the 'erase' character, sent by the backspace key, is usually '^?' I
- had also removed the default binding for '^?'. I hope this won't break
- more than this patch is supposed to fix.

* Sun May 8 2011  Jacek Konieczny <jajcus@jajcus.net>
- Don't fail on unicode host name
- Exception would be raised when formatting informational
- message about TLS connection if there are non-ASCII characters
- in the server hostname. This patch fixes this.

* Sun May 8 2011  Jacek Konieczny <jajcus@jajcus.net>
- Better syntax IPv6 address:port info messages
- Put IPv6 addresses in [] when showing the 'Connecting to addr:port' or
- 'Connected to addr:port' messages.

* Fri May 6 2011  Jacek Konieczny <jajcus@jajcus.net>
- Store locally generated thread-ids as unicode
- When locally generated thread-ids where kept as UUID object
- instead of unicode string comparisons didn't work right.

* Fri May 6 2011  Jacek Konieczny <jajcus@jajcus.net>
- "chat.merge_threads" option
- This option allows reusing single window for any thread-id sent
- by a peer. This is mostly useful for broken XMPP clients which send
- a different thread-id in every message.

* Fri May 6 2011  Jacek Konieczny <jajcus@jajcus.net>
- Use UUIDs as thread-ids
- Up to now CJC generated thread-ids using a fixed prefix
- and a sequence number startin again on each CJC startup.
- This way the same thread-id could be reused in quite a separate
- conversation.

* Tue May 3 2011  Jacek Konieczny <jajcus@jajcus.net>
- More .gitignores

* Tue May 3 2011  Jacek Konieczny <jajcus@jajcus.net>
- Some .gitignores added

* Tue May 3 2011  Jacek Konieczny <jajcus@jajcus.net>
- Updates for the svn->git migration

* Tue May 3 2011  Jacek Konieczny <jajcus@jajcus.net>
- Updates for the svn->github migration

* Tue May 3 2011  Jacek Konieczny <jajcus@jajcus.net>
- new settings: 'ipv6' and 'dual_stack'

* Tue May 3 2011  Jacek Konieczny <jajcus@jajcus.net>
- kind of better DNS error reporting

* Tue Feb 1 2011  Jacek Konieczny <jajcus@jajcus.net>
- memory profilling helpers (using Heapy from Guppy)

* Thu Aug 5 2010  Jacek Konieczny <jajcus@jajcus.net>
- another timestamp pattern for log migration, fixes #44

* Tue Apr 27 2010  Jacek Konieczny <jajcus@jajcus.net>
- archive browsing optimization: do not use peer index when requesting date range

* Mon Apr 26 2010  Jacek Konieczny <jajcus@jajcus.net>
- one more 1.2.0 fix: when fetching archive lookup by bare JID only

* Mon Apr 26 2010  Jacek Konieczny <jajcus@jajcus.net>
- *** Version: 1.2.0 (last-minute fixes included) ***

* Mon Apr 26 2010  Jacek Konieczny <jajcus@jajcus.net>
- avoid trying to import a plugin twice when first import failed

* Mon Apr 26 2010  Jacek Konieczny <jajcus@jajcus.net>
- handle ImportError more gracefully

* Mon Apr 26 2010  Jacek Konieczny <jajcus@jajcus.net>
- locate settings when starting import, not on module load (settings are not loaded then)

* Mon Apr 26 2010  Jacek Konieczny <jajcus@jajcus.net>
- migrate settings on start-up

* Mon Apr 26 2010  Jacek Konieczny <jajcus@jajcus.net>
- *** Version: 1.2.0 ***

* Mon Apr 26 2010  Jacek Konieczny <jajcus@jajcus.net>
- do not reload plugin modules when not asked to

* Mon Apr 26 2010  Jacek Konieczny <jajcus@jajcus.net>
- do not play magic with module import paths and load CJC plugins as modulues of a virtual 'cjc._plugins' package

* Mon Apr 26 2010  Jacek Konieczny <jajcus@jajcus.net>
- tls_ca_cert_file is not tls_cert_file

* Sun Apr 25 2010  Jacek Konieczny <jajcus@jajcus.net>
- initialize the database on CJC start
- inform about the possibility of turning file logging off

* Sun Apr 25 2010  Jacek Konieczny <jajcus@jajcus.net>
- EventListener interface added

* Sun Apr 25 2010  Jacek Konieczny <jajcus@jajcus.net>
- duplicates when scrolling over received chate messages, fixed

* Sun Apr 25 2010  Jacek Konieczny <jajcus@jajcus.net>
- mark the archive end in message window
- variable name fix

* Sun Apr 25 2010  Jacek Konieczny <jajcus@jajcus.net>
- fixed duplicates in archive display when scrolling over some received messages

* Sat Apr 24 2010  Jacek Konieczny <jajcus@jajcus.net>
- /migrate_archive command implemented: migrating old file logs into the new sqlite3 archive

* Sat Apr 24 2010  Jacek Konieczny <jajcus@jajcus.net>
- page-up archive browsing added

* Sat Apr 24 2010  Jacek Konieczny <jajcus@jajcus.net>
- expand '~' in path settings

* Sat Apr 24 2010  Jacek Konieczny <jajcus@jajcus.net>
- expang '~' in roster.cache_file setting
- display roster when loaded from cache

* Sat Apr 24 2010  Jacek Konieczny <jajcus@jajcus.net>
- allow opening chat window when not connecting
- small archive records handling fix

* Sat Apr 24 2010  Jacek Konieczny <jajcus@jajcus.net>
- cache file to persist roster over cjc restart

* Sat Apr 24 2010  Jacek Konieczny <jajcus@jajcus.net>
- emit 'config loaded' event

* Sat Apr 24 2010  Jacek Konieczny <jajcus@jajcus.net>
- usefull command table 'buffer'- with one command: '/close'

* Thu Apr 22 2010  Jacek Konieczny <jajcus@jajcus.net>
- use the True and False constants

* Thu Apr 22 2010  Jacek Konieczny <jajcus@jajcus.net>
- CLI interface for plugins

* Mon Apr 19 2010  Jacek Konieczny <jajcus@jajcus.net>
- include current date (ISO format) when timestamp is not from today

* Mon Apr 19 2010  Jacek Konieczny <jajcus@jajcus.net>
- scrolling fix

* Mon Apr 19 2010  Jacek Konieczny <jajcus@jajcus.net>
- show only those archival records which older than current chat window

* Wed Apr 14 2010  Jacek Konieczny <jajcus@jajcus.net>
- simple chat archive browsing by scrolling over the begining of the current
- chat

* Wed Apr 14 2010  Jacek Konieczny <jajcus@jajcus.net>
- update window after scrolling, even scrolled to the beginning of the buffer

* Wed Apr 14 2010  Jacek Konieczny <jajcus@jajcus.net>
- do not eat KeyError exceptions generated by command or key-function
- implementations. Use more specific exception to signal missing command,
- function, keytable or key binding

* Tue Apr 13 2010  Jacek Konieczny <jajcus@jajcus.net>
- overridable .fill_topunderflow() method- a facility to append extra
- content at the begining of the buffer when scrolling over the top
- of the existing data

* Tue Apr 13 2010  Jacek Konieczny <jajcus@jajcus.net>
- code cleanup and documentation

* Sun Apr 11 2010  Jacek Konieczny <jajcus@jajcus.net>
- initial implementation of the sqlite archive

* Sun Apr 11 2010  Jacek Konieczny <jajcus@jajcus.net>
- major changes:
- plugin subsystem rewritten, so plugin services can be looked up by provided
- interface (as an abstract base class)
- file logging moved from chat and message plugind to the new file_logger
- plugin (preparing for a database-based archive as an alternative)
- Version: 1.1.99, so the trunk differs from the 'stable' 1.1.x branch

* Sun Apr 11 2010  Jacek Konieczny <jajcus@jajcus.net>
- python doesn't recognize \e, use \x1b instead

* Fri Apr 9 2010  Jacek Konieczny <jajcus@jajcus.net>
- catch KeyError instead of checking item for None to detect roster.get_item_by_jid() failure

* Mon Apr 5 2010  Jacek Konieczny <jajcus@jajcus.net>
- Version: 1.1.0

* Mon Apr 5 2010  Jacek Konieczny <jajcus@jajcus.net>
- copyright header updated

* Mon Apr 5 2010  Jacek Konieczny <jajcus@jajcus.net>
- properly display subjectAltName when available

* Mon Apr 5 2010  Jacek Konieczny <jajcus@jajcus.net>
- ^W when cursor inside the first word fixed (fixes #28)

* Mon Apr 5 2010  Jacek Konieczny <jajcus@jajcus.net>
- choice_input fixed (was broken when UTF-8 console support was introduced). fixes #41

* Sun Apr 4 2010  Jacek Konieczny <jajcus@jajcus.net>
- use get() to read optional settings (fixes #38)

* Sun Apr 4 2010  Jacek Konieczny <jajcus@jajcus.net>
- do not duplicate information about certificate error being ignored, when
- tls_verify is on

* Sun Apr 4 2010  Jacek Konieczny <jajcus@jajcus.net>
- 'encrypted connection established' message fix

* Sun Apr 4 2010  Jacek Konieczny <jajcus@jajcus.net>
- remove hardcoded 'subject_name_valid=False'

* Sun Apr 4 2010  Jacek Konieczny <jajcus@jajcus.net>
- 'tls_verify' option added (default true)
- use 'openssl x509' to parse binary certificate when showing unverified
- certificate information

* Sat Apr 3 2010  Jacek Konieczny <jajcus@jajcus.net>
- updated for the recent pyxmpp changes (M2Crypto replaced by the standard 'ssl' module)

* Sat Jan 17 2009  Jacek Konieczny <jajcus@jajcus.net>
- *** Version: 1.0.1 ***

* Sat Jan 17 2009  Jacek Konieczny <jajcus@jajcus.net>
- updates for the 1.0.1 release

* Sat Jan 17 2009  Jacek Konieczny <jajcus@jajcus.net>
- new version of svn2log.py copied from pyxmpp

* Sat Jan 17 2009  Jacek Konieczny <jajcus@jajcus.net>
- not needed for many years...

* Sat Jan 17 2009  Jacek Konieczny <jajcus@jajcus.net>
- UTF-8 input support

* Sun Sep 28 2008  Jacek Konieczny <jajcus@jajcus.net>
- show peer nick in the 'chat ... started' message

* Wed Feb 20 2008  Jacek Konieczny <jajcus@jajcus.net>
- always treat jid argument to /disco as a JID

* Mon Apr 16 2007  Jacek Konieczny <jajcus@jajcus.net>
- typo

* Mon Apr 16 2007  Jacek Konieczny <jajcus@jajcus.net>
- fixed non-ascii characters handling in /version response

* Mon Dec 11 2006  Jacek Konieczny <jajcus@jajcus.net>
- 'typos' patch from PLD applied

* Wed Oct 25 2006  Jacek Konieczny <jajcus@jajcus.net>
- last change (stanza serialization in set_user_info()) reverted-- it was done wrong and not needed

* Wed Oct 25 2006  Jacek Konieczny <jajcus@jajcus.net>
- unset 'to' in the saved presence for auto_away, not in user_info

* Wed Oct 25 2006  Jacek Konieczny <jajcus@jajcus.net>
- include a serialized stanza in set_user_info() debug output

* Wed Oct 25 2006  Jacek Konieczny <jajcus@jajcus.net>
- unset 'to' when saving presence during auto_away

* Wed Oct 25 2006  Jacek Konieczny <jajcus@jajcus.net>
- some set_user_info() debuging

* Mon Oct 16 2006  Jacek Konieczny <jajcus@jajcus.net>
- when auto_popup is on display actual buffer instead of MessageBuffer (I know, this class name sucks). fixes #23

* Mon Oct 16 2006  Jacek Konieczny <jajcus@jajcus.net>
- include newline in the /who command output (fixes #22)

* Fri Sep 29 2006  Jacek Konieczny <jajcus@jajcus.net>
- screen is now in cjc_globals

* Thu Sep 28 2006  Jacek Konieczny <jajcus@jajcus.net>
- screen is now in cjc_globals

* Thu Sep 7 2006  Jacek Konieczny <jajcus@jajcus.net>
- refactorization: cjc_globals module with three singletons (Application, Screen and ThemeManager) instead of passing around again and again references to the same objects

* Wed Sep 6 2006  Jacek Konieczny <jajcus@jajcus.net>
- Updated for recent PyXMPP TLS changes and the new M2Crypto

* Mon Jul 24 2006  Jacek Konieczny <jajcus@jajcus.net>
- new MUC command: /query, to start a 'private' chat

* Sun Jul 23 2006  Jacek Konieczny <jajcus@jajcus.net>
- use user nickname (instead of room name) during private chat with a MUC room occupant (fixes #20)

* Sun Jul 23 2006  Jacek Konieczny <jajcus@jajcus.net>
- default theme for the bottom status bar changed to display active buffer list first and leave a lot of space for status description at the end of line (refs: #11)

* Sun Jul 23 2006  Jacek Konieczny <jajcus@jajcus.net>
- use 'x in s' instead of 's.find(x)>=0'

* Sun Jul 23 2006  Jacek Konieczny <jajcus@jajcus.net>
- don't treat jid-only, no-node-part roster entires as unknown when referenced by jid without leading '@' (fixes #17), requires current PyXMPP

* Sun Jul 23 2006  Jacek Konieczny <jajcus@jajcus.net>
- /info will now show priority together with other presence information (fixes #21)

* Mon Jun 26 2006  Jacek Konieczny <jajcus@jajcus.net>
- convert JID to unicode before using it in a message (fixes #18, thanks chris)

* Tue Jun 6 2006  Jacek Konieczny <jajcus@jajcus.net>
- create ~/.cjc directory and save config files with safe permissions (fixes #6)

* Sun Jun 4 2006  Jacek Konieczny <jajcus@jajcus.net>
- (c) years updated

* Sun Jun 4 2006  Jacek Konieczny <jajcus@jajcus.net>
- addresses updated

* Tue May 30 2006  Jacek Konieczny <jajcus@jajcus.net>
- not needed here (in the new repository)

* Mon May 29 2006  Jacek Konieczny <jajcus@jajcus.net>
- an important notice about repository being moved

* Thu May 25 2006  Jacek Konieczny <jajcus@jajcus.net>
- get_best_user() fixed... now really the best JID will be chosen from several with the same roster name

* Thu May 18 2006  Jacek Konieczny <jajcus@jajcus.net>
- use itertools.{count,izip} instead of xrange and zip

* Mon Apr 17 2006  Jacek Konieczny <jajcus@jajcus.net>
- yet another fix for roster update artefacts

* Sun Apr 16 2006  Jacek Konieczny <jajcus@jajcus.net>
- roster update artefacts (including empty line after a long status description) hopefully removed

* Sun Apr 9 2006  Jacek Konieczny <jajcus@jajcus.net>
- roster export/import

* Sun Apr 9 2006  Jacek Konieczny <jajcus@jajcus.net>
- simple message multicasting (/multi_message command)

* Sat Apr 8 2006  Jacek Konieczny <jajcus@jajcus.net>
- don't try to do anything with nonexistent presence

* Tue Mar 21 2006  Jacek Konieczny <jajcus@jajcus.net>
- s/get_jid/get_from/

* Tue Mar 21 2006  Jacek Konieczny <jajcus@jajcus.net>
- do not save user_info under resource 'None'

* Tue Mar 21 2006  Jacek Konieczny <jajcus@jajcus.net>
- cosmetics

* Sun Mar 5 2006  Jacek Konieczny <jajcus@jajcus.net>
- another jid-as-strning abuse fixed

* Sun Mar 5 2006  Jacek Konieczny <jajcus@jajcus.net>
- another jid-as-strning abuse fixed

* Sun Mar 5 2006  Jacek Konieczny <jajcus@jajcus.net>
- another jid-as-strning abuse fixed

* Fri Feb 24 2006  Jacek Konieczny <jajcus@jajcus.net>
- more 'jid as string' errors fixed

* Sun Jan 8 2006  Jacek Konieczny <jajcus@jajcus.net>
- /set output fixed for password not set

* Mon Dec 26 2005  Jacek Konieczny <jajcus@jajcus.net>
- *** Version: 1.0.0 ***

* Mon Dec 26 2005  Jacek Konieczny <jajcus@jajcus.net>
- updated

* Mon Dec 26 2005  Jacek Konieczny <jajcus@jajcus.net>
- updated

* Mon Dec 26 2005  Jacek Konieczny <jajcus@jajcus.net>
- another implicit encoding removed (jid.as_string()-> unicode(jid).encode(...) )

* Mon Dec 26 2005  Jacek Konieczny <jajcus@jajcus.net>
- copyright years updated

* Sun Dec 25 2005  Jacek Konieczny <jajcus@jajcus.net>
- fixed handling of 'list-single' fields in data forms

* Sun Dec 25 2005  Jacek Konieczny <jajcus@jajcus.net>
- registrations at services

* Sun Dec 25 2005  Jacek Konieczny <jajcus@jajcus.net>
- fix for non-unicode prompts

* Sat Dec 24 2005  Jacek Konieczny <jajcus@jajcus.net>
- query for password when no password is set in the configuration

* Sat Dec 24 2005  Jacek Konieczny <jajcus@jajcus.net>
- more complete vcard display

* Mon Oct 24 2005  Jacek Konieczny <jajcus@jajcus.net>
- one more JID-as-string usage fixed

* Fri Oct 14 2005  Jacek Konieczny <jajcus@jajcus.net>
- some unicode usage cleanup

* Mon Oct 10 2005  Jacek Konieczny <jajcus@jajcus.net>
- decode edited message back to unicode, otherwise it would work with ASCII or patched Python only

* Fri Sep 16 2005  Jacek Konieczny <jajcus@jajcus.net>
- include error stanza source in error messages

* Thu Aug 25 2005  Jacek Konieczny <jajcus@jajcus.net>
- fixed binding commands in specific keytables. This is hack, the keybinding/keyfunction code needs rewrite (no extra object argument needs to be passed with the binding)

* Sat Jul 23 2005  Jacek Konieczny <jajcus@jajcus.net>
- very ugly bug ('query' instead of 'vCard') not noticed earlier as most server implementations are broken... vCard query on GG Transport should work now

* Wed Jul 13 2005  Jacek Konieczny <jajcus@jajcus.net>
- FO_STYLESHEET fixed

* Fri Jul 8 2005  Jacek Konieczny <jajcus@jajcus.net>
- registration code updated and registration canceling added

* Mon Jun 27 2005  Jacek Konieczny <jajcus@jajcus.net>
- registration improvements

* Mon Jun 27 2005  Jacek Konieczny <jajcus@jajcus.net>
- basic in-band registration support (/register command for creating Jabber accounts)

* Mon Jun 27 2005  Jacek Konieczny <jajcus@jajcus.net>
- typo

* Wed May 25 2005  Jacek Konieczny <jajcus@jajcus.net>
- s/Plugin.cjc.error/Plugin.error/

* Tue May 24 2005  Jacek Konieczny <jajcus@jajcus.net>
- /reorder fixed not to mess displayed buffer numbers

* Tue May 24 2005  Jacek Konieczny <jajcus@jajcus.net>
- /reorder command

* Sat May 7 2005  Jacek Konieczny <jajcus@jajcus.net>
- simple meta-contacts: multiple JIDs with the same name are treated as one
- meta-contact. For /message and /chat commands "the best JID" is chosen (JIDs are assigned weights based
- on their presence and domain name (JIDs in local domain are prefered)). For most of other commands all
- JIDs for the given rostername will be used.

* Wed Apr 27 2005  Jacek Konieczny <jajcus@jajcus.net>
- added configurable scrollback buffer length

* Wed Apr 27 2005  Jacek Konieczny <jajcus@jajcus.net>
- '#21: 'unable to verify the first certificate'' is not fatal

* Wed Apr 27 2005  Jacek Konieczny <jajcus@jajcus.net>
- keepalives fixed

* Wed Apr 27 2005  Jacek Konieczny <jajcus@jajcus.net>
- disconnect stream on any stream error
- format strings for recent tls.py changes

* Wed Apr 27 2005  Jacek Konieczny <jajcus@jajcus.net>
- only some certificate verification errors should be automatically ignored  when the cerificate is known to be trustworthy. E.g. expired certificates will not be automatically accepted any more

* Fri Apr 22 2005  Jacek Konieczny <jajcus@jajcus.net>
- fixed get_users() for users with '@' in roster names

* Fri Apr 22 2005  Jacek Konieczny <jajcus@jajcus.net>
- immutable local variable is not good as context holder for a callback-- TLS questions should work now

* Thu Apr 21 2005  Jacek Konieczny <jajcus@jajcus.net>
- a few more ask_question() updates

* Sun Apr 17 2005  Jacek Konieczny <jajcus@jajcus.net>
- support for text-multi and jid-multi fields

* Sun Apr 17 2005  Jacek Konieczny <jajcus@jajcus.net>
- by default use the global 'editor' and 'editor_encoding' options

* Sun Apr 17 2005  Jacek Konieczny <jajcus@jajcus.net>
- new global 'editor' and 'editor_encoding' options

* Thu Apr 14 2005  Jacek Konieczny <jajcus@jajcus.net>
- 'boolean' form fields work now

* Thu Apr 14 2005  Jacek Konieczny <jajcus@jajcus.net>
- multiple-option tab-completion works again (was broken by recent ask_question() changes)

* Mon Apr 11 2005  Jacek Konieczny <jajcus@jajcus.net>
- presence subscription dialog fixed after last ask_question() changes

* Tue Apr 5 2005  Jacek Konieczny <jajcus@jajcus.net>
- many of data form field editing work now. Still thinking how to make
- text-multi editing in the single input line.
- "arg" parameter for ask_question() and its callback removed-- the more pythonic way
- is to use the callback itself for context container (it can be generated
- function, bound method, callable class instance or (deprecated) lambda)

* Wed Mar 30 2005  Jacek Konieczny <jajcus@jajcus.net>
- work on room configuration configured... the configuration form can be displayed now, but read-only

* Tue Mar 29 2005  Jacek Konieczny <jajcus@jajcus.net>
- started work on room configuration

* Fri Mar 4 2005  Jacek Konieczny <jajcus@jajcus.net>
- bind writer object from codecs module to console instead of using custom Formatter for Unicode logging

* Sat Feb 26 2005  Jacek Konieczny <jajcus@jajcus.net>
- call start_color() unconditionally

* Sat Feb 26 2005  Jacek Konieczny <jajcus@jajcus.net>
- /add fixed

* Wed Feb 23 2005  Jacek Konieczny <jajcus@jajcus.net>
- s/automaticaly/automatically/

* Wed Feb 23 2005  Jacek Konieczny <jajcus@jajcus.net>
- s/automaticaly/automatically/

* Wed Feb 23 2005  Jacek Konieczny <jajcus@jajcus.net>
- s/automaticaly/automatically/

* Thu Jan 20 2005  Jacek Konieczny <jajcus@jajcus.net>
- update for the recent PyXMPP changes with disco handling

* Wed Jan 19 2005  Jacek Konieczny <jajcus@jajcus.net>
- better handling of presence from bare JIDs

* Sat Jan 15 2005  Jacek Konieczny <jajcus@jajcus.net>
- theme formatting fixed for MUC rooms

* Fri Jan 14 2005  Jacek Konieczny <jajcus@jajcus.net>
- fixed unhandled_keys cache invalidation

* Wed Jan 12 2005  Jacek Konieczny <jajcus@jajcus.net>
- don't ignore meta for cache of keys without handlers

* Wed Jan 12 2005  Jacek Konieczny <jajcus@jajcus.net>
- text input optimizations

* Mon Jan 10 2005  Jacek Konieczny <jajcus@jajcus.net>
- don't panic if disco buffer is not available when the response comes

* Sun Jan 9 2005  Jacek Konieczny <jajcus@jajcus.net>
- ugly typo fixed

* Sun Jan 9 2005  Jacek Konieczny <jajcus@jajcus.net>
- better error messages
- ignore replies for past disco request (when waiting for reply for other address)

* Sun Jan 9 2005  Jacek Konieczny <jajcus@jajcus.net>
- the way back (history) in disco browser

* Sun Jan 9 2005  Jacek Konieczny <jajcus@jajcus.net>
- clear disco buffer when subitem is requested

* Sun Jan 9 2005  Jacek Konieczny <jajcus@jajcus.net>
- user-friendly (hopefully) service browser

* Sun Jan 9 2005  Jacek Konieczny <jajcus@jajcus.net>
- request disco#info first. gives more usable result

* Sun Jan 9 2005  Jacek Konieczny <jajcus@jajcus.net>
- escaped ":" in conditional formats for node names

* Sun Jan 9 2005  Jacek Konieczny <jajcus@jajcus.net>
- ':' escaping in conditional formats
- use 'a in b' instead of 'b.find(a)'

* Sun Jan 9 2005  Jacek Konieczny <jajcus@jajcus.net>
- updated for recent PyXMPP changes

* Wed Jan 5 2005  Jacek Konieczny <jajcus@jajcus.net>
- basic Service Discovery browsing

* Wed Jan 5 2005  Jacek Konieczny <jajcus@jajcus.net>
- fixed processing of empty formatted list

* Wed Jan 5 2005  Jacek Konieczny <jajcus@jajcus.net>
- 'buffer_preference' setting description fixed

* Wed Jan 5 2005  Jacek Konieczny <jajcus@jajcus.net>
- small fix for /close

* Wed Jan 5 2005  Jacek Konieczny <jajcus@jajcus.net>
- plugin reloading fixed

* Fri Dec 31 2004  Jacek Konieczny <jajcus@jajcus.net>
- Alt-D in list window dumps window content to debug log (for debugging)

* Fri Dec 31 2004  Jacek Konieczny <jajcus@jajcus.net>
- some debug instructions removed for improved config loading performance

* Fri Dec 31 2004  Jacek Konieczny <jajcus@jajcus.net>
- updated for recent PyXMPP changes

* Tue Dec 28 2004  Jacek Konieczny <jajcus@jajcus.net>
- FIXME comment for checking CN removed-- that has been already working

* Tue Dec 28 2004  Jacek Konieczny <jajcus@jajcus.net>
- do not show errors if certificate is ok

* Sat Dec 18 2004  Jacek Konieczny <jajcus@jajcus.net>
- workaround for setups where locale.getlocale() return None as encoding

* Thu Dec 16 2004  Jacek Konieczny <jajcus@jajcus.net>
- fixed handling of non-us characters in JID in messages and chats (IMPORTANT:
- format parameters for JIDs must be preceded with "J:" prefix or UnicodeError
- will happen on non-us-ascii JID)
- other unicode handling improvements

* Tue Nov 2 2004  Jacek Konieczny <jajcus@jajcus.net>
- year update

* Sun Oct 31 2004  Jacek Konieczny <jajcus@jajcus.net>
- better format of ChangeLog entries

* Sun Oct 31 2004  Jacek Konieczny <jajcus@jajcus.net>
- set $(SNAPSHOT) in the released Makefile

* Sun Oct 31 2004  Jacek Konieczny <jajcus@jajcus.net>
- /offline command for sending "unavailable" presence
- don't change own presence information after sending a directed <presence/>

* Sat Oct 30 2004  Jacek Konieczny <jajcus@jajcus.net>
- ignore error on 'cl-stamp' test

* Sat Oct 30 2004  Jacek Konieczny <jajcus@jajcus.net>
- ignore 'cl-stamp' file

* Sat Oct 30 2004  Jacek Konieczny <jajcus@jajcus.net>
- another attempt to make good 'ChangeLog' make target

* Sat Oct 30 2004  Jacek Konieczny <jajcus@jajcus.net>
- ChangeLog depending on .svn/entries was a bad idea

* Sat Oct 30 2004  Jacek Konieczny <jajcus@jajcus.net>
- better ChangeLog generation. Should be done only in the SVN working directory and not
- require any external tools by the svn client.

* Wed Oct 27 2004  Jacek Konieczny <jajcus@jajcus.net>
- snapshot versions support

* Wed Oct 27 2004  Jacek Konieczny <jajcus@jajcus.net>
- don't fail on 'ambigous user name' as an argument fo /info-- show info about all matched users

* Tue Oct 26 2004  Jacek Konieczny <jajcus@jajcus.net>
- create tarballs in dist/ subdirectory

* Tue Oct 26 2004  Jacek Konieczny <jajcus@jajcus.net>
- 'ChangeLog' and 'cosmetics' make targets

* Tue Oct 26 2004  Jacek Konieczny <jajcus@jajcus.net>
- s/cvs/svn/ once more

* Tue Oct 26 2004  Jacek Konieczny <jajcus@jajcus.net>
- executable flag set

* Tue Oct 26 2004  Jacek Konieczny <jajcus@jajcus.net>
- s/CVS/SVN/

* Tue Oct 26 2004  Jacek Konieczny <jajcus@jajcus.net>
- cleanup in the main directory (utilities moved to aux/)

* Tue Oct 26 2004  Jacek Konieczny <jajcus@jajcus.net>
- .cvsignore files are not needed in SVN

* Sun Oct 24 2004  Jacek Konieczny <jajcus@jajcus.net>
- ChangeLog update by makelog.sh

* Sun Oct 24 2004  Jacek Konieczny <jajcus@jajcus.net>
- cosmetics

* Sun Oct 24 2004  Jacek Konieczny <jajcus@jajcus.net>
- thread locking debugging helpers

* Sun Oct 24 2004  Jacek Konieczny <jajcus@jajcus.net>
- deadlock condition in draw_buffer() removed

* Sun Oct 24 2004  Jacek Konieczny <jajcus@jajcus.net>
- ChangeLog update by makelog.sh

* Sun Oct 24 2004  Jacek Konieczny <jajcus@jajcus.net>
- flexible logging configuration support and a sample logging configuration file

* Tue Oct 12 2004  Jacek Konieczny <jajcus@jajcus.net>
- ChangeLog update by makelog.sh

* Tue Oct 12 2004  Jacek Konieczny <jajcus@jajcus.net>
- typo

* Mon Oct 11 2004  Jacek Konieczny <jajcus@jajcus.net>
- ChangeLog update by makelog.sh

* Mon Oct 11 2004  Jacek Konieczny <jajcus@jajcus.net>
- StartTLS support fixes

* Wed Oct 6 2004  Jacek Konieczny <jajcus@jajcus.net>
- ChangeLog update by makelog.sh

* Wed Oct 6 2004  Jacek Konieczny <jajcus@jajcus.net>
- Unicode theme formats and UTF-8 theme files

* Mon Sep 27 2004  Jacek Konieczny <jajcus@jajcus.net>
- ChangeLog update by makelog.sh

* Mon Sep 27 2004  Jacek Konieczny <jajcus@jajcus.net>
- /who command for groupchats (patch by Chris Niekel

* Fri Sep 24 2004  Jacek Konieczny <jajcus@jajcus.net>
- ChangeLog update by makelog.sh

* Fri Sep 24 2004  Jacek Konieczny <jajcus@jajcus.net>
- always use 'replace' for str.encode()

* Sat Sep 18 2004  Jacek Konieczny <jajcus@jajcus.net>
- ChangeLog update by makelog.sh

* Sat Sep 18 2004  Jacek Konieczny <jajcus@jajcus.net>
- [-nick nick] added to /join description

* Sat Sep 18 2004  Jacek Konieczny <jajcus@jajcus.net>
- ChangeLog update by makelog.sh

* Sat Sep 18 2004  Jacek Konieczny <jajcus@jajcus.net>
- ChangeLog update by makelog.sh

* Thu Sep 16 2004  Jacek Konieczny <jajcus@jajcus.net>
- ChangeLog update by makelog.sh

* Thu Sep 16 2004  Jacek Konieczny <jajcus@jajcus.net>
- 'to'-> 'stanza_to', 'fr'-> 'stanza_from', 'sid'-> 'stanza_id', 'typ'-> 'stanza_type' (recent PyXMPP changes)

* Thu Sep 16 2004  Jacek Konieczny <jajcus@jajcus.net>
- ChangeLog update by makelog.sh

* Thu Sep 16 2004  Jacek Konieczny <jajcus@jajcus.net>
- typo fixed

* Tue Sep 14 2004  Jacek Konieczny <jajcus@jajcus.net>
- ChangeLog update by makelog.sh

* Tue Sep 14 2004  Jacek Konieczny <jajcus@jajcus.net>
- typo fixed

* Mon Sep 13 2004  Jacek Konieczny <jajcus@jajcus.net>
- ChangeLog update by makelog.sh

* Mon Sep 13 2004  Jacek Konieczny <jajcus@jajcus.net>
- updated for recent PyXMPP changes

* Sun Sep 12 2004  Jacek Konieczny <jajcus@jajcus.net>
- ChangeLog update by makelog.sh

* Sun Sep 12 2004  Jacek Konieczny <jajcus@jajcus.net>
- stream.jid-> stream.me everywhere

* Sat Sep 11 2004  Jacek Konieczny <jajcus@jajcus.net>
- ChangeLog update by makelog.sh

* Sat Sep 11 2004  Jacek Konieczny <jajcus@jajcus.net>
- changes and additions by Marcin Chojnowski (martii)

* Sat Sep 11 2004  Jacek Konieczny <jajcus@jajcus.net>
- ChangeLog update by makelog.sh

* Sat Sep 11 2004  Jacek Konieczny <jajcus@jajcus.net>
- encode buffer content to locale's encoding before sending it to an external command

* Fri Sep 10 2004  Jacek Konieczny <jajcus@jajcus.net>
- ChangeLog update by makelog.sh

* Fri Sep 10 2004  Jacek Konieczny <jajcus@jajcus.net>
- jogger.pl plugin

* Fri Sep 10 2004  Jacek Konieczny <jajcus@jajcus.net>
- ChangeLog update by makelog.sh

* Fri Sep 10 2004  Jacek Konieczny <jajcus@jajcus.net>
- missing 'message.composer_descr' theme format added

* Thu Sep 9 2004  Jacek Konieczny <jajcus@jajcus.net>
- ChangeLog update by makelog.sh

* Thu Sep 9 2004  Jacek Konieczny <jajcus@jajcus.net>
- updated for the recent logging/output changes
- debug(), info(), warning() and error() functions installed in the
- script's namespace
- Application object available as "cjc" in the script's namespace
- help message improved

* Thu Sep 9 2004  Jacek Konieczny <jajcus@jajcus.net>
- ChangeLog update by makelog.sh

* Thu Sep 9 2004  Jacek Konieczny <jajcus@jajcus.net>
- don't panic on bad arguments to /move

* Wed Sep 8 2004  Jacek Konieczny <jajcus@jajcus.net>
- ChangeLog update by makelog.sh

* Wed Sep 8 2004  Jacek Konieczny <jajcus@jajcus.net>
- /set bad boolean value error handling fixed

* Wed Sep 8 2004  Jacek Konieczny <jajcus@jajcus.net>
- error logging updated

* Wed Sep 8 2004  Jacek Konieczny <jajcus@jajcus.net>
- use all available settings for completion, not only those actually set

* Wed Sep 8 2004  Jacek Konieczny <jajcus@jajcus.net>
- message composition with external editor (when no body is given)

* Wed Sep 8 2004  Jacek Konieczny <jajcus@jajcus.net>
- .clear() fixed. No it resets cursor position and clears the window

* Wed Sep 8 2004  Jacek Konieczny <jajcus@jajcus.net>
- ChangeLog update by makelog.sh

* Wed Sep 8 2004  Jacek Konieczny <jajcus@jajcus.net>
- recently introduced bug fixed and prompt formating improved (include ' ' between the question and the prompt)

* Wed Sep 8 2004  Jacek Konieczny <jajcus@jajcus.net>
- more arguments to ask_question() made optional

* Wed Sep 8 2004  Jacek Konieczny <jajcus@jajcus.net>
- ChangeLog update by makelog.sh

* Wed Sep 8 2004  Jacek Konieczny <jajcus@jajcus.net>
- clearing the pair list was not a good idea-- the theme may be incomplete, some attributes would be lost then

* Wed Sep 8 2004  Jacek Konieczny <jajcus@jajcus.net>
- ChangeLog update by makelog.sh

* Wed Sep 8 2004  Jacek Konieczny <jajcus@jajcus.net>
- don't require-clear option to set a presence description

* Tue Sep 7 2004  Jacek Konieczny <jajcus@jajcus.net>
- ChangeLog update by makelog.sh

* Tue Sep 7 2004  Jacek Konieczny <jajcus@jajcus.net>
- auto_popup=False by default

* Tue Sep 7 2004  Jacek Konieczny <jajcus@jajcus.net>
- allow applications started with /shell, /pipe_in, /pipe_out to use terminal not breaking CJC display. Use-noterm to force no-terminal mode

* Tue Sep 7 2004  Jacek Konieczny <jajcus@jajcus.net>
- updates for some recent CJC code change

* Tue Sep 7 2004  Jacek Konieczny <jajcus@jajcus.net>
- Screen.shell_mode() and Screen.prog_mode() methods to prepare terminal for
- external command execution
- background operation safety and better (hopefully) thread safety
- don't force " " as background character-- should help on slow terminals

* Tue Sep 7 2004  Jacek Konieczny <jajcus@jajcus.net>
- ChangeLog update by makelog.sh

* Tue Sep 7 2004  Jacek Konieczny <jajcus@jajcus.net>
- fixed problem with empty auto_away_msg  and keep_description set

* Sun Sep 5 2004  Jacek Konieczny <jajcus@jajcus.net>
- ChangeLog update by makelog.sh

* Sun Sep 5 2004  Jacek Konieczny <jajcus@jajcus.net>
- theme switching fixed (CJC was lacking curses color pairs when loading new theme, because old pairs were not reused)

* Fri Sep 3 2004  Jacek Konieczny <jajcus@jajcus.net>
- ChangeLog update by makelog.sh

* Fri Sep 3 2004  Jacek Konieczny <jajcus@jajcus.net>
- make /whois and /info work without arguments in chat buffers

* Fri Sep 3 2004  Jacek Konieczny <jajcus@jajcus.net>
- ChangeLog update by makelog.sh

* Fri Sep 3 2004  Jacek Konieczny <jajcus@jajcus.net>
- "-to" option to /online, /away, etc. for directed presence
- "keep_description" setting and "-keep"/"-clear" options to /online, /away, etc. for keeping presence description on "show" changes
- "no_auto_away_when" option to disable auto_away and auto_xa in some states (default: "away,xa,dnd")

* Fri Sep 3 2004  Jacek Konieczny <jajcus@jajcus.net>
- ChangeLog update by makelog.sh

* Fri Sep 3 2004  Jacek Konieczny <jajcus@jajcus.net>
- use 'logging' module for displaying stream data in xmlconsole

* Fri Sep 3 2004  Jacek Konieczny <jajcus@jajcus.net>
- ChangeLog update by makelog.sh

* Fri Sep 3 2004  Jacek Konieczny <jajcus@jajcus.net>
- /whois without arguments should display users own vCard

* Sun Aug 29 2004  Jacek Konieczny <jajcus@jajcus.net>
- ChangeLog update by makelog.sh

* Sun Aug 29 2004  Jacek Konieczny <jajcus@jajcus.net>
- got rid of those evil relative imports

* Sun Aug 29 2004  Jacek Konieczny <jajcus@jajcus.net>
- copyright information added to *.py files

* Sun Aug 29 2004  Jacek Konieczny <jajcus@jajcus.net>
- proper debug messaging handling when no-L/-l option is used

* Sun Aug 29 2004  Jacek Konieczny <jajcus@jajcus.net>
- typo

* Sun Aug 29 2004  Jacek Konieczny <jajcus@jajcus.net>
- show right error message when changing a setting to an invalid value

* Sun Aug 29 2004  Jacek Konieczny <jajcus@jajcus.net>
- ChangeLog update by makelog.sh

* Sun Aug 29 2004  Jacek Konieczny <jajcus@jajcus.net>
- call Completion.__init__ in constructors of classes derived from Completion

* Sun Aug 29 2004  Jacek Konieczny <jajcus@jajcus.net>
- debug/info/error messages processing switched to 'logging' module from standard Python library

* Sun Aug 29 2004  Jacek Konieczny <jajcus@jajcus.net>
- ChangeLog update by makelog.sh

* Sun Aug 29 2004  Jacek Konieczny <jajcus@jajcus.net>
- don't panic on unhandled exception in the stream loop

* Tue Jul 27 2004  Jacek Konieczny <jajcus@jajcus.net>
- ChangeLog update by makelog.sh

* Tue Jul 27 2004  Jacek Konieczny <jajcus@jajcus.net>
- groupchat event notifications fixed and defaults changed to more sane and more annoying ;-)

* Tue Jul 27 2004  Jacek Konieczny <jajcus@jajcus.net>
- permission-safer 'version' target (no error when version.py is not writtable)

* Tue Jul 27 2004  Jacek Konieczny <jajcus@jajcus.net>
- basic, but extensible event notifications ('beeps')

* Tue Jul 27 2004  Jacek Konieczny <jajcus@jajcus.net>
- ChangeLog update by makelog.sh

* Tue Jul 27 2004  Jacek Konieczny <jajcus@jajcus.net>
- don't panic if user_left() is called with stanza=None

* Mon Jul 26 2004  Jacek Konieczny <jajcus@jajcus.net>
- ChangeLog update by makelog.sh

* Mon Jul 26 2004  Jacek Konieczny <jajcus@jajcus.net>
- info about registration added to the 'Quickstart'

* Wed Jul 21 2004  Jacek Konieczny <jajcus@jajcus.net>
- ChangeLog update by makelog.sh

* Wed Jul 21 2004  Jacek Konieczny <jajcus@jajcus.net>
- sort entries in /list output

* Wed Jul 21 2004  Jacek Konieczny <jajcus@jajcus.net>
- show error instead of traceback on invalid regular expression in /list

* Wed Jul 21 2004  Jacek Konieczny <jajcus@jajcus.net>
- don't panic while using /buffer_list when some buffers where closed

* Wed Jul 21 2004  Jacek Konieczny <jajcus@jajcus.net>
- ChangeLog update by makelog.sh

* Wed Jul 21 2004  Jacek Konieczny <jajcus@jajcus.net>
---config-directory command line option

* Wed Jul 21 2004  Jacek Konieczny <jajcus@jajcus.net>
- ChangeLog update by makelog.sh

* Wed Jul 21 2004  Jacek Konieczny <jajcus@jajcus.net>
- *** Version: 0.5 ***

* Wed Jul 21 2004  Jacek Konieczny <jajcus@jajcus.net>
- ChangeLog update by makelog.sh

* Wed Jul 21 2004  Jacek Konieczny <jajcus@jajcus.net>
- cosmetics

* Wed Jul 21 2004  Jacek Konieczny <jajcus@jajcus.net>
- updated

* Wed Jul 21 2004  Jacek Konieczny <jajcus@jajcus.net>
- ChangeLog update by makelog.sh

* Wed Jul 21 2004  Jacek Konieczny <jajcus@jajcus.net>
- Makefile for the manual made more failproof

* Wed Jul 21 2004  Jacek Konieczny <jajcus@jajcus.net>
- updates

* Tue Jul 20 2004  Jacek Konieczny <jajcus@jajcus.net>
- ChangeLog update by makelog.sh

* Tue Jul 20 2004  Jacek Konieczny <jajcus@jajcus.net>
- /list command (filtered roster dump) added

* Tue Jul 20 2004  Jacek Konieczny <jajcus@jajcus.net>
- ChangeLog update by makelog.sh

* Tue Jul 20 2004  Jacek Konieczny <jajcus@jajcus.net>
- /buffer_list command added

* Mon Jul 19 2004  Jacek Konieczny <jajcus@jajcus.net>
- ChangeLog update by makelog.sh

* Mon Jul 19 2004  Jacek Konieczny <jajcus@jajcus.net>
- TLS error handling improvements

* Fri Jul 2 2004  Jacek Konieczny <jajcus@jajcus.net>
- ChangeLog update by makelog.sh

* Fri Jul 2 2004  Jacek Konieczny <jajcus@jajcus.net>
- day change notifications

* Fri Jul 2 2004  Jacek Konieczny <jajcus@jajcus.net>
- 'activity_level' optional argument to append* functions

* Sun Jun 27 2004  Jacek Konieczny <jajcus@jajcus.net>
- ChangeLog update by makelog.sh

* Sun Jun 27 2004  Jacek Konieczny <jajcus@jajcus.net>
- allow substitutions in boolean conditionals values

* Sun Jun 27 2004  Jacek Konieczny <jajcus@jajcus.net>
- presence changes handling fixes

* Sun Jun 27 2004  Jacek Konieczny <jajcus@jajcus.net>
- ChangeLog update by makelog.sh

* Sun Jun 27 2004  Jacek Konieczny <jajcus@jajcus.net>
- use proper theme format for presence change notification
- do not display presence change notification when user goes offline

* Sun Jun 27 2004  Jacek Konieczny <jajcus@jajcus.net>
- ChangeLog update by makelog.sh

* Sun Jun 27 2004  Jacek Konieczny <jajcus@jajcus.net>
- store MUC users presence in user_info
- handle MUC users presence changes
- show error when /join is used while disconnected

* Sat Jun 26 2004  Jacek Konieczny <jajcus@jajcus.net>
- ChangeLog update by makelog.sh

* Sat Jun 26 2004  Jacek Konieczny <jajcus@jajcus.net>
- fixes for /subject without arguments

* Sat Jun 26 2004  Jacek Konieczny <jajcus@jajcus.net>
- /subject without arguments should display the current room subject

* Thu Jun 24 2004  Jacek Konieczny <jajcus@jajcus.net>
- ChangeLog update by makelog.sh

* Thu Jun 24 2004  Jacek Konieczny <jajcus@jajcus.net>
- show error message when get_user() fails

* Sun Jun 20 2004  Jacek Konieczny <jajcus@jajcus.net>
- ChangeLog update by makelog.sh

* Sun Jun 20 2004  Jacek Konieczny <jajcus@jajcus.net>
- cosmetics

* Sun Jun 20 2004  Jacek Konieczny <jajcus@jajcus.net>
- cosmetics

* Sun Jun 20 2004  Jacek Konieczny <jajcus@jajcus.net>
- ChangeLog update by makelog.sh

* Sun Jun 20 2004  Jacek Konieczny <jajcus@jajcus.net>
- auto_popup settings

* Sun Jun 20 2004  Jacek Konieczny <jajcus@jajcus.net>
- 'bool' setting type

* Thu Jun 17 2004  Jacek Konieczny <jajcus@jajcus.net>
- ChangeLog update by makelog.sh

* Thu Jun 17 2004  Jacek Konieczny <jajcus@jajcus.net>
- don't write to the buffer's window when appending text if the buffer is scrolled down

* Wed Jun 16 2004  Jacek Konieczny <jajcus@jajcus.net>
- ChangeLog update by makelog.sh

* Wed Jun 16 2004  Jacek Konieczny <jajcus@jajcus.net>
- live test :)

* Wed Jun 16 2004  Jacek Konieczny <jajcus@jajcus.net>
- ChangeLog update by makelog.sh

* Wed Jun 16 2004  Jacek Konieczny <jajcus@jajcus.net>
- test

* Wed Jun 16 2004  Jacek Konieczny <jajcus@jajcus.net>
- ChangeLog update by makelog.sh

* Wed Jun 16 2004  Jacek Konieczny <jajcus@jajcus.net>
- mail CVS commit information for CIA

* Tue Jun 15 2004  Jacek Konieczny <jajcus@jajcus.net>
- ChangeLog update by makelog.sh

* Tue Jun 15 2004  Jacek Konieczny <jajcus@jajcus.net>
- logging of messages sent fixed

* Tue Jun 15 2004  Jacek Konieczny <jajcus@jajcus.net>
- fix for the text input tab-completion bug with empty input

* Fri Jun 11 2004  Jacek Konieczny <jajcus@jajcus.net>
- ChangeLog update by makelog.sh

* Fri Jun 11 2004  Jacek Konieczny <jajcus@jajcus.net>
- use JIDs not strings as user_info keys

* Fri Jun 11 2004  Jacek Konieczny <jajcus@jajcus.net>
- ChangeLog update by makelog.sh

* Fri Jun 11 2004  Jacek Konieczny <jajcus@jajcus.net>
- 'xmlconsole' plugin unloading

* Fri Jun 11 2004  Jacek Konieczny <jajcus@jajcus.net>
- plugin unloading/reloading fixes

* Fri Jun 11 2004  Jacek Konieczny <jajcus@jajcus.net>
- /reaload_plugin command. 'version' plugin made reloadable

* Fri Jun 11 2004  Jacek Konieczny <jajcus@jajcus.net>
- ChangeLog update by makelog.sh

* Fri Jun 11 2004  Jacek Konieczny <jajcus@jajcus.net>
- plugin management: /load_plugin and /unload_plugin commands and Plugin.unload() callback

* Wed Jun 9 2004  Jacek Konieczny <jajcus@jajcus.net>
- ChangeLog update by makelog.sh

* Wed Jun 9 2004  Jacek Konieczny <jajcus@jajcus.net>
- highlight MUC messages containing our nick

* Wed Jun 9 2004  Jacek Konieczny <jajcus@jajcus.net>
- nick completion for MUC

* Wed Jun 9 2004  Jacek Konieczny <jajcus@jajcus.net>
- muc.default_nick setting added

* Wed Jun 9 2004  Jacek Konieczny <jajcus@jajcus.net>
- ChangeLog update by makelog.sh

* Wed Jun 9 2004  Jacek Konieczny <jajcus@jajcus.net>
- don't display role and affiliation in leave messages

* Mon Jun 7 2004  Jacek Konieczny <jajcus@jajcus.net>
- ChangeLog update by makelog.sh

* Mon Jun 7 2004  Jacek Konieczny <jajcus@jajcus.net>
- role, affiliation and nick change notification and nick changing in a MUC chat

* Sun Jun 6 2004  Jacek Konieczny <jajcus@jajcus.net>
- ChangeLog update by makelog.sh

* Sun Jun 6 2004  Jacek Konieczny <jajcus@jajcus.net>
- themable join/leave message. more information included in the standard join/leave messages

* Sun Jun 6 2004  Jacek Konieczny <jajcus@jajcus.net>
- recursive conditional substitutions

* Sun Jun 6 2004  Jacek Konieczny <jajcus@jajcus.net>
- don't break when closing a buffer not in the list of buffers

* Sun Jun 6 2004  Jacek Konieczny <jajcus@jajcus.net>
- ChangeLog update by makelog.sh

* Sun Jun 6 2004  Jacek Konieczny <jajcus@jajcus.net>
- use the already existing MUC buffer only if the chat is active

* Fri Jun 4 2004  Jacek Konieczny <jajcus@jajcus.net>
- ChangeLog update by makelog.sh

* Fri Jun 4 2004  Jacek Konieczny <jajcus@jajcus.net>
- /leave and /subject commands

* Fri Jun 4 2004  Jacek Konieczny <jajcus@jajcus.net>
- ChangeLog update by makelog.sh

* Fri Jun 4 2004  Jacek Konieczny <jajcus@jajcus.net>
- configurable preference values for buffers which are used to choose which one is the 'next active buffer'

* Fri Jun 4 2004  Jacek Konieczny <jajcus@jajcus.net>
- ChangeLog update by makelog.sh

* Fri Jun 4 2004  Jacek Konieczny <jajcus@jajcus.net>
- timestamp support for 'normal' messages

* Fri Jun 4 2004  Jacek Konieczny <jajcus@jajcus.net>
- treat '#' as the begining of a comment only if it is the first non-whitespace character in the line (fixes bug: #3749)

* Fri Jun 4 2004  Jacek Konieczny <jajcus@jajcus.net>
- theme engine improvements: 'none' color and possibility to use 'attr name empty' attribute definition (meaning no attribute change)

* Fri Jun 4 2004  Jacek Konieczny <jajcus@jajcus.net>
- ChangeLog update by makelog.sh

* Fri Jun 4 2004  Jacek Konieczny <jajcus@jajcus.net>
- default theme fixed

* Fri Jun 4 2004  Jacek Konieczny <jajcus@jajcus.net>
- error handling fixed (includes fix for bug #3785)

* Thu Jun 3 2004  Jacek Konieczny <jajcus@jajcus.net>
- ChangeLog update by makelog.sh

* Thu Jun 3 2004  Jacek Konieczny <jajcus@jajcus.net>
- default theme fix

* Thu Jun 3 2004  Jacek Konieczny <jajcus@jajcus.net>
- fix for exception handling

* Thu Jun 3 2004  Jacek Konieczny <jajcus@jajcus.net>
- ChangeLog update by makelog.sh

* Thu Jun 3 2004  Jacek Konieczny <jajcus@jajcus.net>
- display proper timestamp for delayed chat messages

* Thu Jun 3 2004  Jacek Konieczny <jajcus@jajcus.net>
- time handling switched from POSIX timestamps to datetime.datetime objects

* Wed Jun 2 2004  Jacek Konieczny <jajcus@jajcus.net>
- ChangeLog update by makelog.sh

* Wed Jun 2 2004  Jacek Konieczny <jajcus@jajcus.net>
- timestamp handling

* Wed Jun 2 2004  Jacek Konieczny <jajcus@jajcus.net>
- ChangeLog update by makelog.sh

* Wed Jun 2 2004  Jacek Konieczny <jajcus@jajcus.net>
- MUC support is much better now, working on...

* Wed Jun 2 2004  Jacek Konieczny <jajcus@jajcus.net>
- conditinal formatting

* Wed Jun 2 2004  Jacek Konieczny <jajcus@jajcus.net>
- ChangeLog update by makelog.sh

* Wed Jun 2 2004  Jacek Konieczny <jajcus@jajcus.net>
- updated for the new roster API in PyXMPP

* Mon May 31 2004  Jacek Konieczny <jajcus@jajcus.net>
- ChangeLog update by makelog.sh

* Mon May 31 2004  Jacek Konieczny <jajcus@jajcus.net>
- basic MUC functionality. NFY, but works a bit

* Mon May 31 2004  Jacek Konieczny <jajcus@jajcus.net>
- cosmetics

* Mon May 31 2004  Jacek Konieczny <jajcus@jajcus.net>
- ChangeLog update by makelog.sh

* Mon May 31 2004  Jacek Konieczny <jajcus@jajcus.net>
- fix for new Roster API

* Fri May 28 2004  Jacek Konieczny <jajcus@jajcus.net>
- ChangeLog update by makelog.sh

* Fri May 28 2004  Jacek Konieczny <jajcus@jajcus.net>
- updated for the new roster API in PyXMPP

* Fri May 28 2004  Jacek Konieczny <jajcus@jajcus.net>
- profile support fixes

* Fri May 28 2004  Jacek Konieczny <jajcus@jajcus.net>
- ChangeLog update by makelog.sh

* Fri May 28 2004  Jacek Konieczny <jajcus@jajcus.net>
- ignore profiler output

* Fri May 28 2004  Jacek Konieczny <jajcus@jajcus.net>
- optional code profiling support

* Mon May 17 2004  Jacek Konieczny <jajcus@jajcus.net>
- ChangeLog update by makelog.sh

* Mon May 17 2004  Jacek Konieczny <jajcus@jajcus.net>
- allow python code which is not an expression too

* Mon May 17 2004  Jacek Konieczny <jajcus@jajcus.net>
- make /python evaluate expressions and display result if not None- makes /python a simple calculator

* Sun May 16 2004  Jacek Konieczny <jajcus@jajcus.net>
- ChangeLog update by makelog.sh

* Sun May 16 2004  Jacek Konieczny <jajcus@jajcus.net>
- *** Version: 0.4 ***

* Sun May 16 2004  Jacek Konieczny <jajcus@jajcus.net>
- ChangeLog update by makelog.sh

* Sun May 16 2004  Jacek Konieczny <jajcus@jajcus.net>
- updated

* Fri May 7 2004  Jacek Konieczny <jajcus@jajcus.net>
- ChangeLog update by makelog.sh

* Fri May 7 2004  Jacek Konieczny <jajcus@jajcus.net>
- convert user name to JID before comparing it with own jid

* Wed May 5 2004  Jacek Konieczny <jajcus@jajcus.net>
- ChangeLog update by makelog.sh

* Wed May 5 2004  Jacek Konieczny <jajcus@jajcus.net>
- code reformated so 4 spaces are used for indenting

* Wed May 5 2004  Jacek Konieczny <jajcus@jajcus.net>
- simple scripts to reformat code to my coding style

* Mon Apr 26 2004  Jacek Konieczny <jajcus@jajcus.net>
- ChangeLog update by makelog.sh

* Mon Apr 26 2004  Jacek Konieczny <jajcus@jajcus.net>
- 'case_sensitive' option, default: on

* Sun Apr 25 2004  Jacek Konieczny <jajcus@jajcus.net>
- ChangeLog update by makelog.sh

* Sun Apr 25 2004  Jacek Konieczny <jajcus@jajcus.net>
- don't panic on /me without arguments

* Sun Apr 25 2004  Jacek Konieczny <jajcus@jajcus.net>
- when using keyfunction from other keytable use the function's table object

* Sun Apr 25 2004  Jacek Konieczny <jajcus@jajcus.net>
- ChangeLog update by makelog.sh

* Sun Apr 25 2004  Jacek Konieczny <jajcus@jajcus.net>
- don't allow self presence subscription requests or adding own JID to the roster (own JID presence notification is automatic)

* Sun Apr 25 2004  Jacek Konieczny <jajcus@jajcus.net>
- always allow jid arguments when the jid is found in the roster (even if it doesn't contain '@')

* Sat Apr 24 2004  Jacek Konieczny <jajcus@jajcus.net>
- ChangeLog update by makelog.sh

* Sat Apr 24 2004  Jacek Konieczny <jajcus@jajcus.net>
- when color or attribute name is not known display an error message instead of the traceback

* Sat Apr 24 2004  Jacek Konieczny <jajcus@jajcus.net>
- don't change the buffer in the main window on terminal resize

* Sat Apr 24 2004  Jacek Konieczny <jajcus@jajcus.net>
- on CommandError display the error mesage instead of backtrace

* Sat Apr 24 2004  Jacek Konieczny <jajcus@jajcus.net>
- ChangeLog update by makelog.sh

* Sat Apr 24 2004  Jacek Konieczny <jajcus@jajcus.net>
- better handling of quoted arguments

* Sat Apr 24 2004  Jacek Konieczny <jajcus@jajcus.net>
- default config made really 'default.conf'

* Sat Apr 24 2004  Jacek Konieczny <jajcus@jajcus.net>
- configs are now stored as ~/.cjc/name.conf, default is: ~/.cjc/default.conf. Old configs are automatically renamed when needed

* Tue Apr 6 2004  Jacek Konieczny <jajcus@jajcus.net>
- ChangeLog update by makelog.sh

* Tue Apr 6 2004  Jacek Konieczny <jajcus@jajcus.net>
- help fixed for commands with multiple syntaxe variants (like /theme)

* Tue Mar 23 2004  Jacek Konieczny <jajcus@jajcus.net>
- ChangeLog update by makelog.sh

* Tue Mar 23 2004  Jacek Konieczny <jajcus@jajcus.net>
- register libxml2 error handler, so warnings about bad XML (relative
- 'vcard-temp' namespace) won't clutter the screen
- allow roster name as /info argument

* Tue Mar 23 2004  Jacek Konieczny <jajcus@jajcus.net>
- basic /whois command

* Tue Feb 24 2004  Jacek Konieczny <jajcus@jajcus.net>
- ChangeLog update by makelog.sh

* Tue Feb 24 2004  Jacek Konieczny <jajcus@jajcus.net>
- default theme changed so status and "show" is displayed in presence change message
- presence handling fixed so themed messages "knows" about current presence

* Mon Feb 9 2004  Jacek Konieczny <jajcus@jajcus.net>
- ChangeLog update by makelog.sh

* Mon Feb 9 2004  Jacek Konieczny <jajcus@jajcus.net>
- trace peer changes in chat window (bug #3178)

* Mon Feb 9 2004  Jacek Konieczny <jajcus@jajcus.net>
- change the default disco_identity instead of creating new one

* Sun Feb 8 2004  Jacek Konieczny <jajcus@jajcus.net>
- ChangeLog update by makelog.sh

* Sun Feb 8 2004  Jacek Konieczny <jajcus@jajcus.net>
- 'import select' removed (not needed)

* Sat Jan 24 2004  Jacek Konieczny <jajcus@jajcus.net>
- ChangeLog update by makelog.sh

* Sat Jan 24 2004  Jacek Konieczny <jajcus@jajcus.net>
- replace default DiscoInfo with CJC's own

* Sat Jan 24 2004  Jacek Konieczny <jajcus@jajcus.net>
- ChangeLog update by makelog.sh

* Sat Jan 24 2004  Jacek Konieczny <jajcus@jajcus.net>
- disco features fix ('message' and 'pressence' removed, 'jabber:iq:version' added)

* Sun Jan 18 2004  Jacek Konieczny <jajcus@jajcus.net>
- ChangeLog update by makelog.sh

* Sun Jan 18 2004  Jacek Konieczny <jajcus@jajcus.net>
- *** Version: 0.3 ***

* Sun Jan 18 2004  Jacek Konieczny <jajcus@jajcus.net>
- all unneeded and non-portable magic removed

* Sun Jan 18 2004  Jacek Konieczny <jajcus@jajcus.net>
- ChangeLog update by makelog.sh

* Sun Jan 18 2004  Jacek Konieczny <jajcus@jajcus.net>
- disable xmlconsole after closing it (fix to bug #3180)

* Sun Jan 18 2004  Jacek Konieczny <jajcus@jajcus.net>
- use .newTextChild instead .newChild to create text nodes

* Sun Dec 7 2003  Jacek Konieczny <jajcus@jajcus.net>
- ChangeLog update by makelog.sh

* Sun Dec 7 2003  Jacek Konieczny <jajcus@jajcus.net>
- don't remove newlines etc. in list items, but replace them with spaces

* Sun Dec 7 2003  Jacek Konieczny <jajcus@jajcus.net>
- fix for long strings (eg. status descriptions) in status bar

* Sun Dec 7 2003  Jacek Konieczny <jajcus@jajcus.net>
- don't show tracebacke when /rename argument is not in roster

* Wed Dec 3 2003  Jacek Konieczny <jajcus@jajcus.net>
- ChangeLog update by makelog.sh

* Wed Dec 3 2003  Jacek Konieczny <jajcus@jajcus.net>
- don't break when adding item already in roster

* Sun Nov 30 2003  Jacek Konieczny <jajcus@jajcus.net>
- ChangeLog update by makelog.sh

* Sun Nov 30 2003  Jacek Konieczny <jajcus@jajcus.net>
- tab-completion fixes

* Sun Nov 30 2003  Jacek Konieczny <jajcus@jajcus.net>
- ChangeLog update by makelog.sh

* Sun Nov 30 2003  Jacek Konieczny <jajcus@jajcus.net>
- more portable Makefiles

* Sun Nov 30 2003  Jacek Konieczny <jajcus@jajcus.net>
- ChangeLog update by makelog.sh

* Sun Nov 30 2003  Jacek Konieczny <jajcus@jajcus.net>
- don't fail on auto-away message without '%i'

* Sun Nov 30 2003  Jacek Konieczny <jajcus@jajcus.net>
- don't break on uninitialized item in cmd_remove()

* Sun Nov 30 2003  Jacek Konieczny <jajcus@jajcus.net>
- default terminal color patch by Beeth. Requires patched curses module

* Sun Nov 30 2003  Jacek Konieczny <jajcus@jajcus.net>
- use locale encoding for time formatting

* Thu Nov 27 2003  Jacek Konieczny <jajcus@jajcus.net>
- typo fixed

* Sun Nov 23 2003  Jacek Konieczny <jajcus@jajcus.net>
- s/upper/lower/ in lowercase curses key constants support

* Sun Nov 23 2003  Jacek Konieczny <jajcus@jajcus.net>
- on solaris KEY_* seem to be key_*

* Thu Nov 20 2003  Jacek Konieczny <jajcus@jajcus.net>
- keepalive is back

* Tue Nov 11 2003  Jacek Konieczny <jajcus@jajcus.net>
- pass auth_methods to Client when connecting
- new connection states: 'binding', 'authorized'

* Tue Nov 11 2003  Jacek Konieczny <jajcus@jajcus.net>
- /beep command may be usefull for even binding (when implemented)

* Tue Nov 11 2003  Jacek Konieczny <jajcus@jajcus.net>
- typo in buffer command table name fixed

* Tue Nov 11 2003  Jacek Konieczny <jajcus@jajcus.net>
- don't panic on /group without arguments

* Tue Nov 11 2003  Jacek Konieczny <jajcus@jajcus.net>
- fixed behaviour when writting config file for the first time with bakups disabled

* Tue Nov 11 2003  Jacek Konieczny <jajcus@jajcus.net>
- typo fixed by agaran

* Mon Nov 10 2003  Jacek Konieczny <jajcus@jajcus.net>
- support for SRV records

* Mon Nov 10 2003  Jacek Konieczny <jajcus@jajcus.net>
- support for completed command argument quoting and spaces in completed arguments

* Sun Nov 9 2003  Jacek Konieczny <jajcus@jajcus.net>
- completion improvements

* Sun Nov 9 2003  Jacek Konieczny <jajcus@jajcus.net>
- most completions moved to cjc/completions
- aliases are completed like regular commands
- completion hints for most commands

* Sun Nov 9 2003  Jacek Konieczny <jajcus@jajcus.net>
- basic command options and user name/jid completion

* Sat Nov 8 2003  Jacek Konieczny <jajcus@jajcus.net>
- tab-completion for setting names (/set and /unset commands)

* Sat Nov 8 2003  Jacek Konieczny <jajcus@jajcus.net>
- less debuging

* Sat Nov 8 2003  Jacek Konieczny <jajcus@jajcus.net>
- ignore logs

* Sat Nov 8 2003  Jacek Konieczny <jajcus@jajcus.net>
- presence priority settings for all <show/> values

* Wed Nov 5 2003  Jacek Konieczny <jajcus@jajcus.net>
- include slash in 'Unknown command' error message

* Tue Nov 4 2003  Jacek Konieczny <jajcus@jajcus.net>
- ignore commands from inactive tables while completing

* Mon Nov 3 2003  Jacek Konieczny <jajcus@jajcus.net>
- multiple-choice completion

* Sun Nov 2 2003  Jacek Konieczny <jajcus@jajcus.net>
- updated for new cmdtable/keytable API

* Sun Nov 2 2003  Jacek Konieczny <jajcus@jajcus.net>
- basic tab-completion
- use screen.beep() for beeping

* Sun Nov 2 2003  Jacek Konieczny <jajcus@jajcus.net>
- basic tab-completion

* Sun Nov 2 2003  Jacek Konieczny <jajcus@jajcus.net>
- beep() method for safe beeping

* Sun Nov 2 2003  Jacek Konieczny <jajcus@jajcus.net>
- /disconnect or /quit when already disconnecting will force unclean disconnection

* Sun Nov 2 2003  Jacek Konieczny <jajcus@jajcus.net>
- cleaner cmdtable/keytable API. plugins not updated yet.

* Sun Nov 2 2003  Jacek Konieczny <jajcus@jajcus.net>
- new command handling, similar to keybindings code

* Sat Nov 1 2003  Jacek Konieczny <jajcus@jajcus.net>
- this will never work

* Mon Oct 27 2003  Jacek Konieczny <jajcus@jajcus.net>
- use of psyco disabled (causes SIGSEGV on Python 2.3)

* Fri Oct 10 2003  Jacek Konieczny <jajcus@jajcus.net>
- handle empty code (show error)

* Fri Oct 10 2003  Jacek Konieczny <jajcus@jajcus.net>
- handle empty command (show error)

* Thu Oct 9 2003  Jacek Konieczny <jajcus@jajcus.net>
- new plugin, implements /shell /pipe_in and /pipe_out commands

* Thu Oct 9 2003  Jacek Konieczny <jajcus@jajcus.net>
- as_string() method added

* Thu Oct 9 2003  Jacek Konieczny <jajcus@jajcus.net>
- '\/' may be used to escape empty input or '/' at the begining of user input

* Thu Oct 9 2003  Jacek Konieczny <jajcus@jajcus.net>
- allow empty user input

* Thu Oct 9 2003  Jacek Konieczny <jajcus@jajcus.net>
- the simplest plugin: executes any python code from command-line (any security risk?)

* Thu Oct 9 2003  Jacek Konieczny <jajcus@jajcus.net>
- Alt-a switches to the first active buffer

* Wed Oct 8 2003  Jacek Konieczny <jajcus@jajcus.net>
- connection progress information

* Tue Oct 7 2003  Jacek Konieczny <jajcus@jajcus.net>
- scrolling of roster buffer works again (new keyboard handling)

* Tue Oct 7 2003  Jacek Konieczny <jajcus@jajcus.net>
- safer config saving (will not corrupt old config if save fails)

* Tue Oct 7 2003  Jacek Konieczny <jajcus@jajcus.net>
- better description of accept-input and abort-input key-commands

* Tue Oct 7 2003  Jacek Konieczny <jajcus@jajcus.net>
- saving and loading of keybindings

* Tue Oct 7 2003  Jacek Konieczny <jajcus@jajcus.net>
- fix in error handling code

* Tue Oct 7 2003  Jacek Konieczny <jajcus@jajcus.net>
- improved exception handling

* Tue Oct 7 2003  Jacek Konieczny <jajcus@jajcus.net>
- right function bound to unix-word-rubout and unix-line-discard key-functions

* Sun Oct 5 2003  Jacek Konieczny <jajcus@jajcus.net>
- basic /bind and /unbind functionality

* Sun Oct 5 2003  Jacek Konieczny <jajcus@jajcus.net>
- keybinding list cosmetics

* Sun Oct 5 2003  Jacek Konieczny <jajcus@jajcus.net>
- show buffer number in keybinding description

* Sun Oct 5 2003  Jacek Konieczny <jajcus@jajcus.net>
- escape is ESCAPE

* Sun Oct 5 2003  Jacek Konieczny <jajcus@jajcus.net>
- /bind without arguments implemented (lists current keybindings)

* Fri Oct 3 2003  Jacek Konieczny <jajcus@jajcus.net>
- new keyboard input handling- now keybindings are configurable (but no commands for that yet)

* Thu Oct 2 2003  Jacek Konieczny <jajcus@jajcus.net>
- trying to make some lock debuging (no success)

* Thu Oct 2 2003  Jacek Konieczny <jajcus@jajcus.net>
- ignore_activity setting

* Thu Oct 2 2003  Jacek Konieczny <jajcus@jajcus.net>
- allow to /move buffers past the last one

* Thu Oct 2 2003  Jacek Konieczny <jajcus@jajcus.net>
- more thread safety

* Thu Oct 2 2003  Jacek Konieczny <jajcus@jajcus.net>
- updated for latest pyxmpp

* Thu Oct 2 2003  Jacek Konieczny <jajcus@jajcus.net>
- updated

* Wed Oct 1 2003  Jacek Konieczny <jajcus@jajcus.net>
- more TLS support (ask user about invalid certificate, offer to remember it)

* Wed Oct 1 2003  Jacek Konieczny <jajcus@jajcus.net>
- handling of multiple 'preformatted strings' in one format string

* Wed Oct 1 2003  Jacek Konieczny <jajcus@jajcus.net>
- missing 'import' added

* Wed Oct 1 2003  Jacek Konieczny <jajcus@jajcus.net>
- typo fixed

* Mon Sep 29 2003  Jacek Konieczny <jajcus@jajcus.net>
- close buffer in subscribe_back_decision()

* Mon Sep 29 2003  Jacek Konieczny <jajcus@jajcus.net>
- do not try to change presence from auto-away when not connected
- display error when not connected and trying to change presence

* Mon Sep 29 2003  Jacek Konieczny <jajcus@jajcus.net>
- Ctrl-U keybinding [uriel]

* Mon Sep 22 2003  Jacek Konieczny <jajcus@jajcus.net>
- StartTLS basics

* Sun Sep 21 2003  Jacek Konieczny <jajcus@jajcus.net>
- starting StartTLS support (not finished yet)

* Thu Sep 18 2003  Jacek Konieczny <jajcus@jajcus.net>
- libxml2.treeError added to standard_errors

* Tue Sep 16 2003  Jacek Konieczny <jajcus@jajcus.net>
- s/DiscoIdentity/pyxmpp.DiscoIdentity/

* Tue Sep 16 2003  Jacek Konieczny <jajcus@jajcus.net>
- use client/console as default disco category/type

* Mon Sep 15 2003  Jacek Konieczny <jajcus@jajcus.net>
- python-2.3 compatibility fix

* Fri Aug 15 2003  Jacek Konieczny <jajcus@jajcus.net>
- *** Version: 0.2 ***

* Fri Aug 15 2003  Jacek Konieczny <jajcus@jajcus.net>
- preserve timestamps making dist

* Fri Aug 15 2003  Jacek Konieczny <jajcus@jajcus.net>
- more s/cvs-version/version/

* Fri Aug 15 2003  Jacek Konieczny <jajcus@jajcus.net>
- RELEASE variable in Makefile to make releases

* Fri Aug 15 2003  Jacek Konieczny <jajcus@jajcus.net>
- installation notes

* Thu Aug 14 2003  Jacek Konieczny <jajcus@jajcus.net>
- properly handle auth_methods setting

* Thu Aug 14 2003  Jacek Konieczny <jajcus@jajcus.net>
- README added

* Thu Aug 14 2003  Jacek Konieczny <jajcus@jajcus.net>
- more todo

* Thu Aug 14 2003  Jacek Konieczny <jajcus@jajcus.net>
- added

* Thu Aug 14 2003  Jacek Konieczny <jajcus@jajcus.net>
- really do use psyco if available

* Thu Aug 14 2003  Jacek Konieczny <jajcus@jajcus.net>
- compile installed python modules

* Thu Aug 14 2003  Jacek Konieczny <jajcus@jajcus.net>
- use psyco if available

* Thu Aug 14 2003  Jacek Konieczny <jajcus@jajcus.net>
- make dist

* Thu Aug 14 2003  Jacek Konieczny <jajcus@jajcus.net>
- the license

* Thu Aug 14 2003  Jacek Konieczny <jajcus@jajcus.net>
- startup script for running CJC directly from source tree

* Thu Aug 14 2003  Jacek Konieczny <jajcus@jajcus.net>
- new 'build'/install system

* Thu Aug 14 2003  Jacek Konieczny <jajcus@jajcus.net>
- version.py is autogenerated

* Tue Aug 12 2003  Jacek Konieczny <jajcus@jajcus.net>
- return 1 from command() if command was available and successful

* Tue Aug 12 2003  Jacek Konieczny <jajcus@jajcus.net>
- small fix

* Tue Aug 12 2003  Jacek Konieczny <jajcus@jajcus.net>
- /close made work in single-buffer mode

* Tue Aug 12 2003  Jacek Konieczny <jajcus@jajcus.net>
- more ignores

* Mon Aug 11 2003  Jacek Konieczny <jajcus@jajcus.net>
- updated

* Mon Aug 11 2003  Jacek Konieczny <jajcus@jajcus.net>
- return 1 from cmd_close()

* Mon Aug 11 2003  Jacek Konieczny <jajcus@jajcus.net>
- translate unicode content to local encoding

* Mon Aug 11 2003  Jacek Konieczny <jajcus@jajcus.net>
- updated, some spelling fixes

* Sun Aug 10 2003  Jacek Konieczny <jajcus@jajcus.net>
- CJC manual- a work in progress

* Sun Aug 10 2003  Jacek Konieczny <jajcus@jajcus.net>
- some bugs, found while writting manual, fixed

* Sun Aug 10 2003  Jacek Konieczny <jajcus@jajcus.net>
- Alt-Tab is working again

* Sun Aug 10 2003  Jacek Konieczny <jajcus@jajcus.net>
- encode messages UTF-8 befor writting them to log file

* Sat Aug 9 2003  Jacek Konieczny <jajcus@jajcus.net>
- update

* Sat Aug 9 2003  Jacek Konieczny <jajcus@jajcus.net>
- message logging

* Sat Aug 9 2003  Jacek Konieczny <jajcus@jajcus.net>
- catch exception when removing item not in roster

* Sat Aug 9 2003  Jacek Konieczny <jajcus@jajcus.net>
- now environment variables may be used in theme substitutions

* Sat Aug 9 2003  Jacek Konieczny <jajcus@jajcus.net>
- Window is now a CommandHandler

* Fri Aug 8 2003  Jacek Konieczny <jajcus@jajcus.net>
- buffer moving and switching (/nextbuf,/prevbuf,/move commands)

* Fri Aug 8 2003  Jacek Konieczny <jajcus@jajcus.net>
- Ctrl-W = readline's unix-word-rubout

* Fri Aug 8 2003  Jacek Konieczny <jajcus@jajcus.net>
- updated

* Fri Aug 8 2003  Jacek Konieczny <jajcus@jajcus.net>
- XML console

* Fri Aug 8 2003  Jacek Konieczny <jajcus@jajcus.net>
- show stream errors

* Fri Aug 8 2003  Jacek Konieczny <jajcus@jajcus.net>
- 'stream created' and 'stream closed' events

* Fri Aug 8 2003  Jacek Konieczny <jajcus@jajcus.net>
- 'debug' setting to enable debug logging to status window

* Fri Aug 8 2003  Jacek Konieczny <jajcus@jajcus.net>
- new settings: presence.show_errors and presence.show_changes, for those who want CJC quiet

* Thu Aug 7 2003  Jacek Konieczny <jajcus@jajcus.net>
- testing phase is ending:
- config and theme files in ~/.cjc/ instead of current directory
- plugins and themes may be loaded from global data dir or ~/.cjc/
- debug log is optional

* Thu Aug 7 2003  Jacek Konieczny <jajcus@jajcus.net>
- command_handler made function instead of object

* Thu Aug 7 2003  Jacek Konieczny <jajcus@jajcus.net>
- terminal window resize support

* Thu Aug 7 2003  Jacek Konieczny <jajcus@jajcus.net>
- ignore SIGINT (Ctrl-C)
- terminal window resize support

* Thu Aug 7 2003  Jacek Konieczny <jajcus@jajcus.net>
- s/split_line/split_text/ (there is no split_line here)

* Wed Aug 6 2003  Jacek Konieczny <jajcus@jajcus.net>
- autoconnect setting

* Wed Aug 6 2003  Jacek Konieczny <jajcus@jajcus.net>
- command handling improvements
- command aliases (/alias)

* Wed Aug 6 2003  Jacek Konieczny <jajcus@jajcus.net>
- /clear command (ugly hack, but I think this is enough)

* Wed Aug 6 2003  Jacek Konieczny <jajcus@jajcus.net>
- Ctrl-L- redraw

* Wed Aug 6 2003  Jacek Konieczny <jajcus@jajcus.net>
- some readline(1) keybindings

* Wed Aug 6 2003  Jacek Konieczny <jajcus@jajcus.net>
- announce 'presence' feature

* Wed Aug 6 2003  Jacek Konieczny <jajcus@jajcus.net>
- announce 'message' feature

* Tue Aug 5 2003  Jacek Konieczny <jajcus@jajcus.net>
- probably these should be updated more frequently :)

* Tue Aug 5 2003  Jacek Konieczny <jajcus@jajcus.net>
- don't try to get bare JID from None

* Tue Aug 5 2003  Jacek Konieczny <jajcus@jajcus.net>
- ask if subscribe user who subscribed to us

* Tue Aug 5 2003  Jacek Konieczny <jajcus@jajcus.net>
- remove item from VG_UNKNOWN when it is known

* Tue Aug 5 2003  Jacek Konieczny <jajcus@jajcus.net>
- roster and presence subscription management

* Sun Aug 3 2003  Jacek Konieczny <jajcus@jajcus.net>
- incoming subscribe/unsubscribe/subscribed/unsubscribed presence handling

* Sun Aug 3 2003  Jacek Konieczny <jajcus@jajcus.net>
- invalid comment removed

* Sun Aug 3 2003  Jacek Konieczny <jajcus@jajcus.net>
- clear presence information after disconnect

* Sun Aug 3 2003  Jacek Konieczny <jajcus@jajcus.net>
- cosmetics

* Sun Aug 3 2003  Jacek Konieczny <jajcus@jajcus.net>
- link questions to buffers

* Sun Aug 3 2003  Jacek Konieczny <jajcus@jajcus.net>
- base class for all input widgets

* Sun Aug 3 2003  Jacek Konieczny <jajcus@jajcus.net>
- 'required' flag for input widgets

* Sun Aug 3 2003  Jacek Konieczny <jajcus@jajcus.net>
- list-multi input

* Sun Aug 3 2003  Jacek Konieczny <jajcus@jajcus.net>
- updated

* Sun Aug 3 2003  Jacek Konieczny <jajcus@jajcus.net>
- use arrow characters from the alternate charcter set

* Sun Aug 3 2003  Jacek Konieczny <jajcus@jajcus.net>
- list-single input

* Sun Aug 3 2003  Jacek Konieczny <jajcus@jajcus.net>
- more input widgets

* Sun Aug 3 2003  Jacek Konieczny <jajcus@jajcus.net>
- do not update screen after answer handler was called
- getmaxyx returns window size not maximum coordinates (of course)

* Sat Aug 2 2003  Jacek Konieczny <jajcus@jajcus.net>
- basic 'text-single' input

* Sat Aug 2 2003  Jacek Konieczny <jajcus@jajcus.net>
- s/command_line/self.command_line/g

* Sat Aug 2 2003  Jacek Konieczny <jajcus@jajcus.net>
- some debug output removed

* Sat Aug 2 2003  Jacek Konieczny <jajcus@jajcus.net>
- use new Input class for command line

* Sat Aug 2 2003  Jacek Konieczny <jajcus@jajcus.net>
- input handling modified for asking questions

* Mon Jul 28 2003  Jacek Konieczny <jajcus@jajcus.net>
- command line history handling fixed (long lines and lines containing non-ascii characters)

* Mon Jul 28 2003  Jacek Konieczny <jajcus@jajcus.net>
- remove control characters from items

* Sun Jul 27 2003  Jacek Konieczny <jajcus@jajcus.net>
- nicer default theme

* Sun Jul 27 2003  Jacek Konieczny <jajcus@jajcus.net>
- a new plugin- 'normal' messages handling

* Sun Jul 27 2003  Jacek Konieczny <jajcus@jajcus.net>
- s/thread-/chat-thread-/

* Sun Jul 27 2003  Jacek Konieczny <jajcus@jajcus.net>
- line breaks handling in append() improved

* Sun Jul 27 2003  Jacek Konieczny <jajcus@jajcus.net>
- new get() method for reading arguments without removing them from the command line

* Sun Jul 27 2003  Jacek Konieczny <jajcus@jajcus.net>
- 'normal' messages handling moved to a plugin
- 'choice' setting type added
- handling for stream errors in stream_loop

* Sun Jul 27 2003  Jacek Konieczny <jajcus@jajcus.net>
- 'roster.show' setting and displaying of item removal implemented

* Sun Jul 27 2003  Jacek Konieczny <jajcus@jajcus.net>
- proper display of items added to and removed from list buffer

* Sun Jul 27 2003  Jacek Konieczny <jajcus@jajcus.net>
- presence and message handlers updated for changes in pyxmpp
- message errors are routed to the right chat window

* Sun Jul 27 2003  Jacek Konieczny <jajcus@jajcus.net>
- a debug message removed

* Sun Jul 27 2003  Jacek Konieczny <jajcus@jajcus.net>
- treat error message as status of presence errors

* Sun Jul 27 2003  Jacek Konieczny <jajcus@jajcus.net>
- nicer buffer descriptions in windows' status bars
- longer format variable names (eg. "buffer_name" instead of "bufname")

* Sun Jul 27 2003  Jacek Konieczny <jajcus@jajcus.net>
- more generic %{} handling

* Sun Jul 27 2003  Jacek Konieczny <jajcus@jajcus.net>
- /close command for tests

* Sun Jul 27 2003  Jacek Konieczny <jajcus@jajcus.net>
- do not display empty line at the start of empty buffer

* Sun Jul 27 2003  Jacek Konieczny <jajcus@jajcus.net>
- do not redraw whole screen when only status bars may need update

* Sun Jul 27 2003  Jacek Konieczny <jajcus@jajcus.net>
- after closing a buffer replace it with buffer not visible in other window

* Sun Jul 27 2003  Jacek Konieczny <jajcus@jajcus.net>
- /close command for closing unused buffers

* Sat Jul 26 2003  Jacek Konieczny <jajcus@jajcus.net>
- redraw the screen after all settings are read

* Sat Jul 26 2003  Jacek Konieczny <jajcus@jajcus.net>
- set cursor position at the end of the input in key_down()

* Sat Jul 26 2003  Jacek Konieczny <jajcus@jajcus.net>
- show error when chatting after stream is disconnected

* Sat Jul 26 2003  Jacek Konieczny <jajcus@jajcus.net>
- command history

* Fri Jul 25 2003  Jacek Konieczny <jajcus@jajcus.net>
- erase 'tails' of replaced entries in list buffer

* Fri Jul 25 2003  Jacek Konieczny <jajcus@jajcus.net>
- auto away
- priority handling fixed (was set only on login)

* Fri Jul 25 2003  Jacek Konieczny <jajcus@jajcus.net>
- presence information as JID formatting method

* Fri Jul 25 2003  Jacek Konieczny <jajcus@jajcus.net>
- include presence information in bottom status bar and update status bars whenever presence is changed

* Fri Jul 25 2003  Jacek Konieczny <jajcus@jajcus.net>
- presence 'show' and 'status' fields made JID formatings in themes

* Fri Jul 25 2003  Jacek Konieczny <jajcus@jajcus.net>
- return 1 from keypressed() when a key was pressed

* Fri Jul 25 2003  Jacek Konieczny <jajcus@jajcus.net>
- generate 'keypressed' and 'idle' events

* Fri Jul 25 2003  Jacek Konieczny <jajcus@jajcus.net>
- theme string for unavailable fixed

* Fri Jul 25 2003  Jacek Konieczny <jajcus@jajcus.net>
- properly process /info arguments

* Thu Jul 24 2003  Jacek Konieczny <jajcus@jajcus.net>
- update/redraw redesigned (one function for both)

* Thu Jul 24 2003  Jacek Konieczny <jajcus@jajcus.net>
- all text formatting (except cutting too long lines) removed from Window object

* Thu Jul 24 2003  Jacek Konieczny <jajcus@jajcus.net>
- updated

* Thu Jul 24 2003  Jacek Konieczny <jajcus@jajcus.net>
- show buffer position in window status bar (for debugging)
- refuse to connect, when already connected

* Thu Jul 24 2003  Jacek Konieczny <jajcus@jajcus.net>
- made screem.redraw() really redraw whole screen

* Thu Jul 24 2003  Jacek Konieczny <jajcus@jajcus.net>
- new setting handling (no 'location')

* Thu Jul 24 2003  Jacek Konieczny <jajcus@jajcus.net>
- test plugin with two tests for UI

* Tue Jul 22 2003  Jacek Konieczny <jajcus@jajcus.net>
- display optimizations

* Tue Jul 22 2003  Jacek Konieczny <jajcus@jajcus.net>
- update user_info only when processing roster item (not jid alone)

* Tue Jul 22 2003  Jacek Konieczny <jajcus@jajcus.net>
- get_user_info fixed so it works for offline users

* Tue Jul 22 2003  Jacek Konieczny <jajcus@jajcus.net>
- wait a moment (disconnect_timeout setting) before disconnecting- without this many servers will ignore final <presence/>

* Tue Jul 22 2003  Jacek Konieczny <jajcus@jajcus.net>
- commands: /online /away /xa /dnd /chatready and aliases: /back /busy

* Tue Jul 22 2003  Jacek Konieczny <jajcus@jajcus.net>
- send <presence type='unavailable'/> on disconnect

* Tue Jul 22 2003  Jacek Konieczny <jajcus@jajcus.net>
- /connect/disconnect/connect and /connect/quit behaviour fixed
- /quit and /disconnect may be given a reason and generate "disconnect request" event

* Tue Jul 22 2003  Jacek Konieczny <jajcus@jajcus.net>
- input timeout of 100ms

* Tue Jul 22 2003  Jacek Konieczny <jajcus@jajcus.net>
- /save command fixed

* Tue Jul 22 2003  Jacek Konieczny <jajcus@jajcus.net>
- catch socket error when connecting

* Tue Jul 22 2003  Jacek Konieczny <jajcus@jajcus.net>
- catch more standard errors (now the list is defined in common.py)

* Mon Jul 21 2003  Jacek Konieczny <jajcus@jajcus.net>
- autoload .cjc-theme

* Mon Jul 21 2003  Jacek Konieczny <jajcus@jajcus.net>
- quote empty arguments
- proper debuging (so it goes to status buffer)

* Mon Jul 21 2003  Jacek Konieczny <jajcus@jajcus.net>
- theme changing and loading

* Mon Jul 21 2003  Jacek Konieczny <jajcus@jajcus.net>
- set rostername user_info to real rostername, 'me' or nothing

* Mon Jul 21 2003  Jacek Konieczny <jajcus@jajcus.net>
- include rostername in presence change messages

* Mon Jul 21 2003  Jacek Konieczny <jajcus@jajcus.net>
- nick is taken from rostername first, and if it fails, then from JID's node
- any key from "user info" database may be used as JID format (eg. "rostername")

* Mon Jul 21 2003  Jacek Konieczny <jajcus@jajcus.net>
- pass self to ThemeManager
- allow use of rosternames containing "@"

* Mon Jul 21 2003  Jacek Konieczny <jajcus@jajcus.net>
- mark list buffer active when updated

* Mon Jul 21 2003  Jacek Konieczny <jajcus@jajcus.net>
- update roster window properly even if roster is not yet available

* Mon Jul 21 2003  Jacek Konieczny <jajcus@jajcus.net>
- process own presence like any other (generate 'presence changed' event, update user info)

* Mon Jul 21 2003  Jacek Konieczny <jajcus@jajcus.net>
- let plugins put their buffers in right windows ('layout changed' event)

* Mon Jul 21 2003  Jacek Konieczny <jajcus@jajcus.net>
- include own and unknown jids in roster view

* Sun Jul 20 2003  Jacek Konieczny <jajcus@jajcus.net>
- updated

* Sun Jul 20 2003  Jacek Konieczny <jajcus@jajcus.net>
- changed to use list buffer- much more efficient

* Sun Jul 20 2003  Jacek Konieczny <jajcus@jajcus.net>
- changes for list buffer

* Sun Jul 20 2003  Jacek Konieczny <jajcus@jajcus.net>
- ListBuffer added

* Sun Jul 20 2003  Jacek Konieczny <jajcus@jajcus.net>
- works now

* Sun Jul 20 2003  Jacek Konieczny <jajcus@jajcus.net>
- list buffer implementation for efficient roster display (NFY)

* Sun Jul 20 2003  Jacek Konieczny <jajcus@jajcus.net>
- BackSpace handling fixed
- Home and End keybindings added

* Sat Jul 19 2003  Jacek Konieczny <jajcus@jajcus.net>
- command line scrolling (NFY, but works)

* Sat Jul 19 2003  Jacek Konieczny <jajcus@jajcus.net>
- set_content() fixed so buffers are unmapped from removed windows and window list is not cleared

* Sat Jul 19 2003  Jacek Konieczny <jajcus@jajcus.net>
- missing 'import curses' added

* Sat Jul 19 2003  Jacek Konieczny <jajcus@jajcus.net>
- catch and print also curses.error, which is not based on StandardError

* Fri Jul 18 2003  Jacek Konieczny <jajcus@jajcus.net>
- custom text line editing (curses.textpad is very limited and accepts only ASCII)

* Fri Jul 18 2003  Jacek Konieczny <jajcus@jajcus.net>
- ui module split into package of smaller modules

* Fri Jul 18 2003  Jacek Konieczny <jajcus@jajcus.net>
- some common stuff (like debuging functions)

* Fri Jul 18 2003  Jacek Konieczny <jajcus@jajcus.net>
- command_args module renamed to commands
- CommandHandler from ui included here too (it doesn't belong to UI)

* Thu Jul 17 2003  Jacek Konieczny <jajcus@jajcus.net>
- proper unquoting

* Thu Jul 17 2003  Jacek Konieczny <jajcus@jajcus.net>
- /me command works again

* Wed Jul 16 2003  Jacek Konieczny <jajcus@jajcus.net>
- theme in chat works again and the code is even simpler than before

* Tue Jul 15 2003  Jacek Konieczny <jajcus@jajcus.net>
- use colors only when available

* Mon Jul 14 2003  Jacek Konieczny <jajcus@jajcus.net>
- place cursor always in the command line

* Mon Jul 14 2003  Jacek Konieczny <jajcus@jajcus.net>
- fix for layout "irc"

* Sun Jul 13 2003  Jacek Konieczny <jajcus@jajcus.net>
- active buffer list

* Sun Jul 13 2003  Jacek Konieczny <jajcus@jajcus.net>
- switchable layouts (command /layout plain|vertical|horizontal|icr|irc)
- active buffer list

* Sat Jul 12 2003  Jacek Konieczny <jajcus@jajcus.net>
- use try: ... finally: ... to release locks

* Thu Jul 10 2003  Jacek Konieczny <jajcus@jajcus.net>
- use threads for smoother UI on slow machines (I hate threads)

* Thu Jul 10 2003  Jacek Konieczny <jajcus@jajcus.net>
- attributes for themed strings are defined only in format

* Thu Jul 10 2003  Jacek Konieczny <jajcus@jajcus.net>
- theme support

* Wed Jul 9 2003  Jacek Konieczny <jajcus@jajcus.net>
- attribute switching fixed
- don't ignore newlines in format strings
- JID formatting

* Wed Jul 9 2003  Jacek Konieczny <jajcus@jajcus.net>
- use theme in chat window

* Tue Jul 8 2003  Jacek Konieczny <jajcus@jajcus.net>
- base theme handling seems to work

* Sat Jul 5 2003  Jacek Konieczny <jajcus@jajcus.net>
- strip status bar content so it fits

* Tue Jul 1 2003  Jacek Konieczny <jajcus@jajcus.net>
- work on themes started

* Tue Jul 1 2003  Jacek Konieczny <jajcus@jajcus.net>
- new command arguments handling (quoting)

* Tue Jul 1 2003  Jacek Konieczny <jajcus@jajcus.net>
- roster plugin added

* Tue Jul 1 2003  Jacek Konieczny <jajcus@jajcus.net>
- presence for bare jid computation based on priorities of all resources

* Tue Jul 1 2003  Jacek Konieczny <jajcus@jajcus.net>
- new command arguments handling (quoting)

* Tue Jul 1 2003  Jacek Konieczny <jajcus@jajcus.net>
- new command arguments handling (quoting)
- most roster handling moved to a plugin

* Mon Jun 30 2003  Jacek Konieczny <jajcus@jajcus.net>
- settings descriptions and /unset command

* Mon Jun 30 2003  Jacek Konieczny <jajcus@jajcus.net>
- some settings for the plugin (not used yet)
- include error message in presence error notification

* Tue Jun 24 2003  Jacek Konieczny <jajcus@jajcus.net>
- user name resolution (get_user())

* Tue Jun 24 2003  Jacek Konieczny <jajcus@jajcus.net>
- user name resolution moved to the main module

* Tue Jun 24 2003  Jacek Konieczny <jajcus@jajcus.net>
- JEP-0092 (jabber:iq:version)

* Tue Jun 24 2003  Jacek Konieczny <jajcus@jajcus.net>
- display version information

* Tue Jun 24 2003  Jacek Konieczny <jajcus@jajcus.net>
- version strings, mostly autogenerated

* Mon Jun 23 2003  Jacek Konieczny <jajcus@jajcus.net>
- quickstart notes

* Mon Jun 23 2003  Jacek Konieczny <jajcus@jajcus.net>
- there is '@' not '*' in jid :)

* Mon Jun 23 2003  Jacek Konieczny <jajcus@jajcus.net>
- command and settings handling improvement

* Mon Jun 23 2003  Jacek Konieczny <jajcus@jajcus.net>
- scrolling (PageUp/PageDown) is working and nearly completed

* Sun Jun 22 2003  Jacek Konieczny <jajcus@jajcus.net>
- working on scrolling and text formatiing

* Sun Jun 22 2003  Jacek Konieczny <jajcus@jajcus.net>
- do register /chat command

* Sun Jun 22 2003  Jacek Konieczny <jajcus@jajcus.net>
- one of the most important features: 1-to-1 chat

* Sun Jun 22 2003  Jacek Konieczny <jajcus@jajcus.net>
- Buffer class (from main.py)
- user input and command handling
- many fixes and improvements

* Sun Jun 22 2003  Jacek Konieczny <jajcus@jajcus.net>
- use self.cjc instead of self for accessing stream and *_user_info

* Sun Jun 22 2003  Jacek Konieczny <jajcus@jajcus.net>
- don't copy stream and *_user_info attributes from the application

* Sun Jun 22 2003  Jacek Konieczny <jajcus@jajcus.net>
- more code thrown to ui.py and plugins

* Tue Jun 17 2003  Jacek Konieczny <jajcus@jajcus.net>
- CJC is getting bigger, got plugin support, but is still not very usable

* Sun Jun 15 2003  Jacek Konieczny <jajcus@jajcus.net>
- CJC is going to be usable soon, I hope

* Fri Jun 13 2003  Jacek Konieczny <jajcus@jajcus.net>
- killer example: Console Jabber Client

* Fri Jun 13 2003  Jacek Konieczny <jajcus@jajcus.net>
- New repository initialized by cvs2svn.
