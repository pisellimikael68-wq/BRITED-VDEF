from collections import deque
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .graph_engine import GraphEngine


class GraphTraversal:
    """
    Algorithmes de parcours du Knowledge Graph.
    """

    def __init__(
        self,
        engine: "GraphEngine",
    ):
        self.engine = engine

    # ==========================================================
    # Reachable
    # ==========================================================

    def reachable(
        self,
        topic_id: str,
        max_depth: int = 2,
    ) -> list[str]:

        visited = {topic_id}
        queue = deque([(topic_id, 0)])
        result = []

        while queue:

            current, depth = queue.popleft()

            if depth >= max_depth:
                continue

            for neighbor in self.engine.neighbors(current):

                if neighbor.id in visited:
                    continue

                visited.add(neighbor.id)
                result.append(neighbor.id)
                queue.append((neighbor.id, depth + 1))

        return result

    # ==========================================================
    # Shortest Path
    # ==========================================================

    def shortest_path(
        self,
        source: str,
        target: str,
    ) -> list[str]:

        if source == target:
            return [source]

        visited = {source}
        queue = deque([(source, [source])])

        while queue:

            current, path = queue.popleft()

            for neighbor in self.engine.neighbors(current):

                if neighbor.id in visited:
                    continue

                new_path = path + [neighbor.id]

                if neighbor.id == target:
                    return new_path

                visited.add(neighbor.id)
                queue.append((neighbor.id, new_path))

        return []
    