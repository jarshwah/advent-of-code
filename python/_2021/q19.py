import ast
import itertools
import math
import typing
from collections import Counter

import aocd

from utils import rotations_90

Point3d = tuple[int, int, int]
Points = list[Point3d]


def parse_report(data: str) -> list[Points]:
    scanners = []
    for scanner_report in data.split("\n\n"):
        scanners.append([ast.literal_eval(line) for line in scanner_report.splitlines()[1:]])
    return scanners


def manhattan(p1: Point3d, p2: Point3d) -> int:
    return sum(abs(a - b) for a, b in zip(p1, p2))


def sub_vector(p1: Point3d, p2: Point3d) -> Point3d:
    return tuple([a - b for a, b in zip(p1, p2)])  # type: ignore


def add_vector(p1: Point3d, p2: Point3d) -> Point3d:
    return tuple([a + b for a, b in zip(p1, p2)])  # type: ignore


def count_shift_vectors(points: Points, origin: Points) -> typing.Counter[Point3d]:
    """
    Calculate the shift vectors between all points and origin.
    """
    counter = Counter()
    for point in points:
        for origin_point in origin:
            shifted = sub_vector(origin_point, point)
            counter[shifted] += 1
    return counter


def reorient_to(points: Points, origin: Points) -> tuple[Points, Point3d]:
    """
    Iterate through all rotations of `points`, computing the count of difference
    vectors between the rotated points and `origin`. A matched rotation will have
    at least 12 common difference vectors. Use the common difference vector to
    shift all rotated points towards the origin.
    """
    rotations = zip(*[rotations_90(point) for point in points])
    for rotated_points in rotations:
        shifted_vector, matched = count_shift_vectors(rotated_points, origin).most_common()[0]
        if matched >= 12:
            new_points = [add_vector(shifted_vector, rot) for rot in rotated_points]
            return new_points, shifted_vector
    raise ValueError("No rotations matched")


def solve(data: str) -> tuple[int, int]:
    scanners = parse_report(data)
    distances = []
    fingerprint_threshold = math.comb(12, 2)

    # Compute the manhattan distance between all points of a scanner. No matter
    # the orientation, the distance will be the same for overlapping points. Compare
    # distances between scanners, keeping any greater than the fingerprint threshold. This
    # allows us to build a graph of overlaps that we can re-orient in order.
    for scanner in scanners:
        differences = set()
        for p1 in scanner:
            for p2 in scanner:
                m = manhattan(p1, p2)
                if m != 0:
                    differences.add(m)
        distances.append(differences)

    # Use the distances to compute overlapping scanners {scanner index: [list of overlapping scanner indexes]}
    overlapping: dict[int, list[int]] = {}
    for idx1, distance in enumerate(distances):
        overlapping[idx1] = []
        for idx2, compare in enumerate(distances):
            if idx1 == idx2:
                continue
            matches = len(distance & compare)
            if matches >= fingerprint_threshold:
                overlapping[idx1].append(idx2)

    # The first scanner is correctly oriented
    reoriented = {0: scanners[0]}
    scanner_locations: list[Point3d] = [(0, 0, 0)]
    while len(reoriented) != len(scanners):
        # For non-reoriented scanners, find a reoriented scanner we overlap with
        # and attempt to reorient to that.
        for idx, scanner in enumerate(scanners):
            if idx in reoriented:
                continue
            for match in overlapping[idx]:
                if match in reoriented:
                    reoriented_points, scanner_position = reorient_to(scanner, reoriented[match])
                    reoriented[idx] = reoriented_points
                    scanner_locations.append(scanner_position)
    num_beacons = len(set(itertools.chain(*reoriented.values())))
    max_scanner_distance = max(
        manhattan(combo[0], combo[1]) for combo in itertools.combinations(scanner_locations, 2)
    )
    # print(f"{num_beacons=} {max_scanner_distance=}")
    return num_beacons, max_scanner_distance


def test():
    test_input = get_test_report()
    p1, p2 = solve(test_input)
    assert p1 == 79, p1
    assert p2 == 3621, p2


def get_test_report() -> str:
    return """--- scanner 0 ---
404,-588,-901
528,-643,409
-838,591,734
390,-675,-793
-537,-823,-458
-485,-357,347
-345,-311,381
-661,-816,-575
-876,649,763
-618,-824,-621
553,345,-567
474,580,667
-447,-329,318
-584,868,-557
544,-627,-890
564,392,-477
455,729,728
-892,524,684
-689,845,-530
423,-701,434
7,-33,-71
630,319,-379
443,580,662
-789,900,-551
459,-707,401

--- scanner 1 ---
686,422,578
605,423,415
515,917,-361
-336,658,858
95,138,22
-476,619,847
-340,-569,-846
567,-361,727
-460,603,-452
669,-402,600
729,430,532
-500,-761,534
-322,571,750
-466,-666,-811
-429,-592,574
-355,545,-477
703,-491,-529
-328,-685,520
413,935,-424
-391,539,-444
586,-435,557
-364,-763,-893
807,-499,-711
755,-354,-619
553,889,-390

--- scanner 2 ---
649,640,665
682,-795,504
-784,533,-524
-644,584,-595
-588,-843,648
-30,6,44
-674,560,763
500,723,-460
609,671,-379
-555,-800,653
-675,-892,-343
697,-426,-610
578,704,681
493,664,-388
-671,-858,530
-667,343,800
571,-461,-707
-138,-166,112
-889,563,-600
646,-828,498
640,759,510
-630,509,768
-681,-892,-333
673,-379,-804
-742,-814,-386
577,-820,562

--- scanner 3 ---
-589,542,597
605,-692,669
-500,565,-823
-660,373,557
-458,-679,-417
-488,449,543
-626,468,-788
338,-750,-386
528,-832,-391
562,-778,733
-938,-730,414
543,643,-506
-524,371,-870
407,773,750
-104,29,83
378,-903,-323
-778,-728,485
426,699,580
-438,-605,-362
-469,-447,-387
509,732,623
647,635,-688
-868,-804,481
614,-800,639
595,780,-596

--- scanner 4 ---
727,592,562
-293,-554,779
441,611,-461
-714,465,-776
-743,427,-804
-660,-479,-426
832,-632,460
927,-485,-438
408,393,-506
466,436,-512
110,16,151
-258,-428,682
-393,719,612
-211,-452,876
808,-476,-593
-575,615,604
-485,667,467
-680,325,-822
-627,-443,-432
872,-547,-609
833,512,582
807,604,487
839,-516,451
891,-625,532
-652,-548,-490
30,-46,-14"""


if __name__ == "__main__":
    test()
    data = aocd.get_data(day=19, year=2021)
    p1, p2 = solve(data)
    print("Part 1: ", p1)
    print("Part 2: ", p2)
