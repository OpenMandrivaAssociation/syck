%define	major 0
%define libname %mklibname %{name} %{major}
%define develname %mklibname -d %{name}

Summary:	A library for reading and writing YAML
Name:		syck
Version:	0.55
Release:	%mkrel 5
License:	BSD (and D&R) 
Group:		System/Libraries
URL:		http://www.whytheluckystiff.net/syck/
Source0:	http://rubyforge.org/frs/download.php/4492/%{name}-%{version}.tar.gz
Patch0:		syck-shared.diff
BuildRequires:	autoconf2.5
BuildRequires:	bison
BuildRequires:	flex
BuildRequires:	libtool
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
Requires:	%{libname} = %{version}
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

export WANT_AUTOCONF_2_5=1
rm -rf lib/.deps tests/.deps configure
touch INSTALL NEWS AUTHORS ChangeLog
libtoolize --copy --force; aclocal -I config; autoheader; automake --foreign --add-missing --copy; autoconf

%configure2_5x \
    --enable-shared

%make

%install
rm -rf %{buildroot}

%makeinstall_std

%if %mdkversion < 200900
%post -n %{libname} -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%postun -n %{libname} -p /sbin/ldconfig
%endif

%clean
rm -rf %{buildroot}

%files -n %{libname}
%defattr(-,root,root)
%doc CHANGELOG COPYING README README.BYTECODE README.EXT RELEASE TODO
%{_libdir}/*.so.*

%files -n %{develname}
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/*.a
%{_libdir}/*.la
