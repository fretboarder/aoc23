from pathlib import Path

from aoc23.support import get_input

dstrings = {
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9",
}


def dstring_to_digits(line: str) -> str:
    i, res = 0, ""
    while i < len(line):
        char, advance = line[i], 1
        for d, v in dstrings.items():
            if line[i : i + len(d)] == d:
                char, advance = v, len(d) - 1  # to detect e.g. "eighthree" as 83
                break
        res += char
        i += advance
    return res


def line_to_value(line: str) -> int:
    digits = [c for c in line if c.isdigit()]
    return int(digits[0] + digits[-1]) if len(digits) else 0


def main[A, B]() -> tuple[A, B]:
    lines1 = get_input(Path(__file__).parent / "input01.txt")
    lines2 = get_input(Path(__file__).parent / "input02.txt")
    return sum(line_to_value(line) for line in lines1), sum(
        line_to_value(dstring_to_digits(line)) for line in lines2
    )


if __name__ == "__main__":
    sol1, sol2 = main()
    print("Solution 1", sol1)
    print("Solution 2", sol2)
