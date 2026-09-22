from v2.models.editorial_models import (
    EditorialStrategy,
    EditorialContract,
)


def build_editorial_contract(
    strategy: EditorialStrategy,
) -> EditorialContract:

    contract = EditorialContract()

    contract.audience = strategy.audience
    contract.objective = strategy.objective
    contract.key_message = strategy.key_message
    contract.tone = strategy.tone
    contract.format = strategy.format
    contract.cta = strategy.cta_strategy

    contract.forbidden_points = strategy.forbidden_points.copy()

    return contract
