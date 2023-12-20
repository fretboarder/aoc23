from __future__ import annotations

import time
from abc import ABC
from collections import defaultdict, deque
from dataclasses import dataclass, field
from hashlib import new
from pathlib import Path
from pprint import pp
from typing import Literal, NamedTuple, Protocol, TypedDict, cast

from aoc23.support import get_input

LOW = 0
HIGH = 1


OFF = 0
ON = 1

Pulse = int


class Comp(Protocol):
    def add_out(self, comp: Comp) -> None:
        ...

    def add_in(self, comp: Comp) -> None:
        ...

    def emit(self) -> Pulse:
        ...

    def pulse(self, p: Pulse) -> None:
        ...

    @property
    def state(self) -> Pulse:
        ...

    @property
    def name(self) -> str:
        ...

    @property
    def outputs(self) -> list[Comp]:
        ...

    @property
    def inputs(self) -> list[Comp]:
        ...


@dataclass
class Output:
    name: str
    outputs: list[Comp] = field(init=False, default_factory=list)
    inputs: list[Comp] = field(init=False, default_factory=list)
    state: Pulse = LOW

    def pulse(self, p: Pulse) -> None:
        self.state = p

    def add_out(self, comp: Comp) -> None:
        pass

    def add_in(self, comp: Comp) -> None:
        self.inputs = [comp]

    def emit(self) -> Pulse:
        return self.state


@dataclass
class Button:
    name: str
    outputs: list[Comp] = field(init=False, default_factory=list)
    inputs: list[Comp] = field(init=False, default_factory=list)
    state: Pulse = HIGH

    def __hash__(self) -> int:
        return hash(self.name)

    def add_out(self, comp: Comp) -> None:
        self.outputs = [comp]

    def add_in(self, comp: Comp) -> None:
        pass

    def emit(self) -> Pulse:
        return LOW


@dataclass
class Broadcast:
    name: str
    inputs: list[Comp] = field(init=False, default_factory=list)
    outputs: list[Comp] = field(init=False, default_factory=list)
    state: Pulse = LOW

    def __hash__(self) -> int:
        return hash(self.name)

    def add_out(self, comp: Comp) -> None:
        self.outputs.append(comp)

    def add_in(self, comp: Comp) -> None:
        self.inputs = [comp]

    def pulse(self, p: Pulse) -> None:
        self.state = p

    def emit(self) -> Pulse:
        return self.state


@dataclass
class FlipFlop:
    name: str
    inputs: list[Comp] = field(init=False, default_factory=list)
    outputs: list[Comp] = field(init=False, default_factory=list)
    state: Pulse = LOW

    def __hash__(self) -> int:
        return hash(self.name)

    def add_out(self, comp: Comp) -> None:
        self.outputs.append(comp)

    def add_in(self, comp: Comp) -> None:
        self.inputs = [comp]

    def pulse(self, p: Pulse) -> None:
        pp(f"  FF {self.name} received {p} in state {self.state}")
        if p == LOW:
            self.state = HIGH if self.state == LOW else LOW
        pp(f"  FF {self.name} transitioned to state {self.state}")

    def emit(self) -> Pulse:
        return self.state


@dataclass
class Con:
    name: str
    outputs: list[Comp] = field(init=False, default_factory=list)
    inputs: dict[Comp, Pulse] = field(init=False, default_factory=dict)
    state: Pulse = LOW

    def __hash__(self) -> int:
        return hash(self.name)

    def add_out(self, comp: Comp) -> None:
        self.outputs.append(comp)

    def add_in(self, comp: Comp) -> None:
        self.inputs[comp] = OFF

    def pulse(self, comp: Comp, p: Pulse) -> None:
        self.inputs[comp] = p
        self.state = LOW if all(self.inputs.values()) else HIGH

    def emit(self) -> Pulse:
        return self.state


def solution1(circuit: Circuit) -> int:
    def circuit_state() -> dict[str, Pulse]:
        return {
            comp: attr["comp"].state
            for comp, attr in circuit.items()
            if isinstance(attr["comp"], FlipFlop)
        }

    total_signals = []

    sig_count = defaultdict(lambda: 0)

    for i in range(1000):
        pp(f"=============== ITERATION PUSH {i+1} ==================")
        iteration_signals = []
        root = circuit["button"]["comp"]
        frontier = deque([root])

        while frontier:
            current = frontier.popleft()

            for c in current.outputs:
                emitted = current.emit()
                sig_count[emitted] += 1
                sig = f"{current.name} -{("low" if not emitted else "high")}-> {c.name}"
                pp(sig)
                iteration_signals.append(sig)
                if isinstance(c, Con):
                    cast(Con, c).pulse(current, emitted)
                else:
                    c.pulse(emitted)

                # add the node only if it can emit a signal, e.g. a FlipFlop receiving HIGH
                # doesn't do anything
                if not isinstance(c, FlipFlop) or (
                    isinstance(c, FlipFlop) and emitted == LOW
                ):
                    # if not isinstance(current, Broadcast) or i == 0:if
                    frontier.append(c)

        # if we end up here, there's obviously no loop
        new_sigs = ",".join(iteration_signals)
        if new_sigs not in total_signals:
            total_signals.append(new_sigs)
        else:
            pp("=============== SEEN THIS PATTERN BEFORE ==================")
            pp(new_sigs)
            pp(total_signals.index(new_sigs))

    return sig_count[0] * sig_count[1]


def solution2(lines: list[str]) -> int:
    return 0


class CompAttr(TypedDict):
    comp: Comp
    targets: list[str]


Circuit = dict[str, CompAttr]


def parse_input(lines: list[str]) -> Circuit:
    comptype = {"&": Con, "%": FlipFlop, "broadcaster": Broadcast}
    logic: dict[str, CompAttr] = {
        "button": CompAttr(comp=Button("button"), targets=["broadcaster"]),
        "output": CompAttr(comp=Output("output"), targets=[]),
        "rx": CompAttr(comp=Output("rx"), targets=[]),
    }
    for line in lines:
        name, *targets = line.replace(" -> ", ",").replace(" ", "").split(",")
        key = name[1:] if name[0] in ("&", "%") else name
        tkey = name[0] if name[0] in ("&", "%") else name
        logic[key] = CompAttr(comp=comptype[tkey](key), targets=targets)

    # create the circuit
    for parent, attr in logic.items():
        for output in attr["targets"]:
            if logic[output]["comp"] not in logic[parent]["comp"].outputs:
                logic[parent]["comp"].add_out(logic[output]["comp"])
            # set the inputs
            logic[output]["comp"].add_in(logic[parent]["comp"])

    return logic


def main() -> tuple[int, int]:
    lines = get_input(Path(__file__).parent / "input01.txt")
    return solution1(parse_input(lines)), solution2(lines)


if __name__ == "__main__":
    sol1, sol2 = main()
    pp(f"Solution 1: {sol1}")
    pp(f"Solution 2: {sol2}")  # check main2.py
