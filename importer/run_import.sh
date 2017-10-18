set -x
set -u
set -e

python /app/download_from_objectstore.py /data
#python /app/load_data.py /data