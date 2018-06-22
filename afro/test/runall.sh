IMAGE_PATH=$1
NAME=$2
OFFSET=$3

echo Generate $NAME
time python3 afro/afro/test/generate.py ERROR $IMAGE_PATH $NAME

echo Parse $NAME
time afro -o $OFFSET -l WARNING -e gtf parse $IMAGE_PATH/$NAME.dmg
echo carve nxsb $NAME
time afro -o $OFFSET -l WARNING -e gtf carve nxsb $IMAGE_PATH/$NAME.dmg
echo carve apsb $NAME
time afro -o $OFFSET -l WARNING -e gtf carve apsb $IMAGE_PATH/$NAME.dmg
echo carve nodes $NAME
time afro -o $OFFSET -l WARNING -e gtf carve nodes $IMAGE_PATH/$NAME.dmg

echo Compare results
time python3 afro/afro/test/compare.py ERROR $IMAGE_PATH/$NAME.generation.gtf