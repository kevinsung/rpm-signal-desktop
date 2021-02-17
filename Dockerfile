FROM fedora

# Install utilities
RUN dnf install -y curl dnf-plugins-core rpmdevtools

# Set up environment
RUN rpmdev-setuptree
WORKDIR /root/rpmbuild
COPY ./signal-desktop.spec SPECS/
COPY ./dynamically-link-libcrypto.patch SOURCES/
COPY ./expire-from-source-date-epoch.patch SOURCES/
COPY ./signal-desktop.desktop SOURCES/
RUN curl -o SOURCES/v1.40.0.tar.gz -LJ https://github.com/signalapp/Signal-Desktop/archive/v1.40.0.tar.gz

# Install build dependencies
RUN dnf builddep -y SPECS/signal-desktop.spec

# Build
RUN rpmbuild -ba SPECS/signal-desktop.spec
