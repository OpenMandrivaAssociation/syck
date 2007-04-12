%define name syck
%define version 0.55
%define release %mkrel 3

%define libname %mklibname %name 0

Summary: A library for reading and writing YAML
Name: %{name}
Version: %{version}
Release: %{release}
Source0: %{name}-%{version}.tar.bz2
License: BSD (and D&R) 
Group: Development/Other
Url: http://whytheluckystiff.net/syck/
BuildRoot: %{_tmppath}/%{name}-buildroot

%description
Syck is an extension for reading and writing YAML swiftly in popular 
scripting languages. As Syck loads the YAML, it stores the data directly
in your language's symbol table.

%package -n %libname-devel
Summary: A library for reading and writing YAML
Group: Development/Other

%description -n %libname-devel
Syck is an extension for reading and writing YAML swiftly in popular 
scripting languages. As Syck loads the YAML, it stores the data directly
in your language's symbol table.

%prep
%setup -q

%build
export CFLAGS="%optflags -fPIC"
%configure
%make

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall_std

%clean
rm -rf $RPM_BUILD_ROOT

%files -n %libname-devel
%defattr(-,root,root)
%_includedir/*.h
%_libdir/*.a


