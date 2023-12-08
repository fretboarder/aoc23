import pytest
from aoc23.aoc05 import main as d05


def test_concat_range():
    assert d05.concat_range(range(1, 10), range(10, 25)) == range(1, 25)
    assert d05.concat_range(range(10, 25), range(1, 10)) == range(1, 25)
    assert d05.concat_range(range(10, 25), range(12, 23)) == range(10, 25)
    assert d05.concat_range(range(12, 23), range(10, 25)) == range(10, 25)
    with pytest.raises(ValueError):
        d05.concat_range(range(1, 2), range(3, 4))


def test_is_continuous():
    assert d05.is_continuous(range(1, 10), range(10, 25)) == True
    assert d05.is_continuous(range(10, 25), range(1, 10)) == True
    assert d05.is_continuous(range(10, 25), range(12, 23)) == True
    assert d05.is_continuous(range(12, 23), range(10, 25)) == True
    assert d05.is_continuous(range(1, 2), range(3, 4)) == False


def test_remove_range():
    seed = range(79, 93)
    assert d05.remove_ranges(seed, range(79, 93)) == ()
    assert d05.remove_ranges(seed, range(79, 85)) == (range(85, 93),)
    assert d05.remove_ranges(seed, range(68, 85)) == (range(85, 93),)
    assert d05.remove_ranges(seed, range(85, 93)) == (range(79, 85),)
    assert d05.remove_ranges(seed, range(85, 99)) == (range(79, 85),)
    assert d05.remove_ranges(seed, range(85, 89)) == (range(79, 85), range(89, 93))
    assert d05.remove_ranges(seed, range(79, 85)) == (range(85, 93),)


def test_remove_non_continuous():
    r1 = d05.remove_ranges(range(50, 100), range(60, 70), range(80, 90))
    assert r1 == (range(50, 60), range(70, 80), range(90, 100))
    assert d05.remove_ranges(range(50, 100), range(60, 70)) == (
        range(50, 60),
        range(70, 100),
    )
    assert d05.remove_ranges(range(50, 100), range(50, 60)) == (range(60, 100),)


def test_collect_mappings_no_mapping():
    seed = range(100, 150)
    mapper = d05.Mapper(
        "seed-to-soil", (d05.Mapping(52, 50, 48), d05.Mapping(50, 98, 2))
    )
    res = d05.collect_mappings(mapper, seed)
    assert res == ([], [range(100, 150)])


def test_collect_mappings_all_mapped_in_one_range():
    seed = range(79, 93)
    mapper = d05.Mapper(
        "seed-to-soil", (d05.Mapping(52, 50, 48), d05.Mapping(50, 98, 2))
    )
    res = d05.collect_mappings(mapper, seed)
    assert res == ([range(79, 93)], [])


def test_collect_mappings_all_mapped_in_two_ranges():
    seed = range(79, 93)
    mapper = d05.Mapper(
        "seed-to-soil", (d05.Mapping(52, 50, 38), d05.Mapping(50, 88, 6))
    )
    res = d05.collect_mappings(mapper, seed)
    assert res == ([range(88, 93), range(79, 88)], [])


def test_collect_mappings_one_partially_mapped():
    seed = range(45, 55)
    mapper = d05.Mapper(
        "seed-to-soil", (d05.Mapping(52, 50, 48), d05.Mapping(50, 98, 2))
    )
    res = d05.collect_mappings(mapper, seed)
    assert res == ([range(50, 55)], [range(45, 50)])


def test_collect_mappings_two_partially_mapped():
    seed = range(45, 93)
    mapper = d05.Mapper(
        "seed-to-soil", (d05.Mapping(52, 50, 38), d05.Mapping(50, 88, 6))
    )
    res = d05.collect_mappings(mapper, seed)
    assert res == ([range(88, 93), range(50, 88)], [range(45, 50)])


def test_collect_mappings_two_partially_mapped_two_unmapped():
    seed = range(45, 100)
    mapper = d05.Mapper(
        "seed-to-soil", (d05.Mapping(52, 50, 38), d05.Mapping(50, 88, 6))
    )
    res = d05.collect_mappings(mapper, seed)
    assert res == ([range(50, 88), range(88, 94)], [range(45, 50), range(94, 100)])


def test_collect_mappings_non_continuous_mapping_ranges():
    seed = range(45, 100)
    mapper = d05.Mapper(
        # gap between 78 and 88
        "seed-to-soil",
        (d05.Mapping(52, 50, 28), d05.Mapping(50, 88, 6)),
    )
    res = d05.collect_mappings(mapper, seed)
    assert res == (
        [range(88, 94), range(50, 78)],
        [range(45, 50), range(78, 88), range(94, 100)],
    )
