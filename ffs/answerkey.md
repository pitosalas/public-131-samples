### Answer Key For PS4

#### General Notes
* Overhead is always much smaller than data
* Data blocks can be either the size of the file, or student might count the internal fragmentation of the next block too
* There are two legitimate ways to answer this question
  * If the whole file does not fit in one kind of indirection (i.e. direct, single, double or triple) then don't use it, but instead go to the next kind of indirection. This way is much easier to calculate
  * Or, fill each level of indirection before going to the next. This way is much more difficult to calculate but more realistic
* So there are two legitimate answers for each


Bullet 1: (note that overhead is always far smaller than data)
    Part 1: Small File, Ovh (~4K)
    Part 2: Small File, Data (~2M)
    Part 3: Large FIle, Ovh (~9M)
    Part 4: Large File, Data (~ 9G)
Bullet 2: (Note overhead will always be very small, below 10%)
    Part 1: Small FIle Ovh % ~.2%
    Part 2: Larg File Ovh % ~.01%
Bullet 3: (+1 if they count the inode separately)
    Part 1: Max Mem Ref Small File: 1 
    Part 2: Min Mem Ref Small File: 1
    Part 3: Max Mem Ref Large FIle: 3
    Part 4: Min Mem Ref Large FIle: 1
Bullet 4:
    Part 1: New structure will always be either equal or faster
Bullet 5:
    Part 1: New structure will always be either approx equal
Bullet 6:
    Part 1: If the file fits, the new structure will always work better than the old