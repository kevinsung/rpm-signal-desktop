%global debug_package %{nil}

%define capitalname Signal-Desktop

Name:           signal-desktop
Version:        1.39.6
Release:        1%{?dist}
Summary:        Private messaging from your desktop

License:        AGPLv3
URL:            https://signal.org/
Source0:        https://github.com/signalapp/%{capitalname}/archive/v%{version}.tar.gz
Source1:        %{name}.desktop
# Allow higher Node version
Patch0:         allow-higher-node-version.patch
# We can't read the release date from git so we use SOURCE_DATE_EPOCH instead
# See https://github.com/signalapp/Signal-Desktop/issues/2376
Patch1:         expire-from-source-date-epoch.patch
# Have SQLCipher dynamically link libcrypto
# See https://github.com/signalapp/Signal-Desktop/issues/2634
Patch2:         dynamically-link-libcrypto.patch

BuildRequires:  gcc-c++
BuildRequires:  git
BuildRequires:  make
BuildRequires:  nodejs >= 12.13.0
BuildRequires:  python
BuildRequires:  python2
BuildRequires:  yarnpkg

%description
Signal Desktop is an Electron application that links with Signal on Android or iOS.


%prep
%setup -q -n %{capitalname}-%{version}
%patch0
%patch1
yarn install --frozen-lockfile
%patch2


%build
# Gruntfile.js looks for git commit information which isn't present in a tarball download
# See https://github.com/signalapp/Signal-Desktop/issues/2376
yarn generate exec:build-protobuf exec:transpile concat copy:deps sass
yarn build


%install
# Allow invalid and '$ORIGIN' RPATHS, which are present in bundled libraries
export QA_RPATHS=$(( 0x0002|0x0008 ))

install -d %{buildroot}/%{_libdir}
install -d %{buildroot}/%{_bindir}
cp -a release/linux-unpacked %{buildroot}/%{_libdir}/%{name}
ln -s %{_libdir}/%{name}/%{name} %{buildroot}/%{_bindir}

install -Dm 644 %{SOURCE1} %{buildroot}/%{_datadir}/applications/%{name}.desktop

for size in 16 24 32 48 64 128 256 512 1024; do
  install -Dm 644 build/icons/png/${size}x${size}.png \
    %{buildroot}/%{_datadir}/icons/hicolor/${size}x${size}/apps/%{name}.png
done


%check


%files
%license LICENSE
%{_bindir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/apps/%{name}.png
%{_libdir}/%{name}



%changelog
* Sat Jan  9 16:54:56 EST 2021 Kevin J. Sung <kevjsung@umich.edu>
- adapt from Arch Linux package build
