%global commit a7ef3bfa0c32df4852bf057fab969c1a080edf4d
%global shortcommit %(c=%{commit}; echo ${c:0:7})

Name:           frogatto
Version:        1.3.3
Release:        29%{?dist}
Summary:        An old-school 2D platform game

# Artwork and music not released under an open license
License:        GPLv3+ and proprietary
URL:            http://www.frogatto.com/
Source0:        https://github.com/frogatto/frogatto/archive/%{commit}/%{name}-%{version}-%{shortcommit}.tar.gz
Source1:        %{name}.sh
Source2:        %{name}.desktop
Source3:        %{name}.pod
Source4:        %{name}.appdata.xml
# Patch Makefile not to link lSDLmain
Patch0:         %{name}-1.2-Makefile.patch
# Boost no longer has separate non mt and -mt variants of its libs
Patch1:         %{name}-1.3-no-boost-mt.patch
# Use FreeFont instead of the Ubuntu Font Family
Patch2:         %{name}-1.3-fonts.patch
# Fix gcc6 build only fixes some of the narrowing conversion warnings, there
# are too many, so we add -Wno-narrowing to the CXXFLAGS as a workaround
Patch3:         %{name}-1.3-narrowing-conversion-fixes.patch
# Fix comparison between pointer and integer errors
# https://github.com/anura-engine/anura/commit/18ad198565f7a3280d991a5878316f6e5c9351d3
Patch4:         %{name}-1.3-comparison.patch
# Fix building with Boost 1.70+
Patch5:         %{name}-1.3-boost.patch
# Fix stack overflow in base64 test
# Patch by Ingo van Lil
Patch6:         %{name}-1.3.3-stack-overflow.patch
# Work around surface double free with sdl12-compat
# This needs to be removed once sdl12-compat > 1.2.52 is released
# Patch by Ingo van Lil
Patch7:         %{name}-1.3.3-sdl.patch

# We have problems with these architectures
# https://lists.rpmfusion.org/archives/list/rpmfusion-developers@lists.rpmfusion.org/thread/LQXC5S37G6S4NRZNB7KKGD2Q25OKXSEV/
ExcludeArch:    ppc64 ppc64le aarch64

BuildRequires:  gcc-c++
BuildRequires:  SDL-devel >= 1.2.7
BuildRequires:  SDL_image-devel
BuildRequires:  SDL_mixer-devel
BuildRequires:  SDL_ttf-devel >= 2.0.8
BuildRequires:  mesa-libGLU-devel
BuildRequires:  glew-devel
BuildRequires:  libpng-devel
BuildRequires:  ccache
BuildRequires:  boost-devel
BuildRequires:  perl-podlators
BuildRequires:  libicns-utils
BuildRequires:  desktop-file-utils 
BuildRequires:  libappstream-glib
Requires:       hicolor-icon-theme
Requires:       gnu-free-mono-fonts


%description
An old-school 2D platform game, starring a certain quixotic frog. Frogatto
has gorgeous, high-end pixel art, pumping arcade tunes, and all the gameplay 
nuance of a classic console title. Run and jump over pits and enemies. Grab 
enemies with your tongue, swallow them, and then spit them out at other enemies 
as projectiles! Fight dangerous bosses, and solve vexing puzzles. Collect coins 
and use them to buy upgrades and new abilities in the store. Talk to characters 
in game, and work to unravel Big Bad Milgram's plot against the townsfolk! 


%prep
%setup -qn %{name}-%{commit}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p0
%patch6 -p1
%patch7 -p1

# Fix locale file path
sed -i 's!"./locale/"!"%{_datadir}/locale/"!' src/i18n.cpp

# Edit BASE_CXXFLAGS
sed -i 's/BASE_CXXFLAGS += -g -fno-inline-functions -fthreadsafe-statics -Wnon-virtual-dtor -Werror -Wignored-qualifiers -Wformat -Wswitch/BASE_CXXFLAGS += -fno-inline-functions -fthreadsafe-statics -Wno-narrowing/' Makefile


%build
%set_build_flags
%make_build


%install
# Install wrapper script
install -d %{buildroot}%{_bindir}
install -m 755 -p %{SOURCE1} %{buildroot}%{_bindir}/%{name}

# Install game and data
install -d %{buildroot}%{_libexecdir}/%{name}
install -m 755 -p game %{buildroot}%{_libexecdir}/%{name}
install -d %{buildroot}%{_datadir}/%{name}/modules/%{name}
cp -pr data images music *.cfg \
  %{buildroot}%{_datadir}/%{name}
pushd modules/%{name}
  cp -pr data images music sounds *.cfg \
    %{buildroot}%{_datadir}/%{name}/modules/%{name}
  # Install translations
  cp -pr locale %{buildroot}%{_datadir}
popd

# Install desktop file
install -d %{buildroot}%{_datadir}/applications
desktop-file-install \
  --dir %{buildroot}%{_datadir}/applications \
  %{SOURCE2}

# Extract Mac OS X icons
icns2png -x modules/%{name}/images/os/mac/icon.icns 

# Install icons
for i in 16 32 128 256; do
  install -d -m 755 %{buildroot}%{_datadir}/icons/hicolor/${i}x${i}/apps
  install -m 644 icon_${i}x${i}x32.png \
    %{buildroot}%{_datadir}/icons/hicolor/${i}x${i}/apps/%{name}.png
done

# Install man page
install -d %{buildroot}%{_mandir}/man6
pod2man --section=6 \
  -center="RPM Fusion contributed man pages" \
  -release="%{name} %{version}" \
  -date="July 13th, 2010" \
  %{SOURCE3} > %{buildroot}%{_mandir}/man6/%{name}.6

# Install AppData file
install -d %{buildroot}%{_datadir}/metainfo
install -p -m 644 %{SOURCE4} %{buildroot}%{_datadir}/metainfo
appstream-util validate-relax --nonet \
  %{buildroot}/%{_datadir}/metainfo/*.appdata.xml


%find_lang %{name}


%files -f %{name}.lang
%doc modules/%{name}/CHANGELOG
%license LICENSE
%{_bindir}/%{name}
%{_datadir}/%{name}
%{_libexecdir}/%{name}
%{_datadir}/icons/hicolor/*/apps/%{name}.png
%{_datadir}/applications/%{name}.desktop
%{_datadir}/metainfo/%{name}.appdata.xml
%{_mandir}/man6/%{name}.6*


%changelog
* Fri Aug 02 2024 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 1.3.3-29
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sun Feb 04 2024 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 1.3.3-28
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Aug 03 2023 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 1.3.3-27
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Mon Aug 08 2022 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 1.3.3-26
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild and ffmpeg
  5.1

* Tue Apr 26 2022 Andrea Musuruane <musuruan@gmail.com> - 1.3.3-25
- Fix segfault at startup (BZ #6252). Thanks to Ingo van Lil.
- Use %%set_build_flags macro

* Mon Feb 14 2022 Sérgio Basto <sergio@serjux.com> - 1.3.3-24
- Rebuid for glew-2.2.0

* Thu Feb 10 2022 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 1.3.3-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Aug 19 2021 Leigh Scott <leigh123linux@gmail.com> - 1.3.3-22
- Rebuild for new boost

* Wed Aug 04 2021 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 1.3.3-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Thu Feb 04 2021 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 1.3.3-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Aug 19 2020 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 1.3.3-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Jun 05 2020 Andrea Musuruane <musuruan@gmail.com> - 1.3.3-18
- Added a patch from FreeBSD to build with Boost 1.70+
- Added AppData file
- Added license tag
- Removed desktop scriptlets

* Thu Jun 04 2020 Leigh Scott <leigh123linux@gmail.com> - 1.3.3-17
- Rebuilt for Boost 1.73

* Wed Feb 05 2020 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 1.3.3-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sat Aug 10 2019 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 1.3.3-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Mar 05 2019 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 1.3.3-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sun Sep 30 2018 Sérgio Basto <sergio@serjux.com> - 1.3.3-13
- Rebuild for glew 2.1.0
- Add BuildRequires: gcc-c++

* Sun Aug 19 2018 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 1.3.3-12
- Rebuilt for Fedora 29 Mass Rebuild binutils issue

* Fri Jul 27 2018 RPM Fusion Release Engineering <sergio@serjux.com> - 1.3.3-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Mar 02 2018 RPM Fusion Release Engineering <leigh123linux@googlemail.com> - 1.3.3-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 31 2017 RPM Fusion Release Engineering <kwizart@rpmfusion.org> - 1.3.3-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue Mar 28 2017 Andrea Musuruane <musuruan@gmail.com> - 1.3.3-8
- Workaround not to build for ppc64, ppc64le and aarch64

* Sat Mar 25 2017 Andrea Musuruane <musuruan@gmail.com> - 1.3.3-7
- Fix comparison between pointer and integer errors / fix FTBFS

* Thu Jul  7 2016 Hans de Goede <j.w.r.degoede@gmail.com> - 1.3.3-6
- Fix building with gcc6 / fix FTBFS

* Mon Sep 01 2014 Sérgio Basto <sergio@serjux.com> - 1.3.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Fri May 30 2014 Hans de Goede <j.w.r.degoede@gmail.com> - 1.3.3-4
- Rebuild for new boost

* Sun Mar  2 2014 Hans de Goede <j.w.r.degoede@gmail.com> - 1.3.3-3
- Rebuild for new glew

* Thu Oct 10 2013 Andrea Musuruane <musuruan@gmail.com> - 1.3.3-2
- Fixed requiring gnu-free-mono-fonts (again #2966)

* Wed Sep 25 2013 Andrea Musuruane <musuruan@gmail.com> - 1.3.3-1
- Updated to upstream v1.3.3 as of Aug 21, 2013
- Fixed crash when attempting to enter in editor mode (#2966)
- Used Mac OS X icons
- Removed Group tag

* Mon Aug 26 2013 Hans de Goede <j.w.r.degoede@gmail.com> - 1.3.1-3
- Rebuild for new boost

* Mon Apr  8 2013 Hans de Goede <j.w.r.degoede@gmail.com> - 1.3.1-2
- Explicitly BuildRequires perl-podlators for manpage generation

* Mon Apr  8 2013 Hans de Goede <j.w.r.degoede@gmail.com> - 1.3.1-1
- Rebase to upstream 1.3.1 release
- Rebuild for new boost and glew

* Thu Nov 01 2012 Nicolas Chauvet <kwizart@gmail.com> - 1.2-4
- Rebuilt

* Thu Mar 08 2012 Nicolas Chauvet <kwizart@gmail.com> - 1.2-3
- Rebuilt for c++ ABI breakage

* Thu Feb 09 2012 Nicolas Chauvet <kwizart@gmail.com> - 1.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun Dec 25 2011 Andrea Musuruane <musuruan@gmail.com> 1.2-1
- Updated to upstream 1.2
- Added a patch by YuGiOhJCJ to add joystick support for Microsoft X-Box 
  360 pad and Microsoft SideWinder Game Pad USB

* Sat Jul 16 2011 Andrea Musuruane <musuruan@gmail.com> 1.1.1-1
- Updated to upstream 1.1.1

* Sat Jun 11 2011 Andrea Musuruane <musuruan@gmail.com> 1.1-1
- Updated to upstream 1.1

* Mon May 30 2011 Hans de Goede <j.w.r.degoede@gmail.com> - 1.0.3-3
- Rebuilt for new boost (rf#1773)

* Thu Oct 14 2010 Nicolas Chauvet <kwizart@gmail.com> - 1.0.3-2
- Rebuilt for gcc bug

* Sat Sep 25 2010 Andrea Musuruane <musuruan@gmail.com> 1.0.3-1
- Updated to upstream 1.0.3

* Sat Sep 04 2010 Andrea Musuruane <musuruan@gmail.com> 1.0.2-1
- Updated to upstream 1.0.2

* Sun Jul 25 2010 Andrea Musuruane <musuruan@gmail.com> 1.0-1
- First release
- Included startup script, desktop icon and man page from Debian

