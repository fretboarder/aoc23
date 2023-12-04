import re
from pathlib import Path
from typing import TypedDict

from aoc23.support import get_input


class Card(TypedDict):
    id: int
    matches: int


def parse_line(line: str) -> Card:
    cardnum = re.findall(r"\d+", line)[0]
    winning, my_nums = line.split(":")[1].split("|")
    return Card(
        id=int(cardnum),
        matches=len(
            set(re.findall(r"\d+", winning)) & set(re.findall(r"\d+", my_nums))
        ),
    )


def get_worth(pile: list[Card]) -> int:
    """Solution 1."""
    return sum(2 ** (c["matches"] - 1) for c in pile if c["matches"] > 0)


def accumulate(pile: list[Card]) -> int:
    """Solution 2."""
    by_id = {card["id"]: card["matches"] for card in pile}
    final_pile = {cid: 1 for cid, _ in by_id.items()}

    for cardid, matches in by_id.items():
        copies = final_pile[cardid]
        for cid in range(cardid + 1, cardid + 1 + matches):
            final_pile[cid] += copies
    return sum(list(final_pile.values()))


def main[A, B]() -> tuple[A, B]:
    cards = get_input(Path(__file__).parent / "input01.txt", parse_line)
    return get_worth(cards), accumulate(cards)


if __name__ == "__main__":
    sol1, sol2 = main()
    # Solution 1: 24848
    print("Solution 1", sol1)
    # Solution 2: 7258152
    print("Solution 2", sol2)


#   1   2   3   4   5   6   # card ids
#   4   2   2   1   0   0   # matches
# ---------------------------------------
#   1   1   1   1   1   1   start
#   1   2   2   2   2   1   1 has 4 matches -> 1 more copy of 2 3 4 5
#   1   2   4   4   2   1   2 has 2 matches -> 2 more copies of 3 4
#   1   2   4   8   6   1   3 has 2 matches -> 4 more copies of 4 5
#   1   2   4   8  14   1   4 has 1 matches -> 8 more copies of 5
#   1   2   4   8  14   1   5 has 0 matches -> do nothing
#   1   2   4   8  14   1   6 has 0 matches -> do nothing
