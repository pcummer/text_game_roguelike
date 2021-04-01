class Effect:
    def __init__(self, health=0, attack_damage=0, spell_damage=0, charge=0, charge_required_for_ability=0,
                 charge_gain_on_damage_dealt=0, charge_gain_damage_taken=0, charge_gain_per_timestep=0, rank=0,
                 aggro=0, attack_range=0, enemy=0, next_action_time=0, speed=0):
        self.effect = {
            "health": health,
            "attack_damage": attack_damage,
            "spell_damage": spell_damage,
            "charge": charge,
            "charge_required_for_ability": charge_required_for_ability,
            "charge_gain_on_damage_dealt": charge_gain_on_damage_dealt,
            "charge_gain_on_damage_taken": charge_gain_damage_taken,
            "charge_gain_per_timestep": charge_gain_per_timestep,
            "rank": rank,
            "aggro": aggro,
            "range": attack_range,
            "enemy": enemy,
            "next_action_time": next_action_time,
            "speed": speed,
        }

    def return_effect(self):
        return self.effect
