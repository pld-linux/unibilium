#
# Conditional build:
%bcond_without	tests	# build without tests
%bcond_without	doc		# build doc

Summary:	Terminfo parsing library
Name:		unibilium
Version:	2.0.0
Release:	1
License:	LGPLv3+
Group:		Libraries
Source0:	https://github.com/mauke/unibilium/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	a89b8ef6e752cc76098e1863ff4b5457
URL:		https://github.com/mauke/unibilium
BuildRequires:	gcc
BuildRequires:	libtool
BuildRequires:	pkgconfig
%if %{with doc}
BuildRequires:	/usr/bin/pod2man
%endif
%if %{with tests}
BuildRequires:	/usr/bin/prove
%endif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Unibilium is a very basic terminfo library. It doesn't depend on
curses or any other library. It also doesn't use global variables, so
it should be thread-safe.

%package devel
Summary:	Development files needed for %{name}
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Development files needed for %{name}.

%prep
%setup -q

%build
%{__make} \
	CC="%{__cc}" \
	CFLAGS="%{rpmcflags}" \
	LDFLAGS="%{rpmldflags}" \
	PREFIX=%{_prefix} \
	LIBDIR=%{_libdir}

%if %{with tests}
%{__make} test
%endif

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	PREFIX=%{_prefix} \
	LIBDIR=%{_libdir} \
	DESTDIR=$RPM_BUILD_ROOT

rm -vf $RPM_BUILD_ROOT%{_libdir}/*.{a,la}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc Changes
%attr(755,root,root) %{_libdir}/libunibilium.so.*.*.*
%ghost %{_libdir}/libunibilium.so.0

%files devel
%defattr(644,root,root,755)
%{_libdir}/libunibilium.so
%{_pkgconfigdir}/unibilium.pc
%{_includedir}/%{name}.h
%{_mandir}/man3/unibi_*.3*
%{_mandir}/man3/unibilium.h.3*
