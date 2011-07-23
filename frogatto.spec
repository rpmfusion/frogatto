Name:           frogatto
Version:        1.1.1
Release:        1%{?dist}
Summary:        An old-school 2D platform game

Group:          Amusements/Games
# Artwork and music not released under an open license
License:        GPLv3+ and proprietary
URL:            http://www.frogatto.com/
Source0:        http://www.frogatto.com/files/%{name}-%{version}.tar.bz2
Source1:        %{name}.sh
Source2:        %{name}.desktop
Source3:        %{name}.xpm
Source4:        %{name}.pod
# Patch Makefile not to link lSDLmain
Patch0:         %{name}-1.1-Makefile.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  SDL-devel >= 1.2.7
BuildRequires:  SDL_image-devel
BuildRequires:  SDL_mixer-devel
BuildRequires:  SDL_ttf-devel >= 2.0.8
BuildRequires:  mesa-libGLU-devel
BuildRequires:  glew-devel
BuildRequires:  libpng-devel
BuildRequires:  ccache
BuildRequires:  boost-devel
BuildRequires:  perl
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
%setup -q
%patch0 -p1

# Fix locale file path
sed -i 's!"./locale/"!"%{_datadir}/locale/"!' src/i18n.cpp


%build
make OPT="$RPM_OPT_FLAGS" %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT

# Install wrapper script
install -d %{buildroot}%{_bindir}
install -m 755 -p %{SOURCE1} %{buildroot}%{_bindir}/%{name}

# Install game and data
install -d %{buildroot}%{_libexecdir}/%{name}
install -m 755 -p game %{buildroot}%{_libexecdir}/%{name}
install -d %{buildroot}%{_datadir}/%{name}
cp -pr data images music sounds \
  %{buildroot}%{_datadir}/%{name}

# Install translations
install -d %{buildroot}%{_datadir}/locale
cp -pr locale %{buildroot}%{_datadir}

# Install desktop file
install -d %{buildroot}%{_datadir}/applications
desktop-file-install \
  --dir %{buildroot}%{_datadir}/applications \
  %{SOURCE2}

# Install icon 
install -d %{buildroot}%{_datadir}/icons/hicolor/32x32/apps
install -m 644 -p %{SOURCE3} %{buildroot}%{_datadir}/icons/hicolor/32x32/apps

# Install man page
install -d %{buildroot}%{_mandir}/man6
pod2man --section=6 \
  -center="RPM Fusion contributed man pages" \
  -release="%{name} %{version}" \
  -date="July 13th, 2010" \
  %{SOURCE4} > %{buildroot}%{_mandir}/man6/%{name}.6

%find_lang %{name}


%clean
rm -rf $RPM_BUILD_ROOT


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
%defattr(-,root,root,-)
%{_bindir}/%{name}
%{_datadir}/%{name}
%{_libexecdir}/%{name}
%{_datadir}/icons/hicolor/*/apps/%{name}.xpm
%{_datadir}/applications/%{name}.desktop
%{_mandir}/man6/%{name}.6*
%doc CHANGELOG LICENSE


%changelog
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

