%define	name	lprof

%define	version	1.11.4.2

%define	rel	0.1
%define	release	%mkrel %{rel}

Name:		%{name}
Version:	%{version}
Release:	%{release}
Summary:	Color Profilers
Group: 		Office
License:	GPL
URL:		http://lprof.sourceforge.net
#Source:		http://prdownloads.sourceforge.net/lprof/%{name}-%{version}.tar.bz2
Source0:	lprof-%{version}-cvs20071209.tar.bz2
Patch1:		lprof-mainbase-typo.diff
Patch2:		lprof-fix-chk4qt.diff
Patch3:		lprof-desktop.diff
BuildRequires:	desktop-file-utils
BuildRequires:	ImageMagick
BuildRequires:	liblcms-devel >= 1.09
BuildRequires:	libtiff-devel
BuildRequires:	libvigra-devel
BuildRequires:	python
BuildRequires:	qt3-devel
BuildRequires:  scons
Requires:	qt3-assistant
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}
%description
LProf is an open source color profiler that creates ICC compliant
profiles for devices such as cameras, scanners and monitors.


%prep
rm -rf %{buildroot}
%setup -q -n lprof
#%patch1 -p 0 -b .fix-typo
#%patch2 -p 0 -b .fix-chk4qt
%patch3 -p 0 -b .fix-desktop
#chmod 644 data/help/about.txt

%build
PATH=$PATH:%{_prefix}/lib/qt3/bin
export PATH
scons PREFIX="%{_prefix}" QT_LIBPATH="%{_prefix}/lib/qt3/%{_lib}" ccflags="`echo %{optflags} | sed -e 's/-Wp,-D_FORTIFY_SOURCE=2//g'`" cxxflags="%{optflags}"

%install
rm -rf %{buildroot}

mkdir -p %{buildroot}%{_prefix}
PATH=$PATH:%{_prefix}/lib/qt3/bin
export PATH

# create missing files
touch data/help/{en,ru}/calreports.html
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
