#!/usr/bin/env nix-shell
#!nix-shell --pure -i bash
tmpdir=$(mktemp -d)
socketdir=${1:-$tmpdir}
echo "Using database temp dir $tmpdir"
export LC_ALL='en_US.UTF-8'

trap "pg_ctl stop -D $tmpdir; rm -rf $tmpdir" EXIT
pg_ctl -D $tmpdir init
pg_ctl start -D $tmpdir -o "-k $socketdir -h ''"
createdb -h $socketdir test_ekklesia_portal
echo "Loading test database..."
psql -h $socketdir test_ekklesia_portal -f tests/test_db.sql
doit
pytest
wait
