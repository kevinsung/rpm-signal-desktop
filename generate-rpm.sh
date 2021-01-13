#!/bin/bash

docker build -t rpm-signal-desktop .
container=$(docker create rpm-signal-desktop)
docker cp $container:/root/rpmbuild/RPMS/x86_64/signal-desktop-1.39.6-1.fc33.x86_64.rpm .
docker cp $container:/root/rpmbuild/SRPMS/signal-desktop-1.39.6-1.fc33.src.rpm .
docker rm $container
