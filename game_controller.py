from effect import Effect
from player import Player
from character import Character
from utils import describe_characters
import random


class TopLevelController:
    def __init__(self):
        self.player = Player()
        self.player.default_deck()
        self.gauntlet = None
        self.player_alive = True
        self.deck_controller = DeckController(self.player)

    def play_gauntlet(self):
        while self.player_alive:
            encounter = self.gauntlet.next_encounter()
            if encounter is not None:
                self.begin_battle(encounter.characters)
                self.deck_controller.check_for_drop(encounter)
            else:
                print("You beat the gauntlet!!!")
                break

    def begin_battle(self, enemy_characters):
        describe_characters(enemy_characters)
        allied_characters = self.draft_team()
        battle = BattleController(allied_characters + enemy_characters)
        outcome = battle.play_battle()
        if outcome:
            print('You Won!!!')
        else:
            print('You Died :(')
            self.player_alive = False

    def draft_team(self):
        draft = DraftController(self.player)
        return draft.draft_characters()


class BattleController:
    def __init__(self, characters):
        self.characters = characters
        self.time = 0
        self.battle_max_time = 1000

        for character_in_play in self.characters:
            character_in_play.initialize_stats()

        self.reform_ranks()

    def play_battle(self):
        while not self.check_for_end():
            self.advance_time()
            if self.time > self.battle_max_time:
                return False
        return self.did_player_win()

    def did_player_win(self):
        allied_characters_alive = len([x for x in self.characters if x.stats['enemy'] == 0])
        return allied_characters_alive > 0

    def advance_time(self):
        self.time += 1
        for character_in_play in self.characters:
            character_in_play.take_turn(self.characters)
            self.check_for_death()
            self.reform_ranks()

    def check_for_death(self):
        for character_in_play in self.characters:
            if character_in_play.stats['health'] <= 0:
                self.update_on_death(character_in_play)

    def update_on_death(self, dead_character):
        self.characters.remove(dead_character)
        self.reform_ranks()

    def reform_ranks(self):
        for is_enemy in [0, 1]:
            ranks = [x.stats['rank'] for x in self.characters if x.stats['enemy'] == is_enemy]
            if len(ranks) > 0:
                min_rank = min(ranks)
                for character_in_play in self.characters:
                    if character_in_play.stats['enemy'] == is_enemy:
                        character_in_play.effect(Effect(rank=-min_rank).return_effect())

    def check_for_end(self):
        allied_characters_alive = len([x for x in self.characters if x.stats['enemy'] == 0])
        enemy_characters_alive = len([x for x in self.characters if x.stats['enemy'] == 1])
        return min(allied_characters_alive, enemy_characters_alive) == 0


class DraftController:
    def __init__(self, player):
        self.character_count = 3
        self.card_draw_count = 3
        self.player = player

    def draft_characters(self):
        characters = []
        for i in range(0, self.character_count):
            characters.append(self.draft_character())

        self.player.return_discard_to_deck()
        return characters

    def draft_character(self):
        character = Character()
        character.gain_card(self.pick_from_draw("Character"))
        character.gain_card(self.pick_from_draw("Technique"))
        character.gain_card(self.pick_from_draw("Equipment"))
        self.pick_character_rank(character)
        return character

    def pick_from_draw(self, card_type):
        cards = self.player.draw(card_type, self.card_draw_count)
        confirm = False
        while not confirm:
            card_name = input("Choose one of: " + '|'.join(cards))
            if card_name in cards:
                self.player.deck[card_name].print_description()
                confirm = input("Type yes to confirm: ") == "yes"
            else:
                print('Card name not recognized')

        card = self.player.deck[card_name]
        self.player.discard_card(self.player.deck[card_name])
        return card

    def pick_character_rank(self, character):
        valid_rank = False
        while not valid_rank:
            rank = input("Place character in rank 0, 1, or 2? ")
            if rank.isnumeric():
                rank = int(rank)
                if rank in [0, 1, 2]:
                    valid_rank = True

        character.effect(Effect(rank=rank).return_effect())


class DeckController:
    def __init__(self, player):
        self.player = player

    def check_for_drop(self, encounter):
        drop = random.choices([x for x in encounter.loot_table.keys()], [x for x in encounter.loot_table.values()])[0]
        if drop is not None:
            self.gain_new_card(drop)

    def gain_new_card(self, card):
        if card.name not in self.player.deck.keys():
            card.print_description()
            replaceable_cards = {x: self.player.deck[x] for x in self.player.deck.keys()
                                 if self.player.deck[x].card_type == card.card_type}
            confirm = False
            while not confirm:
                card_to_replace_name = input("Choose one of: " + '|'.join(replaceable_cards))
                if card_to_replace_name in replaceable_cards:
                    replaceable_cards[card_to_replace_name].print_description()
                    confirm = input("Type yes to confirm: ") == "yes"
                    if confirm:
                        self.swap_cards(card, replaceable_cards[card_to_replace_name])
                else:
                    confirm = input("No card will be replaced \n Type yes to confirm: ") == "yes"

    def swap_cards(self, card_gained, card_lost):
        self.player.gain_card(card_gained)
        self.player.permanently_remove_card(card_lost)