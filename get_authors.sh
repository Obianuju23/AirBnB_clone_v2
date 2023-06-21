#!/usr/bin/env bash

set -e

cd "$(dirname "$(readlink -f "$BASH_SOURCE")")"

{
    cat <<-'EOH'
# File @generated by get_authors.sh. DO NOT EDIT.
# This file lists all individuals who have contributed to the contents in this repository.
# See get_authors.sh to make modifications, or see how it was generated.
EOH
echo
git log --format='%aN <%aE>' | LC_ALL=C.UTF-8 sort -uf
} > AUTHORS