import hashlib
import logging
import os
import random
import shutil
import subprocess
import traceback
import fcntl

from afro import item_store
import random_words

SRC_FILES = {
    "MISC": "data/edrm-data-set"
}

LOGGER = logging.getLogger(__name__)

SRC_DIRS = random_words.RANDOM_WORDS


def _proper_fsync(fd):
    # https://lists.apple.com/archives/darwin-dev/2005/Feb/msg00072.html
    # https://developer.apple.com/library/mac/documentation/Darwin/Reference/ManPages/man2/fsync.2.html
    # https://github.com/untitaker/python-atomicwrites/issues/6
    fcntl.fcntl(fd, fcntl.F_FULLFSYNC)

def _sync_directory(directory):
    # Ensure that filenames are written to disk
    fd = os.open(directory, os.O_RDONLY)
    try:
        _proper_fsync(fd)
    except Exception as e:
        raise e
    finally:
        os.close(fd)

def uniq_path(dst_abspath):
    # apply nummeric suffix if path exists
    if os.path.exists(dst_abspath):
        suffix = 0
        suf_path = "%s_%d" % (dst_abspath, suffix)
        while os.path.exists(suf_path):
            suffix += 1
            suf_path = "%s_%d" % (dst_abspath, suffix)
        dst_abspath = suf_path
    return dst_abspath


class VirtualFileSystem:

    def __init__(self, image, mount_point, volumes, size):
        self.mount_point = mount_point
        self.volumes = list(volumes)
        self.logs = []
        self.image = image
        self.size = size
        self.space_used = 0
        self.item_store = item_store.ItemStore()

        for volume in self.volumes:
            self.add(volume, '', '', 'folder')


    def item_abspath(self, item):
        return os.path.join(self.mount_point, item['volume'], item['path'], item['name'])

    def log(self, volume, command, abspath, item_type, comment=''):
        a_time = 0
        c_time = 0
        m_time = 0
        md5 = '-'
        size = 0

        if os.path.exists(abspath):
            a_time = os.stat(abspath).st_atime
            c_time = os.stat(abspath).st_ctime
            m_time = os.stat(abspath).st_mtime

            if item_type == 'file':
                md5 = hashlib.md5(open(abspath, 'rb').read()).hexdigest()
                size = os.path.getsize(abspath)

        self.logs.append({
            'volume': volume,
            'a_time': a_time,
            'm_time': m_time,
            'c_time': c_time,
            'image': self.image,
            'command': command,
            'comment': comment,
            'file': abspath,
            'md5': md5,
            'size': size,
            'type': item_type
        })

    def update_parent_folder(self, volume, path):
        self.change(volume, os.path.dirname(path), os.path.basename(path), 'content_changed')
        self.add(volume, os.path.dirname(path), os.path.basename(path), 'folder', False)
        if random.random() < 0.1:
            _sync_directory(os.path.join(self.mount_point, volume, path))

    def add(self, volume, path, name, item_type, update_parent=True):
        a_time = 0
        c_time = 0
        m_time = 0
        md5 = '-'
        size = 0
        item_id = 0

        dst_abspath = os.path.join(self.mount_point, volume, path, name)

        if os.path.exists(dst_abspath):
            a_time = os.stat(dst_abspath).st_atime
            c_time = os.stat(dst_abspath).st_ctime
            m_time = os.stat(dst_abspath).st_mtime
            item_id = os.stat(dst_abspath).st_ino

            if item_type == 'file':
                md5 = hashlib.md5(open(dst_abspath, 'rb').read()).hexdigest()
                size = os.path.getsize(dst_abspath)


        self.item_store.add_item(
            item_type,
            None, None, item_id, # TODO xid, parent_id, item_id
            'active',
            volume, path, name, # TODO volume, path, name
            a_time, m_time, c_time,
            size, md5
        )

        if update_parent:
            self.update_parent_folder(volume, path)

    def change(self, volume, path, name, status):
        for index, item in enumerate(self.item_store.items):
            if item['volume'] == volume and item['path'] == path and item['name'] == name:
                # dst_abspath = os.path.join(self.mount_point, volume, path, name)
                # if os.path.exists(dst_abspath):
                #     item['id'] = os.stat(dst_abspath).st_ino
                item['status'] = status
                self.item_store.items[index] = item

    def dst_directories(self, volume):
        return list(filter(
            lambda item: item['type'] == 'folder' and item['status'] == 'active' and item['volume'] == volume,
            self.item_store.items
        ))

    def dst_non_root_directories(self, volume):
        return list(filter(
            lambda item: item['name'] != '',
            self.dst_directories(volume)
        ))

    def dst_files(self, volume):
        return list(filter(
            lambda item: item['type'] == 'file' and item['status'] == 'active' and item['volume'] == volume,
            self.item_store.items
        ))

    def random_action(self):
        volume = random.choice(self.volumes)

        space_left = self.space_used < 0.8 * self.size
        files_exists = bool(self.dst_files(volume))
        multiple_directories_exist = bool(self.dst_non_root_directories(volume))

        # always available
        actions = [self.add_folder]

        if space_left:
            actions.append(self.add_file)

        if files_exists:
            actions.append(self.delete_file)

        if files_exists and space_left:
            actions.append(self.change_file)

        if files_exists and multiple_directories_exist:
            actions.append(self.move_file)
            actions.append(self.clone_file)

        if multiple_directories_exist:
            actions.append(self.delete_folder)
        #    actions.append(self.move_folder)

        action = random.choice(actions)
        try:
            action(volume)
            return True
        except OSError as oserror:
            if 'Directory not empty' in str(oserror):
                return False
            print("Error:%s\n%s" % (oserror, traceback.format_exc()))
            return False
        except Exception as e:
            print("Error:%s\n%s" % (e, traceback.format_exc()))
            return False

    def add_file(self, volume):
        LOGGER.debug('add_file')
        # files aus filepool platzieren
        src_dir = SRC_FILES[random.choice(list(SRC_FILES.keys()))]
        src_name = random.choice(os.listdir(src_dir))
        src_abspath = os.path.join(src_dir, src_name)

        dst_item = random.choice(self.dst_directories(volume))
        dst_abspath = os.path.join(self.item_abspath(dst_item), src_name)

        dst_abspath = uniq_path(dst_abspath)

        # create (copy) file
        with open(src_abspath, 'rb') as src_io:
            fd = os.open(dst_abspath, os.O_WRONLY | os.O_CREAT | os.O_EXCL)
            os.write(fd, src_io.read())
            os.close(fd)

        # adjust vfs
        self.add(volume, os.path.join(dst_item['path'], dst_item['name']), src_name, 'file')
        self.space_used += os.path.getsize(src_abspath)
        self.log(volume, "add_file", dst_abspath, 'file')

    def delete_file(self, volume):
        LOGGER.debug('delete_file')
        # select random file
        src_item = random.choice(self.dst_files(volume))
        src_abspath = self.item_abspath(src_item)

        # log first
        self.change(volume, src_item['path'], src_item['name'], "deleted")
        self.space_used -= os.path.getsize(src_abspath)
        self.log(volume, "delete_file", src_abspath, 'file')

        # remove file
        os.remove(src_abspath)

        self.update_parent_folder(volume, src_item['path'])

    def move_file(self, volume):
        LOGGER.debug('move_file')
        # select random file
        src_item = random.choice(self.dst_files(volume))
        src_abspath = self.item_abspath(src_item)

        # chose random dir to move to
        possible_dirs = list(filter(
            lambda d: os.path.join(d['path'], d['name']) != src_item['path'],
            self.dst_directories(volume)
        ))
        if not possible_dirs:
            raise Exception('File move not possible')
        dst_item = random.choice(possible_dirs)
        dst_abspath = os.path.join(self.item_abspath(dst_item), src_item['name'])

        self.change(volume, src_item['path'], src_item['name'], "moved")

        dst_abspath = uniq_path(dst_abspath)

        # move file
        os.rename(src_abspath, dst_abspath)

        self.update_parent_folder(volume, src_item['path'])
        self.add(volume, os.path.join(dst_item['path'], dst_item['name']), src_item['name'], "file")
        self.log(volume, "move_file", dst_abspath, 'file')

    def change_file(self, volume):
        LOGGER.debug('change_file')
        # select random file
        src_item = random.choice(self.dst_files(volume))
        src_abspath = self.item_abspath(src_item)

        # select random parameter
        size = os.path.getsize(src_abspath)
        change_offset = random.randint(1, size)
        change_count = random.randint(1, size + 10 * 4096)

        # change file
        file_descriptor = os.open(src_abspath, os.O_WRONLY)
        os.lseek(file_descriptor, change_offset, os.SEEK_SET)
        os.write(file_descriptor, change_count * b'A')
        os.close(file_descriptor)

        # log
        self.change(volume, src_item['path'], src_item['name'], "changed")
        self.add(volume, src_item['path'], src_item['name'], "file")
        self.log(volume, "change_file", src_abspath, 'file', "(%d:%d)" % (change_offset, change_count))

    def clone_file(self, volume):
        LOGGER.debug('clone_file')
        # select random file
        src_item = random.choice(self.dst_files(volume))
        src_abspath = self.item_abspath(src_item)

        # choose random dir to move to
        possible_dirs = list(filter(
            lambda d: os.path.join(d['path'], d['name']) != src_item['path'],
            self.dst_directories(volume)
        ))
        if not possible_dirs:
            raise Exception('File clone not possible')
        dst_item = random.choice(possible_dirs)
        dst_abspath = os.path.join(self.item_abspath(dst_item), src_item['name'])

        dst_abspath = uniq_path(dst_abspath)

        # clone file
        args = ["cp", "-c", src_abspath, dst_abspath]
        LOGGER.debug(args)
        process = subprocess.Popen(
            args,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)
        _, err = process.communicate()
        if err:
            raise Exception('Clone failed %s' % err)

        self.log(volume, "clone_file", dst_abspath, 'file')
        self.add(volume, os.path.join(dst_item['path'], dst_item['name']), src_item['name'], "file")

    def add_folder(self, volume):
        LOGGER.debug('add_folder')
        # choose location
        dst_item = random.choice(self.dst_directories(volume))
        dst_abspath = self.item_abspath(dst_item)
        dst_name = random.choice(SRC_DIRS)
        dst_path = os.path.join(dst_abspath, dst_name)

        dst_path = uniq_path(dst_path)

        # create path
        os.mkdir(dst_path)

        self.log(volume, "add_folder", dst_path, 'folder')
        self.add(volume, os.path.join(dst_item['path'], dst_item['name']), dst_name, "folder")

    def delete_folder(self, volume):
        LOGGER.debug('delete_folder')
        # select random folder
        src_item = random.choice(self.dst_non_root_directories(volume))
        src_abspath = self.item_abspath(src_item)

        # remove folder
        os.rmdir(src_abspath)  # TODO: fails often

        self.update_parent_folder(volume, src_item['path'])
        self.log(volume, "delete_folder", src_abspath, 'folder')
        self.change(volume, src_item['path'], src_item['name'], "deleted")


    '''
    def move_folder(self, volume):
        LOGGER.debug('move_folder')
        # select random file
        src = random.choice(self.dst_directories(volume))
        src_dir = os.path.join(src['path'], src['name'])
        src_name = os.path.basename(src_dir)
        src_parent_dir = os.path.dirname(src_dir)

        # chose random dir to move to
        dst_dir = random.choice(self.dst_directories(volume))
        while src_parent_dir == os.path.join(dst_dir['path'], dst_dir['name']) or \
            src_dir == os.path.join(dst_dir['path'], dst_dir['name']) or \
            src_dir in self.root_dirs:

            dst_dir = random.choice(self.dst_directories(volume))
        dst_path = os.path.join(dst_dir, src_name)

        self.change(volume, src_path, "moved")

        # move file
        os.rename(src_path, dst_path)

        self.log(volume, "move_folder", dst_path, 'folder')
        self.add(volume, dst_path, "folder")
    '''
