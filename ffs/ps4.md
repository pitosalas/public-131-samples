# Cosi 131a - Problem Set 4
## November 28, 2023

The Unix  “Fast File System” system keeps track of the individual blocks in a file using  an asymmetric multi-level index data structure. The design is meant to be space efficient for smaller files and still accommodate huge files. 

### The disk volume:

* Once formatted, the underlying disk volume is organized into 4KB blocks of data
* Each block is addressable via a 32 bit (4 bytes) logical block address or LBA

### Files and inodes:

* The data in a file is stored in blocks.
* Each file is located through a data structure called an Inode
* The Inode contains information about the file such as the file name, creation time, owner of the file, and so on
* It also contains an index In order to keep track of all the disk blocks belonging to the file

### The Index:

* The index contains 15 pointers, each is an LBA
* The first 12 pointers are direct pointers
* The 13th pointer is to an “indirect block”
* The 14th pointer is to a “double indirect block”
* The 15th pointer is to a “triple indirect block”
* Given a 4K block size and 4-byte LBA, a block will contain 2^12/2^2 = 2^10 pointers
* An indirect block is a table of direct pointers.
* A double indirect block contains 2^10 pointers to other indirect blocks
* A triple indirect block contains 2^10 pointers to other double indirect blocks.

### Access:

In order to access a block in a file, the file system determines based on its LBA where to look for the pointer to the block. For example if the LBA is less than 12, then it will find a pointer to it in the top part of the index. If it is more than 12 it will have to then look into the first indirect block and the other ones, etc.

## Questions:

We are using the FFS to store three files, respectively of a) 2MB, and b) 9GB. Let’s define as “overhead” the memory space for the index block and any necessary single, double and triple indirect blocks. And let’s define as “data” the memory space for the data blocks. And we define the overhead percentage as (overhead/(data + overhead).

### Answer the following for both case a) and case b) separately.

* In each case what is the total overhead memory and total data memory?  (four parts)
* In each case, what is the overhead percentage in each case? (two parts)
* In each case, what is the maximum and minimum number of memory references required to locate a block?(4 parts)

### Analyze the tradeoff if we changed the FFS so that the 13th, 14th and 15th pointers all pointing to an indirect block (i.e. no double or triple). Answer this in general. You may pick examples of file sizes to illustrate your answers. 

* Under what circumstances would this change cause some operations be faster or slower? (one part)
* Under what circumstances would this change lead to using more or less ake more or less memory (one part)
* Under what circumstances would this change work better for large or small files? Please explain your answers (one part)

There are FOUR (4) Major questions and 13 total parts. All your answers should include the formulas you used to calculate your answers not just a number. Make them legible. Use this notation to indicate powers of two: 2^8 etc.

## ChatGPT Note: You are not permitted to use ChatGPT to answer this question or any part of it. And by the way, ChatGPT is bad with specific numbers and calculations.