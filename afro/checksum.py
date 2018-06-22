import numpy as np

def create_checksum(data):
    sum1 = np.uint64(0)
    sum2 = np.uint64(0)

    modValue = np.uint64(4294967295) # 2<<31 - 1

    for i in range(int(len(data)/4)):
        dt = np.dtype(np.uint32)
        dt = dt.newbyteorder('L')
        d = np.frombuffer(data[i*4:(i+1)*4], dtype=dt)

        sum1 = (sum1 + np.uint64(d)) % modValue
        sum2 = (sum2 + sum1) % modValue

    check1 = modValue - ((sum1 + sum2) % modValue)
    check2 = modValue - ((sum1 + check1) % modValue)

    return (check2 << 32) | check1


def check_checksum(data):
    dt = np.dtype(np.uint64)
    dt = dt.newbyteorder('L')
    return (np.frombuffer(data[:8], dtype=dt) == create_checksum(data[8:]))[0]

if __name__ == '__main__':

    with open('test.blk', 'rb') as io:
        data = io.read()
        print(check_checksum(data))