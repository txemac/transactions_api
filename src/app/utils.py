from database.schemas import TransactionPostList


def check_amounts(
        transactions: TransactionPostList
) -> bool:
    """
    Check if amount are negatives (inflow) or positives (outflow).

    :param TransactionPostList transactions: list of transactions
    :return bool: True if all right
    """
    for t in transactions.transactions:
        if (t.type == 'inflow' and t.amount < 0) or \
                (t.type == 'outflow' and t.amount > 0):
            return False

    return True
