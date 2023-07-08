from database.dbApi import DB_API
from aiogram.types import User, Message


class Bonus:
    db_api: DB_API = DB_API()
    db_api.connect()

    def check_the_limit(self):
        user_id: int = User.get_current().id
        current_bonus_amount = self.db_api.get_bonus(user_id)[0]
        if current_bonus_amount > 1000:
            return False
        return True

    def add_bonus(self, amount):
        if self.check_the_limit():
            user_id: int = User.get_current().id
            current_bonus_amount = self.db_api.get_bonus(user_id)[0]
            current_bonus_amount += amount
            self.db_api.update_bonus(current_bonus_amount, user_id)

    def referral_bonus(self):
        if self.check_the_limit():
            try:
                user_id: int = User.get_current().id
                referrals = self.db_api.check_referral(user_id)
                print(len(referrals))
                if len(referrals) != 0:
                    current_bonus_amount = self.db_api.get_bonus(user_id)[0]
                    bonus_per_user = 50
                    bonus_plus_referrals = (len(referrals) * bonus_per_user) + current_bonus_amount
                    self.db_api.update_bonus(bonus_plus_referrals, user_id)

                    for user_id_ref in referrals:
                        self.db_api.clear_referral_number(user_id_ref)
                else:
                    return 'empty'
            except Exception as err:
                print(err)
