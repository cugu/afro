""" Multiple output functions """
import hashlib
import logging
import posixpath

from . import libapfs
from . import item_store, block


LOGGER = logging.getLogger(__name__)


def get_path(itemmap, fid):
    if fid in itemmap:
        name = itemmap[fid].name or '?'
        parent_path = get_path(itemmap, itemmap[fid].parent) if itemmap[fid].parent > 1 else ''
        return parent_path + '/' + name
    return '?'

def process_extent(extent, remaining, blocksize, file_io, md5):
    for b in range(int(extent['length'] / blocksize)):
        data = block.get_block(extent['start'] + b, blocksize, file_io)
        if remaining < blocksize:
            chunk_size = remaining
        else:
            chunk_size = blocksize
        remaining -= chunk_size
        md5.update(data[:chunk_size])
    return {'md5': md5, 'remaining': remaining}

class Item:

    def __init__(self):
        self.parent = None
        self.node_id = None
        self.extent_id = None
        self.name = None
        self.creationtime = None
        self.accesstime = None
        self.modificationtime = None
        self.file_size = None
        self.type = None

def process_file_entries(file_entries, apfs, blocksize, file_io, image_name, name):
    """ Print file entries as table """

    extentmap = dict()
    itemmap = dict()

    for xid in file_entries:

        extentmap[xid] = dict()
        itemmap[xid] = dict()

        for volume in file_entries[xid]:

            extentmap[xid][volume] = dict()
            itemmap[xid][volume] = dict()

            for file_entry in file_entries[xid][volume]:
                try:
                    if file_entry.key_hdr.kind == apfs.Kind.extent and \
                            isinstance(file_entry.val, libapfs.apfs.Apfs.ExtentVal):

                        extentmap[xid][volume].setdefault(file_entry.key_hdr.obj_id, list())
                        extentmap[xid][volume][file_entry.key_hdr.obj_id].append({
                            'start': file_entry.val.phys_block_num.val,
                            'length': file_entry.val.len,
                            'offset': file_entry.key.offset
                        })

                    elif file_entry.key_hdr.kind == apfs.Kind.inode and \
                            isinstance(file_entry.val, libapfs.apfs.Apfs.InodeVal):

                        item = Item()
                        for index, xf_h in enumerate(file_entry.val.xf_header):
                            if xf_h.type == apfs.XfieldType.name:
                                item.name = file_entry.val.xf[index].name
                            elif xf_h.type == apfs.XfieldType.size:
                                item.file_size = file_entry.val.xf[index].size
                        if item.name is None:
                            raise Exception("name not found")
                        item.node_id = file_entry.key_hdr.obj_id
                        item.parent = file_entry.val.parent_id
                        item.extent_id = file_entry.val.extents_id
                        item.creationtime = file_entry.val.changed_timestamp
                        item.accesstime = file_entry.val.accessed_timestamp
                        item.modificationtime = file_entry.val.modified_timestamp
                        if file_entry.val.xf_num_exts == 1:
                            item.type = 'folder'
                        else:
                            item.type = 'file'

                        itemmap[xid][volume][file_entry.key_hdr.obj_id] = item

                except Exception as ex:
                    LOGGER.error("File entry %s %s parsing failed %s", file_entry.key_hdr.obj_id, file_entry.key_hdr.kind, ex)

    store = item_store.ItemStore()
    for xid in file_entries:

        for volume in file_entries[xid]:

            for item in sorted(itemmap[xid][volume].values(), key=lambda item: item.parent):

                # path on image
                path = get_path(itemmap[xid][volume], item.node_id)

                extents = []

                if item.type == 'file':
                    md5 = hashlib.md5()
                    remaining = (item.file_size or 0)

                    extents = sorted(
                        extentmap[xid][volume].get(item.extent_id, []),
                        key=lambda extent: extent['offset']
                    )

                    for extent in extents:
                        intermediate = process_extent(extent, remaining, blocksize, file_io, md5)
                        md5 = intermediate['md5']
                        remaining = intermediate['remaining']

                store.add_item(
                    item.type,
                    xid, item.parent, item.node_id,
                    'exists',
                    volume, posixpath.dirname(path), item.name,
                    (item.accesstime or 0) / 1000000000,
                    (item.modificationtime or 0) / 1000000000,
                    (item.creationtime or 0) / 1000000000,
                    (item.file_size or 0), md5.hexdigest() if extents else '0',
                    extents
                )

    return store
