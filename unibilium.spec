#
# Conditional build:
%bcond_without	tests		# build without tests
%bcond_without	doc		# build doc

Summary:	Terminfo parsing library
Name:		unibilium
Version:	2.1.1
Release:	1
License:	LGPLv3+
Group:		Libraries
Source0:	https://github.com/neovim/unibilium/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	845c59ce10150d7808ee9862fef231cb
URL:		https://github.com/neovim/unibilium
BuildRequires:	libtool
BuildRequires:	ncurses-devel
BuildRequires:	pkgconfig
%if %{with doc}
BuildRequires:	perl-tools-pod
%endif
%if %{with tests}
BuildRequires:	/usr/bin/prove
BuildRequires:	perl-base
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
%ghost %{_libdir}/libunibilium.so.4

%files devel
%defattr(644,root,root,755)
%{_libdir}/libunibilium.so
%{_pkgconfigdir}/unibilium.pc
%{_includedir}/%{name}.h
%{_mandir}/man3/unibi_*.3*
%{_mandir}/man3/unibilium.h.3*
