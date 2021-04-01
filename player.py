import random
import cards


class Player:
    def __init__(self):
        self.deck = {}
        self.discard = {}

    def default_deck(self):
        for card in random.sample([x for x in cards.available_character_cards.values()], k=5):
            self.gain_card(card)

        for card in random.sample([x for x in cards.available_technique_cards.values()], k=5):
            self.gain_card(card)

        for card in random.sample([x for x in cards.available_equipment_cards.values()], k=5):
            self.gain_card(card)

    def draw(self, card_type, number_of_cards):
        deck = {key: self.deck[key] for key in self.deck.keys() if self.deck[key].card_type == card_type}
        results = []
        for i in range(0, number_of_cards):
            results.append(random.choice([x for x in deck.keys() if x not in results]))
        return results

    def gain_card(self, card):
        self.deck[card.name] = card

    def permanently_remove_card(self, card):
        del self.deck[card.name]

    def discard_card(self, card):
        del self.deck[card.name]
        self.discard[card.name] = card

    def return_discard_to_deck(self):
        for card in self.discard.values():
            self.gain_card(card)
        self.discard = {}
