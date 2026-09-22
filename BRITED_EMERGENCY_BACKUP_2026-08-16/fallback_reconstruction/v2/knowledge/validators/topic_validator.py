from abc import ABC, abstractmethod

from v2.models.knowledge_models import Topic
from v2.knowledge.reports.topic_quality import TopicQualityReport


class TopicValidator(ABC):

    @abstractmethod
    def validate(
        self,
        topic: Topic,
    ) -> TopicQualityReport:
        pass