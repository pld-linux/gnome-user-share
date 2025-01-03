Summary:	An integrated file sharing solution for the GNOME Desktop
Summary(pl.UTF-8):	Zintegrowane rozwiązanie do współdzielenia plików dla środowiska GNOME
Name:		gnome-user-share
Version:	47.2
Release:	1
License:	GPL v2
Group:		X11/Applications
Source0:	https://download.gnome.org/sources/gnome-user-share/47/%{name}-%{version}.tar.xz
# Source0-md5:	55986957295b3e7e08df6e8f6d3c8bf8
Patch0:		%{name}-meson.patch
URL:		https://gitlab.gnome.org/GNOME/gnome-user-share/
BuildRequires:	gettext-tools
BuildRequires:	glib2-devel >= 1:2.74.0
BuildRequires:	libselinux-devel
BuildRequires:	meson >= 0.58.0
BuildRequires:	ninja >= 1.5
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 2.011
BuildRequires:	systemd-units
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
BuildRequires:	yelp-tools
Requires(post,postun):	glib2 >= 1:2.74.0
Requires(post,preun):	systemd-units >= 1:250.1
Requires:	apache-base >= 2.4
Requires:	apache-mod_auth_digest >= 2.4
Requires:	apache-mod_authn_file >= 2.4
Requires:	apache-mod_authz_groupfile >= 2.4
Requires:	apache-mod_dav >= 2.4
Requires:	apache-mod_dnssd >= 0.6
Requires:	glib2 >= 1:2.74.0
Requires:	systemd-units >= 1:250.1
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
An integrated file sharing solution for the GNOME Desktop. It uses
WebDAV.

%description -l pl.UTF-8
Zintegrowane rozwiązanie do współdzielenia plików dla środowiska
GNOME. Używa WebDAV.

%prep
%setup -q
%patch0 -p1

%build
%meson build \
	-Dhttpd=/usr/sbin/httpd \
	-Dmodules_path=%{_libdir}/apache

%ninja_build -C build

%install
rm -rf $RPM_BUILD_ROOT

%ninja_install -C build

# not supported by glibc (as of 2.40)
%{__rm} -r $RPM_BUILD_ROOT%{_localedir}/ie

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%glib_compile_schemas
%systemd_user_post gnome-user-share-webdav.service

%preun
%systemd_user_preun gnome-user-share-webdav.service

%postun
%glib_compile_schemas

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc MAINTAINERS NEWS README.md
%attr(755,root,root) %{_libexecdir}/gnome-user-share-webdav
%{systemduserunitdir}/gnome-user-share-webdav.service
%{_datadir}/GConf/gsettings/gnome-user-share.convert
%{_datadir}/glib-2.0/schemas/org.gnome.desktop.file-sharing.gschema.xml
%{_datadir}/%{name}
%{_desktopdir}/gnome-user-share-webdav.desktop
