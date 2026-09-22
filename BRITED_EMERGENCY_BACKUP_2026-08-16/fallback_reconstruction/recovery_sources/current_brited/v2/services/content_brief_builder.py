from v2.models.content_brief import ContentBrief
from v2.core.context import BritedContext


def build_content_brief(context: BritedContext) -> ContentBrief:

    brief = ContentBrief()

    knowledge = context.knowledge
    contract = context.editorial_contract
    angle = context.selected_angle

    brief.subject = context.subject

    brief.audience = contract.audience
    brief.objective = contract.objective
    brief.key_message = contract.key_message

    brief.tone = contract.tone
    brief.format = contract.format
    brief.cta = contract.cta

    brief.angle_title = angle.title
    brief.angle_description = angle.description

    brief.mandatory_points = contract.mandatory_points

    brief.references = knowledge.references

    brief.knowledge_summary = (
        knowledge.definitions
        + knowledge.rules
        + knowledge.taxation
        + knowledge.mistakes
        + knowledge.misconceptions
        + knowledge.frequently_asked_questions
    )

    return brief
