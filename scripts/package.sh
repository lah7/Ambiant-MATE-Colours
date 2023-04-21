#!/bin/bash -xe
#
# For the maintainer to create a package, and a compressed tarball
# for the release notes too.
#

cd "$(dirname $0)/../"

# Update changelog
dch

# Get source code for Ambiant-MATE
if [ ! -d Ambiant-MATE/ ]; then
    git clone https://github.com/lah7/Ambiant-MATE.git --depth 1
    rm -rf Ambiant-MATE/*.git
    rm -rf Ambiant-MATE/debian
fi

# Ensure dependencies are installed
sudo apt-get install librsvg2-bin imagemagick

# Prepare source build
debuild -S

# Upload to Launchpad
dput ppa:lah7/ambiant-mate ../*.changes

# Create a local build
./scripts/create-tarball.sh
scripts/build.sh
