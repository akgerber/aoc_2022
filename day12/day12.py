from dataclasses import dataclass

START_CHAR = 'S'
END_CHAR = 'E'

@dataclass(frozen=True)
class HillMap:
    elevations: list[list[int]]
    start: tuple[int, int]
    end: tuple[int, int]
    num_positions: int
    width: int
    height: int


def prepare_input(lines: list[str]) -> HillMap:
    start = None
    end = None
    num_chars_seen = 0
    assert(len(lines) > 0)
    first_line_len = len(lines[0])
    elevations = []
    for y, line in enumerate(lines):
        assert(len(line) == first_line_len)
        elev_line = []
        for x, c in enumerate(line):
            if c == START_CHAR:
                start = (x,y)
                elev_line.append(ord('a') - ord('a'))
            elif c == END_CHAR:
                end = (x,y)
                elev_line.append(ord('z') - ord('a'))
            else:
                elev_line.append(ord(c) - ord('a'))
        elevations.append(elev_line)
        num_chars_seen = len(line) * y
    assert(start is not None)
    assert(end is not None)
    return HillMap(elevations=elevations, start=start, end=end,
                   num_positions=num_chars_seen, width=len(elevations[0]),
                   height=len(elevations))

def find_shortest_path_len(hill_map: HillMap) -> int:
    seen:set(tuple(int, int)) = set()

    def get_unseen_neighbors(x: int, y: int) -> list[tuple[int, int]]:
        offsets = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        unseen_neighbors = []
        for dx, dy in offsets:
            i, j = x+dx, y+dy
            if i < 0 or j < 0 or i >= hill_map.width or j >= + hill_map.height:
                continue
            elif (i,j) in seen:
                continue
            elif (hill_map.elevations[j][i] - hill_map.elevations[y][x]) <= 1:
                seen.add((i,j))
                unseen_neighbors.append((i,j))
            else:
                # too high to climb
                continue
        return unseen_neighbors
            

    # Breadth-first search
    depth = 0
    positions = [hill_map.start]

    while depth < hill_map.num_positions:
        deeper_positions = []
        for (x, y) in positions:
            unseen_neighbors = get_unseen_neighbors(x, y)
            for neighbor in unseen_neighbors:
                if neighbor == hill_map.end:
                    return depth + 1
            deeper_positions.extend(unseen_neighbors)
        # This indicates no path exists which violates the problem definition
        assert(len(deeper_positions) > 0)
        positions = deeper_positions
        depth += 1

    # This indicates no path exists which violates the problem definition
    assert(False)

if __name__ == "__main__":
    lines = []
    #with open("input_easy.txt") as f:
    with open("input.txt") as f:
        for line in f.readlines():
            lines.append(line.strip())
    hill_map = prepare_input(lines)
    path_len = find_shortest_path_len(hill_map)
    print(path_len)