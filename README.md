![afro logo](logo/afro.png)

# afro (APFS file recovery) ![https://travis-ci.org/cugu/afro](https://api.travis-ci.org/cugu/afro.svg?branch=master)![apfs.ksy-status](https://cugu.eu/file-watcher/?url=https://raw.githubusercontent.com/cugu/apfs.ksy/master/apfs.ksy&md5=dd07549e87b5c3bdf3dcafed29a5aff1&name=apfs.ksy)

afro can parse APFS volumes. It can also recover deleted files from APFS that other tool do not find.

## Installation

    git clone https://github.com/cugu/afro
    cd afro
    python3 setup.py install

## Usage

AFRO needs to know the start of the APFS partition. The partition can be found out as described below.

### Export partition

AFRO needs to know the start of the APFS container, you can find the start of the APFS container using mmls from the [sleuthkit](https://github.com/sleuthkit/sleuthkit).

    mmls test/wsdf.dmg

This results in:

```
GUID Partition Table (EFI)
Offset Sector: 0
Units are in 512-byte sectors

      Slot      Start        End          Length       Description
000:  Meta      0000000000   0000000000   0000000001   Safety Table
001:  -------   0000000000   0000000039   0000000040   Unallocated
002:  Meta      0000000001   0000000001   0000000001   GPT Header
003:  Meta      0000000002   0000000033   0000000032   Partition Table
004:  000       0000000040   0000195319   0000195280   disk image
005:  -------   0000195320   0000195352   0000000033   Unallocated
```

You have to search for the APFS partition in this list. In the example above 004 is the APFS partition which starts at offset 40. `-o 40` needs to be included in the following commands. APFS is not recognized by the sleuth kit so the description is only `disk image`.

### Export files

All files of an apfs image can be extracted using the following command:

    afro -o 40 -e files test/wsdf.dd

The exported files are saved in a folder named after the image with the suffix '.extracted'. Because APFS images can contain multiple volumes, each volume is extracted into a separate folder inside the '.extracted' folder. Each volume can contain multiple versions of the file system which are stored in separate numbered folders. Inside those folders two folders exists 'private-dir' and 'root'. Those folders are not visible to the user, but exist on every APFS file system.

Example:

    wsdf.dmg.carve_apsb.extracted
    ├─ wsdf                  <- First volume
    │  ├─ 5                  <- First version
    │  │  ├─ private-dir
    │  │  └─ root            <- Root directory
    │  │     ├─ folder
    │  │     │  └─ foo.txt
    │  │     └─ bar.txt
    │  └─ 6                  <- Second version
    │     └─ …
    └─ my_volume_name        <- Second volume
       └─ …

### Create body file

To get an overview over the files a body file can be created:

    afro -o 40 -e bodyfile apfs_volume.dd

More information on the body file format can be found in the [sleuthkit wiki](https://wiki.sleuthkit.org/index.php?title=Body_file). The body file can be further investigated using [mactime](https://wiki.sleuthkit.org/index.php?title=Mactime) and [Timeline Explorer](https://ericzimmerman.github.io/).


## Documentation on APFS

 - [**Apple File System Reference**](https://developer.apple.com/support/apple-file-system/Apple-File-System-Reference.pdf): Official, but incomplete APFS specification
 - [**Decoding the APFS file system**](http://www.sciencedirect.com/science/article/pii/S1742287617301408): Paper by Kurt H.Hansen and Fergus Toolan Fergus in _Digital Investigation_. Published: 2017-09-22.
 - [**Apple File System Guide**](https://developer.apple.com/library/content/documentation/FileManagement/Conceptual/APFS_Guide/Introduction/Introduction.html): Official documentation on APFS. Lacks lots of information on APFS. Last update: 2017-09-21.
 - [**APFS filesystem format**](https://blog.cugu.eu/post/apfs/): Deprecated blog post by myself. Still contains some useful diagrams. Last update: 2017-04-30.
 - Information about the checksum calculation can be found in [checksum.md](docs/checksum.md).


## Contributing
Pull requests and issues are welcome!

## Licenses
The afro software is licensed as [GPLv3](licences/gpl-3.0.txt).
The ksy file (libapfs/apfs.ksy) is licensed under [MIT license](licences/mit.txt).

