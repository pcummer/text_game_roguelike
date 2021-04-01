def select_target_by_aggro(targets):
    best_target = None
    highest_aggro = -1E9
    for target in targets:
        if target.stats['aggro'] > highest_aggro:
            best_target = target
            highest_aggro = best_target.stats['aggro']
    return best_target


def describe_characters(characters):
    for character in characters:
        for card in character.cards.values():
            card.print_description()
