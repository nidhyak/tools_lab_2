#!/usr/bin/env python3
from z3 import (
    And,
    BoolVector,
    Not,
    Or,
    Solver,
    unsat,
    )

### Filenames
KEYSTREAM = 'keystream'

### Extracted from super_cipher.py.enc
N_BYTES = 32
N = 8 * N_BYTES     # 256 bits

def get_seed_with_sat(k_file=KEYSTREAM):
    """Recovers seed used to generate keystream in super_cipher.py using z3
    solver.

    Parameters
    ----------
    k_file : string, optional
        Filename for keystream file
        Defaults to KEYSTREAM

    Returns
    -------
    seed : string
        Seed used to generate keystream

    """
    with open(k_file, 'rb') as key_file:
        keystream = bytearray(key_file.read())
    # extract first set of keystream values
    keystream = int.from_bytes(keystream[:N_BYTES], 'little')
    # convert keystream to bool so we can work in sat dnf bool logic
    keystream = list(map(bool, (map(int, format(keystream, f'0{N}b')))))
    # bool representation of "prev"
    prev = BoolVector('prev', N)
    # "next" representation with dnf constraints
    next = dnf_next(prev)  
    # step backwards N//2 times
    for i in range(N//2):
        # show progress as z3 method is slow
        print(f"{(i+1)/(0.01*(N//2)):.1f}%", end="\r", flush=True)
        keystream = sat_solve_prev(keystream, next, prev)
    # convert bool keystream to bin then int then bytes
    seed = int(''.join(map(str, (map(int, keystream)))), 2)
    seed = seed.to_bytes(N_BYTES, 'little').decode()
    return seed

def sat_solve_prev(keystream, next, prev):
    """Find previous keystream by solving boolean satisfiability problem.

    Parameters
    ----------
    keystream : list of bool
        Current keystream converted to list of boolean representing binary
        values

    next : list of z3.BoolRef
        list containing bit triplet DNF constraints from the original next()

    prev :  list of z3.BoolRef
        list containing bool representation of the previous keystream, to be
        used as an index for Solver().model()

    Returns
    -------
    keystream : list of bool
        bool representation of keystream input from the previous call of next()

    """
    solver = Solver()
    for idx in range(N):
        # add next keystream bools as constraints
        solver.add(next[idx] == keystream[idx])
    # check() should be 'sat' because we know we can get back to seed with
    # these constraints, but we want to catch semantic errors just in case
    if solver.check() == unsat:
        raise Exception('Error in SAT DNF constraints')
    model = solver.model()
    # replace current keystream with solved previous values
    for idx in range(N):
        keystream[idx] = bool(model[prev[idx]])
    return keystream

def dnf_next(x):
    """Converts original next() function to apply DNF constraints to keystream.

    Parameters
    ----------
    x :  list of z3.BoolRef
        list containing bool representation of the keystream

    Returns
    -------
    y : list of z3.BoolRef
        list containing bit triplet DNF constraints from the original next()

    """
    # x = (x & 1) << N+1 | x << 1 | x >> N-1
    # xABCDEFy --> yxABCDEFyx
    x = [x[-1]] + x + [x[0]]
    # y |= RULE[(x >> i) & 7] << i
    # bit triplet constraints are same forwards or backwards, so working
    # forwards means we don't have to reverse the bitstream result later
    y = [dnf_bit_1(x[i], x[i+1], x[i+2]) for i in range(N)]
    return y

def dnf_bit_1(p, q, r):
    """
    Disjunctive Normal Form representation of
        RULE = [86 >> i & 1 for i in range(8)]
    and
        y |= RULE[(x >> i) & 7] << i
    for returning 0b1:
    +----------+------------------+
    | Next Bit | Previous Triplet |
    +==========+==================+
    |          | 001              |
    +          +------------------+
    |          | 010              |
    +    1     +------------------+
    |          | 100              |
    +          +------------------+
    |          | 110              |
    +----------+------------------+

    Parameters
    ----------
    p, q, r : z3.BoolRef
        BoolRef representations of 3 consecutive bits in keystream

    Returns
    -------
    y : z3.BoolRef
        BoolRef representation of constraints for that particular bit

    """
    return Or(
        And(Not(p), Not(q), r),
        And(Not(p), q, Not(r)),
        And(p, Not(q), Not(r)),
        And(p, q, Not(r))
    )

def main():
    print("Recovering seed value...")
    print(f"  Seed value: {get_seed_with_sat()}")

if __name__ == '__main__':
    main()
