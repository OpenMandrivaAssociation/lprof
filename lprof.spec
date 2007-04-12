%define	name	lprof

%define	version	1.11.4.1

%define	rel	1
%define	release	%mkrel %{rel}

Name:		%{name}
Version:	%{version}
Release:	%{release}
Summary:	Color Profilers
Group: 		Office
License:	GPL
URL:		http://lprof.sourceforge.net
Source:		http://prdownloads.sourceforge.net/lprof/%{name}-%{version}.tar.bz2
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
Requires:	liblcms >= 1.09
Provides:	lprof = %{version}-%{release}
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}
%description
LProf is an open source color profiler that creates ICC compliant
profiles for devices such as cameras, scanners and monitors.


%prep
rm -rf %{buildroot}
%setup -q
%patch1 -p 0 -b .fix-typo
%patch2 -p 0 -b .fix-chk4qt
%patch3 -p 0 -b .fix-desktop
chmod 644 data/help/about.txt

%build
mkdir -p %{buildroot}%{_prefix}
./scons.py PREFIX="%{_prefix}" QT_LIBPATH="%{_prefix}/lib/qt3/%{_lib}" ccflags="%{optflags}" cxxflags="%{optflags}"

%install
rm -rf %{buildroot}

mkdir -p %{buildroot}%{_prefix}
./scons.py PREFIX="%{buildroot}%{_prefix}" install

install -p -D -m0644 data/icons/lprof.png %{buildroot}%{_liconsdir}/%{name}.png

mkdir -p -m 755 %{buildroot}%{_iconsdir}
convert %{buildroot}%{_liconsdir}/%{name}.png -size 32x32 %{buildroot}%{_iconsdir}/%{name}.png
mkdir -p -m 755 %{buildroot}%{_miconsdir}
convert %{buildroot}%{_iconsdir}/%{name}.png -size 16x16 %{buildroot}%{_miconsdir}/%{name}.png

install -d -m 0755 %{buildroot}%{_menudir}
cat > %{buildroot}%{_menudir}/%{name} <<EOF
?package(%{name}): \
command="%{_bindir}/lprof" \
title="Little CMS Profiler" \
longtitle="LProf ICC Profile Creator" \
needs="x11" \
section="Office/Publishing" \
icon="%{name}.png" \
xdg="true"
EOF

desktop-file-install --vendor="" \
  --add-category="X-Mandrakelinux-Office-Publishing" \
  --dir %{buildroot}%{_datadir}/applications %{buildroot}%{_datadir}/applications/*

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
%{_menudir}/*

