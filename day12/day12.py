from dataclasses import dataclass
from collections import deque
from typing import Deque

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
        for i, j in offsets:
            l, m = x+i, y+j
            print(f"x:{x} y:{y} l:{l} m:{m}")
            if l < 0 or m < 0 or l >= hill_map.width or m >= + hill_map.height:
                print("off map")
                continue
            elif (l,m) in seen:
                print("seen")
                continue
            elif (hill_map.elevations[y][x] - hill_map.elevations[m][l]) <= 1:
                print("good")
                seen.add((l,m))
                unseen_neighbors.append((l,m))
            else:
                print(f"too high: curr:{hill_map.elevations[y][x]} poss:{hill_map.elevations[m][l]}")
        return unseen_neighbors
            

    @dataclass
    class Iteration:
        # name could be better
        depth: int
        positions: list[tuple[int,int]]

    node_queue:Deque[Iteration] = deque()
    path_len = 0
    node_queue.append(Iteration(depth=0, positions=[hill_map.end]))
    #BFS 
    while (iteration := node_queue.popleft()) and path_len < hill_map.num_positions:
        print(f"s current iteration:{iteration} node_queue={node_queue}")
        #seen.add((x, y))
        deeper_positions = []
        for (x, y) in iteration.positions:
            unseen_neighbors = get_unseen_neighbors(x, y)
            for (i, j) in unseen_neighbors:
                if (i,j) == hill_map.start:
                    print("bingo")
                    return iteration.depth + 1
            deeper_positions.extend(unseen_neighbors)
            print(f"num seen: {len(seen)}")
        # This indicates no path exists which violates the problem definition
        assert(len(deeper_positions) > 0)
        node_queue.append(Iteration(depth=iteration.depth+1, positions=deeper_positions))


    # Should never reach here
    assert(False)

if __name__ == "__main__":
    lines = []
    #with open("input_easy.txt") as f:
    #with open("input_med.txt") as f:
    with open("input.txt") as f:
        for line in f.readlines():
            lines.append(line.strip())
    hill_map = prepare_input(lines)
    print(hill_map)
    path_len = find_shortest_path_len(hill_map)
    print(path_len)