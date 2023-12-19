from __future__ import annotations

from abc import ABC
from dataclasses import dataclass
from pathlib import Path
from pprint import pp
from typing import Literal

from aoc23.support import get_input


class Expr(ABC):
    pass


@dataclass
class LessThan(Expr):
    op1: str
    op2: int


@dataclass
class GreaterThan(Expr):
    op1: str
    op2: int


@dataclass
class Or(Expr):
    op1: Expr
    op2: Expr


class Always(Expr):
    pass


@dataclass
class Target:
    name: str  # a name


@dataclass
class Cond:
    expr: Expr
    target: Target


@dataclass
class Instr:
    cond: list[Cond]


def parse_cond(cstr: str) -> Cond:
    cond, tgt = cstr.split(":")
    var = cond[0]
    op = cond[1]
    val = int(cond[2:])
    if op == "<":
        return Cond(LessThan(var, val), Target(tgt))
    return Cond(GreaterThan(var, val), Target(tgt))


def parse_instruction(line: str) -> tuple[str, Instr]:
    name, rest = line.replace(r"}", "").split(r"{")
    conds = rest.split(",")
    conditions = [parse_cond(c) for c in conds[:-1]]
    conditions.append(Cond(Always(), Target(conds[-1])))
    return name, Instr(conditions)


Rating = dict[str, int]


def parse_input(lines: list[str]) -> tuple[dict[str, Instr], list[Rating]]:
    instructions: list[tuple[str, Instr]] = []

    for i, line in enumerate(lines):
        if line == "":
            break
        instructions.append(parse_instruction(line))

    i += 1
    ratings: list[Rating] = []
    for line in lines[i:]:
        keyvals = line.replace(r"{", "").replace(r"}", "").split(",")
        inp = {}
        for kv in keyvals:
            k, v = kv.split("=")
            inp |= {k: int(v)}
        ratings.append(inp)

    return dict(instructions), ratings


def evaluate(rating: Rating, instr: Instr) -> Target:
    for c in instr.cond:
        match c:
            case Cond(LessThan(var, val), target):
                if rating[var] < val:
                    return target
            case Cond(GreaterThan(var, val), target):
                if rating[var] > val:
                    return target
            case Cond(Always(), target):
                return target
    msg = "This shouldn't happen"
    raise ValueError(msg)


def solution(instructions: dict[str, Instr], vals: list[Rating]) -> int:
    def eval_accept(instr: Instr, inp: Rating) -> Literal["A", "R"]:
        match evaluate(inp, instr):
            case Target(term) if term in ("A", "R"):
                return term
            case Target(next_instr):
                return eval_accept(instructions[next_instr], inp)

    results = []
    for inp in vals:
        instr = instructions["in"]
        result = eval_accept(instr, inp)
        results.append((inp, result, sum(inp.values())))

    pp(results, indent=4)

    return sum(r for _, t, r in results if t == "A")


def main() -> tuple[int, int]:
    instr, vals = parse_input(get_input(Path(__file__).parent / "input01.txt"))
    return solution(instr, vals), 0  # solution(lines)


if __name__ == "__main__":
    sol1, sol2 = main()
    pp(f"Solution 1: {sol1}")
    pp(f"Solution 2: {sol2}")  # check main2.py
