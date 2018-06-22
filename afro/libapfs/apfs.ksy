meta:
  id: apfs
  license: MIT
  encoding: UTF-8
  endian: le

seq:
#  - id: padding
#    size: offset
  - id: block0
    type: obj
    size: 4096
#  - id: blocks
#    type: obj
#    size: 4096
#    repeat: expr
#    repeat-expr: 400

instances:
  block_size:
    value: _root.block0.body.as<container_superblock>.block_size
#  random_block:
#    pos: 20213 * block_size   # enter block number here to jump directly that block in the WebIDE
#    type: obj           # opens a sub stream for making positioning inside the block work
#    size: block_size

types:

# block navigation

  ref_obj:
    doc: |
      Universal type to address a block: it both parses one u8-sized
      block address and provides a lazy instance to parse that block
      right away.
    seq:
      - id: val
        type: u8
    instances:
      target:
        io: _root._io
        pos: val * _root.block_size
        type: obj
        size: _root.block_size
    -webide-representation: 'Blk {val:dec}'

# meta structs

  obj_header:
    seq:
      - id: cksum
        type: u8
        doc: Flechters checksum, according to the docs.
      - id: oid
        type: u8
        doc: ID of the obj itself. Either the position of the obj or an incrementing number starting at 1024.
      - id: xid
        type: u8
        doc: Incrementing version number of the xid of the obj (highest == latest)
      - id: type
        type: u2
        enum: obj_type
      - id: flags
        type: u2
        doc: 0x4000 oid = position, 0x8000 = container
      - id: subtype
        type: u2
        enum: obj_subtype
      - id: pad
        type: u2

  obj:
    seq:
      - id: hdr
        type: obj_header
      - id: body
        #size-eos: true
        type:
          switch-on: hdr.type
          cases:
            obj_type::container_superblock: container_superblock
            obj_type::rootnode: node
            obj_type::node: node
            obj_type::space_manager: space_manager
            obj_type::spaceman_internal_pool: spaceman_internal_pool
            obj_type::btree: btree
            obj_type::checkpoint: checkpoint
            obj_type::volume_superblock: volume_superblock
    -webide-representation: '{hdr.type}'


# container_superblock (type: 0x01)

  container_superblock:
    seq:
      - id: magic
        size: 4
        contents: [NXSB]
      - id: block_size
        type: u4
      - id: block_count
        type: u8
      - id: features
        type: u8
      - id: read_only_compatible_features
        type: u8
      - id: incompatible_features
        type: u8
      - id: uuid
        size: 16
      - id: next_oid
        type: u8
      - id: next_xid
        type: u8
      - id: xp_desc_blocks
        type: u4
      - id: xp_data_blocks
        type: u4
      - id: xp_desc_base
        type: u8
      - id: xp_data_base
        type: u8
      - id: xp_desc_len
        type: u4
      - id: xp_data_len
        type: u4
      - id: xp_desc_index
        type: u4
      - id: xp_desc_index_len
        type: u4
      - id: xp_data_index
        type: u4
      - id: xp_data_index_len
        type: u4
      - id: spaceman_oid
        type: u8
      - id: omap_oid
        type: ref_obj
      - id: reaper_oid
        type: u8
      - id: pad2
        type: u4
      - id: max_file_systems
        type: u4
      - id: fs_oids
        type: u8
        repeat: expr
        repeat-expr: max_file_systems
    instances:
      checkpoint_offset:
        pos: (xp_desc_base + xp_desc_index) * _root.block_size
        type: obj
      spaceman_offset:
        pos: (xp_data_base + xp_data_index) * _root.block_size
        type: obj


# node (type: 0x02)

  node:
    seq:
      - id: node_type
        type: u2
      - id: level
        type: u2
        doc: Zero for leaf nodes, > 0 for index nodes
      - id: entry_count
        type: u4
      - id: unknown_40
        type: u2
      - id: keys_offset
        type: u2
      - id: keys_length
        type: u2
      - id: data_offset
        type: u2
      - id: unknown_48
        type: u8
      - id: entries
        type: node_entry
        repeat: expr
        repeat-expr: entry_count

## node entries

  node_entry:
    seq:
      - id: key_offset
        type: s2
      - id: key_length
        type: u2
        if: (_parent.node_type & 4) == 0
      - id: data_offset
        type: s2
      - id: data_length
        type: u2
        if: (_parent.node_type & 4) == 0
    instances:
      key_hdr:
        pos: key_offset + _parent.keys_offset + 56
        type: key_hdr
        -webide-parse-mode: eager
      key:
        pos: key_offset + _parent.keys_offset + 56 + 8
        type:
          switch-on: key_hdr.kind
          cases:
            kind::omap: omap_key
            kind::lookup: lookup_key
            kind::inode: empty_key
            kind::xattr: drec_key
            kind::sibling: sibling_key
            kind::extent_refcount: empty_key
            kind::extent: extent_key
            kind::drec: drec_key
            kind::sibling_map: empty_key
        -webide-parse-mode: eager
      val:
        pos: _root.block_size - data_offset - 40 * (_parent.node_type & 1)
        type:
          switch-on: '(_parent.level > 0) ? 256 : key_hdr.kind.to_i'
          cases:
            256: pointer_val # applies to all pointer vals, i.e. any entry val in index nodes
            kind::omap.to_i: omap_val
            kind::lookup.to_i: lookup_val
            kind::inode.to_i: inode_val
            kind::xattr.to_i: xattr_val
            kind::sibling.to_i: sibling_val
            kind::extent_refcount.to_i: extent_refcount_val
            kind::extent.to_i: extent_val
            kind::drec.to_i: drec_val
            kind::sibling_map.to_i: sibling_map_val
        -webide-parse-mode: eager
    -webide-representation: '{key_hdr} {key} -> {val}'

## node entry keys

  key_hdr:
    seq:
      - id: key_low # this is a work-around for JavaScript's inability to handle 64 bit vals
        type: u4
      - id: key_high
        type: u4
    instances:
      obj_id:
        value: key_low + ((key_high & 0x0FFFFFFF) << 32)
        -webide-parse-mode: eager
      kind:
        value: key_high >> 28
        enum: kind
        -webide-parse-mode: eager
    -webide-representation: '({kind}) #{obj_id:dec}'

  empty_key:
    -webide-representation: ''

  omap_key:
    seq:
      - id: xid
        type: u8
      - id: oid
        type: u8
    -webide-representation: 'ID {oid:dec} v{xid:dec}'

  history_key:
    seq:
      - id: xid
        type: u8
      - id: obj_id
        type: ref_obj
    -webide-representation: '{obj_id} v{xid:dec}'

  lookup_key:
    seq:
      - id: offset
        type: ref_obj
    -webide-representation: '{obj_id}'

  drec_key:
    seq:
      - id: name_length
        type: u1
      - id: flag_1
        type: u1
      - id: unknown_2
        type: u2
#        if: flag_1 != 0
      - id: name
        size: name_length
        type: strz
    -webide-representation: '"{name}"'

  sibling_key:
    seq:
      - id: object
        type: u8
    -webide-representation: '#{object:dec}'

  extent_key:
    seq:
      - id: offset # seek pos in file
        type: u8
    -webide-representation: '{offset:dec}'

## node entry vals

  pointer_val: # for any index nodes
    seq:
      - id: pointer
        type: u8
    -webide-representation: '-> {pointer:dec}'

  history_val: # ???
    seq:
      - id: unknown_0
        type: u4
      - id: unknown_4
        type: u4
    -webide-representation: '{unknown_0}, {unknown_4}'

  omap_val: # 0x00
    seq:
      - id: block_start
        type: u4
      - id: block_length
        type: u4
      - id: obj_id
        type: ref_obj
    -webide-representation: '{obj_id}, from {block_start:dec}, len {block_length:dec}'

  inode_val: # 0x30
    seq:
      - id: parent_id
        type: u8
      - id: extents_id
        type: u8
      - id: creation_timestamp
        type: u8
      - id: modified_timestamp
        type: u8
      - id: changed_timestamp
        type: u8
      - id: accessed_timestamp
        type: u8
      - id: flags
        type: u8
      - id: nchildren_or_nlink
        type: u4
      - id: unknown_60
        type: u4
      - id: unknown_64
        type: u4
      - id: bsdflags
        type: u4
      - id: owner_id
        type: u4
      - id: group_id
        type: u4
      - id: mode
        type: u2
      - id: unknown_82
        type: u2
      - id: unknown_84
        type: u4
      - id: unknown_88
        type: u4
      - id: xf_num_exts
        type: u2
        doc: File 0x02 or Folder 0x01 cmp. TN1150
      - id: xf_used_data
        type: u2
      - id: xf_header
        type: xf_header
        repeat: expr
        repeat-expr: xf_num_exts
      - id: xf
        repeat: expr
        repeat-expr: xf_num_exts
        size: xf_header[_index].length + ((8 - xf_header[_index].length) % 8)
        type:
          switch-on: xf_header[_index].type
          cases:
            xfield_type::name: xf_name
            xfield_type::size: xf_size
            xfield_type::device_node: xf_device_node
            xfield_type::sparse_size: xf_sparse_size
    -webide-representation: '#{extents_id:dec} / #{parent_id:dec} {xf_used_data}'

  xf_name:
    seq:
      - id: name
        type: strz

  xf_size:
    seq:
      - id: size
        type: u8
      - id: stored_size
        type: u8
      - id: unknown_16
        type: u8
      - id: unknown_size # could be compressed size
        type: u8
      - id: unknown_32
        type: u8

  xf_device_node:
    seq:
      - id: major_minor # Works around lack of a u3 type
        type: u4
    instances:
      major:
        value: major_minor >> 24
      minor:
        value: major_minor & 0xFFFFFF

  xf_sparse_size:
    seq:
      - id: size
        type: u8

  xf_header:
    seq:
      - id: type
        enum: xfield_type
        type: u2
      - id: length
        type: u2

  sibling_val: # 0x50
    seq:
      - id: node_id
        type: u8
      - id: length
        type: u2
      - id: name
        size: length
        type: str
    -webide-representation: '#{node_id:dec} "{name}"'

  extent_refcount_val: # 0x60
    seq:
      - id: count
        type: u4
    -webide-representation: '{count:dec}'

  lookup_val: # 0x20
    seq:
      - id: block_count
        type: u4
      - id: unknown_4
        type: u2
      - id: block_size
        type: u2
      - id: inode
        type: u8
      - id: unknown_16
        type: u4
    -webide-representation: '#{inode:dec}, Cnt {block_count:dec} * {block_size:dec}, {unknown_4:dec}, {unknown_16:dec}'

  extent_val: # 0x80
    seq:
      - id: len
        type: u8
      - id: phys_block_num
        type: ref_obj
      - id: flags
        type: u8
    -webide-representation: '{phys_block_num}, Len {len:dec}, {flags:dec}'

  drec_val: # 0x90
    seq:
      - id: node_id
        type: u8
      - id: timestamp
        type: u8
      - id: item_length
        type: u2
        enum: item_type
    -webide-representation: '#{node_id:dec}, {item_type}'

  sibling_map_val: # 0xc0
    seq:
      - id: map_node_id
        type: u8
    -webide-representation: '#{map_node_id:dec}'

  xattr_val: # 0x40
    seq:
      - id: ea_type
        type: u2
        enum: ea_type
      - id: data_length
        type: u2
      - id: data
        size: data_length
        type:
          switch-on: ea_type
          cases:
            ea_type::symlink: strz # symlink
            # all remaining cases are handled as a "bunch of bytes", thanks to the "size" argument
    -webide-representation: '{ea_type} {data}'


# space_manager (type: 0x05)

  space_manager:
    seq:
      - id: block_size
        type: u4
      - id: blocks_per_chunk
        type: u4
      - id: chunks_per_cib
        type: u4
      - id: cibs_per_cab
        type: u4
      - id: block_count
        type: u4
      - id: chunk_count
        type: u4
      - id: cib_count
        type: u4
      - id: cab_count
        type: u4
      - id: entry_count
        type: u4
      - id: unknown_68
        type: u4
      - id: free_block_count
        type: u8
      - id: entries_offset
        type: u4
      - id: unknown_84
        size: 92
      - id: prev_spaceman_internal_pool_block
        type: u8
    instances:
      spaceman_internal_pool_blocks:
        pos: entries_offset
        repeat: expr
        repeat-expr: entry_count
        type: u8

# spaceman internal pool (type: 0x07)

  spaceman_internal_pool:
    seq:
      - id: unknown_32
        size: 4
      - id: entry_count
        type: u4
      - id: entries
        type: spaceman_internal_pool_entry
        repeat: expr
        repeat-expr: entry_count

  spaceman_internal_pool_entry:
    seq:
      - id: xid
        type: u8
      - id: unknown_8
        type: u4
      - id: unknown_12
        type: u4
      - id: block_count
        type: u4
      - id: free_block_count
        type: u4
      - id: bitmap_block
        type: u8

# btree (type: 0x0b)

  btree:
    seq:
      - id: btree_type
        type: u8
        enum: tree_type
      - id: unknown_0
        size: 8
      - id: root
        type: ref_obj

# checkpoint (type: 0x0c)

  checkpoint:
    seq:
      - id: unknown_0
        type: u4
      - id: entry_count
        type: u4
      - id: entries
        type: checkpoint_entry
        repeat: expr
        repeat-expr: entry_count

  checkpoint_entry:
    seq:
      - id: type
        type: u2
        enum: obj_type
      - id: flags
        type: u2
      - id: subtype
        type: u4
        enum: obj_subtype
      - id: size
        type: u4
      - id: unknown_52
        type: u4
      - id: unknown_56
        type: u4
      - id: unknown_60
        type: u4
      - id: oid
        type: u8
      - id: object
        type: ref_obj

# volume_superblock (type: 0x0d)

  volume_superblock: # missing: next_obj_id, fs_flags, unmount_time
    seq:
      - id: magic
        size: 4
        contents: [APSB]
      - id: fs_index
        type: u4
      - id: unknown_40
        size: 16
      - id: features
        type: u4
        enum: features
      - id: unknown_60
        size: 12 # readonly_compatible_features, incompatible_features
      - id: fs_reserve_block_count
        type: u8
      - id: fs_quota_block_count
        type: u8
      - id: fs_alloc_count
        type: u8
      - id: unknown_92
        size: 32 # root_tree_type, extentref_tree_type, snap_meta_tree_type
      - id: omap_oid
        type: ref_obj
        doc: 'Maps node IDs to the inode Btree nodes'
      - id: root_tree_oid
        type: u8
      - id: extentref_tree_oid
        type: ref_obj
        doc: 'Maps file extents to inodes'
      - id: snap_meta_tree_oid
        type: ref_obj
      - id: unknown_160
        size: 16 # revert_to_xid, total_blocks_freed?
      - id: next_doc_id # next_obj_id?
        type: u8
      - id: num_files
        type: u8
      - id: num_directories
        type: u8
      - id: num_symlinks
        type: u8
      - id: num_other_fsobjects
        type: u8
      - id: num_snapshots
        type: u8
      - id: unknown_1601
        size: 16 # revert_to_xid, total_blocks_freed?
      - id: vol_uuid
        size: 16
      - id: last_mod_time
        type: u8
      - id: formatted_by_last_xid
        type: u8
      - id: formatted_by_id
        size: 32
        type: strz
      - id: formatted_by_timestamp
        type: u8
      - id: modified_by_last_xid
        type: u8
      - id: modified_by_id
        type: strz
        size: 32
      - id: modified_by_timestamp
        type: u8
      - id: rest
        size: 344
      - id: volname
        type: strz

# enums

enums:

  obj_type:
    1: container_superblock
    2: rootnode
    3: node
    5: space_manager
    7: spaceman_internal_pool
    11: btree
    12: checkpoint
    13: volume_superblock
    17: reaper
    32: unknown

  obj_subtype:
    0: empty
    9: history
    11: omap
    14: files
    15: extents
    16: unknown

  tree_type:
    0: om_tree
    1: fs_tree

  features:
    1: case_insensitive
    8: case_sensitive

  kind:
    0x0: omap
    0x2: lookup
    0x3: inode
    0x4: xattr
    0x5: sibling
    0x6: extent_refcount
    0x8: extent
    0x9: drec
    0xc: sibling_map

  xfield_type:
    516: name
    8200: size
    8718: device_node
    10253: sparse_size
    # Undiscoverd xfield_types:
    #   Doc_id
    #   Dstream
    #   Dir_Stats_key
    #   Uuid
    #   Sparse_bytes

  item_type:
    1: named_pipe
    2: character_special
    4: directory
    6: block_special
    8: regular
    10: symbolic_link
    12: socket
    14: whiteout

  ea_type:
    2: generic
    6: symlink