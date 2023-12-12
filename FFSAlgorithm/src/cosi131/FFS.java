package cosi131;

import java.util.ArrayList;

public class FFS {

	public static final int PHYSICAL_BLOCK_SIZE = 4096;
	public static final int DIRECT_BLOCK_ADDRESSES_IN_FCB = 10;
	public static final int BLOCKS_PER_INDEX = PHYSICAL_BLOCK_SIZE / 4;

	ArrayList<MemoryBlock> physical_memory = new ArrayList<MemoryBlock>();

	int usedDirectLinks = 0;
	BlockAddress[] directLinks = new BlockAddress[DIRECT_BLOCK_ADDRESSES_IN_FCB];
	SingleIndexBlock singleIndexBlock;
	DoubleIndexBlock doubleIndexBlock;
	TripleIndexBlock tripleIndexBlock;

	class MemoryBlock {
		int contents;

		MemoryBlock(int value) {
			contents = value;
		}
	}

	class BlockAddress {
		int address;

		BlockAddress(int address) {
			this.address = address;

		}

		void dump() {
			System.out.printf("Address points to: %d\n", physical_memory.get(address).contents);
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

	public boolean add_direct_block(int val) {
		int addess_of_newly_allocated_memory_block = physical_memory.size();
		physical_memory.add(new MemoryBlock(val));
		if (usedDirectLinks < DIRECT_BLOCK_ADDRESSES_IN_FCB) {
			directLinks[usedDirectLinks] = new BlockAddress(addess_of_newly_allocated_memory_block);
			usedDirectLinks++;
			return true;
		}
		return false;
	}

	public static void main(String[] args) {
		FFS ffs = new FFS();
		ffs.add_direct_block(99);
		ffs.add_direct_block(-5);
		ffs.dumpAll();
	}

	public void dumpAll() {
		System.out.printf("Total direct links: %d\n", usedDirectLinks);
		for (int i = 0; i < usedDirectLinks; i++) {
			System.out.printf("Direct Link %d refers to address: %d containing value %d\n", i, directLinks[i].address,
					physical_memory.get(directLinks[i].address).contents);
		}

	}
}
