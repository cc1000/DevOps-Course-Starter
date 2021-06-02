echo "Calling webhook to trigger app restart: $1"
curl -dH -X POST "$1"