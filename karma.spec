#
# TODO:
# - revise/more splitting (which binaries to base, -devel and some -progs?)
# - move some(?) binaries to $PATH
# - probably some patching to work outside /usr/local/karma
#
Summary:	A powerful programmers toolkit (runtime part)
Summary(pl.UTF-8):	Potężny zbiór narzędzi dla programistów (część uruchomieniowa)
Name:		karma
# NOTE: 1.7.25 at Source URL misses sources
Version:	1.7.20
Release:	1
License:	LGPL (KarmaLib), GPL (modules)
Group:		Libraries
Source0:	ftp://ftp.atnf.csiro.au/pub/software/karma/%{name}-%{version}-common.tar.bz2
# Source0-md5:	e60db3b01a007342df3d9b82c1ab029d
Patch0:		%{name}-makefix.patch
Patch1:		%{name}-gkh.patch
URL:		https://www.atnf.csiro.au/computing/software/karma/
BuildRequires:	/bin/csh
BuildRequires:	xorg-lib-libX11-devel
BuildRequires:	xorg-lib-libXaw-devel
BuildRequires:	xorg-lib-libXmu-devel
BuildRequires:	xorg-lib-libXt-devel
BuildRequires:	xorg-proto-xproto-devel
BuildRequires:	rpmbuild(macros) >= 1.213
BuildRequires:	xview-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Karma is a toolkit for interprocess communications, authentication,
encryption, graphics display, user interface and manipulating the
Karma network data structure. It contains KarmaLib (the structured
libraries and API) and a large number of modules (applications) to
perform many standard tasks. A wide range of visualisation
applications have been developed with Karma.

%description -l pl.UTF-8
Karma jest zbiorem narzędzi do komunikacji międzyprocesowej,
uwierzytelniania, szyfrowania, wyświetlania grafiki, interfejsów
użytkownika i manipulowania strukturami sieci Karma. Zawiera KarmaLib
(strukturalne biblioteki i API) oraz dużą liczbę modułów (aplikacji)
do wykonywania wielu standardowych zadań. Wiele aplikacji do
wizualizacji zostało stworzonych przy użyciu Karmy.

%package devel
Summary:	A powerful programmers toolkit (development part)
Summary(pl.UTF-8):	Potężny zbiór narzędzi dla programistów (część programistyczna)
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Development part of KarmaLib.

%description devel -l pl.UTF-8
Część KarmaLib przeznaczona dla programistów.

%prep
%setup -q
%patch -P0 -p1
%patch -P1 -p1

%build
%ifarch %{ix86}
MACHINE=i386
MACHINE_OS=i386_Linux
%endif
%ifarch sparc sparc64
MACHINE=sparc
MACHINE_OS=sparc_Linux
%endif
%ifarch alpha
MACHINE=alpha
MACHINE_OS=alpha_Linux
%endif
%ifarch ppc
MACHINE=powerpc
MACHINE_OS=powerpc_Linux
%endif
%ifarch %{x8664}
MACHINE=amd64
MACHINE_OS=amd64_Linux
%endif
OS=Linux
KARMABASE=%{_libdir}/karma
KARMAROOT=`pwd`
KARMAINCLUDEPATH=`pwd`/include
KARMA_VERSION=`fgrep KARMA_VERSION include/k_version.h |tr '"' ' ' |awk '{print $4}'`
KARMALIBPATH=`pwd`/dist/lib
KARMASTATICLIBPATH=`pwd`/dist/lib
KARMABINPATH=`pwd`/dist/bin
export MACHINE MACHINE_OS OS KARMABASE KARMAROOT KARMAINCLUDEPATH KARMA_VERSION \
	KARMALIBPATH KARMASTATICLIBPATH KARMABINPATH

install -d build/${MACHINE_OS}/{lib,kutil,modules} dist/{bin,lib,admin.bin}

ln -sf `which make` dist/admin.bin/gmake
PATH=$PATH:`pwd`/dist/admin.bin:`pwd`/csh_script
export PATH

csh_script/make_build.libs
%{__make} -C build/${MACHINE_OS}/lib \
	GCC="%{__cc}" \
	LDso="%{__cc}" \
	KOPTIMISE="%{rpmcflags}" \
	XLIBPATH=/usr/%{_lib} \
	XINCLUDEPATH=/usr/include

%{__make} -C source/kutil \
	GCC="%{__cc}" \
	KOPTIMISE="%{rpmcflags}" \
	ADMINBINPATH=`pwd`/dist/admin.bin

csh_script/make_build.modules
%{__make} -C build/${MACHINE_OS}/modules \
	GCC="%{__cc}" \
	KOPTIMISE="%{rpmcflags}" \
	XLIBPATH=/usr/%{_lib} \
	XINCLUDEPATH=/usr/include

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_libdir}/karma,%{_includedir}/karma}

cp -af dist/lib/* $RPM_BUILD_ROOT%{_libdir}
cp -af dist/bin $RPM_BUILD_ROOT%{_libdir}/karma
cp -af csh_script $RPM_BUILD_ROOT%{_libdir}/karma
cp -rf include/{*.h,Xkw,shader} $RPM_BUILD_ROOT%{_includedir}/karma

%{__rm} www/{README.lib,update-policy,modules.html}
cp -f doc/modules/Overview www/modules.html

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc Release* ToDo doc/{README,update-policy} doc/{modules,widgets}
%attr(755,root,root) %{_libdir}/libkarma.so.*.*
%attr(755,root,root) %{_libdir}/libkarmaX11.so.*.*
%attr(755,root,root) %{_libdir}/libkarmaXt.so.*.*
%attr(755,root,root) %{_libdir}/libkarmagraphics.so.*.*
%attr(755,root,root) %{_libdir}/libkarmawidgets.so.*.*
%dir %{_libdir}/karma
%dir %{_libdir}/karma/bin
%attr(755,root,root) %{_libdir}/karma/bin/*
%dir %{_libdir}/karma/csh_script
%{_libdir}/karma/csh_script/machine_type
%{_libdir}/karma/csh_script/switch-karma
%attr(755,root,root) %{_libdir}/karma/csh_script/[!ms]*
%attr(755,root,root) %{_libdir}/karma/csh_script/ma[!c]*
%attr(755,root,root) %{_libdir}/karma/csh_script/s[!w]*

%files devel
%defattr(644,root,root,755)
%doc www
%attr(755,root,root) %{_libdir}/libkarma.so
%attr(755,root,root) %{_libdir}/libkarmaX11.so
%attr(755,root,root) %{_libdir}/libkarmaXt.so
%attr(755,root,root) %{_libdir}/libkarmagraphics.so
%attr(755,root,root) %{_libdir}/libkarmawidgets.so
%{_includedir}/karma
