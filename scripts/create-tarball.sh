#!/bin/bash
#
# Creates a compressed tar.xz package containing the icons for a release.
#
cd $(dirname "$0")/../
./scripts/build.sh
VERSION=$(python3 -c "f=open('debian/changelog'); print(f.readline().split('(')[1].split(')')[0])")
tar -vc usr/ | xz -z -9 > ubuntu-mate-colours-$VERSION.tar.xz
