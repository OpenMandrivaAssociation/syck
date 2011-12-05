%define	major 0
%define libname %mklibname %{name} %{major}
%define develname %mklibname -d %{name}

Summary:	A library for reading and writing YAML
Name:		syck
Version:	0.70
Release:	1
License:	BSD (and D&R)
Group:		System/Libraries
URL:		https://github.com/indeyets/syck/wiki
Source0:	http://rubyforge.org/frs/download.php/4492/%{name}-%{version}.tar.gz
Patch0:		syck-shared.diff
BuildRequires:	autoconf automake libtool
BuildRequires:	bison
BuildRequires:	flex
BuildRequires:	re2c
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
Syck is an extension for reading and writing YAML swiftly in popular scripting
languages. As Syck loads the YAML, it stores the data directly in your
language's symbol table.

%package -n	%{libname}
Summary:	A library for reading and writing YAML
Group:          System/Libraries

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
Obsoletes:	%{mklibname syck -d 0}

%description -n	%{develname}
Syck is an extension for reading and writing YAML swiftly in popular scripting
languages. As Syck loads the YAML, it stores the data directly in your
language's symbol table.

This package contains the static syck library and its header files.

%prep

%setup -q -n %{name}-%{version}
%patch0 -p1

%build
export CFLAGS="%{optflags} -fPIC"
rm -rf autom4te.cache configure
touch INSTALL NEWS AUTHORS ChangeLog
#libtoolize --copy --force; aclocal -I config; autoheader; automake --foreign --add-missing --copy; autoconf
autoreconf -fi

%configure2_5x \
    --enable-shared \
    --disable-static

make

%install
rm -rf %{buildroot}

%makeinstall_std

# cleanup
rm -f %{buildroot}%{_libdir}/*.*a

%files -n %{libname}
%doc CHANGELOG COPYING README README.BYTECODE README.EXT RELEASE TODO
%{_libdir}/*.so.%{major}*

%files -n %{develname}
%{_includedir}/*
%{_libdir}/*.so
