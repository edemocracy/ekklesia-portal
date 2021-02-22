#!/usr/bin/env nix-shell
#!nix-shell --pure -i bash
tmpdir=$(mktemp -d)
echo $tmpdir

export LC_ALL='en_US.UTF-8'

trap "pg_ctl stop -D $tmpdir; rm -rf $tmpdir" EXIT
pg_ctl -D $tmpdir init
pg_ctl start -D $tmpdir -o "-k /tmp -h ''"
createdb -h /tmp ekklesia_portal
psql -h /tmp ekklesia_portal -f tests/test_db.sql
ipython makebabel.ipy compile
pytest
wait
