""" parse file system

Parse:
1. Parse container superblock.
    3. Parse OMAP.
    4. Iterate over volumes.
        5. Get volume superblocks from OMAP.
            6. Parse volume superblock.
                7. Parse OMAP.
                8. Go to root directory.
                    9. Parse Root directory. Parse required entries.
    10. Go to previous container superblock. Recurse 1.
"""
import logging

from kaitaistruct import KaitaiStream, BytesIO

from . import libapfs, block

LOGGER = logging.getLogger(__name__)


def add_file_entries(file_entries, new_file_entries, xid_override, volume_override=None):
    for xid in new_file_entries:
        file_entries.setdefault(xid_override, dict())
        for volume in new_file_entries[xid]:
            volume_override = volume_override or volume
            file_entries[xid_override].setdefault(volume_override, list())
            file_entries[xid_override][volume_override] += new_file_entries[xid][volume]
    return file_entries


def parse_node(node, _):
    # 'unknown' is the default volume name
    # node_type 1 contains only pointer records
    if node.body.btn_flags == 1:
        return {node.hdr.o_xid.val: {'unknown': []}}
    return {node.hdr.o_xid.val: {'unknown': node.body.btn_data}}


def parse_apsb(apsb, apfs):
    file_entries = dict()

    for omap_entry in libapfs.get_apsb_objects(apsb):
        # get root directory
        root_node = omap_entry.val.ov_paddr.target
        new_file_entries = parse_node(root_node, apfs)
        file_entries = add_file_entries(file_entries, new_file_entries, apsb.hdr.o_xid.val, apsb.body.apfs_volname)

    return file_entries


def parse_nxsb(nxsb, apfs):
    file_entries = dict()

    for fs_entry in libapfs.get_nxsb_objects(nxsb):
        # get volume superblock
        apsb = fs_entry.val.ov_paddr.target
        new_file_entries = parse_apsb(apsb, apfs)
        file_entries = add_file_entries(file_entries, new_file_entries, nxsb.hdr.o_xid.val)

    return file_entries


def parse(image_io):
    """ parse image and print files """

    # get file entries
    apfs = libapfs.Apfs(KaitaiStream(image_io))

    # get from container superblock
    nxsb = apfs.block0
    block_size = nxsb.body.nx_block_size
    file_entries = parse_nxsb(nxsb, apfs)
    prev_nxsb = nxsb.body.nx_xp_desc_base + nxsb.body.nx_xp_desc_index + 1
    count = nxsb.body.nx_xp_desc_len

    # get from older container superblocks
    for _ in range(count - 1):
        data = block.get_block(prev_nxsb, block_size, image_io)
        nxsb = apfs.Obj(KaitaiStream(BytesIO(data)), apfs, apfs)
        try:
            file_entries = {**file_entries, **parse_nxsb(nxsb, apfs)}
            prev_nxsb = nxsb.body.nx_xp_desc_base + nxsb.body.nx_xp_desc_index + 1
        except Exception:
            break

    return file_entries
