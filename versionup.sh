#!/bin/sh

# Version up script.
#
# Usage:
# $ ./versionup.sh {RELEASE_VERSION}
#
# Example:
# $ ./versionup.sh 0.2.1
#
# Prior to run this script, be sure to create release branch.
# $ git flow release start $VERSION

VERSION=$1

if [ -z "$VERSION" ]
then
    echo "No version was given."
    exit 1
fi

# XXX: Check version string contains three digit delimited by period.

sed -i "" -E "s/^__version__ = '[0-9].[0-9].[0-9]'$/__version__ = '$VERSION'/" src/clitool/__init__.py
sed -i "" -E "s/^VERSION = '[0-9].[0-9].[0-9]'$/VERSION = '$VERSION'/" wscript
sed -i "" -E "s/^release = '[0-9].[0-9].[0-9]'$/release = '$VERSION'/" doc/conf.py
sed -i "" -E "s/^version = '[0-9].[0-9]'$/version = '${VERSION%%.[0-9]}'/" doc/conf.py

git add src/clitool/__init__.py wscript doc/conf.py
git df

echo "If diff is okay, continue following commands."

cat <<EOF
$ git commit -m "update release version -> $VERSION"
$ git flow release finish $VERSION
EOF
