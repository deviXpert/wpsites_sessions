#!/bin/bash
EXPECTED_HOST="${EHMC_EXPECTED_HOST:-hotpink-lobster-615998.hostingersite.com}"; case "$WP_URL" in *"$EXPECTED_HOST"*) ;; *) echo "Refusing: WP_URL is not $EXPECTED_HOST" >&2; exit 1;; esac
# usage: wp.sh METHOD path [json]
if [ -n "$3" ]; then curl -sS -X "$1" -u "$WP_USER:$WP_APP_PASSWORD" -H 'Content-Type: application/json' --data-binary "$3" "$WP_URL/wp-json/$2"
else curl -sS -X "$1" -u "$WP_USER:$WP_APP_PASSWORD" "$WP_URL/wp-json/$2"; fi
