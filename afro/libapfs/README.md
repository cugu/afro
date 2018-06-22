Howto generate apfs.py:

1. Install Kaitai:

	brew install kaitai-struct-compiler
	pip3 install kaitaistruct

2. Create parser:

	kaitai-struct-compiler apfs-extractor/libapfs/apfs.ksy -t python -d apfs-extractor/libapfs/

python3 apfs-extractor.py -o 20480 parse ../data/image_50M_1.dmg test
