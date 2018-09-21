# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

from pkg_resources import parse_version
from kaitaistruct import __version__ as ks_version, KaitaiStruct, KaitaiStream, BytesIO
from enum import Enum


if parse_version(ks_version) < parse_version('0.7'):
    raise Exception("Incompatible Kaitai Struct Python API: 0.7 or later is required, but you have %s" % (ks_version))

class Apfs(KaitaiStruct):
    """https://developer.apple.com/support/apple-file-system/apple-file-system-reference.pdf."""

    class Features(Enum):
        case_insensitive = 1
        case_sensitive = 8

    class InoExtType(Enum):
        ino_ext_type_snap_xid = 1
        ino_ext_type_delta_tree_oid = 2
        ino_ext_type_document_id = 3
        ino_ext_type_name = 4
        ino_ext_type_prev_fsize = 5
        ino_ext_type_reserved_6 = 6
        ino_ext_type_finder_info = 7
        ino_ext_type_dstream = 8
        ino_ext_type_reserved_9 = 9
        ino_ext_type_dir_stats_key = 10
        ino_ext_type_fs_uuid = 11
        ino_ext_type_reserved_12 = 12
        ino_ext_type_sparse_bytes = 13
        ino_ext_type_rdev = 14

    class ObjectType(Enum):
        object_type_invalid = 0
        object_type_nx_superblock = 1
        object_type_btree = 2
        object_type_btree_node = 3
        object_type_spaceman = 5
        object_type_spaceman_cab = 6
        object_type_spaceman_cib = 7
        object_type_spaceman_bitmap = 8
        object_type_spaceman_free_queue = 9
        object_type_extent_list_tree = 10
        object_type_omap = 11
        object_type_checkpoint_map = 12
        object_type_fs = 13
        object_type_fstree = 14
        object_type_blockreftree = 15
        object_type_snapmetatree = 16
        object_type_nx_reaper = 17
        object_type_nx_reap_list = 18
        object_type_omap_snapshot = 19
        object_type_efi_jumpstart = 20
        object_type_fusion_middle_tree = 21
        object_type_nx_fusion_wbc = 22
        object_type_nx_fusion_wbc_list = 23
        object_type_er_state = 24
        object_type_gbitmap = 25
        object_type_gbitmap_tree = 26
        object_type_gbitmap_block = 27
        object_type_test = 255

    class TreeType(Enum):
        om_tree = 0
        fs_tree = 1

    class JObjTypes(Enum):
        apfs_type_any = 0
        apfs_type_snap_metadata = 1
        apfs_type_extent = 2
        apfs_type_inode = 3
        apfs_type_xattr = 4
        apfs_type_sibling_link = 5
        apfs_type_dstream_id = 6
        apfs_type_crypto_state = 7
        apfs_type_file_extent = 8
        apfs_type_dir_rec = 9
        apfs_type_dir_stats = 10
        apfs_type_snap_name = 11
        apfs_type_sibling_map = 12

    class JXattrFlags(Enum):
        xattr_data_embedded = 2
        symlink = 6

    class CheckpointMapFlags(Enum):
        checkpoint_map_last = 1

    class ItemType(Enum):
        named_pipe = 1
        character_special = 2
        directory = 4
        block_special = 6
        regular = 8
        symbolic_link = 10
        socket = 12
        whiteout = 14

    class ObjectTypeFlags(Enum):
        obj_virtual = 0
        obj_nonpersistent = 134217728
        obj_encrypted = 268435456
        obj_noheader = 536870912
        obj_physical = 1073741824
        obj_ephemeral = 2147483648
    def __init__(self, _io, _parent=None, _root=None):
        self._io = _io
        self._parent = _parent
        self._root = _root if _root else self
        self._read()

    def _read(self):
        self._raw_block0 = self._io.read_bytes(4096)
        io = KaitaiStream(BytesIO(self._raw_block0))
        self.block0 = self._root.Obj(io, self, self._root)

    class JSiblingValT(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.parent_id = self._io.read_u8le()
            self.name_len = self._io.read_u2le()
            self.name = (self._io.read_bytes(self.name_len)).decode(u"utf-8")


    class JInodeValT(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.parent_id = self._io.read_u8le()
            self.private_id = self._io.read_u8le()
            self.create_time = self._io.read_u8le()
            self.mod_time = self._io.read_u8le()
            self.change_time = self._io.read_u8le()
            self.access_time = self._io.read_u8le()
            self.internal_flags = self._io.read_u8le()
            self.nchildren_or_nlink = self._io.read_u4le()
            self.default_protection_class = self._io.read_u4le()
            self.write_generation_counter = self._io.read_u4le()
            self.bsd_flags = self._io.read_u4le()
            self.owner = self._io.read_u4le()
            self.group = self._io.read_u4le()
            self.mode = self._io.read_u2le()
            self.pad1 = self._io.read_u2le()
            self.pad2 = self._io.read_u8le()
            self.xfields = self._root.XfBlobT(self._io, self, self._root)


    class JKeyT(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.obj_id_and_type_low = self._io.read_u4le()
            self.obj_id_and_type_high = self._io.read_u4le()

        @property
        def obj_id(self):
            if hasattr(self, '_m_obj_id'):
                return self._m_obj_id if hasattr(self, '_m_obj_id') else None

            self._m_obj_id = (self.obj_id_and_type_low + ((self.obj_id_and_type_high & 268435455) << 32))
            return self._m_obj_id if hasattr(self, '_m_obj_id') else None

        @property
        def obj_type(self):
            if hasattr(self, '_m_obj_type'):
                return self._m_obj_type if hasattr(self, '_m_obj_type') else None

            self._m_obj_type = self._root.JObjTypes((self.obj_id_and_type_high >> 28))
            return self._m_obj_type if hasattr(self, '_m_obj_type') else None


    class XfDeviceNode(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.major_minor = self._io.read_u4le()

        @property
        def major(self):
            if hasattr(self, '_m_major'):
                return self._m_major if hasattr(self, '_m_major') else None

            self._m_major = (self.major_minor >> 24)
            return self._m_major if hasattr(self, '_m_major') else None

        @property
        def minor(self):
            if hasattr(self, '_m_minor'):
                return self._m_minor if hasattr(self, '_m_minor') else None

            self._m_minor = (self.major_minor & 16777215)
            return self._m_minor if hasattr(self, '_m_minor') else None


    class PointerValT(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.pointer = self._io.read_u8le()


    class JXattrKeyT(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.name_len = self._io.read_u1()
            self.name = (KaitaiStream.bytes_terminate(self._io.read_bytes(self.name_len), 0, False)).decode(u"utf-8")


    class CheckpointMappingT(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.cpm_type = self._root.ObjectType(self._io.read_u2le())
            self.cpm_flags = self._io.read_u2le()
            self.cpm_subtype = self._root.ObjectType(self._io.read_u4le())
            self.cpm_size = self._io.read_u4le()
            self.cpm_pad = self._io.read_u4le()
            self.cpm_fs_oid = self._io.read_u8le()
            self.cpm_oid = self._io.read_u8le()
            self.cpm_paddr = self._root.OidT(self._io, self, self._root)


    class NodeEntry(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.key_offset = self._io.read_s2le()
            if (self._parent.btn_flags & 4) == 0:
                self.key_length = self._io.read_u2le()

            self.data_offset = self._io.read_s2le()
            if (self._parent.btn_flags & 4) == 0:
                self.data_length = self._io.read_u2le()


        @property
        def j_key_t(self):
            if hasattr(self, '_m_j_key_t'):
                return self._m_j_key_t if hasattr(self, '_m_j_key_t') else None

            _pos = self._io.pos()
            self._io.seek(((self.key_offset + self._parent.btn_table_space.len) + 56))
            self._m_j_key_t = self._root.JKeyT(self._io, self, self._root)
            self._io.seek(_pos)
            return self._m_j_key_t if hasattr(self, '_m_j_key_t') else None

        @property
        def key(self):
            if hasattr(self, '_m_key'):
                return self._m_key if hasattr(self, '_m_key') else None

            _pos = self._io.pos()
            self._io.seek((((self.key_offset + self._parent.btn_table_space.len) + 56) + 8))
            _on = self.j_key_t.obj_type
            if _on == self._root.JObjTypes.apfs_type_inode:
                self._m_key = self._root.JEmptyKeyT(self._io, self, self._root)
            elif _on == self._root.JObjTypes.apfs_type_sibling_map:
                self._m_key = self._root.JEmptyKeyT(self._io, self, self._root)
            elif _on == self._root.JObjTypes.apfs_type_extent:
                self._m_key = self._root.JEmptyKeyT(self._io, self, self._root)
            elif _on == self._root.JObjTypes.apfs_type_any:
                self._m_key = self._root.OmapKeyT(self._io, self, self._root)
            elif _on == self._root.JObjTypes.apfs_type_dstream_id:
                self._m_key = self._root.JEmptyKeyT(self._io, self, self._root)
            elif _on == self._root.JObjTypes.apfs_type_xattr:
                self._m_key = self._root.JXattrKeyT(self._io, self, self._root)
            elif _on == self._root.JObjTypes.apfs_type_sibling_link:
                self._m_key = self._root.JSiblingKeyT(self._io, self, self._root)
            elif _on == self._root.JObjTypes.apfs_type_file_extent:
                self._m_key = self._root.JExtentKeyT(self._io, self, self._root)
            elif _on == self._root.JObjTypes.apfs_type_dir_rec:
                self._m_key = self._root.JDrecKeyT(self._io, self, self._root)
            self._io.seek(_pos)
            return self._m_key if hasattr(self, '_m_key') else None

        @property
        def val(self):
            if hasattr(self, '_m_val'):
                return self._m_val if hasattr(self, '_m_val') else None

            _pos = self._io.pos()
            self._io.seek(((self._root.block_size - self.data_offset) - (40 * (self._parent.btn_flags & 1))))
            _on = (256 if self._parent.btn_level > 0 else self.j_key_t.obj_type.value)
            if _on == self._root.JObjTypes.apfs_type_any.value:
                self._m_val = self._root.OmapValT(self._io, self, self._root)
            elif _on == self._root.JObjTypes.apfs_type_extent.value:
                self._m_val = self._root.JPhysExtValT(self._io, self, self._root)
            elif _on == self._root.JObjTypes.apfs_type_dstream_id.value:
                self._m_val = self._root.JExtentRefcountValT(self._io, self, self._root)
            elif _on == self._root.JObjTypes.apfs_type_inode.value:
                self._m_val = self._root.JInodeValT(self._io, self, self._root)
            elif _on == self._root.JObjTypes.apfs_type_sibling_link.value:
                self._m_val = self._root.JSiblingValT(self._io, self, self._root)
            elif _on == self._root.JObjTypes.apfs_type_xattr.value:
                self._m_val = self._root.JXattrValT(self._io, self, self._root)
            elif _on == self._root.JObjTypes.apfs_type_sibling_map.value:
                self._m_val = self._root.JSiblingMapValT(self._io, self, self._root)
            elif _on == self._root.JObjTypes.apfs_type_file_extent.value:
                self._m_val = self._root.JExtentValT(self._io, self, self._root)
            elif _on == self._root.JObjTypes.apfs_type_dir_rec.value:
                self._m_val = self._root.JDrecValT(self._io, self, self._root)
            elif _on == 256:
                self._m_val = self._root.PointerValT(self._io, self, self._root)
            self._io.seek(_pos)
            return self._m_val if hasattr(self, '_m_val') else None


    class OmapValT(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.ov_flags = self._io.read_u4le()
            self.ov_size = self._io.read_u4le()
            self.ov_paddr = self._root.PaddrT(self._io, self, self._root)


    class XfSize(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.size = self._io.read_u8le()
            self.stored_size = self._io.read_u8le()
            self.unknown_16 = self._io.read_u8le()
            self.unknown_size = self._io.read_u8le()
            self.unknown_32 = self._io.read_u8le()


    class CheckpointMapPhysT(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.cpm_flags = self._root.CheckpointMapFlags(self._io.read_u4le())
            self.cpm_count = self._io.read_u4le()
            self.cpm_map = [None] * (self.cpm_count)
            for i in range(self.cpm_count):
                self.cpm_map[i] = self._root.CheckpointMappingT(self._io, self, self._root)



    class HistoryValT(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.unknown_0 = self._io.read_u4le()
            self.unknown_4 = self._io.read_u4le()


    class ChunkInfoBlock(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.cib_index = self._io.read_u4le()
            self.cib_chunk_info_count = self._io.read_u4le()
            self.cib_chunk_info = [None] * (self.cib_chunk_info_count)
            for i in range(self.cib_chunk_info_count):
                self.cib_chunk_info[i] = self._root.ChunkInfoT(self._io, self, self._root)



    class Nloc(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.false = self._io.read_u2le()
            self.len = self._io.read_u2le()


    class ApfsModifiedByT(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.id = self._io.read_bytes(32)
            self.timestamp = self._io.read_u8le()
            self.last_xid = self._root.XidT(self._io, self, self._root)


    class XfName(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.name = (self._io.read_bytes_term(0, False, True, True)).decode(u"utf-8")


    class JDrecKeyT(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.name_len = self._io.read_u1()
            self.hash = self._io.read_bytes(3)
            self.name = (KaitaiStream.bytes_terminate(self._io.read_bytes(self.name_len), 0, False)).decode(u"utf-8")


    class BtreeNodePhysT(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.btn_flags = self._io.read_u2le()
            self.btn_level = self._io.read_u2le()
            self.btn_nkeys = self._io.read_u4le()
            self.btn_table_space = self._root.Nloc(self._io, self, self._root)
            self.btn_free_space = self._root.Nloc(self._io, self, self._root)
            self.btn_key_free_list = self._root.Nloc(self._io, self, self._root)
            self.btn_val_free_list = self._root.Nloc(self._io, self, self._root)
            self.btn_data = [None] * (self.btn_nkeys)
            for i in range(self.btn_nkeys):
                self.btn_data[i] = self._root.NodeEntry(self._io, self, self._root)



    class JExtentRefcountValT(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.count = self._io.read_u4le()


    class HistoryKeyT(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.xid = self._io.read_u8le()
            self.obj_id = self._root.OidT(self._io, self, self._root)


    class JDrecValT(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.file_id = self._io.read_u8le()
            self.date_added = self._io.read_u8le()
            self.flags = self._root.XfBlobT(self._io, self, self._root)


    class Obj(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.hdr = self._root.ObjPhys(self._io, self, self._root)
            _on = self.hdr.o_type
            if _on == self._root.ObjectType.object_type_btree:
                self.body = self._root.BtreeNodePhysT(self._io, self, self._root)
            elif _on == self._root.ObjectType.object_type_checkpoint_map:
                self.body = self._root.CheckpointMapPhysT(self._io, self, self._root)
            elif _on == self._root.ObjectType.object_type_fs:
                self.body = self._root.ApfsSuperblockT(self._io, self, self._root)
            elif _on == self._root.ObjectType.object_type_btree_node:
                self.body = self._root.BtreeNodePhysT(self._io, self, self._root)
            elif _on == self._root.ObjectType.object_type_spaceman:
                self.body = self._root.ChunkInfoBlock(self._io, self, self._root)
            elif _on == self._root.ObjectType.object_type_nx_superblock:
                self.body = self._root.NxSuperblockT(self._io, self, self._root)
            elif _on == self._root.ObjectType.object_type_spaceman_cib:
                self.body = self._root.ChunkInfoT(self._io, self, self._root)
            elif _on == self._root.ObjectType.object_type_omap:
                self.body = self._root.OmapPhysT(self._io, self, self._root)


    class JPhysExtValT(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.block_count = self._io.read_u4le()
            self.unknown_4 = self._io.read_u2le()
            self.block_size = self._io.read_u2le()
            self.inode = self._io.read_u8le()
            self.unknown_16 = self._io.read_u4le()


    class ObjPhys(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.o_cksum = self._io.read_u8le()
            self.o_oid = self._root.OidT(self._io, self, self._root)
            self.o_xid = self._root.XidT(self._io, self, self._root)
            self.o_type = self._root.ObjectType(self._io.read_u2le())
            self.o_flags = self._io.read_u2le()
            self.o_subtype = self._root.ObjectType(self._io.read_u4le())


    class ChunkInfoT(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.ci_xid = self._io.read_u8le()
            self.ci_addr = self._io.read_u8le()
            self.ci_block_count = self._io.read_u4le()
            self.ci_free_count = self._io.read_u4le()
            self.ci_bitmap_addr = self._io.read_u8le()


    class SpaceManager(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.block_size = self._io.read_u4le()
            self.blocks_per_chunk = self._io.read_u4le()
            self.chunks_per_cib = self._io.read_u4le()
            self.cibs_per_cab = self._io.read_u4le()
            self.block_count = self._io.read_u4le()
            self.chunk_count = self._io.read_u4le()
            self.cib_count = self._io.read_u4le()
            self.cab_count = self._io.read_u4le()
            self.entry_count = self._io.read_u4le()
            self.unknown_68 = self._io.read_u4le()
            self.free_block_count = self._io.read_u8le()
            self.entries_offset = self._io.read_u4le()
            self.unknown_84 = self._io.read_bytes(92)
            self.prev_spaceman_internal_pool_block = self._io.read_u8le()

        @property
        def spaceman_internal_pool_blocks(self):
            if hasattr(self, '_m_spaceman_internal_pool_blocks'):
                return self._m_spaceman_internal_pool_blocks if hasattr(self, '_m_spaceman_internal_pool_blocks') else None

            _pos = self._io.pos()
            self._io.seek(self.entries_offset)
            self._m_spaceman_internal_pool_blocks = [None] * (self.entry_count)
            for i in range(self.entry_count):
                self._m_spaceman_internal_pool_blocks[i] = self._io.read_u8le()

            self._io.seek(_pos)
            return self._m_spaceman_internal_pool_blocks if hasattr(self, '_m_spaceman_internal_pool_blocks') else None


    class XFieldT(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.x_type = self._root.InoExtType(self._io.read_u1())
            self.x_flags = self._io.read_u1()
            self.x_size = self._io.read_u2le()


    class ApfsSuperblockT(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.apfs_magic = self._io.read_bytes(4)
            self.apfs_fs_index = self._io.read_u4le()
            self.apfs_features = self._io.read_u8le()
            self.apfs_readonly_compatible_features = self._io.read_u8le()
            self.apfs_incompatible_features = self._io.read_u8le()
            self.apfs_unmount_time = self._io.read_u8le()
            self.apfs_fs_reserve_block_count = self._io.read_u8le()
            self.apfs_fs_quota_block_count = self._io.read_u8le()
            self.apfs_fs_alloc_count = self._io.read_u8le()
            self.apfs_meta_crypto = self._io.read_bytes(32)
            self.apfs_omap_oid = self._root.OidT(self._io, self, self._root)
            self.apfs_root_tree_oid = self._root.OidT(self._io, self, self._root)
            self.apfs_extentref_tree_oid = self._root.OidT(self._io, self, self._root)
            self.apfs_snap_meta_tree_oid = self._root.OidT(self._io, self, self._root)
            self.apfs_revert_to_xid = self._root.XidT(self._io, self, self._root)
            self.apfs_revert_to_sblock_oid = self._root.OidT(self._io, self, self._root)
            self.apfs_next_obj_id = self._io.read_u8le()
            self.apfs_num_files = self._io.read_u8le()
            self.apfs_num_directories = self._io.read_u8le()
            self.apfs_num_symlinks = self._io.read_u8le()
            self.apfs_num_other_fsobjects = self._io.read_u8le()
            self.apfs_num_snapshots = self._io.read_u8le()
            self.apfs_total_blocks_alloced = self._io.read_u8le()
            self.apfs_total_blocks_freed = self._io.read_u8le()
            self.apfs_vol_uuid = self._io.read_bytes(16)
            self.apfs_last_mod_time = self._io.read_u8le()
            self.apfs_fs_flags = self._io.read_u8le()
            self.apfs_formatted_by = self._root.ApfsModifiedByT(self._io, self, self._root)
            self.apfs_modified_by = [None] * (8)
            for i in range(8):
                self.apfs_modified_by[i] = self._root.ApfsModifiedByT(self._io, self, self._root)

            self.apfs_volname = (KaitaiStream.bytes_terminate(self._io.read_bytes(256), 0, False)).decode(u"utf-8")
            self.apfs_next_doc_id = self._io.read_u4le()
            self.apfs_role = self._io.read_u2le()
            self.reserved = self._io.read_u2le()
            self.apfs_root_to_xid = self._root.XidT(self._io, self, self._root)
            self.apfs_er_state_oid = self._root.OidT(self._io, self, self._root)


    class PaddrT(KaitaiStruct):
        """universal type to address a block: it both parses one u8-sized
        block address and provides a lazy instance to parse that block
        right away.
        """
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.val = self._io.read_u8le()

        @property
        def target(self):
            if hasattr(self, '_m_target'):
                return self._m_target if hasattr(self, '_m_target') else None

            io = self._root._io
            _pos = io.pos()
            io.seek((self.val * self._root.block_size))
            self._raw__m_target = io.read_bytes(self._root.block_size)
            io = KaitaiStream(BytesIO(self._raw__m_target))
            self._m_target = self._root.Obj(io, self, self._root)
            io.seek(_pos)
            return self._m_target if hasattr(self, '_m_target') else None


    class OmapPhysT(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.om_flags = self._io.read_u4le()
            self.om_snap_count = self._io.read_u4le()
            self.om_tree_type = self._io.read_u4le()
            self.om_snapshot_tree_type = self._io.read_u4le()
            self.om_tree_oid = self._root.OidT(self._io, self, self._root)
            self.om_snapshot_tree_oid = self._root.OidT(self._io, self, self._root)
            self.om_most_recent_snap = self._root.XidT(self._io, self, self._root)
            self.om_pending_revert_min = self._root.XidT(self._io, self, self._root)
            self.om_pending_revert_max = self._root.XidT(self._io, self, self._root)


    class JSiblingMapValT(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.file_id = self._io.read_u8le()


    class JSiblingKeyT(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.sibling_id = self._io.read_u8le()


    class XfDocumentId(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.id = self._io.read_u4le()


    class JExtentValT(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.len = self._io.read_u8le()
            self.phys_block_num = self._io.read_u8le()
            self.flags = self._io.read_u8le()


    class NxSuperblockT(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.nx_magic = self._io.read_bytes(4)
            self.nx_block_size = self._io.read_u4le()
            self.nx_block_count = self._io.read_u8le()
            self.nx_features = self._io.read_u8le()
            self.nx_readonly_compatible_features = self._io.read_u8le()
            self.nx_incompatible_features = self._io.read_u8le()
            self.nx_uuid = self._io.read_bytes(16)
            self.nx_next_oid = self._root.OidT(self._io, self, self._root)
            self.nx_next_xid = self._root.XidT(self._io, self, self._root)
            self.nx_xp_desc_blocks = self._io.read_u4le()
            self.nx_xp_data_blocks = self._io.read_u4le()
            self.nx_xp_desc_base = self._io.read_u8le()
            self.nx_xp_data_base = self._io.read_u8le()
            self.nx_xp_desc_next = self._io.read_u4le()
            self.nx_xp_data_next = self._io.read_u4le()
            self.nx_xp_desc_index = self._io.read_u4le()
            self.nx_xp_desc_len = self._io.read_u4le()
            self.nx_xp_data_index = self._io.read_u4le()
            self.nx_xp_data_len = self._io.read_u4le()
            self.nx_spaceman_oid = self._root.OidT(self._io, self, self._root)
            self.nx_omap_oid = self._root.OidT(self._io, self, self._root)
            self.nx_reaper_oid = self._root.OidT(self._io, self, self._root)
            self.nx_test_type = self._io.read_u4le()
            self.nx_max_file_systems = self._io.read_u4le()
            self.nx_fs_oids = [None] * (self.nx_max_file_systems)
            for i in range(self.nx_max_file_systems):
                self.nx_fs_oids[i] = self._root.OidT(self._io, self, self._root)

            self.nx_counters = [None] * (32)
            for i in range(32):
                self.nx_counters[i] = self._io.read_u8le()

            self.nx_blocked_out_prange = self._root.PrangeT(self._io, self, self._root)
            self.nx_evict_mapping_tree_oid = self._root.OidT(self._io, self, self._root)
            self.nx_flags = self._io.read_u8le()
            self.nx_efi_jumpstart = self._io.read_u8le()
            self.nx_fusion_uuid = self._io.read_bytes(16)
            self.nx_keylocker = self._root.PrangeT(self._io, self, self._root)
            self.nx_ephemeral_info = [None] * (4)
            for i in range(4):
                self.nx_ephemeral_info[i] = self._io.read_u8le()

            self.nx_test_oid = self._root.OidT(self._io, self, self._root)
            self.nx_fusion_mt_oid = self._root.OidT(self._io, self, self._root)
            self.nx_fusion_wbc_oid = self._root.OidT(self._io, self, self._root)
            self.nx_fusion_wbc = self._root.PrangeT(self._io, self, self._root)

        @property
        def checkpoint_offset(self):
            if hasattr(self, '_m_checkpoint_offset'):
                return self._m_checkpoint_offset if hasattr(self, '_m_checkpoint_offset') else None

            _pos = self._io.pos()
            self._io.seek(((self.nx_xp_desc_base + self.nx_xp_desc_index) * self._root.block_size))
            self._m_checkpoint_offset = self._root.Obj(self._io, self, self._root)
            self._io.seek(_pos)
            return self._m_checkpoint_offset if hasattr(self, '_m_checkpoint_offset') else None

        @property
        def spaceman_offset(self):
            if hasattr(self, '_m_spaceman_offset'):
                return self._m_spaceman_offset if hasattr(self, '_m_spaceman_offset') else None

            _pos = self._io.pos()
            self._io.seek(((self.nx_xp_data_base + self.nx_xp_data_index) * self._root.block_size))
            self._m_spaceman_offset = self._root.Obj(self._io, self, self._root)
            self._io.seek(_pos)
            return self._m_spaceman_offset if hasattr(self, '_m_spaceman_offset') else None


    class XfSparseSize(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.size = self._io.read_u8le()


    class OmapKeyT(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.ok_oid = self._root.OidT(self._io, self, self._root)
            self.ok_xid = self._root.XidT(self._io, self, self._root)


    class XfBlobT(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.xf_num_exts = self._io.read_u2le()
            self.xf_used_data = self._io.read_u2le()
            self.xf_data = [None] * (self.xf_num_exts)
            for i in range(self.xf_num_exts):
                self.xf_data[i] = self._root.XFieldT(self._io, self, self._root)

            self._raw_xf = [None] * (self.xf_num_exts)
            self.xf = [None] * (self.xf_num_exts)
            for i in range(self.xf_num_exts):
                _on = self.xf_data[i].x_type
                if _on == self._root.InoExtType.ino_ext_type_rdev:
                    self._raw_xf[i] = self._io.read_bytes((self.xf_data[i].x_size + ((8 - self.xf_data[i].x_size) % 8)))
                    io = KaitaiStream(BytesIO(self._raw_xf[i]))
                    self.xf[i] = self._root.XfDeviceNode(io, self, self._root)
                elif _on == self._root.InoExtType.ino_ext_type_sparse_bytes:
                    self._raw_xf[i] = self._io.read_bytes((self.xf_data[i].x_size + ((8 - self.xf_data[i].x_size) % 8)))
                    io = KaitaiStream(BytesIO(self._raw_xf[i]))
                    self.xf[i] = self._root.XfSparseSize(io, self, self._root)
                elif _on == self._root.InoExtType.ino_ext_type_name:
                    self._raw_xf[i] = self._io.read_bytes((self.xf_data[i].x_size + ((8 - self.xf_data[i].x_size) % 8)))
                    io = KaitaiStream(BytesIO(self._raw_xf[i]))
                    self.xf[i] = self._root.XfName(io, self, self._root)
                elif _on == self._root.InoExtType.ino_ext_type_document_id:
                    self._raw_xf[i] = self._io.read_bytes((self.xf_data[i].x_size + ((8 - self.xf_data[i].x_size) % 8)))
                    io = KaitaiStream(BytesIO(self._raw_xf[i]))
                    self.xf[i] = self._root.XfDocumentId(io, self, self._root)
                elif _on == self._root.InoExtType.ino_ext_type_prev_fsize:
                    self._raw_xf[i] = self._io.read_bytes((self.xf_data[i].x_size + ((8 - self.xf_data[i].x_size) % 8)))
                    io = KaitaiStream(BytesIO(self._raw_xf[i]))
                    self.xf[i] = self._root.XfSize(io, self, self._root)
                else:
                    self.xf[i] = self._io.read_bytes((self.xf_data[i].x_size + ((8 - self.xf_data[i].x_size) % 8)))



    class OidT(KaitaiStruct):
        """similar to paddr_t."""
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.val = self._io.read_u8le()

        @property
        def target(self):
            if hasattr(self, '_m_target'):
                return self._m_target if hasattr(self, '_m_target') else None

            io = self._root._io
            _pos = io.pos()
            io.seek((self.val * self._root.block_size))
            self._raw__m_target = io.read_bytes(self._root.block_size)
            io = KaitaiStream(BytesIO(self._raw__m_target))
            self._m_target = self._root.Obj(io, self, self._root)
            io.seek(_pos)
            return self._m_target if hasattr(self, '_m_target') else None


    class PrangeT(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.pr_start_paddr = self._io.read_u8le()
            self.pr_block_count = self._io.read_u8le()


    class JExtentKeyT(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.offset = self._io.read_u8le()


    class JXattrValT(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.flags = self._root.JXattrFlags(self._io.read_u2le())
            self.xdata_length = self._io.read_u2le()
            _on = self.flags
            if _on == self._root.JXattrFlags.symlink:
                self.xdata = (KaitaiStream.bytes_terminate(self._io.read_bytes(self.xdata_length), 0, False)).decode(u"utf-8")
            else:
                self.xdata = self._io.read_bytes(self.xdata_length)


    class XidT(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.val = self._io.read_u8le()


    class JEmptyKeyT(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            pass


    @property
    def block_size(self):
        if hasattr(self, '_m_block_size'):
            return self._m_block_size if hasattr(self, '_m_block_size') else None

        self._m_block_size = self._root.block0.body.nx_block_size
        return self._m_block_size if hasattr(self, '_m_block_size') else None


