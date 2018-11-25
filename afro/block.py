def get_block(idx, block_size, file_io):
    """ Get data of a single block """
    file_io.seek(idx * block_size)
    return file_io.read(block_size)
