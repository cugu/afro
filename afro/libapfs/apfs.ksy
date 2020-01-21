meta:
  id: apfs
  license: mit
  encoding: utf-8
  endian: le
doc: https://developer.apple.com/support/apple-file-system/apple-file-system-reference.pdf

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
    value: _root.block0.body.as<nx_superblock_t>.nx_block_size
#  random_block:
#    pos: 20213 * block_size   # enter block number here to jump directly that block in the webide
#    type: obj           # opens a sub stream for making positioning inside the block work
#    size: block_size

types:

# base types

  paddr_t:
    doc: |
      universal type to address a block: it both parses one u8-sized
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
    -webide-representation: 'blk {val:dec}'

  prange_t:
    seq:
      - id: pr_start_paddr
        type: u8
      - id: pr_block_count
        type: u8

  oid_t:
    doc: similar to paddr_t
    seq:
      - id: val
        type: u8
    instances:
      target:
        io: _root._io
        pos: val * _root.block_size
        type: obj
        size: _root.block_size
    -webide-representation: 'blk {val:dec}'

  xid_t:
    seq:
      - id: val
        type: u8

# meta structs

  obj_phys:
    seq:
      - id: o_cksum
        type: u8
        doc: the fletcher 64 checksum of the object.
      - id: o_oid
        type: oid_t
        doc: the objectʼs identifier.
      - id: o_xid
        type: xid_t
        doc: the identifier of the most recent transaction that this object was modified in.
      - id: o_type
        type: u2
        doc: the objectʼs type and flags.
        enum: object_type
      - id: o_flags
        type: u2
        enum: object_type_flags
      - id: o_subtype
        type: u4
        enum: object_type
        doc: the objectʼs subtype.
    # instances:
    #   type:
    #     value: type & 0x0000ffff
    #     enum: object_type
    #   flags:
    #     value: o_type & 0xffff0000
    #     enum: object_type_flags
    #   storagetype:
    #     value: o_flags.to_i & 0xc000
    #   flags_defined:
    #     value: o_flags.to_i & 0xf800

  obj:
    seq:
      - id: hdr
        type: obj_phys
      - id: body
        #size-eos: true
        type:
          switch-on: hdr.o_type
          cases:
            object_type::object_type_nx_superblock: nx_superblock_t
            object_type::object_type_btree: btree_node_phys_t
            object_type::object_type_btree_node: btree_node_phys_t
            object_type::object_type_spaceman: chunk_info_block
            object_type::object_type_spaceman_cib: chunk_info_t
            object_type::object_type_omap: omap_phys_t
            object_type::object_type_checkpoint_map: checkpoint_map_phys_t
            object_type::object_type_fs: apfs_superblock_t
    -webide-representation: '{hdr.o_type}'


# nx_superblock_t (type: 0x01)

  nx_superblock_t:
    seq:
      - id: nx_magic
        size: 4
        # contents: [nxsb]
      - id: nx_block_size
        type: u4
      - id: nx_block_count
        type: u8
      - id: nx_features
        type: u8
      - id: nx_readonly_compatible_features
        type: u8
      - id: nx_incompatible_features
        type: u8
      - id: nx_uuid
        size: 16
      - id: nx_next_oid
        type: oid_t
      - id: nx_next_xid
        type: xid_t
      - id: nx_xp_desc_blocks
        type: u4
      - id: nx_xp_data_blocks
        type: u4
      - id: nx_xp_desc_base
        type: u8
      - id: nx_xp_data_base
        type: u8
      - id: nx_xp_desc_next
        type: u4
      - id: nx_xp_data_next
        type: u4
      - id: nx_xp_desc_index
        type: u4
      - id: nx_xp_desc_len
        type: u4
      - id: nx_xp_data_index
        type: u4
      - id: nx_xp_data_len
        type: u4
      - id: nx_spaceman_oid
        type: oid_t
      - id: nx_omap_oid
        type: oid_t
      - id: nx_reaper_oid
        type: oid_t
      - id: nx_test_type
        type: u4
      - id: nx_max_file_systems
        type: u4
      - id: nx_fs_oids
        type: oid_t
        repeat: expr
        repeat-expr: nx_max_file_systems
      - id: nx_counters
        repeat: expr
        repeat-expr: 32 # nx_num_counters
        type: u8
      - id: nx_blocked_out_prange
        type: prange_t
      - id: nx_evict_mapping_tree_oid
        type: oid_t
      - id: nx_flags
        type: u8
      - id: nx_efi_jumpstart
        type: u8
      - id: nx_fusion_uuid
        size: 16
      - id: nx_keylocker
        type: prange_t
      - id: nx_ephemeral_info
        type: u8
        repeat: expr
        repeat-expr: 4
      - id: nx_test_oid
        type: oid_t
      - id: nx_fusion_mt_oid
        type: oid_t
      - id: nx_fusion_wbc_oid
        type: oid_t
      - id: nx_fusion_wbc
        type: prange_t
    instances:
      checkpoint_offset:
        pos: (nx_xp_desc_base + nx_xp_desc_index) * _root.block_size
        type: obj
      spaceman_offset:
        pos: (nx_xp_data_base + nx_xp_data_index) * _root.block_size
        type: obj


# node (type: 0x02)

  nloc:
    seq:
      - id: off
        type: u2
      - id: len
        type: u2

  btree_node_phys_t:
    seq:
      - id: btn_flags
        type: u2
      - id: btn_level
        type: u2
        doc: zero for leaf nodes, > 0 for index nodes
      - id: btn_nkeys
        type: u4
      - id: btn_table_space
        type: nloc
      - id: btn_free_space
        type: nloc
      - id: btn_key_free_list
        type: nloc
      - id: btn_val_free_list
        type: nloc
      - id: btn_data
        type: node_entry
        repeat: expr
        repeat-expr: btn_nkeys

## node entries

  node_entry:
    seq:
      - id: key_offset
        type: s2
      - id: key_length
        type: u2
        if: (_parent.btn_flags & 4) == 0 # btnode_fixed_kv_size
      - id: data_offset
        type: s2
      - id: data_length
        type: u2
        if: (_parent.btn_flags & 4) == 0 # btnode_fixed_kv_size
    instances:
      j_key_t:
        pos: key_offset + _parent.btn_table_space.len + 56
        type: j_key_t
        -webide-parse-mode: eager
      key:
        pos: key_offset + _parent.btn_table_space.len + 56 + 8
        type:
          switch-on: j_key_t.obj_type
          cases:
            j_obj_types::apfs_type_any: omap_key_t
            j_obj_types::apfs_type_extent: j_empty_key_t
            j_obj_types::apfs_type_inode: j_empty_key_t
            j_obj_types::apfs_type_xattr: j_xattr_key_t
            j_obj_types::apfs_type_sibling_link: j_sibling_key_t
            j_obj_types::apfs_type_dstream_id: j_empty_key_t
            j_obj_types::apfs_type_file_extent: j_extent_key_t
            j_obj_types::apfs_type_dir_rec: j_drec_key_t
            j_obj_types::apfs_type_sibling_map: j_empty_key_t
        -webide-parse-mode: eager
      val:
        pos: _root.block_size - data_offset - 40 * (_parent.btn_flags & 1)
        type:
          switch-on: '(_parent.btn_level > 0) ? 256 : j_key_t.obj_type.to_i'
          cases:
            256: pointer_val_t # applies to all pointer vals, i.e. any entry val in index nodes
            j_obj_types::apfs_type_any.to_i: omap_val_t
            j_obj_types::apfs_type_extent.to_i: j_phys_ext_val_t
            j_obj_types::apfs_type_inode.to_i: j_inode_val_t
            j_obj_types::apfs_type_xattr.to_i: j_xattr_val_t
            j_obj_types::apfs_type_sibling_link.to_i: j_sibling_val_t
            j_obj_types::apfs_type_dstream_id.to_i: j_extent_refcount_val_t
            j_obj_types::apfs_type_file_extent.to_i: j_extent_val_t
            j_obj_types::apfs_type_dir_rec.to_i: j_drec_val_t
            j_obj_types::apfs_type_sibling_map.to_i: j_sibling_map_val_t
        -webide-parse-mode: eager
    -webide-representation: '{j_key_t} {key} -> {val}'

## node entry keys

  j_key_t:
    seq:
      - id: obj_id_and_type_low # this is a work-around for javascript's inability to handle 64 bit vals
        type: u4
      - id: obj_id_and_type_high
        type: u4
    instances:
      obj_id:
        value: obj_id_and_type_low + ((obj_id_and_type_high & 0x0fffffff) << 32)
        -webide-parse-mode: eager
      obj_type:
        value: obj_id_and_type_high >> 28
        enum: j_obj_types
        -webide-parse-mode: eager
    -webide-representation: '({obj_type}) #{obj_id:dec}'

  j_empty_key_t:
    -webide-representation: ''

  omap_key_t:
    seq:
      - id: ok_oid
        type: oid_t
      - id: ok_xid
        type: xid_t
    -webide-representation: 'xid {ok_xid:dec}'

  history_key_t:
    seq:
      - id: xid
        type: u8
      - id: obj_id
        type: oid_t
    -webide-representation: '{obj_id} v{xid:dec}'

  j_drec_key_t:
    seq:
      - id: name_len
        type: u1
      - id: hash
        size: 3
      - id: name
        size: name_len
        type: strz
    -webide-representation: '"{name}"'

  j_xattr_key_t:
    seq:
      - id: name_len
        type: u1
      - id: name
        size: name_len
        type: strz
    -webide-representation: '"{name}"'

  j_sibling_key_t:
    seq:
      - id: sibling_id
        type: u8
    -webide-representation: '#{sibling_id:dec}'

  j_extent_key_t:
    seq:
      - id: offset # seek pos in file
        type: u8
    -webide-representation: '{offset:dec}'

## node entry vals

  pointer_val_t: # for any index nodes
    seq:
      - id: pointer
        type: u8
    -webide-representation: '-> {pointer:dec}'

  history_val_t: # ???
    seq:
      - id: unknown_0
        type: u4
      - id: unknown_4
        type: u4
    -webide-representation: '{unknown_0}, {unknown_4}'

  omap_val_t: # 0x00
    seq:
      - id: ov_flags
        type: u4
      - id: ov_size
        type: u4
      - id: ov_paddr
        type: paddr_t
    -webide-representation: '{ov_paddr}, len {ov_size:dec}'

  j_inode_val_t: # 0x30
    seq:
      - id: parent_id
        type: u8
      - id: private_id
        type: u8
      - id: create_time
        type: u8
      - id: mod_time
        type: u8
      - id: change_time
        type: u8
      - id: access_time
        type: u8
      - id: internal_flags
        type: u8
      - id: nchildren_or_nlink
        type: u4
      - id: default_protection_class
        type: u4
      - id: write_generation_counter
        type: u4
      - id: bsd_flags
        type: u4
      - id: owner
        type: u4
      - id: group
        type: u4
      - id: mode
        type: u2
      - id: pad1
        type: u2
      - id: pad2
        type: u8
      - id: xfields
        type: xf_blob_t

  xf_blob_t:
    seq:
      - id: xf_num_exts
        type: u2
        doc: file 0x02 or folder 0x01 cmp. tn1150
      - id: xf_used_data
        type: u2
      - id: xf_data
        type: x_field_t
        repeat: expr
        repeat-expr: xf_num_exts
      - id: xf
        repeat: expr
        repeat-expr: xf_num_exts
        size: xf_data[_index].x_size + ((8 - xf_data[_index].x_size) % 8)
        type:
          switch-on: xf_data[_index].x_type
          cases:
            ino_ext_type::ino_ext_type_name: xf_name
            ino_ext_type::ino_ext_type_dstream: xf_size
            ino_ext_type::ino_ext_type_rdev: xf_device_node
            ino_ext_type::ino_ext_type_document_id: xf_document_id
            ino_ext_type::ino_ext_type_sparse_bytes: xf_sparse_size
    -webide-representation: '#{private_id:dec} / #{parent_id:dec} {xf_used_data}'

  x_field_t:
    seq:
      - id: x_type
        enum: ino_ext_type
        type: u1
      - id: x_flags
        type: u1
      - id: x_size
        type: u2

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
      - id: major_minor # works around lack of a u3 type
        type: u4
    instances:
      major:
        value: major_minor >> 24
      minor:
        value: major_minor & 0xffffff

  xf_document_id:
    seq:
      - id: id
        type: u4

  xf_sparse_size:
    seq:
      - id: size
        type: u8



  j_sibling_val_t: # 0x50
    seq:
      - id: parent_id
        type: u8
      - id: name_len
        type: u2
      - id: name
        size: name_len
        type: str
    -webide-representation: '#{parent_id:dec} "{name}"'

  j_extent_refcount_val_t: # 0x60
    seq:
      - id: count
        type: u4
    -webide-representation: '{count:dec}'

  j_phys_ext_val_t: # 0x20
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
    -webide-representation: '#{inode:dec}, cnt {block_count:dec} * {block_size:dec}, {unknown_4:dec}, {unknown_16:dec}'

  j_extent_val_t: # 0x80
    seq:
      - id: len
        type: u8
      - id: phys_block_num
        type: u8
      - id: flags
        type: u8
    -webide-representation: '{phys_block_num}, len {len:dec}, {flags:dec}'

  j_drec_val_t: # 0x90
    seq:
      - id: file_id
        type: u8
      - id: date_added
        type: u8
      - id: flags
        type: xf_blob_t
    -webide-representation: '#{file_id:dec}, {item_type}'

  j_sibling_map_val_t: # 0xc0
    seq:
      - id: file_id
        type: u8
    -webide-representation: '#{file_id:dec}'

  j_xattr_val_t: # 0x40
    seq:
      - id: flags
        type: u2
        enum: j_xattr_flags
      - id: xdata_length
        type: u2
      - id: xdata
        size: xdata_length
        type:
          switch-on: flags
          cases:
            j_xattr_flags::symlink: strz # symlink
            # all remaining cases are handled as a "bunch of bytes", thanks to the "size" argument
    -webide-representation: '{j_xattr_flags} {data}'


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

  chunk_info_block:
    seq:
      - id: cib_index
        type: u4
      - id: cib_chunk_info_count
        type: u4
      - id: cib_chunk_info
        type: chunk_info_t
        repeat: expr
        repeat-expr: cib_chunk_info_count

  chunk_info_t:
    seq:
      - id: ci_xid
        type: u8
      - id: ci_addr
        type: u8
      - id: ci_block_count
        type: u4
      - id: ci_free_count
        type: u4
      - id: ci_bitmap_addr
        type: u8

# omap_phys_t (type: 0x0b)

  omap_phys_t:
    seq:
      - id: om_flags
        type: u4
      - id: om_snap_count
        type: u4
      - id: om_tree_type
        type: u4
      - id: om_snapshot_tree_type
        type: u4
      - id: om_tree_oid
        type: oid_t
      - id: om_snapshot_tree_oid
        type: oid_t
      - id: om_most_recent_snap
        type: xid_t
      - id: om_pending_revert_min
        type: xid_t
      - id: om_pending_revert_max
        type: xid_t

# checkpoint (type: 0x0c)

  checkpoint_map_phys_t:
    seq:
      - id: cpm_flags
        type: u4
        enum: checkpoint_map_flags
      - id: cpm_count
        type: u4
      - id: cpm_map
        type: checkpoint_mapping_t
        repeat: expr
        repeat-expr: cpm_count

  checkpoint_mapping_t:
    seq:
      - id: cpm_type
        type: u2
        enum: object_type
      - id: cpm_flags
        type: u2
      - id: cpm_subtype
        type: u4
        enum: object_type
      - id: cpm_size
        type: u4
      - id: cpm_pad
        type: u4
      - id: cpm_fs_oid
        type: u8
      - id: cpm_oid
        type: u8
      - id: cpm_paddr
        type: oid_t

# apfs_superblock_t (type: 0x0d)

  apfs_superblock_t: # missing: next_obj_id, fs_flags, unmount_time
    seq:
      - id: apfs_magic
        size: 4
        # contents: [apsb]
      - id: apfs_fs_index
        type: u4
      - id: apfs_features
        type: u8
        # enum: features
      - id: apfs_readonly_compatible_features
        type: u8
      - id: apfs_incompatible_features
        type: u8
      - id: apfs_unmount_time
        type: u8
      - id: apfs_fs_reserve_block_count
        type: u8
      - id: apfs_fs_quota_block_count
        type: u8
      - id: apfs_fs_alloc_count
        type: u8
      - id: apfs_meta_crypto # todo
        size: 32 # root_tree_type, extentref_tree_type, snap_meta_tree_type
      - id: apfs_omap_oid
        type: oid_t
      - id: apfs_root_tree_oid
        type: oid_t
      - id: apfs_extentref_tree_oid
        type: oid_t
      - id: apfs_snap_meta_tree_oid
        type: oid_t
      - id: apfs_revert_to_xid
        type: xid_t
      - id: apfs_revert_to_sblock_oid
        type: oid_t
      - id: apfs_next_obj_id
        type: u8
      - id: apfs_num_files
        type: u8
      - id: apfs_num_directories
        type: u8
      - id: apfs_num_symlinks
        type: u8
      - id: apfs_num_other_fsobjects
        type: u8
      - id: apfs_num_snapshots
        type: u8

      - id: apfs_total_blocks_alloced
        type: u8
      - id: apfs_total_blocks_freed
        type: u8
      - id: apfs_vol_uuid
        size: 16
      - id: apfs_last_mod_time
        type: u8
      - id: apfs_fs_flags
        type: u8
      - id: apfs_formatted_by
        type: apfs_modified_by_t
      - id: apfs_modified_by
        type: apfs_modified_by_t
        repeat: expr
        repeat-expr: 8 # apfs_max_hist
      - id: apfs_volname
        type: strz
        size: 256
      - id: apfs_next_doc_id
        type: u4
      - id: apfs_role
        type: u2
      - id: reserved
        type: u2
      - id: apfs_root_to_xid
        type: xid_t
      - id: apfs_er_state_oid
        type: oid_t

  apfs_modified_by_t:
    seq:
      - id: id
        size: 32 # apfs_modified_namelen
      - id: timestamp
        type: u8
      - id: last_xid
        type: xid_t

# enums

enums:

  object_type:
    0x0001: object_type_nx_superblock
    0x0002: object_type_btree
    0x0003: object_type_btree_node
    0x0005: object_type_spaceman
    0x0006: object_type_spaceman_cab
    0x0007: object_type_spaceman_cib
    0x0008: object_type_spaceman_bitmap
    0x0009: object_type_spaceman_free_queue
    0x000a: object_type_extent_list_tree
    0x000b: object_type_omap
    0x000c: object_type_checkpoint_map
    0x000d: object_type_fs
    0x000e: object_type_fstree
    0x000f: object_type_blockreftree
    0x0010: object_type_snapmetatree
    0x0011: object_type_nx_reaper
    0x0012: object_type_nx_reap_list
    0x0013: object_type_omap_snapshot
    0x0014: object_type_efi_jumpstart
    0x0015: object_type_fusion_middle_tree
    0x0016: object_type_nx_fusion_wbc
    0x0017: object_type_nx_fusion_wbc_list
    0x0018: object_type_er_state
    0x0019: object_type_gbitmap
    0x001a: object_type_gbitmap_tree
    0x001b: object_type_gbitmap_block
    0x0000: object_type_invalid
    0x00ff: object_type_test

  object_type_flags:
    0x0000: obj_virtual
    0x8000: obj_ephemeral
    0x4000: obj_physical
    0x2000: obj_noheader
    0x1000: obj_encrypted
    0x0800: obj_nonpersistent

  checkpoint_map_flags:
    0x00000001: checkpoint_map_last

  tree_type:
    0: om_tree
    1: fs_tree

  features:
    1: case_insensitive
    8: case_sensitive

  j_obj_types:
    0: apfs_type_any
    1: apfs_type_snap_metadata
    2: apfs_type_extent
    3: apfs_type_inode
    4: apfs_type_xattr
    5: apfs_type_sibling_link
    6: apfs_type_dstream_id
    7: apfs_type_crypto_state
    8: apfs_type_file_extent
    9: apfs_type_dir_rec
    10: apfs_type_dir_stats
    11: apfs_type_snap_name
    12: apfs_type_sibling_map

  ino_ext_type:
    1: ino_ext_type_snap_xid
    2: ino_ext_type_delta_tree_oid
    3: ino_ext_type_document_id
    4: ino_ext_type_name
    5: ino_ext_type_prev_fsize
    6: ino_ext_type_reserved_6
    7: ino_ext_type_finder_info
    8: ino_ext_type_dstream
    9: ino_ext_type_reserved_9
    10: ino_ext_type_dir_stats_key
    11: ino_ext_type_fs_uuid
    12: ino_ext_type_reserved_12
    13: ino_ext_type_sparse_bytes
    14: ino_ext_type_rdev

  item_type:
    1: named_pipe
    2: character_special
    4: directory
    6: block_special
    8: regular
    10: symbolic_link
    12: socket
    14: whiteout

  j_xattr_flags:
    2: xattr_data_embedded
    6: symlink
