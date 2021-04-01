import cards
from cards import CharacterCard
from effect import Effect
from utils import select_target_by_aggro
from character import Character


class EnemyCharacterCard(CharacterCard):
    def __init__(self, name, effects):
        super().__init__(name, effects)
        self.description = ""
        self.ability_description = ""

    def print_description(self):
        print("Name: ", self.name)
        print(self.description)
        print(self.ability_description)
        print({key: self.effects[key] for key in self.effects if self.effects[key] != 0})


class Slime(EnemyCharacterCard):
    def __init__(self, name):
        super().__init__(name, effects=Effect(health=30,
                                              attack_damage=10,
                                              spell_damage=0,
                                              speed=30,
                                              charge_required_for_ability=5,
                                              charge_gain_per_timestep=1,
                                              enemy=1).return_effect())
        self.description = "Fetid detritus given malevolent form by excess dark magic"
        self.ability_description = "Ability: Range 1 spit that damages the target"

    def ability(self, character, targets):
        ability_range = 1
        base_damage = 20
        damage_scaling = 1.0
        targets = [x for x in targets if (x.stats['enemy'] != character.stats['enemy']) and
                   ((x.stats['rank'] + character.stats['rank']) <= ability_range)]
        target = select_target_by_aggro(targets)
        if target is not None:
            spell_damage = base_damage + damage_scaling * character.stats['spell_damage']
            target.effect(Effect(health=-spell_damage).return_effect())
            print(character.get_name() + ' spat slime at ' + target.get_name() + ' for ' + str(spell_damage))


class Cultist(EnemyCharacterCard):
    def __init__(self, name):
        super().__init__(name, effects=Effect(health=90,
                                              attack_damage=10,
                                              spell_damage=20,
                                              speed=45,
                                              charge_required_for_ability=40,
                                              charge_gain_per_timestep=4,
                                              charge_gain_damage_taken=0.5,
                                              enemy=1).return_effect())
        self.description = "A howling cultist desperate for the forbidden power of forgotten gods"
        self.ability_description = "Ability: Range 2 life drain that damages the target and heals the caster"

    def ability(self, character, targets):
        ability_range = 2
        base_damage = 10
        damage_scaling = 1.0
        targets = [x for x in targets if (x.stats['enemy'] != character.stats['enemy']) and
                   ((x.stats['rank'] + character.stats['rank']) <= ability_range)]
        target = select_target_by_aggro(targets)
        if target is not None:
            spell_damage = base_damage + damage_scaling * character.stats['spell_damage']
            target.effect(Effect(health=-spell_damage).return_effect())
            character.effect(Effect(health=spell_damage).return_effect())
            print(character.get_name() + ' drained ' + str(spell_damage) + ' life from ' + target.get_name())


class Encounter:
    def __init__(self):
        self.characters = []
        self.loot_table = {}

    def print_description(self):
        pass


class SlimeEncounter(Encounter):
    def __init__(self):
        super().__init__()
        for i in range(0, 3):
            character = Character()
            character.gain_card(Slime("Slime " + 'I' * (i + 1)))
            self.characters.append(character)

        self.loot_table = {
            cards.Ambush(): 1.0,
            cards.Resolute(): 1.0
        }

    def print_description(self):
        print("A band of slimes coalesces from the walls in total silence")
        for character in self.characters:
            character.print_cards()


class CultistEncounter(Encounter):
    def __init__(self):
        super().__init__()
        for i in range(0, 3):
            character = Character()
            character.gain_card(Cultist("Cultist " + 'I' * (i + 1)))
            character.gain_card(cards.Berserk())
            self.characters.append(character)

        character = Character()
        character.gain_card(Cultist("Cultist " + 'I' * 4))
        character.gain_card(cards.RitualDagger())
        self.characters.append(character)

        self.loot_table = {
            cards.RitualDagger(): 1.0,
            cards.Berserk(): 1.0
        }

    def print_description(self):
        print("A coven of mad cultists charge forward, a wicked blade dripping sacrificial blood")
        for character in self.characters:
            character.print_cards()


class Gauntlet:
    def __init__(self, encounters):
        self.encounters = encounters

    def next_encounter(self):
        if len(self.encounters) > 0:
            return self.encounters.pop(0)


class SewerGauntlet(Gauntlet):
    def __init__(self):
        encounters = [
            SlimeEncounter(),
            CultistEncounter()
        ]
        super().__init__(encounters)
