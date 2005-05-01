Summary:	An integrated file sharing solution for the GNOME Desktop
Summary(pl):	Zintegrowane rozwi±zanie do wspó³dzielenia plików dla ¶rodowiska GNOME
Name:		gnome-user-share
Version:	0.5
Release:	0.1
License:	GPL v2
Group:		X11/Applications
Source0:	http://ftp.gnome.org/pub/GNOME/sources/gnome-user-share/0.5/%{name}-%{version}.tar.bz2
# Source0-md5:	61ca94a3676d3e137f104159471a97b0
BuildRequires:	howl-devel
BuildRequires:	libglade2-devel
BuildRequires:	libgnomeui-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
An integrated file sharing solution for the GNOME Desktop. It uses
WebDAV.

%description -l pl
Zintegrowane rozwi±zanie do wspó³dzielenia plików dla ¶rodowiska
GNOME. U¿ywa WebDAV.

%prep
%setup -q

%build
export CFLAGS
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%find_lang %{name}

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
%{_sysconfdir}/gconf/schemas/desktop_gnome_file_sharing.schemas
%{_datadir}/%{name}
