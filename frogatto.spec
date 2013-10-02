%global commit a7ef3bfa0c32df4852bf057fab969c1a080edf4d
%global shortcommit %(c=%{commit}; echo ${c:0:7})

Name:           frogatto
Version:        1.3.3
Release:        1%{?dist}
Summary:        An old-school 2D platform game

# Artwork and music not released under an open license
License:        GPLv3+ and proprietary
URL:            http://www.frogatto.com/
Source0:        https://github.com/frogatto/frogatto/archive/%{commit}/%{name}-%{version}-%{shortcommit}.tar.gz
Source1:        %{name}.sh
Source2:        %{name}.desktop
Source3:        %{name}.pod
# Patch Makefile not to link lSDLmain
Patch0:         %{name}-1.2-Makefile.patch
# Boost no longer has separate non mt and -mt variants of its libs
Patch1:         %{name}-1.3-no-boost-mt.patch
# Use FreeFont instead of the Ubuntu Font Family
Patch2:         %{name}-1.3-fonts.patch

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
BuildRequires:  gnu-free-mono-fonts
BuildRequires:  libicns-utils
BuildRequires:  desktop-file-utils 
Requires:       hicolor-icon-theme


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

# Fix locale file path
sed -i 's!"./locale/"!"%{_datadir}/locale/"!' src/i18n.cpp


%build
make %{?_smp_mflags} \
  BASE_CXXFLAGS="$RPM_OPT_FLAGS -fno-inline-functions -fthreadsafe-statics"


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

%find_lang %{name}


%post
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :


%postun
if [ $1 -eq 0 ] ; then
    touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi


%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :


%files -f %{name}.lang
%doc modules/%{name}/CHANGELOG LICENSE
%{_bindir}/%{name}
%{_datadir}/%{name}
%{_libexecdir}/%{name}
%{_datadir}/icons/hicolor/*/apps/%{name}.png
%{_datadir}/applications/%{name}.desktop
%{_mandir}/man6/%{name}.6*


%changelog
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

