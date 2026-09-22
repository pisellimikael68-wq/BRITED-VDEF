from v2.knowledge.registry import KnowledgeRegistry
from v2.knowledge.engine.graph_engine import GraphEngine


registry = KnowledgeRegistry()
engine = GraphEngine(registry)

print("Nombre de topics :", len(registry.topics))

if registry.topics:

    topic = registry.topics[0]

    print()
    print("Topic :", topic.id)

    print("Existe :", engine.exists(topic.id))

    print("Voisins :", len(engine.neighbors(topic.id)))

    print("Reachable :", len(engine.reachable(topic.id)))

    print("Recommendations :", len(engine.recommend(topic.id)))

    print("Degree :", engine.degree(topic.id))
    