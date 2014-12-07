%define major 0
%define libname %mklibname %{name} %{major}
%define develname %mklibname -d %{name}
%bcond_with	crosscompile

Summary:	A library for reading and writing YAML
Name:		syck
Version:	0.70
Release:	13
License:	BSD (and D&R)
Group:		System/Libraries
URL:		https://github.com/indeyets/syck/wiki
Source0:	http://rubyforge.org/frs/download.php/4492/%{name}-%{version}.tar.gz
Patch0:		syck-shared.diff
Patch1:		syck-automake-1.13.patch
Patch2:		syck-bison3.patch
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

%configure \
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
