from __future__ import annotations

from abc import ABC, abstractmethod
from collections import defaultdict, deque
from dataclasses import dataclass, field
from pathlib import Path
from pprint import pp
from typing import Protocol, TypedDict, cast

import graphviz
from aoc23.support import get_input

LOW = 0
HIGH = 1


Pulse = int


class CompAttr(TypedDict):
    comp: Module
    targets: list[str]


Circuit = dict[str, CompAttr]


def circuit_graph(c: Circuit) -> graphviz.Digraph:
    # Create a graph
    dot = graphviz.Digraph(comment="Circuit")

    visited: set[Module] = set()
    root = c["button"]["comp"]
    frontier: deque[tuple[int, Module]] = deque([(0, root)])
    while frontier:
        indent, current = frontier.pop()
        if current in visited:
            continue
        visited.add(current)
        shape = (
            "square"
            if isinstance(current, Flop)
            else "hexagon"
            if isinstance(current, Con)
            else "triangle"
        )
        if isinstance(current, Con) and len(current.inputs) == 1:
            shape = "cds"
        col = "red" if current.state == LOW else "blue"
        dot.node(
            current.name,
            shape=shape,
            label=f"{current.__class__.__name__}({current.name})",
            color=col,
        )

        for ch in current.outputs:
            dot.edge(current.name, ch.name)
            frontier.append((indent + 2, ch))

    return dot


def parse_input(lines: list[str]) -> Circuit:
    comptype = {"&": Con, "%": Flop, "broadcaster": Broadcast}
    logic: dict[str, CompAttr] = {
        "button": CompAttr(comp=Button("button"), targets=["broadcaster"]),
        "output": CompAttr(comp=Output("output"), targets=[]),
        "rx": CompAttr(comp=Reset("rx"), targets=[]),
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


class Module(ABC):
    def __init__(self, name: str) -> None:
        self._name = name
        self._outputs: list[Module] = []
        self._inputs: list[Module] = []
        self._state: Pulse = LOW

    def __hash__(self) -> int:
        return hash(self.name)

    def add_out(self, comp: Module) -> None:
        self.outputs.append(comp)

    def pulse(self, p: Pulse) -> None:
        self._state = p

    def emit(self) -> Pulse:
        return self._state

    @abstractmethod
    def add_in(self, comp: Module) -> None:
        ...

    @property
    def state(self) -> Pulse:
        return self._state

    @property
    def name(self) -> str:
        return self._name

    @property
    def outputs(self) -> list[Module]:
        return self._outputs

    @property
    def inputs(self) -> list[Module]:
        return self._inputs


class Output(Module):
    def add_in(self, comp: Module) -> None:
        self._inputs = [comp]


class Reset(Module):
    def add_out(self, comp: Module) -> None:
        raise NotImplementedError

    def add_in(self, comp: Module) -> None:
        self._inputs = [comp]


class Button(Module):
    def __init__(self, name: str) -> None:
        super().__init__(name)
        self._state: Pulse = HIGH

    def add_in(self, comp: Module) -> None:
        raise NotImplementedError

    def emit(self) -> Pulse:
        return LOW


class Broadcast(Module):
    def add_in(self, comp: Module) -> None:
        self._inputs = [comp]


class Flop(Module):
    def add_in(self, comp: Module) -> None:
        self._inputs = [comp]

    def pulse(self, p: Pulse) -> None:
        # pp(f"  FF {self.name} received {p} in state {self.state}")
        if p == LOW:
            self._state = HIGH if self._state == LOW else LOW
        # pp(f"  FF {self.name} transitioned to state {self.state}")


class Con(Module):
    def __init__(self, name: str) -> None:
        super().__init__(name)
        self._inputs: dict[Module, Pulse] = {}

    def add_in(self, comp: Module) -> None:
        self._inputs[comp] = LOW

    def pulse(self, comp: Module, p: Pulse) -> None:
        self._inputs[comp] = p
        self._state = LOW if all(self._inputs.values()) else HIGH


def solution1(circuit: Circuit) -> int:
    sig_count = defaultdict(lambda: 0)

    for _ in range(1000):
        root = circuit["button"]["comp"]
        frontier = deque([root])

        while frontier:
            current = frontier.popleft()
            for c in current.outputs:
                emitted = current.emit()
                sig_count[emitted] += 1
                if isinstance(c, Con):
                    cast(Con, c).pulse(current, emitted)
                else:
                    c.pulse(emitted)
                # add the node only if it can emit a pulse, e.g. a FlipFlop receiving HIGH
                # doesn't emit!
                if not isinstance(c, Flop) or (isinstance(c, Flop) and emitted == LOW):
                    frontier.append(c)

    return sig_count[0] * sig_count[1]


def solution2(circuit: Circuit) -> int:
    # circuit_graph(circuit).view()
    return 0


def main() -> tuple[int, int]:
    lines = get_input(Path(__file__).parent / "input01.txt")
    return solution1(parse_input(lines)), solution2(parse_input(lines))


if __name__ == "__main__":
    sol1, sol2 = main()
    pp(f"Solution 1: {sol1}")
    pp(f"Solution 2: {sol2}")  # check main2.py
