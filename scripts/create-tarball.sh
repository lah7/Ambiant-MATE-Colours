#!/bin/bash
#
# Creates a compressed tar.xz package with all the colours for the release notes.
#
cd $(dirname "$0")/../

VERSION=$(dpkg-parsechangelog --show-field Version)

./scripts/build.sh
tar -vc usr/ | xz -z -9 > ambiant-mate-colours-$VERSION.tar.xz
