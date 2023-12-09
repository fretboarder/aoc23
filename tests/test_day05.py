from aoc23.aoc05 import main as d05


def test_mapper_smaller_range():
    seed = range(1, 9)
    mapper = d05.Mapper(
        # gap at range(23, 25)
        "seed-to-soil",
        (d05.Mapping(112, 12, 10), d05.Mapping(225, 25, 10)),
    )
    result = mapper.process(seed)
    assert result == [range(1, 9)]


def test_mapper_larger_range():
    seed = range(100, 900)
    mapper = d05.Mapper(
        # gap at range(23, 25)
        "seed-to-soil",
        (d05.Mapping(112, 12, 10), d05.Mapping(225, 25, 10)),
    )
    result = mapper.process(seed)
    assert result == [range(100, 900)]


def test_mapper_superrange():
    seed = range(10, 31)
    mapper = d05.Mapper(
        # gap at range(23, 25)
        "seed-to-soil",
        (d05.Mapping(112, 12, 10), d05.Mapping(225, 25, 10)),
    )
    result = mapper.process(seed)
    assert result == [range(10, 12), range(112, 122), range(22, 25), range(225, 231)]


def test_mapper_range_in_gap():
    seed = range(23, 25)
    mapper = d05.Mapper(
        # gap at range(23, 25)
        "seed-to-soil",
        (d05.Mapping(112, 12, 10), d05.Mapping(225, 25, 10)),
    )
    result = mapper.process(seed)
    assert result == [range(23, 25)]


def test_mapper_range_stops_in_first_channel():
    seed = range(5, 15)
    mapper = d05.Mapper(
        # gap at range(23, 25)
        "seed-to-soil",
        (d05.Mapping(112, 12, 10), d05.Mapping(225, 25, 10)),
    )
    result = mapper.process(seed)
    assert result == [range(5, 12), range(112, 115)]


def test_mapper_range_starts_in_first_channel_and_stops_in_gap():
    seed = range(15, 24)
    mapper = d05.Mapper(
        # gap at range(23, 25)
        "seed-to-soil",
        (d05.Mapping(112, 12, 10), d05.Mapping(225, 25, 10)),
    )
    result = mapper.process(seed)
    assert result == [range(115, 122), range(22, 24)]


def test_mapper_range_covers_second_channel():
    seed = range(25, 36)
    mapper = d05.Mapper(
        # gap at range(23, 25)
        "seed-to-soil",
        (d05.Mapping(112, 12, 10), d05.Mapping(225, 25, 10)),
    )
    result = mapper.process(seed)
    assert result == [range(225, 235)]
