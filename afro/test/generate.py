import collections
import logging
import os
import subprocess
import sys
import traceback

from tabulate import tabulate

import actions
from afro import log

ACTION_COUNT = 1000

LOGGER = logging.getLogger(__name__)


def create_volume(disk, volume_name):
    run([
        "diskutil", "apfs",
        "addVolume", disk,
        "APFS", volume_name
    ])

def detach(diskname):
    # unmount image
    run(["hdiutil", "detach", diskname])

def attach(imagepath):
    # mount image
    out = run(["hdiutil", "attach", imagepath])
    return parse_diskname(out)

def parse_diskname(out):
    diskline = list(filter(lambda l: b'EF57347C' in l, out.split(b'\n')))[0]
    diskname = diskline.split()[0]
    LOGGER.debug(out.decode("utf-8"))
    LOGGER.info(diskname)
    return diskname

def run(args):
    LOGGER.debug(args)
    process = subprocess.Popen(
        args,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE)
    out, err = process.communicate()
    if err:
        LOGGER.error(err)
        sys.exit(1)
    return out

def create_image(directory, size, action_count, volume_count):
    image_name = "image_%s_%s" % (size, volume_count)
    image_path = os.path.join(directory, image_name)

    # create image directory
    os.makedirs(directory, exist_ok=True)

    # remove exisiting image
    if os.path.exists(image_path + ".dmg"):
        LOGGER.warning("Remove %s.dmg", image_path)
        os.remove(image_path + ".dmg")

    # create image
    run([
        "hdiutil", "create",
        "-size", size,
        "-fs", "APFS",
        "-volname", image_name + "_0",
        os.path.join(directory, image_name)
    ])
    diskname = attach(image_path + '.dmg')

    # add volumes
    volumes = [image_name + '_0']
    for i in range(1, volume_count):
        volume_name = image_name + "_%d" % i
        create_volume(diskname, volume_name)
        volumes.append(volume_name)

    # create virtual file system
    factor = 1
    if 'M' in size:
        factor = pow(1024, 2)
    elif 'G' in size:
        factor = pow(1024, 3)
    bytesize = int(size.replace('M', '').replace('G', '')) * factor
    vfs = actions.VirtualFileSystem(
        image='%s.dmg' %
        image_name,
        mount_point='/Volumes/',
        volumes=volumes,
        size=bytesize)

    # perform actions
    successfull_actions = 0
    while successfull_actions < action_count:
        if vfs.random_action():
            successfull_actions += 1
        if successfull_actions % 100 == 0:
            detach(diskname)
            diskname = attach(image_path + ".dmg")
            #for volume in volumes:
            #     _sync_directory(os.path.join('/Volumes', volume))
    detach(diskname)

    # log actions
    with open(os.path.join(directory, "%s.generation.log" % image_name), 'w+') as actions_io:
        actions_io.write("Image: %s\n" % image_name)
        actions_io.write("Actions: \n")
        actions_io.write(tabulate(vfs.logs, headers="keys", floatfmt=".4f"))
        actions_io.write("\n")

        c = collections.Counter()
        for l in vfs.logs:
            c[l['command']] += 1
        actions_io.write(tabulate(c.items()))
        actions_io.write("\n")

    # create GTF
    vfs.item_store.save_gtf(os.path.join(directory, "%s.generation.gtf" % image_name))


def main(path, images):
    # create image for every
    for image in images:
        size = image.split('_')[1]
        volume_count = int(image.split('_')[2])
        try:
            create_image(os.path.abspath(path), size, ACTION_COUNT, volume_count)
        except Exception as e:
            LOGGER.error(
                "Image creation failed %s\n%s" %
                (e, traceback.format_exc()))
            sys.exit(1)


if __name__ == '__main__':
    # setup logging
    log.set_logging(sys.argv[1])
    # start generation
    main(sys.argv[2], sys.argv[3:])
