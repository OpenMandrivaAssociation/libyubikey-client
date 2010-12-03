%define	major 0
%define libname	%mklibname libyubikey-client %{major}
%define develname %mklibname -d libyubikey-client

Summary:	Implements online validation of Yubikey OTPs
Name:		libyubikey-client
Version:	1.5
Release:	%mkrel 5
Group:		System/Libraries
License:	BSD
URL:		http://code.google.com/p/yubico-c-client/
Source0:	http://yubico-c-client.googlecode.com/files/%{name}-%{version}.tar.gz
BuildRequires:	autoconf
BuildRequires:	chrpath
BuildRequires:	curl-devel
BuildRequires:	libtool
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
This is a library written in C to validate a Yubikey OTP against the Yubico
online server.

%package -n	%{libname}
Summary:	Implements online validation of Yubikey OTPs
Group:          System/Libraries

%description -n	%{libname}
This is a library written in C to validate a Yubikey OTP against the Yubico
online server.

%package -n	%{develname}
Summary:	Static library and header files for the libyubikey-client library
Group:		Development/C
Provides:	%{name}-devel = %{version}
Requires:	%{libname} = %{version}

%description -n	%{develname}
This is a library written in C to validate a Yubikey OTP against the Yubico
online server.

This package contains the static libyubikey-client library and its header files.

%package -n	ykclient
Summary:	Command line interface to libyubikey-client
Group:          System/Libraries

%description -n	ykclient
This is a library written in C to validate a Yubikey OTP against the Yubico
online server.

 o Command line interface to libyubikey-client.

%prep

%setup -q -n %{name}-%{version}

%build
autoreconf -fis

%configure2_5x \
    --with-libcurl=%{_prefix}

%make
%make selftest

%check
./selftest

%install
rm -rf %{buildroot}

%makeinstall_std

# nuke rpath
chrpath -d %{buildroot}%{_bindir}/ykclient

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
%doc AUTHORS ChangeLog NEWS README
%{_libdir}/*.so.%{major}*

%files -n %{develname}
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/*.*a

%files -n ykclient
%defattr(-,root,root)
%{_bindir}/ykclient
