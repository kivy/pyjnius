#!/usr/bin/env bash
set -ex

if [[ ! $GITHUB_REF =~ ^refs/tags/ ]]; then
   exit 0
fi

owner=kivy
repository=pyjnius
access_token=$GITHUB_OAUTH_TOKEN

tag=${GITHUB_REF#refs/tags/}
draft="false"
prerelease="false"
version_name="$tag"
message="Release $tag"

python -m twine check dist/*

twine="python -m twine upload -u kivybot --disable-progress-bar"

if [[ $GITHUB_REF =~ -test$ ]]; then
    twine="$twine --repository-url https://test.pypi.org/legacy/"
    draft="true"
    prerelease="true"
    message="test release $tag"
fi

API_JSON="{
    \"tag_name\": \"$tag\",
    \"name\": \"$version_name\",
    \"body\": \"$message\n\",
    \"draft\": $draft,
    \"prerelease\": $prerelease
}"

echo $API_JSON

$twine dist/*
curl --data "$API_JSON"\
     Https://api.github.com/repos/$owner/$repository/releases?access_token=$access_token
