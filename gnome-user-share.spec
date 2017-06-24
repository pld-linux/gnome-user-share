Summary:	An integrated file sharing solution for the GNOME Desktop
Summary(pl.UTF-8):	Zintegrowane rozwiązanie do współdzielenia plików dla środowiska GNOME
Name:		gnome-user-share
Version:	3.18.3
Release:	1
License:	GPL v2
Group:		X11/Applications
Source0:	http://ftp.gnome.org/pub/GNOME/sources/gnome-user-share/3.18/%{name}-%{version}.tar.xz
# Source0-md5:	554faf22a881be31218001ba9bf918f3
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake >= 1:1.11
BuildRequires:	gettext-tools
BuildRequires:	glib2-devel >= 1:2.28.0
BuildRequires:	gnome-common
BuildRequires:	gtk+3-devel >= 3.0
BuildRequires:	intltool >= 0.35.0
BuildRequires:	libcanberra-gtk3-devel
BuildRequires:	libnotify-devel
BuildRequires:	libselinux-devel
BuildRequires:	libtool >= 2:2
BuildRequires:	nautilus-devel >= 3.0.0
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.592
BuildRequires:	systemd-units
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
BuildRequires:	yelp-tools
Requires(post,postun):	glib2 >= 1:2.26.0
Requires:	apache-base >= 2.2
Requires:	apache-mod_auth_digest
Requires:	apache-mod_authn_file
Requires:	apache-mod_authz_groupfile
Requires:	apache-mod_dav
Requires:	apache-mod_dnssd >= 0.6
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
An integrated file sharing solution for the GNOME Desktop. It uses
WebDAV.

%description -l pl.UTF-8
Zintegrowane rozwiązanie do współdzielenia plików dla środowiska
GNOME. Używa WebDAV.

%prep
%setup -q

%build
%{__intltoolize}
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-silent-rules
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/nautilus/extensions-3.0/*.la

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%glib_compile_schemas

%postun
%glib_compile_schemas

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc ChangeLog NEWS README
%attr(755,root,root) %{_libexecdir}/gnome-user-share-webdav
%attr(755,root,root) %{_libdir}/nautilus/extensions-3.0/libnautilus-share-extension.so
%{systemduserunitdir}/gnome-user-share-webdav.service
%{_datadir}/GConf/gsettings/gnome-user-share.convert
%{_datadir}/glib-2.0/schemas/org.gnome.desktop.file-sharing.gschema.xml
%{_datadir}/%{name}
%{_desktopdir}/gnome-user-share-webdav.desktop
