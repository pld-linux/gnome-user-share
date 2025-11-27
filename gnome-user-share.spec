Summary:	An integrated file sharing solution for the GNOME Desktop
Summary(pl.UTF-8):	Zintegrowane rozwiązanie do współdzielenia plików dla środowiska GNOME
Name:		gnome-user-share
Version:	48.2
Release:	1
License:	GPL v2
Group:		X11/Applications
Source0:	https://download.gnome.org/sources/gnome-user-share/48/%{name}-%{version}.tar.xz
# Source0-md5:	048f5779c0aef70348974a8231d102c2
# cargo vendor-filterer --platform='*-unknown-linux-*' --tier=2 --features selinux
Source1:	%{name}-vendor-48.0.tar.xz
# Source1-md5:	6d407f9d1be601f00c27f85c90850bff
Patch0:		%{name}-meson.patch
Patch1:		%{name}-x32.patch
URL:		https://gitlab.gnome.org/GNOME/gnome-user-share/
BuildRequires:	cargo
# for selinux
BuildRequires:	clang
%ifarch x32
BuildRequires:	clang-libs(x86-x32)
BuildRequires:	clang-libs(x86-64)
%endif
BuildRequires:	gettext-tools
BuildRequires:	glib2-devel >= 1:2.74.0
BuildRequires:	libselinux-devel >= 2.8
BuildRequires:	meson >= 0.58.0
BuildRequires:	ninja >= 1.5
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 2.042
BuildRequires:	rust >= 1.80.0
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
Requires:	libselinux >= 2.8
Requires:	systemd-units >= 1:250.1
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
An integrated file sharing solution for the GNOME Desktop. It uses
WebDAV.

%description -l pl.UTF-8
Zintegrowane rozwiązanie do współdzielenia plików dla środowiska
GNOME. Używa WebDAV.

%prep
%setup -q -a1
%patch -P0 -p1
%ifarch x32
%patch -P1 -p1
%endif

%{__mv} %{name}-48.0/vendor vendor

# use offline registry
CARGO_HOME="$(pwd)/.cargo"

mkdir -p "$CARGO_HOME"
cat >$CARGO_HOME/config.toml <<EOF
[source.crates-io]
replace-with = 'vendored-sources'

[source.vendored-sources]
directory = '$PWD/vendor'
EOF

%build
%ifarch x32
export PKG_CONFIG_ALLOW_CROSS=1
# This is stupid, but the only way to make bindgen parse selinux.h, without this
# bindgen cannot resolve ino_t to rust type and leaves it as __uint64_t.
# This happens because bingen, for some reason, cannot load x32 libclang and
# instead is loading 64bit one.
export BINDGEN_EXTRA_CLANG_ARGS="-Dino_t=uint64_t"
%endif
%meson \
	-Dhttpd=/usr/sbin/httpd \
	-Dmodules_path=%{_libdir}/apache

%meson_build

%install
rm -rf $RPM_BUILD_ROOT

%ifarch x32
export PKG_CONFIG_ALLOW_CROSS=1
%endif
%meson_install

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
