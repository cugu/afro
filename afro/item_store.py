import csv
import copy
import os
import logging
import posixpath

from . import block

LOGGER = logging.getLogger(__name__)

class ItemStore:
    def __init__(self):
        self.items = []
        self.seen = set()

    def reset(self):
        self.items = []
        self.seen = set()

    def add_item(self, item_type, xid, parent_id, item_id, status, volume, path, name, accesstime, modificationtime, creationtime, size, md5, extents=[]):
        if status == "exists" and (name is None or name == ""):
            print("name not found (%d, %d, %d)" % (xid, parent_id, item_id))
        new_item = {
            'id': item_id,
            'xid': xid,
            'parent_id': parent_id,
            'name': name,
            'atime': accesstime,
            'mtime': modificationtime,
            'crtime': creationtime,
            'size': size,
            'md5': md5,
            'type': item_type,
            'volume': volume,
            'path': path,
            'status': status,
            'extents': extents
        }
        if tuple(new_item) not in self.seen:
            self.items.append(new_item)
            hitem = copy.deepcopy(new_item)
            del hitem['extents'] # TODO list is not hashable
            self.seen.add(tuple(hitem.items()))

    def save_files(self, name, blocksize, image_file_io):
        # add suffix if file exists
        basename = name
        i = 0
        while os.path.exists(name):
            name = basename + "_%d" % i
            i += 1

        os.mkdir(name)

        for item in self.items:
            full_path = os.path.join(name, str(item['volume']), str(item['xid']), str(item['path'][1:]))
            if full_path:
                os.makedirs(full_path, exist_ok=True)
            file_path = os.path.join(full_path, item['name'])
            if item['type'] == 'folder':
                os.makedirs(file_path, exist_ok=True)
            else:
                with open(file_path, 'bw+') as file_io:
                    remaining = (item['size'] or 0)
                    for extent in item['extents']:
                        for b in range(int(extent['length'] / blocksize)):
                            data = block.get_block(extent['start'] + b, blocksize, image_file_io)
                            if remaining < blocksize:
                                chunk_size = remaining
                            else:
                                chunk_size = blocksize
                            remaining -= chunk_size
                            file_io.write(data[:chunk_size])


    def save_bodyfile(self, name):
        # add suffix if file exists
        basename = name
        i = 0
        while os.path.exists(name):
            name = basename + "_%d" % i
            i += 1

        with open(name, 'w+') as csvfile:
            fieldnames = [
                'md5', 'name', 'id', 'mode', 'uid', 'gid',
                'size', 'atime', 'mtime', 'ctime', 'crtime',
            ]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter='|', extrasaction='ignore')
            writer.writeheader()
            for item in self.items:
                item = copy.deepcopy(item)
                xid = item['xid'] if item['xid'] is not None else 0
                item['id'] = "%s-%s-%s" % (0, xid, item['id']) # TODO: add volume number
                item['name'] = posixpath.join(item['path'], item['name'])
                item['mode'] = 'f' if item['type'] == 'file' else 'd'
                item['uid'] = 0
                item['gid'] = 0
                item['ctime'] = 0
                writer.writerow(item)

    def save_gtf(self, name):
        basename = name
        i = 0
        while os.path.exists(name):
            name = basename + "_%d" % i
            i += 1

        with open(name, 'w+') as csvfile:
            fieldnames = [
                'type', 'xid', 'parent_id', 'id', 'status', 'volume',
                'path', 'name', 'atime', 'mtime', 'crtime', 'size', 'md5'
            ]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames, extrasaction='ignore')
            writer.writeheader()
            writer.writerows(self.items)
