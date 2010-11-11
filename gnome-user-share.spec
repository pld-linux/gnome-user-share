Summary:	An integrated file sharing solution for the GNOME Desktop
Summary(pl.UTF-8):	Zintegrowane rozwiązanie do współdzielenia plików dla środowiska GNOME
Name:		gnome-user-share
Version:	2.30.1
Release:	1
License:	GPL v2
Group:		X11/Applications
Source0:	http://ftp.gnome.org/pub/GNOME/sources/gnome-user-share/2.30/%{name}-%{version}.tar.bz2
# Source0-md5:	532f3d310ec9b42bf2dd015ab5b64092
BuildRequires:	avahi-glib-devel
BuildRequires:	gettext-devel
BuildRequires:	gnome-bluetooth-devel
BuildRequires:	libcanberra-gtk-devel
BuildRequires:	libglade2-devel
BuildRequires:	libgnomeui-devel
BuildRequires:	nautilus-devel
BuildRequires:	perl-XML-Parser
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.198
Requires(post,preun):	GConf2
Requires:	apache-mod_auth_digest
Requires:	apache-mod_authz_groupfile
Requires:	apache-mod_dav
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
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

rm -f $RPM_BUILD_ROOT%{_libdir}/nautilus/extensions-2.0/*la

%find_lang %{name} --with-gnome --with-omf --all-name

%clean
rm -rf $RPM_BUILD_ROOT

%post
%gconf_schema_install desktop_gnome_file_sharing.schemas

%preun
%gconf_schema_uninstall desktop_gnome_file_sharing.schemas

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_libdir}/%{name}
%attr(755,root,root) %{_libdir}/nautilus/extensions-2.0/libnautilus-share-extension.so
%{_sysconfdir}/gconf/schemas/desktop_gnome_file_sharing.schemas
%{_sysconfdir}/xdg/autostart/%{name}.desktop
%{_desktopdir}/*.desktop
%{_datadir}/%{name}
%{_iconsdir}/*/*/*/*.png
