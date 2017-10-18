#!/bin/sh

set -e
set -u

DIR="$(dirname $0)"

dc() {
	docker-compose -p sportparken -f ${DIR}/docker-compose.yml $*
}

trap 'dc kill ; dc rm -f' EXIT

rm -rf ${DIR}/backups
mkdir -p ${DIR}/backups


dc build

dc up -d database
sleep 50

dc exec -T database update-table.sh bag bag_pand public sportparken
dc exec -T database update-table.sh bag bag_nummeraanduiding public sportparken

dc run --rm importer
dc run --rm db-backup
