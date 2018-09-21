"""
Usage: afro image

Options:
        --help          Print usage
    -o, --offset        Offset into image file (in sectors)
    -l, --log LEVEL     Loglevel
    -b, --blocksize     Set blocksize (default: Read from first block or 4096)


"""

import io
import argparse
import logging

from kaitaistruct import KaitaiStream, BytesIO

from . import item_store, log, parse, carve, process

LOGO = """      `-+yhddhy+-`
    .sNMMMMMMMMMMms.
   +NMMMMMMMMMMMMMMN+
  +MMMMMMMMMMMMMMMMMM+
 .mMMMMMMNmhhmNMMMMMMd.
 .NMMMMN+`    `+NMMMMm.
 `hMMMN:        :NMMMh
  .mMMm.        .mMMm.
   .yNMy`      `sMNy.
     .odds/::/shdh-
        `.::::.`.sh/
                  .so"""

class OffsetBufferedReader(io.BufferedReader):
    """docstring for OffsetBytesIO"""

    def __init__(self, raw, offset):
        super().__init__(raw)
        self.offset = offset
        self.seek(0)

    def seek(self, offset, whence=0):
        if whence == 0:
            super().seek(self.offset + offset, whence)
        else:
            super().seek(offset, whence)


def extract(args):
    """ open image and extract information """

    if args.log:
        numeric_level = getattr(logging, args.log.upper(), None)
        if not isinstance(numeric_level, int):
            raise ValueError('Invalid log level: %s' % args.log)

        log.set_logging(args.log)

    export = args.export
    if not export:
        export = ['bodyfile']

    with open(args.image, 'rb') as image_io:
        image_io = OffsetBufferedReader(image_io, args.offset * 512)

        file_entries = []
        apfs = libapfs.Apfs(KaitaiStream(image_io))
        block_size = apfs.block_size
        image_io.seek(0)

        if args.method == 'parse':
            file_entries = parse.parse(image_io, args.image)
        elif args.method == 'carve':
            if args.carver == 'nxsb':
                file_entries = carve.nxsb(image_io, block_size, args.image)
            elif args.carver == 'apsb':
                file_entries = carve.apsb(image_io, block_size, args.image)
            elif args.carver == 'nodes':
                file_entries = carve.nodes(image_io, block_size, args.image)
            else:
                print('Carving method unknown')
                sys.exit(1)
        else:
            print('Extraction method unknown')
            sys.exit(2)


        method = 'parse'
        if args.method == 'carve':
            method = 'carve_%s' % args.carver

            # process file entries
        item_store = process.process_file_entries(
            file_entries,
            apfs,
            block_size,
            image_io,
            args.image,
            method
        )

        if 'bodyfile' in export:
            item_store.save_bodyfile("%s.%s.bodyfile" % (args.image, method))
        if 'gtf' in export:
            item_store.save_gtf("%s.%s.gtf" % (args.image, method))
        if 'files' in export:
            item_store.save_files("%s.%s.extracted" % (args.image, method), block_size, image_io)

def main():
    """ Parse arguments and execure correct extraction method """
    parser = argparse.ArgumentParser(description='Recover files from an APFS image')
    parser.add_argument('-o', '--offset', type=int, default=0, help='offset to file system')
    parser.add_argument('-l', '--log', default='INFO', help='set log level')
    parser.add_argument('-e', '--export', action='append', default=['bodyfile', 'gtf', 'files'], choices=['bodyfile', 'gtf', 'files'], help='set outputs')
    parser.add_argument('-m', '--method', default="carve", choices=['parse', 'carve'], help='set extraction method')
    parser.add_argument('-c', '--carver', default="apsb", choices=['nxsb', 'apsb', 'nodes'], help='set carving method')


    parser.add_argument('image', help='path to the image')
    args = parser.parse_args()
    extract(args)


if __name__ == '__main__':
    print(LOGO)
    main()
