#
# Conditional build:
%bcond_without	prof	# profiling library
#
%define		pkgname	vector
Summary:	Efficient Arrays
Summary(pl.UTF-8):	Wydajne tablice
Name:		ghc-%{pkgname}
Version:	0.12.1.2
Release:	2
License:	BSD
Group:		Development/Languages
#Source0Download: http://hackage.haskell.org/package/vector
Source0:	http://hackage.haskell.org/package/%{pkgname}-%{version}/%{pkgname}-%{version}.tar.gz
# Source0-md5:	31d98b44b3a62d0ec86209ef9668bf87
URL:		http://hackage.haskell.org/package/vector
# for ghc<8 also ghc-fail 4.9.x, semigroups >= 0.18 < 0.20
BuildRequires:	ghc >= 8.0
BuildRequires:	ghc-base >= 4.5
BuildRequires:	ghc-base < 4.15
BuildRequires:	ghc-deepseq >= 1.1
BuildRequires:	ghc-deepseq < 1.5
BuildRequires:	ghc-ghc-prim >= 0.2
BuildRequires:	ghc-ghc-prim < 0.7
BuildRequires:	ghc-primitive >= 0.5.0.1
BuildRequires:	ghc-primitive < 0.8
%if %{with prof}
BuildRequires:	ghc-prof >= 8.0
BuildRequires:	ghc-base-prof >= 4.5
BuildRequires:	ghc-deepseq-prof >= 1.1
BuildRequires:	ghc-ghc-prim-prof >= 0.2
BuildRequires:	ghc-primitive-prof >= 0.5.0.1
%endif
BuildRequires:	rpmbuild(macros) >= 1.608
%requires_eq	ghc
Requires:	ghc-base >= 4.5
Requires:	ghc-deepseq >= 1.1
Requires:	ghc-ghc-prim >= 0.2
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
Requires:	ghc-base-prof >= 4.5
Requires:	ghc-deepseq-prof >= 1.1
Requires:	ghc-ghc-prim-prof >= 0.2
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
%attr(755,root,root) %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/libHSvector-%{version}-*.so
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/libHSvector-%{version}-*.a
%exclude %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/libHSvector-%{version}-*_p.a
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Vector.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Vector.dyn_hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Vector
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Vector/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Vector/*.dyn_hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Vector/Fusion
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Vector/Fusion/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Vector/Fusion/*.dyn_hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Vector/Fusion/Bundle
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Vector/Fusion/Bundle/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Vector/Fusion/Bundle/*.dyn_hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Vector/Fusion/Stream
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Vector/Fusion/Stream/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Vector/Fusion/Stream/*.dyn_hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Vector/Generic
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Vector/Generic/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Vector/Generic/*.dyn_hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Vector/Generic/Mutable
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Vector/Generic/Mutable/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Vector/Generic/Mutable/*.dyn_hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Vector/Internal
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Vector/Internal/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Vector/Internal/*.dyn_hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Vector/Primitive
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Vector/Primitive/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Vector/Primitive/*.dyn_hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Vector/Storable
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Vector/Storable/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Vector/Storable/*.dyn_hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Vector/Unboxed
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Vector/Unboxed/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Vector/Unboxed/*.dyn_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/include

%if %{with prof}
%files prof
%defattr(644,root,root,755)
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/libHSvector-%{version}-*_p.a
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Vector.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Vector/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Vector/Fusion/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Vector/Fusion/Bundle/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Vector/Fusion/Stream/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Vector/Generic/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Vector/Generic/Mutable/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Vector/Internal/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Vector/Primitive/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Vector/Storable/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Vector/Unboxed/*.p_hi
%endif

%files doc
%defattr(644,root,root,755)
%doc %{name}-%{version}-doc/*
