from collections import Counter
from dataclasses import dataclass, field
from itertools import groupby
from pathlib import Path
from pprint import pp

from aoc23.support import get_input

CARD_MAP_1 = {"T": 10, "J": 11, "Q": 12, "K": 13, "A": 14}
CARD_MAP_1.update({str(c): c for c in range(2, 10)})
CARD_MAP_2 = {**CARD_MAP_1, "J": 1}


class HandType(Enum):
    HIGH_CARD = 0
    ONE_PAIR = 1
    TWO_PAIRS = 2
    THREE_OF_A_KIND = 3
    FULL_HOUSE = 4
    FOUR_OF_A_KIND = 5
    FIVE_OF_A_KIND = 6


@dataclass
class Cards:
    hand: list[int]
    bid: int
    hand_type: HandType = field(init=False)
    high_card: int = field(init=False)
    joker_hand: list[int] = field(init=False)
    joker_hand_type: HandType = field(init=False)

    @staticmethod
    def _get_hand_type(hand: list[int]) -> tuple[HandType, int]:
        grouped_hand = [list(g) for _, g in groupby(sorted(hand))]
        match len(grouped_hand):
            case 5:
                hand_type = HandType.HIGH_CARD
                high_card = max(hand)
            case 4:
                hand_type = HandType.ONE_PAIR
                high_card = Counter(hand).most_common()[0][0]
                if high_card == 1:
                    # pair must not be the joker
                    high_card = max(Counter(hand).keys())
            case 3:
                # three of a kind or two pairs
                if 3 in [len(c) for c in grouped_hand]:
                    hand_type = HandType.THREE_OF_A_KIND
                    high_card = Counter(hand).most_common()[0][0]
                    if high_card == 1:
                        # triple must not be the joker
                        high_card = max(Counter(hand).keys())
                else:
                    hand_type = HandType.TWO_PAIRS
                    if Counter(hand).most_common()[-1][0] == 1:
                        # the single card is a joker -> 3-of-a-kind
                        high_card = max(v for v, n in Counter(hand).most_common()[:2])
                    else:
                        # two pairs can be converted -> 4-of-a-kind with joker
                        high_card = max(
                            [
                                val
                                for val, cnt in Counter(hand).most_common()
                                if cnt == 2
                            ]
                        )

            case 2:
                # full_house or four of a kind
                if 4 in [len(c) for c in grouped_hand]:
                    hand_type = HandType.FOUR_OF_A_KIND
                else:
                    hand_type = HandType.FULL_HOUSE
                high_card = Counter(hand).most_common()[0][0]
                if high_card == 1:
                    # must not be the joker
                    high_card = max(Counter(hand).keys())
            case 1:
                hand_type = HandType.FIVE_OF_A_KIND
                high_card = hand[0]
            case _:
                raise ValueError("this is not expected!")
        return hand_type, high_card

    def _handle_jokers(self):
        c = Counter(self.hand)
        if 1 not in c:
            self.joker_hand = self.hand
            self.joker_hand_type = self.hand_type
            return
        self.joker_hand = list(
            map(lambda c: self.high_card if c == 1 else c, self.hand)
        )
        self.joker_hand_type, _ = Cards._get_hand_type(self.joker_hand)

    def __post_init__(self):
        self.hand_type, self.high_card = Cards._get_hand_type(self.hand)
        self._handle_jokers()

    def __eq__(self, other) -> bool:
        # hands are considered equal if they are of same type
        return self.joker_hand_type.value == other.joker_hand_type.value

    def __lt__(self, other) -> bool:
        is_less = self.hand < other.hand
        return (
            is_less
            if self == other
            else self.joker_hand_type.value < other.joker_hand_type.value
        )


def parse_line(card_map: dict[str, int]):
    def parse(line: str) -> Cards:
        hand, bid = line.split()
        return Cards([card_map[c] for c in hand], int(bid))

    return parse


def solution1(cards: list[Cards]) -> int:
    return sum([rank * c.bid for rank, c in enumerate(sorted(cards), start=1)])


def solution2(cards: list[Cards]) -> int:
    return sum([rank * c.bid for rank, c in enumerate(sorted(cards), start=1)])


def main[A, B]() -> tuple[A, B]:
    cards1 = get_input(Path(__file__).parent / "input01.txt", parse_line(CARD_MAP_1))
    cards2 = get_input(Path(__file__).parent / "input01.txt", parse_line(CARD_MAP_2))
    return solution1(cards1), solution2(cards2)


if __name__ == "__main__":
    sol1, sol2 = main()
    # Solution 1: 250453939
    pp(f"Solution 1: {sol1}")
    # Solution 2: 248652697
    pp(f"Solution 2: {sol2}")
