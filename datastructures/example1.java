BLOCK_ADDRESS_SIZE = 4;
PHYSICAL_BLOCK_SIZE = 4096;
BYTES_PER_BLOCK = PHYSICAL_BLOCK_SIZE;
BLOCKS_PER_INDEX = PHYSICAL_BLOCK_SIZE / BLOCK_ADDRESS_SIZE;
DIRECT_BLOCK_ADDRESSES_IN_FCB = 10;


class DiskBlock {
    Byte[] contents = new Byte[BYTES_PER_BLOCK];
}

class BlockAddress {
    Byte[] address = new Byte[BLOCK_ADDRESS_SIZE];
}

class SingleIndexBlock {
    BlockAddress[] blocks = new BlockAddress[BLOCKS_PER_INDEX];
}

class DoubleIndexBlock {
    SingleIndexBlock[] blocks = new SingleIndexBlock[BLOCKS_PER_INDEX];
}

class TripleIndexBlock {
    DoubleIndexBlock[] blocks = new DoubleIndexBlock[BLOCKS_PER_INDEX];
}  

class FCB {
    ByBlockAddresste[] directBlockAddresses = new BlockAddress[];
    SingleIndexBlock singleIndexBlock;
    DoubleIndexBlock doubleIndexBlock;
    TripleIndexBlock tripleIndexBlock;
}
