%define major 0
%define libname %mklibname %{name} %{major}
%define develname %mklibname -d %{name}
%bcond_with	crosscompile

Summary:	A library for reading and writing YAML
Name:		syck
Version:	0.70
Release:	9
License:	BSD (and D&R)
Group:		System/Libraries
URL:		https://github.com/indeyets/syck/wiki
Source0:	http://rubyforge.org/frs/download.php/4492/%{name}-%{version}.tar.gz
Patch0:		syck-shared.diff
Patch1:		syck-automake-1.13.patch
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libtool
BuildRequires:	bison
BuildRequires:	flex
BuildRequires:	re2c

%description
Syck is an extension for reading and writing YAML swiftly in popular scripting
languages. As Syck loads the YAML, it stores the data directly in your
language's symbol table.

%package -n	%{libname}
Summary:	A library for reading and writing YAML
Group:		System/Libraries

%description -n	%{libname}
Syck is an extension for reading and writing YAML swiftly in popular scripting
languages. As Syck loads the YAML, it stores the data directly in your
language's symbol table.

%package -n	%{develname}
Summary:	Static library and header files for the syck library
Group:		Development/C
Requires:	%{libname} >= %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}
Provides:	lib%{name}-devel = %{version}-%{release}
Obsoletes:	%{mklibname syck -d 0} < 0.70

%description -n	%{develname}
Syck is an extension for reading and writing YAML swiftly in popular scripting
languages. As Syck loads the YAML, it stores the data directly in your
language's symbol table.

This package contains the static syck library and its header files.

%prep
%setup -q -n %{name}-%{version}
%apply_patches

%build
%if %{with crosscompile}
export ac_cv_func_malloc_0_nonnull=yes
%endif
export CFLAGS="%{optflags} -fPIC -DYYPARSE_PARAM=parser"
rm -rf autom4te.cache configure
touch INSTALL NEWS AUTHORS ChangeLog
#libtoolize --copy --force; aclocal -I config; autoheader; automake --foreign --add-missing --copy; autoconf
autoreconf -fi

%configure2_5x \
    --enable-shared \
    --disable-static

# Can't be built with -j12 yet
%make -j1

%install
%makeinstall_std
mkdir %{buildroot}/%{_lib}
mv %{buildroot}%{_libdir}/libsyck.so.%{major}* %{buildroot}/%{_lib}
ln -srf %{buildroot}/%{_lib}/libsyck.so.%{major}.*.* %{buildroot}%{_libdir}/libsyck.so

%files -n %{libname}
/%{_lib}/libsyck.so.%{major}*

%files -n %{develname}
%doc CHANGELOG COPYING README README.BYTECODE README.EXT RELEASE TODO
%{_includedir}/*
%{_libdir}/libsyck.so

%changelog
* Thu Jan 17 2013 Per Øyvind Karlsen <peroyvind@mandriva.org> 0.70-4
- move library under /%%{_lib} as it's required by /bin/rpm

* Mon Dec 05 2011 Oden Eriksson <oeriksson@mandriva.com> 0.70-1
+ Revision: 737869
- 0.70
- drop the static lib and the libtool *.la file
- various fixes

* Fri May 06 2011 Oden Eriksson <oeriksson@mandriva.com> 0.55-9
+ Revision: 670254
- mass rebuild

* Sat Dec 04 2010 Oden Eriksson <oeriksson@mandriva.com> 0.55-8mdv2011.0
+ Revision: 609169
- rebuild

* Sun Sep 20 2009 Thierry Vignaud <tv@mandriva.org> 0.55-7mdv2010.0
+ Revision: 445306
- rebuild

* Sun Jan 04 2009 Olivier Thauvin <nanardon@mandriva.org> 0.55-6mdv2009.1
+ Revision: 324878
- rebuild

* Wed Jul 09 2008 Oden Eriksson <oeriksson@mandriva.com> 0.55-5mdv2009.0
+ Revision: 232975
- rebuild

  + Pixel <pixel@mandriva.com>
    - do not call ldconfig in %%post/%%postun, it is now handled by filetriggers

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Tue Aug 07 2007 Oden Eriksson <oeriksson@mandriva.com> 0.55-4mdv2008.0
+ Revision: 59847
- make it provide shared libs as well


* Sun Jun 18 2006 Olivier Thauvin <nanardon@mandriva.org>
+2006-06-18 13:07:14 (37591)
- fix CFLAGS (my bad)

* Sun Jun 18 2006 Olivier Thauvin <nanardon@mandriva.org>
+2006-06-18 01:56:08 (37510)
- ensure it is build with -Fpic

* Wed Jun 07 2006 Olivier Thauvin <nanardon@mandriva.org>
+2006-06-07 22:20:40 (36796)
- add files

* Wed Jun 07 2006 Olivier Thauvin <nanardon@mandriva.org>
+2006-06-07 22:19:30 (36795)
- initial mandriva rpm

