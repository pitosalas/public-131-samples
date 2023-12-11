# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

# Copyright (C) 2023 Pito Salas

# sourcery skip: square-identity
from dataclasses import dataclass

@dataclass
class Info:
    alloc: int
    overhead: int
    direct: int
    indirect: int
    double: int
    triple: int

# Constants
mb = 2**20
kb = 2**10
gb = 2**30

block = 4 * kb
file1_size = 2 * mb
file2_size = 9 * gb
file3_size = 3 * gb
lba = 4
lba_per_block = int(block / lba)
inode = 15 * 4

# Capacities of each level
direct_capacity = 12 * block
indirect_capacity = lba_per_block * block
double_indirect_capacity = lba_per_block * lba_per_block * block
triple_indirect_capacity = lba_per_block * lba_per_block * lba_per_block * block

# Helpers
def p(n):   
    return(f"{n:,.2f} Bytes, {(n/mb):,.2f} Meg")

print_on = True
def pp(s):
    if print_on:
        print(s)

def pp_info(so_far: Info):
    pp(f"Allocated: {p(so_far.alloc)}, Overhead: {p(so_far.overhead)}")
    pp(f"Direct: {so_far.direct}, Indirect: {so_far.indirect}, Double: {so_far.double}, Triple: {so_far.triple}")

def fill_direct(size: int) -> (bool, Info):
    found = False
    so_far = Info(0, 0, 0, 0, 0, 0)
    so_far.overhead = inode
# start filling it with direct pointers
    for so_far.direct in range(1, 12):
        so_far.alloc = so_far.direct * block
        if (so_far.alloc) > size:
            found = True
            break
    pp_info(so_far)
    return(found, so_far)

def fill_indirect(size: int, so_far: Info)  -> (bool, Info):
    if so_far.alloc >= size:
        return so_far
    found = False
    pp("Adding indirect block")
    so_far.overhead += block # for the indirect block
    so_far.indirect = 0
# now start filling it with pointers
    for so_far.indirect in range(1, lba_per_block+1):
        so_far.alloc += block
        if (so_far.alloc > size):
            found = True
            break
    pp_info(so_far)
    return(found, so_far)

def fill_double_indirect(size: int, so_far: Info)  -> (bool, Info):
    if so_far.alloc >= size:
        return True, so_far
    pp("Adding double indirect block")
    so_far.overhead += block
    found = False
    for so_far.double in range(1, lba_per_block):
        # so_far.allocate an indirect block
        so_far.overhead += block
        # and start filling it with pointers
        for _ in range(1, lba_per_block):
            so_far.alloc += block
            if (so_far.alloc > size):
                found = True
                break
        if found:
            break
    pp_info(so_far)
    return found, so_far

def fill_trip_indirect(size: int, so_far: Info)  -> (bool, Info):
    if so_far.alloc >= size:
        return so_far   
    pp("Adding triple indirect block")
    so_far.overhead += block
    found = False
    for so_far.triple in range(1, lba_per_block):
        # so_far.allocate a double indirect block
        so_far.overhead += block
        # start filling it with pointers to indirect blocks
        for so_far.triple in range(1, lba_per_block):
            so_far.overhead += block
            for _ in range(1,lba_per_block):
                so_far.alloc += block
                if so_far.alloc > size:
                    found = True
                    break
            if found:
                break
        if found:
            break
    
    pp_info(so_far)
    return found, so_far


def xsearch(size):
    pp(f"\n\n***** TYPE 1 ALLOCATING ***** {p(size)} ******")
    found, so_far = fill_direct(size)
    if not found:
        found, so_far = fill_indirect(size, so_far)
    if not found:
        found, so_far = fill_double_indirect(size, so_far)
    if not found:
        found, so_far = fill_trip_indirect(size, so_far)
    return found, so_far

def ysearch(size):
    pp(f"\n\n***** TYPE 2 ALLOCATING ***** {p(size)} ******")
    if size <= direct_capacity:
        pp("Just direct")
        found, so_far = fill_direct(size)
        return found, so_far
    if size <= indirect_capacity:
        pp("Just indirect")
        found, so_far = fill_indirect(size, Info(0, 0, 0, 0, 0, 0))
        return found, so_far
    if size <= double_indirect_capacity:
        pp("Just double indirect")
        found, so_far = fill_double_indirect(size, Info(0, 0, 0, 0, 0, 0))
        return found, so_far
    if size <= triple_indirect_capacity:
        pp("Just triple indirect")
        found, so_far = fill_trip_indirect(size, Info(0, 0, 0, 0, 0, 0))
        return found, so_far
    pp("Cannot store this file")
    return False, Info(0, 0, 0, 0, 0, 0)

def plot():
    import matplotlib.pyplot as plt
    import numpy as np
    # Log spaced inputs 
    x_vals = np.logspace(10, 32, 100, base=2.0)
    
    # Initialize output arrays
    y1_vals, y2_vals = [], []
    y3_vals, y4_vals, y5_vals, y6_vals = [], [], [], []
    
    # Run function over inputs
    for x in x_vals:
        y1, y2, y3, y4, y5, y6 = xsearch(x) 
        
        y1_vals.append(y1)
        y2_vals.append(y2)
        
        y3_vals.append(y3)
        y4_vals.append(y4) 
        y5_vals.append(y5)
        y6_vals.append(y6)
    
    # Plot with scientific right y-axis  
    fig, ax1 = plt.subplots()
    ax1.set_xscale("log") 
    
    ax1.plot(x_vals, y3_vals, label="direct")
    ax1.plot(x_vals, y4_vals, label="indirect")
    ax1.plot(x_vals, y5_vals, label="double indirect")
    ax1.plot(x_vals, y6_vals, label="triple indirect")
    
    ax2 = ax1.twinx() 
    ax2.set_yscale('log')
    ax2.plot(x_vals, y1_vals, label="storage", color="black", linestyle="--")
    ax2.plot(x_vals, y2_vals, label="so_far.overhead", color="black", linestyle=":")
    ax1.legend(loc=(0.0, 1.1))
    ax2.legend(loc=(0.7, 1.1))
    
    fig.tight_layout()
    plt.show()

def report():
    s1, o1, di1, i1, d1, t1 = xsearch(file1_size)
    s2, o2, di2, i2, d2, t2 = xsearch(file2_size)

    print(f"""File size: {p(file1_size)},\n   total storage: {p(s1)},\n   total overhead {p(o1)}\n   overhead {o1/(s1+o1)*100.0:.2f}%""")
    print(f"""   pointers: direct: {di1}, indirect: {i1}, double indirect: {d1}, triple indirect: {t1}""")
    print(f"""File size: {p(file2_size)},\n   total storage: {p(s2)},\n   total overhead {p(o2)}\n   overhead {o2/(s2+o2)*100.0:.2f}%""")
    print(f"""   pointers: direct: {di2}, indirect: {i2}, double indirect: {d2}, triple indirect: {t2}""")
    
    print(f"\n\nCase 1: File size: {p(file1_size)}:\n   total data memory: {p(s1)}, total ovh: {p(o1)}")
    print(f"   overhead {o1/(s1+o1)*100.0:.2f}%""")
    print(f"Case 2: File size: {p(file2_size)}:\n   total data memory: {p(s2)}, total ovh: {p(o2)}")
    print(f"   overhead {o2/(s2+o2)*100.0:.2f}%""")


#report()
xsearch(file2_size)
ysearch(file2_size)


