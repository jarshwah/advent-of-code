#cython: language_level=3, boundscheck=False, wraparound=False, nonecheck=False, cdivision=True
from cpython cimport array
import array
import sys

cdef int A[14]
cdef int B[14]
cdef int BIGGEST[9]
cdef int SMALLEST[9]

cache = []

def init_globals(a, b):
    global A
    global B
    global BIGGEST
    global SMALLEST
    global cache
    cdef array.array na = array.array('i', a)
    cdef array.array nb = array.array('i', b)
    A = na
    B = nb
    BIGGEST = [9, 8, 7, 6, 5, 4, 3, 2, 1]
    SMALLEST = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    cache = [{} for n in range(14)]


cdef long long monad(int w, long long z, int a, int b, int c):
    cdef long long x
    x = z % 26
    z //= c
    if x != w - a:
        z = 26 * z + w + b
    return z


cpdef long long solve(int digit, long long z, int largest):
    global A
    global B
    global BIGGEST
    global SMALLEST
    global cache
    cdef long long ans, new_answer, next_z, max_next
    cdef int a, b, c, check, reductions_left
    cdef int[9] search_order

    if digit == 14:
        if z == 0:
            return 0
        return -1

    if (z in cache[digit]):
        return cache[digit][z]

    cache[digit][z] = -1;
    reductions_left = 0
    search_order = SMALLEST
    if largest == 1:
        search_order = BIGGEST
    a = A[digit]
    b = B[digit]
    c = 26 if a <= 0 else 1
    for idx in range(digit, 14):
        if A[idx] <= 0:
            reductions_left += 1
    max_next = 26 ** reductions_left

    for check in search_order:
        next_z = monad(check, z, a, b, c)
        if c == 26 and next_z > z:
            # need to get smaller on these steps
            continue
        if next_z > max_next:
            # Z can't be reduced down in time
            continue
        ans = solve(digit + 1, next_z, largest)
        if ans == -1:
            continue
        new_answer = (check * 10 ** (14 - digit - 1)) + ans
        cache[digit][z] = new_answer
        return new_answer
    return cache[digit][z]
