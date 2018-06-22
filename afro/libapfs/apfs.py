# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

from pkg_resources import parse_version
from kaitaistruct import __version__ as ks_version, KaitaiStruct, KaitaiStream, BytesIO
from enum import Enum


if parse_version(ks_version) < parse_version('0.7'):
    raise Exception("Incompatible Kaitai Struct Python API: 0.7 or later is required, but you have %s" % (ks_version))

class Apfs(KaitaiStruct):

    class Features(Enum):
        case_insensitive = 1
        case_sensitive = 8

    class EaType(Enum):
        generic = 2
        symlink = 6

    class TreeType(Enum):
        om_tree = 0
        fs_tree = 1

    class ObjSubtype(Enum):
        empty = 0
        history = 9
        omap = 11
        files = 14
        extents = 15
        unknown = 16

    class XfieldType(Enum):
        name = 516
        size = 8200
        device_node = 8718
        sparse_size = 10253

    class Kind(Enum):
        omap = 0
        lookup = 2
        inode = 3
        xattr = 4
        sibling = 5
        extent_refcount = 6
        extent = 8
        drec = 9
        sibling_map = 12

    class ObjType(Enum):
        container_superblock = 1
        rootnode = 2
        node = 3
        space_manager = 5
        spaceman_internal_pool = 7
        btree = 11
        checkpoint = 12
        volume_superblock = 13
        reaper = 17
        unknown = 32

    class ItemType(Enum):
        named_pipe = 1
        character_special = 2
        directory = 4
        block_special = 6
        regular = 8
        symbolic_link = 10
        socket = 12
        whiteout = 14
    def __init__(self, _io, _parent=None, _root=None):
        self._io = _io
        self._parent = _parent
        self._root = _root if _root else self
        self._read()

    def _read(self):
        self._raw_block0 = self._io.read_bytes(4096)
        io = KaitaiStream(BytesIO(self._raw_block0))
        self.block0 = self._root.Obj(io, self, self._root)

    class ExtentKey(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.offset = self._io.read_u8le()


    class SpacemanInternalPool(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.unknown_32 = self._io.read_bytes(4)
            self.entry_count = self._io.read_u4le()
            self.entries = [None] * (self.entry_count)
            for i in range(self.entry_count):
                self.entries[i] = self._root.SpacemanInternalPoolEntry(self._io, self, self._root)



    class XfHeader(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.type = self._root.XfieldType(self._io.read_u2le())
            self.length = self._io.read_u2le()


    class InodeVal(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.parent_id = self._io.read_u8le()
            self.extents_id = self._io.read_u8le()
            self.creation_timestamp = self._io.read_u8le()
            self.modified_timestamp = self._io.read_u8le()
            self.changed_timestamp = self._io.read_u8le()
            self.accessed_timestamp = self._io.read_u8le()
            self.flags = self._io.read_u8le()
            self.nchildren_or_nlink = self._io.read_u4le()
            self.unknown_60 = self._io.read_u4le()
            self.unknown_64 = self._io.read_u4le()
            self.bsdflags = self._io.read_u4le()
            self.owner_id = self._io.read_u4le()
            self.group_id = self._io.read_u4le()
            self.mode = self._io.read_u2le()
            self.unknown_82 = self._io.read_u2le()
            self.unknown_84 = self._io.read_u4le()
            self.unknown_88 = self._io.read_u4le()
            self.xf_num_exts = self._io.read_u2le()
            self.xf_used_data = self._io.read_u2le()
            self.xf_header = [None] * (self.xf_num_exts)
            for i in range(self.xf_num_exts):
                self.xf_header[i] = self._root.XfHeader(self._io, self, self._root)

            self._raw_xf = [None] * (self.xf_num_exts)
            self.xf = [None] * (self.xf_num_exts)
            for i in range(self.xf_num_exts):
                _on = self.xf_header[i].type
                if _on == self._root.XfieldType.size:
                    self._raw_xf[i] = self._io.read_bytes((self.xf_header[i].length + ((8 - self.xf_header[i].length) % 8)))
                    io = KaitaiStream(BytesIO(self._raw_xf[i]))
                    self.xf[i] = self._root.XfSize(io, self, self._root)
                elif _on == self._root.XfieldType.device_node:
                    self._raw_xf[i] = self._io.read_bytes((self.xf_header[i].length + ((8 - self.xf_header[i].length) % 8)))
                    io = KaitaiStream(BytesIO(self._raw_xf[i]))
                    self.xf[i] = self._root.XfDeviceNode(io, self, self._root)
                elif _on == self._root.XfieldType.name:
                    self._raw_xf[i] = self._io.read_bytes((self.xf_header[i].length + ((8 - self.xf_header[i].length) % 8)))
                    io = KaitaiStream(BytesIO(self._raw_xf[i]))
                    self.xf[i] = self._root.XfName(io, self, self._root)
                elif _on == self._root.XfieldType.sparse_size:
                    self._raw_xf[i] = self._io.read_bytes((self.xf_header[i].length + ((8 - self.xf_header[i].length) % 8)))
                    io = KaitaiStream(BytesIO(self._raw_xf[i]))
                    self.xf[i] = self._root.XfSparseSize(io, self, self._root)
                else:
                    self.xf[i] = self._io.read_bytes((self.xf_header[i].length + ((8 - self.xf_header[i].length) % 8)))



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


    class NodeEntry(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.key_offset = self._io.read_s2le()
            if (self._parent.node_type & 4) == 0:
                self.key_length = self._io.read_u2le()

            self.data_offset = self._io.read_s2le()
            if (self._parent.node_type & 4) == 0:
                self.data_length = self._io.read_u2le()


        @property
        def key_hdr(self):
            if hasattr(self, '_m_key_hdr'):
                return self._m_key_hdr if hasattr(self, '_m_key_hdr') else None

            _pos = self._io.pos()
            self._io.seek(((self.key_offset + self._parent.keys_offset) + 56))
            self._m_key_hdr = self._root.KeyHdr(self._io, self, self._root)
            self._io.seek(_pos)
            return self._m_key_hdr if hasattr(self, '_m_key_hdr') else None

        @property
        def key(self):
            if hasattr(self, '_m_key'):
                return self._m_key if hasattr(self, '_m_key') else None

            _pos = self._io.pos()
            self._io.seek((((self.key_offset + self._parent.keys_offset) + 56) + 8))
            _on = self.key_hdr.kind
            if _on == self._root.Kind.lookup:
                self._m_key = self._root.LookupKey(self._io, self, self._root)
            elif _on == self._root.Kind.omap:
                self._m_key = self._root.OmapKey(self._io, self, self._root)
            elif _on == self._root.Kind.extent_refcount:
                self._m_key = self._root.EmptyKey(self._io, self, self._root)
            elif _on == self._root.Kind.xattr:
                self._m_key = self._root.DrecKey(self._io, self, self._root)
            elif _on == self._root.Kind.sibling:
                self._m_key = self._root.SiblingKey(self._io, self, self._root)
            elif _on == self._root.Kind.sibling_map:
                self._m_key = self._root.EmptyKey(self._io, self, self._root)
            elif _on == self._root.Kind.extent:
                self._m_key = self._root.ExtentKey(self._io, self, self._root)
            elif _on == self._root.Kind.inode:
                self._m_key = self._root.EmptyKey(self._io, self, self._root)
            elif _on == self._root.Kind.drec:
                self._m_key = self._root.DrecKey(self._io, self, self._root)
            self._io.seek(_pos)
            return self._m_key if hasattr(self, '_m_key') else None

        @property
        def val(self):
            if hasattr(self, '_m_val'):
                return self._m_val if hasattr(self, '_m_val') else None

            _pos = self._io.pos()
            self._io.seek(((self._root.block_size - self.data_offset) - (40 * (self._parent.node_type & 1))))
            _on = (256 if self._parent.level > 0 else self.key_hdr.kind.value)
            if _on == self._root.Kind.sibling.value:
                self._m_val = self._root.SiblingVal(self._io, self, self._root)
            elif _on == self._root.Kind.inode.value:
                self._m_val = self._root.InodeVal(self._io, self, self._root)
            elif _on == self._root.Kind.extent.value:
                self._m_val = self._root.ExtentVal(self._io, self, self._root)
            elif _on == self._root.Kind.lookup.value:
                self._m_val = self._root.LookupVal(self._io, self, self._root)
            elif _on == self._root.Kind.xattr.value:
                self._m_val = self._root.XattrVal(self._io, self, self._root)
            elif _on == self._root.Kind.extent_refcount.value:
                self._m_val = self._root.ExtentRefcountVal(self._io, self, self._root)
            elif _on == self._root.Kind.drec.value:
                self._m_val = self._root.DrecVal(self._io, self, self._root)
            elif _on == 256:
                self._m_val = self._root.PointerVal(self._io, self, self._root)
            elif _on == self._root.Kind.sibling_map.value:
                self._m_val = self._root.SiblingMapVal(self._io, self, self._root)
            elif _on == self._root.Kind.omap.value:
                self._m_val = self._root.OmapVal(self._io, self, self._root)
            self._io.seek(_pos)
            return self._m_val if hasattr(self, '_m_val') else None


    class XattrVal(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.ea_type = self._root.EaType(self._io.read_u2le())
            self.data_length = self._io.read_u2le()
            _on = self.ea_type
            if _on == self._root.EaType.symlink:
                self.data = (KaitaiStream.bytes_terminate(self._io.read_bytes(self.data_length), 0, False)).decode(u"UTF-8")
            else:
                self.data = self._io.read_bytes(self.data_length)


    class DrecVal(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.node_id = self._io.read_u8le()
            self.timestamp = self._io.read_u8le()
            self.item_length = self._root.ItemType(self._io.read_u2le())


    class SpacemanInternalPoolEntry(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.xid = self._io.read_u8le()
            self.unknown_8 = self._io.read_u4le()
            self.unknown_12 = self._io.read_u4le()
            self.block_count = self._io.read_u4le()
            self.free_block_count = self._io.read_u4le()
            self.bitmap_block = self._io.read_u8le()


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


    class ContainerSuperblock(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.magic = self._io.ensure_fixed_contents(b"\x4E\x58\x53\x42")
            self.block_size = self._io.read_u4le()
            self.block_count = self._io.read_u8le()
            self.features = self._io.read_u8le()
            self.read_only_compatible_features = self._io.read_u8le()
            self.incompatible_features = self._io.read_u8le()
            self.uuid = self._io.read_bytes(16)
            self.next_oid = self._io.read_u8le()
            self.next_xid = self._io.read_u8le()
            self.xp_desc_blocks = self._io.read_u4le()
            self.xp_data_blocks = self._io.read_u4le()
            self.xp_desc_base = self._io.read_u8le()
            self.xp_data_base = self._io.read_u8le()
            self.xp_desc_len = self._io.read_u4le()
            self.xp_data_len = self._io.read_u4le()
            self.xp_desc_index = self._io.read_u4le()
            self.xp_desc_index_len = self._io.read_u4le()
            self.xp_data_index = self._io.read_u4le()
            self.xp_data_index_len = self._io.read_u4le()
            self.spaceman_oid = self._io.read_u8le()
            self.omap_oid = self._root.RefObj(self._io, self, self._root)
            self.reaper_oid = self._io.read_u8le()
            self.pad2 = self._io.read_u4le()
            self.max_file_systems = self._io.read_u4le()
            self.fs_oids = [None] * (self.max_file_systems)
            for i in range(self.max_file_systems):
                self.fs_oids[i] = self._io.read_u8le()


        @property
        def checkpoint_offset(self):
            if hasattr(self, '_m_checkpoint_offset'):
                return self._m_checkpoint_offset if hasattr(self, '_m_checkpoint_offset') else None

            _pos = self._io.pos()
            self._io.seek(((self.xp_desc_base + self.xp_desc_index) * self._root.block_size))
            self._m_checkpoint_offset = self._root.Obj(self._io, self, self._root)
            self._io.seek(_pos)
            return self._m_checkpoint_offset if hasattr(self, '_m_checkpoint_offset') else None

        @property
        def spaceman_offset(self):
            if hasattr(self, '_m_spaceman_offset'):
                return self._m_spaceman_offset if hasattr(self, '_m_spaceman_offset') else None

            _pos = self._io.pos()
            self._io.seek(((self.xp_data_base + self.xp_data_index) * self._root.block_size))
            self._m_spaceman_offset = self._root.Obj(self._io, self, self._root)
            self._io.seek(_pos)
            return self._m_spaceman_offset if hasattr(self, '_m_spaceman_offset') else None


    class RefObj(KaitaiStruct):
        """Universal type to address a block: it both parses one u8-sized
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


    class LookupKey(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.offset = self._root.RefObj(self._io, self, self._root)


    class OmapVal(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.block_start = self._io.read_u4le()
            self.block_length = self._io.read_u4le()
            self.obj_id = self._root.RefObj(self._io, self, self._root)


    class XfName(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.name = (self._io.read_bytes_term(0, False, True, True)).decode(u"UTF-8")


    class VolumeSuperblock(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.magic = self._io.ensure_fixed_contents(b"\x41\x50\x53\x42")
            self.fs_index = self._io.read_u4le()
            self.unknown_40 = self._io.read_bytes(16)
            self.features = self._root.Features(self._io.read_u4le())
            self.unknown_60 = self._io.read_bytes(12)
            self.fs_reserve_block_count = self._io.read_u8le()
            self.fs_quota_block_count = self._io.read_u8le()
            self.fs_alloc_count = self._io.read_u8le()
            self.unknown_92 = self._io.read_bytes(32)
            self.omap_oid = self._root.RefObj(self._io, self, self._root)
            self.root_tree_oid = self._io.read_u8le()
            self.extentref_tree_oid = self._root.RefObj(self._io, self, self._root)
            self.snap_meta_tree_oid = self._root.RefObj(self._io, self, self._root)
            self.unknown_160 = self._io.read_bytes(16)
            self.next_doc_id = self._io.read_u8le()
            self.num_files = self._io.read_u8le()
            self.num_directories = self._io.read_u8le()
            self.num_symlinks = self._io.read_u8le()
            self.num_other_fsobjects = self._io.read_u8le()
            self.num_snapshots = self._io.read_u8le()
            self.unknown_1601 = self._io.read_bytes(16)
            self.vol_uuid = self._io.read_bytes(16)
            self.last_mod_time = self._io.read_u8le()
            self.formatted_by_last_xid = self._io.read_u8le()
            self.formatted_by_id = (KaitaiStream.bytes_terminate(self._io.read_bytes(32), 0, False)).decode(u"UTF-8")
            self.formatted_by_timestamp = self._io.read_u8le()
            self.modified_by_last_xid = self._io.read_u8le()
            self.modified_by_id = (KaitaiStream.bytes_terminate(self._io.read_bytes(32), 0, False)).decode(u"UTF-8")
            self.modified_by_timestamp = self._io.read_u8le()
            self.rest = self._io.read_bytes(344)
            self.volname = (self._io.read_bytes_term(0, False, True, True)).decode(u"UTF-8")


    class SiblingVal(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.node_id = self._io.read_u8le()
            self.length = self._io.read_u2le()
            self.name = (self._io.read_bytes(self.length)).decode(u"UTF-8")


    class CheckpointEntry(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.type = self._root.ObjType(self._io.read_u2le())
            self.flags = self._io.read_u2le()
            self.subtype = self._root.ObjSubtype(self._io.read_u4le())
            self.size = self._io.read_u4le()
            self.unknown_52 = self._io.read_u4le()
            self.unknown_56 = self._io.read_u4le()
            self.unknown_60 = self._io.read_u4le()
            self.oid = self._io.read_u8le()
            self.object = self._root.RefObj(self._io, self, self._root)


    class Obj(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.hdr = self._root.ObjHeader(self._io, self, self._root)
            _on = self.hdr.type
            if _on == self._root.ObjType.container_superblock:
                self.body = self._root.ContainerSuperblock(self._io, self, self._root)
            elif _on == self._root.ObjType.spaceman_internal_pool:
                self.body = self._root.SpacemanInternalPool(self._io, self, self._root)
            elif _on == self._root.ObjType.space_manager:
                self.body = self._root.SpaceManager(self._io, self, self._root)
            elif _on == self._root.ObjType.rootnode:
                self.body = self._root.Node(self._io, self, self._root)
            elif _on == self._root.ObjType.node:
                self.body = self._root.Node(self._io, self, self._root)
            elif _on == self._root.ObjType.checkpoint:
                self.body = self._root.Checkpoint(self._io, self, self._root)
            elif _on == self._root.ObjType.btree:
                self.body = self._root.Btree(self._io, self, self._root)
            elif _on == self._root.ObjType.volume_superblock:
                self.body = self._root.VolumeSuperblock(self._io, self, self._root)


    class KeyHdr(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.key_low = self._io.read_u4le()
            self.key_high = self._io.read_u4le()

        @property
        def obj_id(self):
            if hasattr(self, '_m_obj_id'):
                return self._m_obj_id if hasattr(self, '_m_obj_id') else None

            self._m_obj_id = (self.key_low + ((self.key_high & 268435455) << 32))
            return self._m_obj_id if hasattr(self, '_m_obj_id') else None

        @property
        def kind(self):
            if hasattr(self, '_m_kind'):
                return self._m_kind if hasattr(self, '_m_kind') else None

            self._m_kind = self._root.Kind((self.key_high >> 28))
            return self._m_kind if hasattr(self, '_m_kind') else None


    class SiblingKey(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.object = self._io.read_u8le()


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


    class ObjHeader(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.cksum = self._io.read_u8le()
            self.oid = self._io.read_u8le()
            self.xid = self._io.read_u8le()
            self.type = self._root.ObjType(self._io.read_u2le())
            self.flags = self._io.read_u2le()
            self.subtype = self._root.ObjSubtype(self._io.read_u2le())
            self.pad = self._io.read_u2le()


    class OmapKey(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.xid = self._io.read_u8le()
            self.oid = self._io.read_u8le()


    class Checkpoint(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.unknown_0 = self._io.read_u4le()
            self.entry_count = self._io.read_u4le()
            self.entries = [None] * (self.entry_count)
            for i in range(self.entry_count):
                self.entries[i] = self._root.CheckpointEntry(self._io, self, self._root)



    class XfSparseSize(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.size = self._io.read_u8le()


    class PointerVal(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.pointer = self._io.read_u8le()


    class Btree(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.btree_type = self._root.TreeType(self._io.read_u8le())
            self.unknown_0 = self._io.read_bytes(8)
            self.root = self._root.RefObj(self._io, self, self._root)


    class HistoryVal(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.unknown_0 = self._io.read_u4le()
            self.unknown_4 = self._io.read_u4le()


    class Node(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.node_type = self._io.read_u2le()
            self.level = self._io.read_u2le()
            self.entry_count = self._io.read_u4le()
            self.unknown_40 = self._io.read_u2le()
            self.keys_offset = self._io.read_u2le()
            self.keys_length = self._io.read_u2le()
            self.data_offset = self._io.read_u2le()
            self.unknown_48 = self._io.read_u8le()
            self.entries = [None] * (self.entry_count)
            for i in range(self.entry_count):
                self.entries[i] = self._root.NodeEntry(self._io, self, self._root)



    class LookupVal(KaitaiStruct):
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


    class ExtentRefcountVal(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.count = self._io.read_u4le()


    class SiblingMapVal(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.map_node_id = self._io.read_u8le()


    class ExtentVal(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.len = self._io.read_u8le()
            self.phys_block_num = self._root.RefObj(self._io, self, self._root)
            self.flags = self._io.read_u8le()


    class EmptyKey(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            pass


    class HistoryKey(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.xid = self._io.read_u8le()
            self.obj_id = self._root.RefObj(self._io, self, self._root)


    class DrecKey(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.name_length = self._io.read_u1()
            self.flag_1 = self._io.read_u1()
            self.unknown_2 = self._io.read_u2le()
            self.name = (KaitaiStream.bytes_terminate(self._io.read_bytes(self.name_length), 0, False)).decode(u"UTF-8")


    @property
    def block_size(self):
        if hasattr(self, '_m_block_size'):
            return self._m_block_size if hasattr(self, '_m_block_size') else None

        self._m_block_size = self._root.block0.body.block_size
        return self._m_block_size if hasattr(self, '_m_block_size') else None


