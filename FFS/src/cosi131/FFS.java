package cosi131;

public class FFS {

	public static final int PHYSICAL_BLOCK_SIZE = 4096;
	public static final int BLOCK_ADDRESS_SIZE = 4;
	public static final int BYTES_PER_BLOCK = PHYSICAL_BLOCK_SIZE;
	public static final int BLOCKS_PER_INDEX = PHYSICAL_BLOCK_SIZE / BLOCK_ADDRESS_SIZE;
	public static final int DIRECT_BLOCK_ADDRESSES_IN_FCB = 10;
	
	BlockAddress[] directLinks = new BlockAddress[DIRECT_BLOCK_ADDRESSES_IN_FCB];
    SingleIndexBlock singleIndexBlock;
    DoubleIndexBlock doubleIndexBlock;
    TripleIndexBlock tripleIndexBlock;

	
	class DiskBlock {
	    byte[] contents = new byte[PHYSICAL_BLOCK_SIZE];
	}

	class BlockAddress {
	    byte[] address = new byte[BLOCK_ADDRESS_SIZE];

	    BlockAddress(int number) {
	    	address[0] = (byte) (number >> 24);
	    	address[1] = (byte) (number >> 16);
	    	address[2] = (byte) (number >> 8);
	    	address[3] = (byte) (number);
	    }
	    
	    int to_integer() {
	    	int result = ((address[0] & 0xFF) << 24) | ((address[1] & 0xFF) << 16) | ((address[2] & 0xFF) << 8) | (address[3] & 0xFF);
	    	return result;
	    }
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

	public static void main(String[] args) {
		FFS files = new FFS();
		files.directLinks[0] = files.new BlockAddress(100);

	}
	
	
}
