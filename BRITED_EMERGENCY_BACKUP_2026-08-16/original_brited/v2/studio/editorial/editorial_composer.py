"""
BRITED Editorial Composer

Assemble tous les composants éditoriaux
nécessaires à la génération d'un Script.
"""

from v2.models.knowledge_models import Topic

from v2.studio.editorial.editorial_blueprint import EditorialBlueprint
from v2.studio.editorial.editorial_context import EditorialContext

from v2.studio.editorial.playbook.engines.hook_engine import HookEngine


class EditorialComposer:

    """
    Assemble le Blueprint éditorial.
    """

    def __init__(self):

        self.hook_engine = HookEngine()

        # bientôt
        # self.cta_engine = CTAEngine()
        # self.transition_engine = TransitionEngine()
        # self.analogy_engine = AnalogyEngine()

    # ==========================================================
    # PUBLIC
    # ==========================================================

    def compose(

        self,

        topic: Topic,

        context: EditorialContext,

    ) -> EditorialBlueprint:

        hook = self.hook_engine.select(context)

        return EditorialBlueprint(

            topic=topic,

            hook=hook,

            transition=None,

            analogy=None,

            cta=None,

        )
    