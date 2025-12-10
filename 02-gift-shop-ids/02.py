#!/usr/bin/env python3
import argparse
import sys
from itertools import count, takewhile
from typing import TextIO, Iterator


class Range(object):
    def __init__(self, start: int, end: int):
        self.start = start
        self.end = end
    
    def __str__(self):
        return f"{self.start}-{self.end}"

    def contains(self, value: int) -> bool:
        return self.start <= value <= self.end


def get_inputs(fileobj: TextIO) -> list[Range]:
    input_ranges = []
    for line in fileobj:
        line = line.strip()
        if not line:
            continue

        ranges = line.split(',')
        for range in ranges:
            input_ranges.append(Range(*map(int, range.split('-'))))

    return input_ranges


def digit_concatenations(r: Range, ncopies: int=2) -> Iterator[int]:
    length = len(str(r.start))//ncopies
    start = int(str(r.start)[:length]) if length > 0 else 0

    if len(str(r.start)) % ncopies != 0:
        length += ncopies - (len(str(r.start)) % ncopies)
        start = 10**(length-1)

    def make_candidate(i):
        return int(str(i) * ncopies)

    candidates = (make_candidate(i) for i in count(start) if make_candidate(i) >= r.start)
    yield from takewhile(r.contains, candidates)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='02')
    parser.add_argument('file', type=argparse.FileType('r'), default=sys.stdin)
    args = parser.parse_args()

    print("Part 1")

    ranges = get_inputs(args.file)
    tot = 0
    for r in ranges:
        for d in digit_concatenations(r, 2):
            tot += d
    print(tot)

    print("Part 2")
    tot = 0
    for r in ranges:
        invalid_ids = set()
        for ncopies in range(2, len(str(r.end))+1):
            for d in digit_concatenations(r, ncopies):
                invalid_ids.add(d)
        tot += sum(invalid_ids)
    print(tot)