from collections import defaultdict
import itertools
import math
from parse import compile
import typing as t
import aocd

from utils import only


Range = t.Set[int]
Sections = t.Dict[str, Range]
Ticket = t.List[int]
Tickets = t.List[Ticket]
InputData = t.Tuple[Sections, Ticket, Tickets]


range_parser = compile("{location}: {r1s:d}-{r1e:d} or {r2s:d}-{r2e:d}")


def parse_input(
    data: str,
) -> InputData:
    sections: Sections = {}
    ticket: Ticket = []
    tickets: Tickets = []

    section_strings, your_ticket, nearby_tickets = data.split("\n\n")
    for sect in section_strings.splitlines():
        named = range_parser.parse(sect).named
        sections[named["location"]] = set(
            itertools.chain(
                range(named["r1s"], named["r1e"] + 1), range(named["r2s"], named["r2e"] + 1)
            )
        )

    ticket = [int(num) for num in your_ticket.splitlines()[1].split(",")]
    tickets = [[int(num) for num in tx.split(",")] for tx in nearby_tickets.splitlines()[1:]]

    return sections, ticket, tickets


def part_one(sections: Sections, your_ticket: Ticket, nearby: Tickets) -> int:
    valid = set(itertools.chain(*sections.values()))
    return sum(itertools.chain(*(set(ticket) - valid for ticket in nearby)))


def part_two(sections: Sections, your_ticket: Ticket, nearby: Tickets) -> int:
    valid_ranges = set(itertools.chain(*sections.values()))
    valid_tickets = [ticket for ticket in nearby if not set(ticket) - valid_ranges] + [your_ticket]

    columns: t.List[Range] = [
        {ticket[n] for ticket in valid_tickets} for n in range(len(your_ticket))
    ]
    candidates: t.Dict[str, t.Set[int]] = defaultdict(set)

    # multiple candidates for each section
    for section, valid_range in sections.items():
        for idx, column in enumerate(columns):
            if not column - valid_range:
                candidates[section].add(idx)

    # solve from smallest to largest
    section_names = sorted(candidates, key=lambda k: len(candidates[k]))
    for n, section_name in enumerate(section_names, 1):
        if not len(candidates[section_name]) == 1:
            raise ValueError("Go recurse all possibles")
        section_position = only(candidates[section_name])
        # section now allocated, remove candidate from other sections
        for wrong_name in section_names[n:]:
            candidates[wrong_name].discard(section_position)

    return math.prod(
        your_ticket[only(column)]
        for section, column in candidates.items()
        if section.startswith("departure")
    )


if __name__ == "__main__":
    data = aocd.get_data(day=16, year=2020)
    sections, ticket, tickets = parse_input(data)
    print("Part 1: ", part_one(sections, ticket, tickets))
    print("Part 2: ", part_two(sections, ticket, tickets))
