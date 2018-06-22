# should be run from afro dir

IMAGE_PATH=/Volumes/SHARE/
rm -rf $IMAGE_PATH/*

cd afro
kaitai-struct-compiler afro/libapfs/apfs.ksy -t python -d afro/libapfs/
python3 setup.py install --force
cd ..

bash afro/afro/test/runall.sh $IMAGE_PATH image_2G_4 40
bash afro/afro/test/runall.sh $IMAGE_PATH image_5G_4 409640
bash afro/afro/test/runall.sh $IMAGE_PATH image_10G_4 409640
bash afro/afro/test/runall.sh $IMAGE_PATH image_100G_4 409640
bash afro/afro/test/runall.sh $IMAGE_PATH image_500G_4 409640