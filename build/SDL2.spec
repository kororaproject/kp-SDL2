%global hgdate 20121107
%global hgrev 6659

Name:		SDL2
Version:	2.0
Release:	0.1.20121107hg6659%{?dist}
# hg clone http://hg.libsdl.org/SDL SDL2
Summary:	Simple DirectMedia Layer v2
License:	zlib
URL:		http://www.libsdl.org/
# hg clone http://hg.libsdl.org/SDL SDL2
# rm -rf SDL2/.hg
# tar cvfj SDL2-20121107hg6659.tar.bz2 SDL2
Source0:	%{name}-%{hgdate}hg%{hgrev}.tar.bz2
Source1:	SDL_config.h
Patch0:		SDL2-2.0-multilib.patch
BuildRequires:	alsa-lib-devel
BuildRequires:	audiofile-devel
BuildRequires:	mesa-libEGL-devel
BuildRequires:	mesa-libGL-devel
BuildRequires:	mesa-libGLU-devel
BuildRequires:	mesa-libGLES-devel
BuildRequires:	libXext-devel
BuildRequires:	libX11-devel
BuildRequires:	libXrandr-devel
BuildRequires:	libXrender-devel
BuildRequires:	pulseaudio-libs-devel
BuildRequires:	tslib-devel
%ifarch %{ix86}
BuildRequires:	nasm
%endif

%description
Simple DirectMedia Layer (SDL) is a cross-platform multimedia library designed
to provide fast access to the graphics frame buffer and audio device.
This is version 2.

%package devel
Summary:	Files needed to develop Simple DirectMedia Layer v2 applications
Requires:	SDL2%{?_isa} = %{version}-%{release}
Requires:	alsa-lib-devel
Requires:	audiofile-devel
Requires:	mesa-libEGL-devel
Requires:	mesa-libGL-devel
Requires:	mesa-libGLU-devel
Requires:	mesa-libGLES-devel
Requires:	libX11-devel
Requires:	libXext-devel
Requires:	libXrandr-devel
Requires:	libXrender-devel
Requires:	pulseaudio-libs-devel
Requires:	tslib-devel

%description devel
Simple DirectMedia Layer (SDL) is a cross-platform multimedia library designed
to provide fast access to the graphics frame buffer and audio device. This
package provides the libraries, include files, and other resources needed for
developing SDL v2 applications.

%prep
%setup -q -n %{name}
%patch0 -p1 -b .multilib

for F in CREDITS; do 
    iconv -f iso8859-1 -t utf-8 < "$F" > "${F}.utf"
    touch --reference "$F" "${F}.utf"
    mv "${F}.utf" "$F"
done

%build
%configure --disable-video-svga --disable-video-ggi --disable-video-aalib --enable-sdl-dlopen --disable-arts --disable-esd --enable-pulseaudio-shared --enable-alsa --disable-video-ps3 --disable-rpath
make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot}

# Rename SDL_config.h to SDL_config-<arch>.h to avoid file conflicts on
# multilib systems and install SDL_config.h wrapper
mv %{buildroot}/%{_includedir}/SDL2/SDL_config.h %{buildroot}/%{_includedir}/SDL2/SDL_config-%{_arch}.h
install -m644 %{SOURCE1} %{buildroot}/%{_includedir}/SDL2/SDL_config.h

# For compatibility with case-insensitive Debian/Ubuntu
pushd %{buildroot}%{_libdir}
ln -s libSDL2.so libsdl2.so
ln -s libSDL2-2.0.so.0 libsdl2-2.0.so.0
ln -s libSDL2-2.0.so.0.0.0 libsdl2-2.0.so.0.0.0
popd

rm -rf %{buildroot}%{_libdir}/*.la %{buildroot}%{_libdir}/*.a

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%doc BUGS COPYING CREDITS README-SDL.txt
%{_libdir}/libSDL2-2.0.so.*
%{_libdir}/libsdl2-2.0.so.*

%files devel
%doc README TODO WhatsNew
%{_bindir}/*-config
%{_libdir}/lib*.so
%{_libdir}/pkgconfig/sdl2.pc
%{_includedir}/SDL2
%{_datadir}/aclocal/*

%changelog
* Wed Nov 7 2012 Tom Callaway <spot@fedoraproject.org> - 2.0-0.1.20121107hg6659
- initial SDL2 package
