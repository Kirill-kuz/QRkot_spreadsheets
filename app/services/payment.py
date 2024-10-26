from typing import List
from datetime import datetime

from app.models.base import Invested


def investment_procces(
        target: Invested, sources: List[Invested]) -> List[Invested]:
    updated = []
    for source in sources:
        if target.fully_invested:
            break

        donation = min(
            source.full_amount - source.invested_amount,
            target.full_amount - target.invested_amount
        )

        for obj in (target, source):
            obj.invested_amount += donation
            if obj.full_amount == obj.invested_amount:
                obj.fully_invested = True
                obj.close_date = datetime.utcnow()

        updated.append(source)

    return updated
