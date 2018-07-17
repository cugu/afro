# afro (APFS file recovery) ![stability-experimental](https://img.shields.io/badge/stability-experimental-orange.svg)

![afro logo](logo/afro.png)

afro can parse APFS images. It not only extracts the latest data but also older versions of the files.

## Installation

    git clone https://github.com/cugu/afro
    cd afro
    python3 setup.py install

## Usage

### Export partition

AFRO only works on partitions, you can extract a partition using mmcat from the [sleuthkit](https://github.com/sleuthkit/sleuthkit).

    mmcat apfs_image.dmg 4 > apfs_partition.dd

### Export files

All files of an apfs image can be extracted using the following command:

    afro -e files parse apfs_partition.dd

The exported files are saved in a folder named after the image with the suffix '.extracted'. Because APFS images can contain multiple volumes, each volume is extracted into a separate folder inside the '.extracted' folder. Each volume can contain multiple versions of the file system which are stored in separate numbered folders. Inside those folders two folders exists 'private-dir' and 'root'. Those folders are not visible to the user, but exist on every APFS file system.

Example:

    imagename.extracted
    ├─ volume1               <- First volume
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

    afro -e bodyfile -e files  parse apfs_partition.dd

More information on the body file format can be found in the [sleuthkit wiki](https://wiki.sleuthkit.org/index.php?title=Body_file). The body file can be further investigated using [mactime](https://wiki.sleuthkit.org/index.php?title=Mactime) and [Timeline Explorer](https://ericzimmerman.github.io/).


## Documentation on APFS

 - [**Decoding the APFS file system**](http://www.sciencedirect.com/science/article/pii/S1742287617301408): Paper by Kurt H.Hansen and Fergus Toolan Fergus in _Digital Investigation_. Published: 2017-09-22.
 - [**Apple File System Guide**](https://developer.apple.com/library/content/documentation/FileManagement/Conceptual/APFS_Guide/Introduction/Introduction.html): Official documentation on APFS. Lacks lots of information on APFS. Last update: 2017-09-21.
 - [**APFS filesystem format**](https://blog.cugu.eu/post/apfs/): Deprecated blog post by myself. Still contains some useful diagrams. Last update: 2017-04-30.
 - Information about the checksum calculation can be found in [checksum.md](docs/checksum.md).


## Contributing
Pull requests and issues are welcome!

## Licenses
The afro software is licensed as [GPLv3](licences/gpl-3.0.txt).
The ksy file (libapfs/apfs.ksy) is licensed under [MIT license](licences/mit.txt).

