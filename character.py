from effect import Effect
import utils


class Character:
    def __init__(self):
        self.stats = Effect().return_effect()

        self.cards = {}
        self.action_time = 100

    def effect(self, effects):
        for stat in effects:
            self.stats[stat] += effects[stat]
        if effects['health'] < 0:
            self.charge_gain(damage_taken=-effects['health'])
        self.stats['rank'] = max(0, self.stats['rank'])

    def charge_gain(self, damage_dealt=0, damage_taken=0, time_passed=0):
        self.stats['charge'] += damage_dealt * self.stats['charge_gain_on_damage_dealt']
        self.stats['charge'] += damage_taken * self.stats['charge_gain_on_damage_taken']
        self.stats['charge'] += time_passed * self.stats['charge_gain_per_timestep']

    def attack(self, targets):
        targets = [x for x in targets if (x.stats['enemy'] != self.stats['enemy']) and
                   ((x.stats['rank'] + self.stats['rank']) <= self.stats['range'])]
        if len(targets) > 0:
            target = utils.select_target_by_aggro(targets)
            if target is not None:
                attack_effect = Effect(health=-self.stats['attack_damage']).return_effect()
                target.effect(attack_effect)
                self.gain_aggro(self.stats['attack_damage'])
                self.charge_gain(damage_dealt=-attack_effect['health'])
                print(self.get_name() + " attacked " + target.get_name() + ' for ' + str(attack_effect['health']))

    def on_hit_effect(self, target):
        equipment_card = [x for x in self.cards.values() if x.card_type == "Equipment"][0]
        equipment_card.on_hit_effect(self, target)

    def ability(self, targets):
        character_card = [x for x in self.cards.values() if x.card_type == "Character"][0]
        character_card.ability(self, targets)

    def get_name(self):
        character_card = [x for x in self.cards.values() if x.card_type == "Character"][0]
        return character_card.name

    def initialize_stats(self):
        for stat in self.stats:
            self.stats[stat] = 0

        for card in self.cards:
            self.effect(self.cards[card].effects)

    def gain_card(self, card):
        self.cards[card.name] = card

    def take_turn(self, targets):
        self.stats['next_action_time'] -= self.stats['speed']
        self.charge_gain(time_passed=1)
        if self.stats['next_action_time'] <= 0:
            self.stats['next_action_time'] += self.action_time
            if self.stats['charge'] >= self.stats['charge_required_for_ability']:
                self.gain_aggro(self.stats['charge_required_for_ability'])
                self.stats['charge'] = 0
                self.ability(targets)
            else:
                self.attack(targets)

    def print_status(self):
        print("Name: ", self.get_name())
        print({key: self.stats[key] for key in self.stats if self.stats[key] != 0})

    def print_cards(self):
        print("Name: ", self.get_name())
        for card in self.cards.values():
            card.print_description()

    def gain_aggro(self, amount):
        aggro_change = Effect(aggro=amount).return_effect()
        self.effect(aggro_change)
