class Buffs:
    class Darkvison:
        def __init__(self):
            self.id = 0
            self.name = 'Darkvison'
            self.description = [
                "You can see in dim light within 60 feet of you",
                "as if it were bright light,",
                "and in darkness as if it were dim light.",
                "You can't discern color in darkness,",
                "only shades of gray."
            ]
            self.image = 'images/buffs/Darkvision.png'

    class GnomeCunning:
        def __init__(self):
            self.id = 1
            self.name = 'Gnome Cunning'
            self.description = [
                "You have advantage on all Intelligence, Wisdom,",
                "and Charisma saves against magic."
            ]
            self.image = 'images/buffs/Gnome Cunning.png'

    class ArtificersLore:
        def __init__(self):
            self.id = 2
            self.name = 'Artificers Lore'
            self.description = [
                "Whenever you make an Intelligence (History) check",
                "related to magical, alchemical, "
                "or technological items,",
                "you can add twice your proficiency bonus",
                "instead of any other proficiency bonus that may apply."
            ]
            self.image = 'images/buffs/Artificers Lore.png'

    class ToolExpertise:
        def __init__(self):
            self.id = 3
            self.name = 'Tool Expertise'
            self.description = [
                "your proficiency bonus is now doubled",
                "for any ability check you make that",
                "uses your proficiency with a tool."
            ]
            self.image = 'images/buffs/Tool Expertise.png'

    class ArcaneFirearm:
        def __init__(self):
            self.id = 4
            self.name = 'Arcane Firearm'
            self.description = [
                "You can use your arcane firearm as a spellcasting focus",
                "for your artificer spells. When you cast an",
                "artificer spell through the firearm, roll a d8,",
                "and you gain a bonus to one of the spell's damage",
                "rolls equal to the number rolled."
            ]
            self.image = 'images/buffs/Arcane Firearm.png'


BUFFS_ID_DICT = {
    0: Buffs.Darkvison, 1: Buffs.GnomeCunning, 2: Buffs.ArtificersLore,
    3: Buffs.ToolExpertise, 4: Buffs.ArcaneFirearm
}
