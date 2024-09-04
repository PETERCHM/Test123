# expenses.py
class Expense:
    def __init__(self, description, amount, paid_by, shared_by, custom_shares=None):
        self.description = description
        self.amount = amount
        self.paid_by = paid_by
        self.shared_by = shared_by
        self.custom_shares = custom_shares if custom_shares else {}

    def split_expense(self):
        total_custom_share = sum(self.custom_shares.values())
        remaining_amount = self.amount - total_custom_share
        equal_share_users = [user for user in self.shared_by if user not in self.custom_shares]

        equal_share = remaining_amount / len(equal_share_users) if equal_share_users else 0
        split = {}
        for user in self.shared_by:
            if user in self.custom_shares:
                split[user] = self.custom_shares[user]
            else:
                split[user] = equal_share
        return split
