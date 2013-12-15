#
# Conditional build:
%bcond_without	prof	# profiling library
#
%define		pkgname	vector
Summary:	Efficient Arrays
Summary(pl.UTF-8):	Wydajne tablice
Name:		ghc-%{pkgname}
Version:	0.10.0.1
Release:	1
License:	BSD
Group:		Development/Languages
#Source0Download: http://hackage.haskell.org/package/vector
Source0:	http://hackage.haskell.org/package/%{pkgname}-%{version}/%{pkgname}-%{version}.tar.gz
# Source0-md5:	a0d48ebfe68c8b90cb1d09589d86a79c
URL:		http://hackage.haskell.org/package/vector
BuildRequires:	ghc >= 6.12.3
BuildRequires:	ghc-base >= 4
BuildRequires:	ghc-base < 5
BuildRequires:	ghc-deepseq >= 1.1
BuildRequires:	ghc-deepseq < 1.4
BuildRequires:	ghc-ghc-prim
BuildRequires:	ghc-primitive < 0.6
BuildRequires:	ghc-primitive >= 0.5.0.1
%if %{with prof}
BuildRequires:	ghc-prof >= 6.12.3
BuildRequires:	ghc-base-prof >= 4
BuildRequires:	ghc-base-prof < 5
BuildRequires:	ghc-deepseq-prof >= 1.1
BuildRequires:	ghc-deepseq-prof < 1.4
BuildRequires:	ghc-ghc-prim-prof
BuildRequires:	ghc-primitive-prof < 0.6
BuildRequires:	ghc-primitive-prof >= 0.5.0.1
%endif
BuildRequires:	rpmbuild(macros) >= 1.608
%requires_eq	ghc
Requires:	ghc-base >= 4
Requires:	ghc-base < 5
Requires:	ghc-deepseq >= 1.1
Requires:	ghc-deepseq < 1.4
Requires:	ghc-ghc-prim
Requires:	ghc-primitive < 0.6
Requires:	ghc-primitive >= 0.5.0.1
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# debuginfo is not useful for ghc
%define		_enable_debug_packages	0

# don't compress haddock files
%define		_noautocompressdoc	*.haddock

%description
An efficient implementation of Int-indexed arrays (both mutable and
immutable), with a powerful loop optimisation framework.

%description -l pl.UTF-8
Wydajna implementacja tablic indeksowanych typem Int (zarówno
zmiennych, jak i niezmiennych) z potężnym szkieletem do optymalizacji
pętli.

%package prof
Summary:	Profiling %{pkgname} library for GHC
Summary(pl.UTF-8):	Biblioteka profilująca %{pkgname} dla GHC
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	ghc-base-prof >= 4
Requires:	ghc-base-prof < 5
Requires:	ghc-deepseq-prof >= 1.1
Requires:	ghc-deepseq-prof < 1.4
Requires:	ghc-ghc-prim-prof
Requires:	ghc-primitive-prof < 0.6
Requires:	ghc-primitive-prof >= 0.5.0.1

%description prof
Profiling %{pkgname} library for GHC. Should be installed when
GHC's profiling subsystem is needed.

%description prof -l pl.UTF-8
Biblioteka profilująca %{pkgname} dla GHC. Powinna być zainstalowana
kiedy potrzebujemy systemu profilującego z GHC.

%package doc
Summary:	HTML documentation for ghc %{pkgname} package
Summary(pl.UTF-8):	Dokumentacja w formacie HTML dla pakietu ghc %{pkgname}
Group:		Documentation

%description doc
HTML documentation for ghc %{pkgname} package.

%description doc -l pl.UTF-8
Dokumentacja w formacie HTML dla pakietu ghc %{pkgname}.

%prep
%setup -q -n %{pkgname}-%{version}

%build
runhaskell Setup.hs configure -v2 \
	%{?with_prof:--enable-library-profiling} \
	--prefix=%{_prefix} \
	--libdir=%{_libdir} \
	--libexecdir=%{_libexecdir} \
	--docdir=%{_docdir}/%{name}-%{version}

runhaskell Setup.hs build
runhaskell Setup.hs haddock --executables

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_libdir}/%{ghcdir}/package.conf.d

runhaskell Setup.hs copy --destdir=$RPM_BUILD_ROOT

# work around automatic haddock docs installation
%{__rm} -rf %{name}-%{version}-doc
cp -a $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}/html %{name}-%{version}-doc
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}

runhaskell Setup.hs register \
	--gen-pkg-config=$RPM_BUILD_ROOT%{_libdir}/%{ghcdir}/package.conf.d/%{pkgname}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
%ghc_pkg_recache

%postun
%ghc_pkg_recache

%files
%defattr(644,root,root,755)
%doc LICENSE
%{_libdir}/%{ghcdir}/package.conf.d/%{pkgname}.conf
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/HSvector-%{version}.o
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/libHSvector-%{version}.a
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Vector.hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Vector
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Vector/*.hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Vector/Fusion
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Vector/Fusion/*.hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Vector/Fusion/Stream
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Vector/Fusion/Stream/*.hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Vector/Generic
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Vector/Generic/*.hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Vector/Internal
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Vector/Internal/*.hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Vector/Primitive
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Vector/Primitive/*.hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Vector/Storable
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Vector/Storable/*.hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Vector/Unboxed
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Vector/Unboxed/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/include

%if %{with prof}
%files prof
%defattr(644,root,root,755)
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/libHSvector-%{version}_p.a
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Vector.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Vector/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Vector/Fusion/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Vector/Fusion/Stream/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Vector/Generic/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Vector/Internal/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Vector/Primitive/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Vector/Storable/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Vector/Unboxed/*.p_hi
%endif

%files doc
%defattr(644,root,root,755)
%doc %{name}-%{version}-doc/*
