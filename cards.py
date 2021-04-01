import effect
import utils


class Card:
    def __init__(self, name, card_type, effects):
        self.name = name
        self.card_type = card_type
        self.effects = effects

    def print_description(self):
        print("Name: ", self.name)
        print({key: self.effects[key] for key in self.effects if self.effects[key] != 0})


class CharacterCard(Card):
    def __init__(self, name, effects):
        super().__init__(name, "Character", effects)
        self.ability_description = ""

    def ability(self, character, targets):
        pass

    def print_description(self):
        print("Name: ", self.name)
        print(self.ability_description)
        print({key: self.effects[key] for key in self.effects if self.effects[key] != 0})


class WizardCharacterCard(CharacterCard):
    def __init__(self, name):
        super().__init__(name=name,
                         effects=effect.Effect(health=100,
                                               attack_damage=5,
                                               spell_damage=20,
                                               speed=40).return_effect())

    def ability(self, character, targets):
        pass


class FireWizardCharacterCard(WizardCharacterCard):
    def __init__(self):
        super().__init__("Fire Wizard")
        self.effects['charge_required_for_ability'] += 40
        self.ability_description = "A deadly firestorm damages all foes within range 3"

    def ability(self, character, targets):
        ability_range = 3
        base_damage = 10
        damage_scaling = 1.5
        targets = [x for x in targets if (x.stats['enemy'] != character.stats['enemy']) and
                   ((x.stats['rank'] + character.stats['rank']) <= ability_range)]
        for target in targets:
            spell_damage = base_damage + damage_scaling * character.stats['spell_damage']
            target.effect(effect.Effect(health=-spell_damage).return_effect())
            print(character.get_name() + '\'s firestorm hit ' + target.get_name() + ' for ' + str(spell_damage))


class LifeWizardCharacterCard(WizardCharacterCard):
    def __init__(self):
        super().__init__("Life Wizard")
        self.effects['charge_required_for_ability'] += 80
        self.ability_description = "Restores health to an ally in need"

    def ability(self, character, targets):
        ability_range = 2
        base_healing = 40
        healing_scaling = 1.0
        targets = [x for x in targets if (x.stats['enemy'] == character.stats['enemy']) and
                   ((x.stats['rank'] + character.stats['rank']) <= ability_range)]
        target = utils.select_target_by_aggro(targets)
        if target is not None:
            spell_damage = base_healing + healing_scaling * character.stats['spell_damage']
            target.effect(effect.Effect(health=spell_damage).return_effect())
            print(character.get_name() + ' healed ' + target.get_name() + ' for ' + str(spell_damage))


class ForceWizardCharacterCard(WizardCharacterCard):
    def __init__(self):
        super().__init__("Force Wizard")
        self.effects['charge_required_for_ability'] += 60
        self.ability_description = "Pull an enemy within range 2 one rank forward"

    def ability(self, character, targets):
        ability_range = 2
        pull_distance = 1
        base_damage = 5
        damage_scaling = 0.5
        targets = [x for x in targets if (x.stats['enemy'] != character.stats['enemy']) and
                   ((x.stats['rank'] + character.stats['rank']) <= ability_range)]
        target = utils.select_target_by_aggro(targets)
        if target is not None:
            spell_damage = base_damage + damage_scaling * character.stats['spell_damage']
            target.effect(effect.Effect(health=-spell_damage, rank=-pull_distance).return_effect())
            print(character.get_name() + ' pulled ' + target.get_name() + ' for ' + str(spell_damage))


class WarriorCharacterCard(CharacterCard):
    def __init__(self, name):
        super().__init__(name=name,
                         effects=effect.Effect(health=200,
                                               attack_damage=15,
                                               spell_damage=5,
                                               speed=50).return_effect())

    def ability(self, character, targets):
        pass


class ShieldBreaker(WarriorCharacterCard):
    def __init__(self):
        super().__init__("Shield Breaker")
        self.effects['charge_required_for_ability'] += 40
        self.ability_description = "Bash a front rank enemy one rank backward"

    def ability(self, character, targets):
        ability_range = 0
        push_distance = 1
        base_damage = 10
        damage_scaling = 0.1
        targets = [x for x in targets if (x.stats['enemy'] != character.stats['enemy']) and
                   ((x.stats['rank'] + character.stats['rank']) <= ability_range)]
        target = utils.select_target_by_aggro(targets)
        if target is not None:
            spell_damage = base_damage + damage_scaling * character.stats['spell_damage']
            target.effect(effect.Effect(health=-spell_damage, rank=push_distance).return_effect())
            print(character.get_name() + ' pushed ' + target.get_name() + ' for ' + str(spell_damage))


class Barbarian(WarriorCharacterCard):
    def __init__(self):
        super().__init__("Barbarian")
        self.effects['charge_required_for_ability'] += 50
        self.ability_description = "Slash all enemies in the front rank"

    def ability(self, character, targets):
        ability_range = 0
        base_damage = 10
        damage_scaling = 0.5
        targets = [x for x in targets if (x.stats['enemy'] != character.stats['enemy']) and
                   ((x.stats['rank'] + character.stats['rank']) <= ability_range)]
        for target in targets:
            spell_damage = base_damage + damage_scaling * character.stats['spell_damage']
            target.effect(effect.Effect(health=-spell_damage).return_effect())
            print(character.get_name() + ' sliced ' + target.get_name() + ' for ' + str(spell_damage))


class RuneBlade(WarriorCharacterCard):
    def __init__(self):
        super().__init__("Rune Blade")
        self.effects['charge_required_for_ability'] += 80
        self.ability_description = "Inscribe runes to gain speed and attack damage"

    def ability(self, character, targets):
        stat_scaling = 0.5
        stat_change = character.stats['spell_damage']*stat_scaling
        stat_gain = effect.Effect(attack_damage=stat_change,
                                  speed=stat_change)
        character.effect(stat_gain)
        print(character.get_name() + ' gained ' + str(stat_change) + ' strength and speed')


class RogueCharacterCard(CharacterCard):
    def __init__(self, name):
        super().__init__(name=name,
                         effects=effect.Effect(health=120,
                                               attack_damage=15,
                                               spell_damage=10,
                                               speed=60).return_effect())

    def ability(self, character, targets):
        pass


class Saboteur(RogueCharacterCard):
    def __init__(self):
        super().__init__("Saboteur")
        self.effects['charge_required_for_ability'] += 40
        self.ability_description = "Throw a flash bomb with range 3 to reduce an enemy's offensive prowess"

    def ability(self, character, targets):
        stat_scaling = 0.2
        stat_change = character.stats['spell_damage']*stat_scaling
        stat_loss = effect.Effect(attack_damage=-stat_change,
                                  spell_damage=-stat_change,
                                  speed=-stat_change)
        ability_range = 3
        targets = [x for x in targets if (x.stats['enemy'] != character.stats['enemy']) and
                   ((x.stats['rank'] + character.stats['rank']) <= ability_range)]
        target = utils.select_target_by_aggro(targets)
        if target is not None:
            target.effect(stat_loss)
            print(character.get_name() + ' gained ' + str(stat_change) + ' strength and speed')


class Shadow(RogueCharacterCard):
    def __init__(self):
        super().__init__("Shadow")
        self.effects['charge_required_for_ability'] += 20
        self.ability_description = "Fade into the shadows to reduce aggro"

    def ability(self, character, targets):
        aggro_reduction = 10
        aggro_scaling = 1.0
        aggro_change = aggro_reduction + character.stats['spell_damage'] * aggro_scaling
        aggro_effect = effect.Effect(aggro=-aggro_change)
        character.effect(aggro_effect)
        print(character.get_name() + ' faded into the shadows dropping ' + str(aggro_change) + ' aggro')


class Assassin(RogueCharacterCard):
    def __init__(self):
        super().__init__(name="Assassin")
        self.effects['charge_required_for_ability'] += 70
        self.ability_description = "Brutally strike a front rank enemy for massive damage"

    def ability(self, character, targets):
        ability_range = 0
        base_damage = 90
        damage_scaling = 2.0
        targets = [x for x in targets if (x.stats['enemy'] != character.stats['enemy']) and
                   ((x.stats['rank'] + character.stats['rank']) <= ability_range)]
        target = utils.select_target_by_aggro(targets)
        if target is not None:
            spell_damage = base_damage + damage_scaling * character.stats['spell_damage']
            target.effect(effect.Effect(health=-spell_damage).return_effect())
            print(character.get_name() + ' assassinated ' + target.get_name() + ' for ' + str(spell_damage))


available_character_cards = {
    "fire_wizard": FireWizardCharacterCard(),
    "life_wizard": LifeWizardCharacterCard(),
    "force_wizard": ForceWizardCharacterCard(),
    "shield_breaker": ShieldBreaker(),
    "barbarian": Barbarian(),
    "rune_blade": RuneBlade(),
    "saboteur": Saboteur(),
    "shadow": Shadow(),
    "assassin": Assassin()
}


class EquipmentCard(Card):
    def __init__(self, name, effects):
        super().__init__(name, 'Equipment', effects)
        self.on_hit_effect_description = "No on hit effect"

    def on_hit_effect(self, character, target):
        pass

    def print_description(self):
        print("Name: ", self.name)
        print({key: self.effects[key] for key in self.effects if self.effects[key] != 0})
        print(self.on_hit_effect_description)


class TechniqueCard(Card):
    def __init__(self, name, effects):
        super().__init__(name, "Technique", effects)


class BroadswordOfSmiting(EquipmentCard):
    def __init__(self):
        super().__init__(name="Broadsword of Smiting",
                         effects=effect.Effect(attack_damage=20,
                                               speed=10).return_effect())


class StaffOfFlames(EquipmentCard):
    def __init__(self):
        super().__init__(name="Staff of Flames",
                         effects=effect.Effect(attack_damage=5,
                                               spell_damage=20,
                                               attack_range=2).return_effect())


class BowOfThorns(EquipmentCard):
    def __init__(self):
        super().__init__(name="Bow of Thorns",
                         effects=effect.Effect(attack_damage=10,
                                               spell_damage=5,
                                               attack_range=3).return_effect())


class RitualDagger(EquipmentCard):
    def __init__(self):
        super().__init__(name="Ritual Dagger",
                         effects=effect.Effect(attack_damage=5,
                                               spell_damage=15,
                                               speed=10).return_effect())
        self.on_hit_effect_description = "Gain 5 charge on hit"

    def on_hit_effect(self, character, target):
        charge_gain = effect.Effect(charge=5).return_effect()
        character.effect(charge_gain)


class FlagellantsFlail(EquipmentCard):
    def __init__(self):
        super().__init__(name="Flagellant's Flail",
                         effects=effect.Effect(attack_damage=35).return_effect())
        self.on_hit_effect_description = "Sacrifice 10 health on hit"

    def on_hit_effect(self, character, target):
        health_loss = effect.Effect(health=-10).return_effect()
        character.effect(health_loss)


class CavaliersLance(EquipmentCard):
    def __init__(self):
        super().__init__(name="Cavalier's Lance",
                         effects=effect.Effect(attack_damage=20,
                                               attack_range=1).return_effect())


class DragonBaneBattleAxe(EquipmentCard):
    def __init__(self):
        super().__init__(name="Dragonbane Battleaxe",
                         effects=effect.Effect(attack_damage=60,
                                               speed=-10).return_effect())


class StaffOfEntropy(EquipmentCard):
    def __init__(self):
        super().__init__(name="Staff of Entropy",
                         effects=effect.Effect(attack_range=2,
                                               spell_damage=10).return_effect())
        self.on_hit_effect_description = "Remove 3 charge from target on hit"

    def on_hit_effect(self, character, target):
        charge_drain = effect.Effect(charge=-3).return_effect()
        target.effect(charge_drain)


class SharpshootersLongbow(EquipmentCard):
    def __init__(self):
        super().__init__(name="Sharpshooter's Longbow",
                         effects=effect.Effect(attack_range=4,
                                               attack_damage=10).return_effect())


available_equipment_cards = {
    "broadsword_of_smiting": BroadswordOfSmiting(),
    "staff_of_flames": StaffOfFlames(),
    "bow_of_thorns": BowOfThorns(),
    "ritual_dagger": RitualDagger(),
    "flagellants_flail": FlagellantsFlail(),
    "cavaliers_lance": CavaliersLance(),
    "dragonbane_battleaxe": DragonBaneBattleAxe(),
    "staff_of_entropy": StaffOfEntropy(),
    "sharpshooters_longbow": SharpshootersLongbow()
}


class Patience(TechniqueCard):
    def __init__(self):
        super().__init__(name="Patience",
                         effects=effect.Effect(charge_gain_per_timestep=5).return_effect())


class Preparedness(TechniqueCard):
    def __init__(self):
        super().__init__(name="Preparedness",
                         effects=effect.Effect(charge=50, charge_gain_per_timestep=1).return_effect())


class Aggression(TechniqueCard):
    def __init__(self):
        super().__init__(name="Aggression",
                         effects=effect.Effect(charge_gain_on_damage_dealt=0.5).return_effect())


class Restraint(TechniqueCard):
    def __init__(self):
        super().__init__(name="Restraint",
                         effects=effect.Effect(charge_gain_on_damage_dealt=-0.2,
                                               charge_gain_damage_taken=1.0).return_effect())


class Balance(TechniqueCard):
    def __init__(self):
        super().__init__(name="Balance",
                         effects=effect.Effect(charge_gain_on_damage_dealt=0.2,
                                               charge_gain_damage_taken=0.2,
                                               charge_gain_per_timestep=1).return_effect())


class Berserk(TechniqueCard):
    def __init__(self):
        super().__init__(name="Berserk",
                         effects=effect.Effect(charge_gain_on_damage_dealt=0.3,
                                               charge_gain_damage_taken=0.5).return_effect())


class Ambush(TechniqueCard):
    def __init__(self):
        super().__init__(name="Ambush",
                         effects=effect.Effect(charge_gain_on_damage_dealt=0.8,
                                               charge_gain_damage_taken=-0.5).return_effect())


class Haste(TechniqueCard):
    def __init__(self):
        super().__init__(name="Haste",
                         effects=effect.Effect(charge_gain_on_damage_dealt=0.8,
                                               charge_gain_per_timestep=-2).return_effect())


class Resolute(TechniqueCard):
    def __init__(self):
        super().__init__(name="Resolute",
                         effects=effect.Effect(charge_gain_damage_taken=0.8).return_effect())


available_technique_cards = {
    "patience": Patience(),
    "preparedness": Preparedness(),
    "aggression": Aggression(),
    "restraint": Restraint(),
    "resolute": Resolute(),
    "ambush": Ambush(),
    "berserk": Berserk(),
    "haste": Haste(),
    "balance": Balance()
}
