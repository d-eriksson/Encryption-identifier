import math

def calculate_entropy(filepath):
    byteDestribution = [0] * 256
    totalBytes = 0
    entropy = 0
    with open(filepath, "rb") as f:
        byte = f.read(1)
        while byte:
            # Do stuff with byte.
            val = int.from_bytes(byte, byteorder='little')
            byteDestribution[val]+=1
            totalBytes+=1
            byte = f.read(1)
    for count in byteDestribution:
        # If no bytes of this value were seen in the value, it doesn't affect
        # the entropy of the file.
        if count == 0:
            continue
        # p is the probability of seeing this byte in the file, as a floating-
        # point number
        p = 1.0 * count / totalBytes
        entropy -= p * math.log(p, 256)
    
    return(entropy)