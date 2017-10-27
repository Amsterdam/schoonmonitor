set -x
set -u
set -e

python /app/download_from_objectstore.py /data2
python /app/load_xls_pg.py /data2/aanvalsplan_schoon/crow docker
