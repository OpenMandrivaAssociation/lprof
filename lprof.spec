%define	name	lprof

%define	version	1.11.4.2
%define cvssnapshot 20071212

%define	rel	0.2
%define	release	%mkrel %{rel}

Name:		%{name}
Version:	%{version}
Release:	%{release}
Summary:	Color Profilers
Group: 		Office
License:	GPL
URL:		http://lprof.sourceforge.net
#Source:		http://prdownloads.sourceforge.net/lprof/%{name}-%{version}.tar.bz2
Source0:	lprof-%{version}-cvs%{cvssnapshot}.tar.bz2
Patch3:		lprof-desktop.diff
# (fc) 1.11.4.2-0.2mdv fix buffer overflow in dispread (Daniel Berrange, Fedora)
Patch4:		lprof-dispread-buffer-overflow.patch
# (fc) 1.11.4.2-0.2mdv 0.70-0.1.beta7.3mdv fix buffer overflow in iccdump (Daniel Berrange, Fedora)
Patch5:  	lprof-iccdump-buffer-overflow.patch

BuildRequires:	desktop-file-utils
BuildRequires:	ImageMagick
BuildRequires:	lcms-devel
BuildRequires:	libtiff-devel
BuildRequires:	libvigra-devel
BuildRequires:	python
BuildRequires:	qt3-devel
BuildRequires:  scons
BuildRequires:	libusb-devel
Requires:	qt3-assistant
%description
LProf is an open source color profiler that creates ICC compliant
profiles for devices such as cameras, scanners and monitors.


%prep
rm -rf %{buildroot}
%setup -q -n lprof
%patch3 -p0 -b .fix-desktop
%patch4 -p1 -b .dispread-buffer-overflow
%patch5 -p1 -b .iccdump-buffer-overflow

if [ "%{_lib}" != "lib" ]; then 
  sed -i -e "s/(i, 'lib')/(i, 'lib64')/g" SConstruct
  sed -i -e 's,/usr/lib,'$(pkg-config --variable libdir x11)',g' -e 's,/usr/pkg/lib,'$(pkg-config --variable libdir qt-mt)',g'  build_config.py
fi


%build
PATH=$PATH:%{_prefix}/lib/qt3/bin
export PATH
scons PREFIX="%{_prefix}" QT_LIBPATH="%{_prefix}/lib/qt3/%{_lib}" ccflags="`echo %{optflags} | sed -e 's/-Wp,-D_FORTIFY_SOURCE=2/-Wp,-D_FORTIFY_SOURCE=1/g'`" cxxflags="%{optflags}"

%install
rm -rf %{buildroot}

mkdir -p %{buildroot}%{_prefix}
PATH=$PATH:%{_prefix}/lib/qt3/bin
export PATH

scons PREFIX="%{buildroot}%{_prefix}" install

install -p -D -m0644 data/icons/lprof.png %{buildroot}%{_liconsdir}/%{name}.png

mkdir -p -m 755 %{buildroot}%{_iconsdir}
convert %{buildroot}%{_liconsdir}/%{name}.png -size 32x32 %{buildroot}%{_iconsdir}/%{name}.png
mkdir -p -m 755 %{buildroot}%{_miconsdir}
convert %{buildroot}%{_iconsdir}/%{name}.png -size 16x16 %{buildroot}%{_miconsdir}/%{name}.png

%post
%update_menus

%postun
%clean_menus

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc COPYING README.NetBSD sRGB_profile_License KNOWN_BUGS README
%{_bindir}/*
%{_datadir}/applications/*
%{_datadir}/%{name}
%{_datadir}/pixmaps/%{name}.png
%{_iconsdir}/%{name}.png
%{_liconsdir}/%{name}.png
%{_miconsdir}/%{name}.png

