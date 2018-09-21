Howto generate apfs.py:

1. Install Kaitai:

    brew install kaitai-struct-compiler
    pip3 install kaitaistruct

2. Create parser:

    kaitai-struct-compiler -t python afro/libapfs/apfs.ksy
    mv apfs.py afro/libapfs/

afro -o 40 parse ../data/image_50M_1.dmg test
