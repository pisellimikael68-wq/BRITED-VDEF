from abc import ABC

from v2.core.context import BritedContext
from v2.services.logger import PipelineLogger


class BasePipeline(ABC):

    agents = []

    def execute_agents(self, context: BritedContext) -> BritedContext:

        for agent in self.agents:

            PipelineLogger.section(agent.__class__.__name__)

            context = agent.run(context)

        return context
    