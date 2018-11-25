""" low level api methods to apfs """


def get_nxsb_objects(nxsb):
    """ get entries of the container superblock """

    # get omap in container superblock
    object_map = nxsb.body.nx_omap_oid.target
    if object_map.hdr.o_type == 2 or object_map.hdr.o_type == 3:
        object_map_root = object_map
    else:
        object_map_root = object_map.body.om_tree_oid.target

    # iterate omap
    return object_map_root.body.btn_data


def get_apsb_objects(apsb):
    """ get entries of the volume superblock """

    object_map = apsb.body.apfs_omap_oid.target
    if object_map.hdr.o_type == 2 or object_map.hdr.o_type == 3:
        object_map_root = object_map
    else:
        object_map_root = object_map.body.om_tree_oid.target

    # iterate omap
    return object_map_root.body.btn_data
