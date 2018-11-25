import numpy as np


def create_checksum(data):
    sum1 = np.uint64(0)
    sum2 = np.uint64(0)

    mod_value = np.uint64(4294967295)  # 2<<31 - 1

    for i in range(int(len(data) / 4)):
        dtype = np.dtype(np.uint32)
        dtype = dtype.newbyteorder('L')
        data = np.frombuffer(data[i * 4:(i + 1) * 4], dtype=dtype)

        sum1 = (sum1 + np.uint64(data)) % mod_value
        sum2 = (sum2 + sum1) % mod_value

    check1 = mod_value - ((sum1 + sum2) % mod_value)
    check2 = mod_value - ((sum1 + check1) % mod_value)

    return (check2 << 32) | check1


def check_checksum(data):
    dtype = np.dtype(np.uint64)
    dtype = dtype.newbyteorder('L')
    return (np.frombuffer(data[:8], dtype=dtype) == create_checksum(data[8:]))[0]


if __name__ == '__main__':

    with open('test.blk', 'rb') as io:
        print(check_checksum(io.read()))
