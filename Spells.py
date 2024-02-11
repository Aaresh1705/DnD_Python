class Spells:
    def __init__(self):
        pass

    class Level0:
        def __init__(self):
            pass

        class AcidSplash:
            def __init__(self):
                self.name = 'Acid Splash'
                self.school = 'Conjuration'
                self.casting_time = 'Action'
                self.range = 60
                self.duration = 'Instantaneous'
                self.components = 'V, S'

                self.description = ('You hurl a bubble of acid. Choose one creature you can see within range, '
                                    'or choose two creatures you can see within range that are within 5 feet of each '
                                    'other. A target must succeed on a Dexterity saving throw or take 1d6 acid damage.')
                self.higher_levels = ('This spell’s damage increases by 1d6 when you reach 5th level (2d6), '
                                      '11th level (3d6), and 17th level (4d6).')

            def damage(self, level):
                if level >= 17:
                    return '4d6'
                elif level >= 11:
                    return '3d6'
                elif level >= 5:
                    return '2d6'
                else:
                    return '1d6'

        class BoomingBlade:
            def __init__(self):
                self.name = 'Booming Blade'
                self.school = 'Conjuration'

        class CreateBonfire:
            def __init__(self):
                self.name = 'Create Bonfire'
                self.school = 'Conjuration'

        class DancingLights:
            def __init__(self):
                self.name = 'Dancing Lights'
                self.school = 'Conjuration'

        class FireBolt:
            def __init__(self):
                self.name = 'Fire Bolt'
                self.school = 'Conjuration'

        class Frostbite:
            def __init__(self):
                self.name = 'Frostbite'
                self.school = 'Conjuration'

        class GreenFlameBlade:
            def __init__(self):
                self.name = 'Green-Flame Blade'
                self.school = 'Conjuration'

        class Guidance:
            def __init__(self):
                self.name = 'Guidance'
                self.school = 'Conjuration'

        class Light:
            def __init__(self):
                self.name = 'Light'
                self.school = 'Conjuration'

        class LightningLure:
            def __init__(self):
                self.name = 'Lightning Lure'
                self.school = 'Conjuration'

        class MageHand:
            def __init__(self):
                self.name = 'Mage Hand'
                self.school = 'Conjuration'

        class MagicStone:
            def __init__(self):
                self.name = 'Magic Stone'
                self.school = 'Conjuration'

        class Mending:
            def __init__(self):
                self.name = 'Mending'
                self.school = 'Conjuration'

        class Message:
            def __init__(self):
                self.name = 'Message'
                self.school = 'Conjuration'

        class PoisonSpray:
            def __init__(self):
                self.name = 'Poison Spray'
                self.school = 'Conjuration'

        class Prestidigitation:
            def __init__(self):
                self.name = 'Prestidigitation'
                self.school = 'Conjuration'

        class RayOfFrost:
            def __init__(self):
                self.name = 'Ray of Frost'
                self.school = 'Conjuration'

        class Resistance:
            def __init__(self):
                self.name = 'Resistance'
                self.school = 'Conjuration'

        class ShockingGrasp:
            def __init__(self):
                self.name = 'Shocking Grasp'
                self.school = 'Conjuration'

        class SpareTheDying:
            def __init__(self):
                self.name = 'Spare the Dying'
                self.school = 'Conjuration'

        class SwordBurst:
            def __init__(self):
                self.name = 'Sword Burst'
                self.school = 'Conjuration'

        class ThornWhip:
            def __init__(self):
                self.name = 'Thorn Whip'
                self.school = 'Conjuration'

        class Thunderclap:
            def __init__(self):
                self.name = 'Thunderclap'
                self.school = 'Conjuration'

    class Level1:
        def __init__(self):
            pass

        class AbsorbElements:
            def __init__(self):
                self.name = 'Absorb Elements'
                self.school = 'Abjuration'

        class Alarm:
            def __init__(self):
                self.name = 'Alarm'
                self.school = 'Abjuration'

        class ArcaneWeaponUA:
            def __init__(self):
                self.name = 'Arcane Weapon (UA)'
                self.school = 'Transmutation'

        class Catapult:
            def __init__(self):
                self.name = 'Catapult'
                self.school = 'Transmutation'

        class CureWounds:
            def __init__(self):
                self.name = 'Cure Wounds'
                self.school = 'Evocation'

        class DetectMagic:
            def __init__(self):
                self.name = 'Detect Magic'
                self.school = 'Divination'

        class DisguiseSelf:
            def __init__(self):
                self.name = 'Disguise Self'
                self.school = 'Illusion'

        class ExpeditiousRetreat:
            def __init__(self):
                self.name = 'Expeditious Retreat'
                self.school = 'Transmutation'

        class FaerieFire:
            def __init__(self):
                self.name = 'Faerie Fire'
                self.school = 'Evocation'

        class FalseLife:
            def __init__(self):
                self.name = 'False Life'
                self.school = 'Necromancy'

        class FeatherFall:
            def __init__(self):
                self.name = 'Feather Fall'
                self.school = 'Transmutation'

        class Grease:
            def __init__(self):
                self.name = 'Grease'
                self.school = 'Conjuration'

        class Identify:
            def __init__(self):
                self.name = 'Identify'
                self.school = 'Divination'

        class Jump:
            def __init__(self):
                self.name = 'Jump'
                self.school = 'Transmutation'

        class Longstrider:
            def __init__(self):
                self.name = 'Longstrider'
                self.school = 'Transmutation'

        class PurifyFoodAndDrink:
            def __init__(self):
                self.name = 'Purify Food and Drink'
                self.school = 'Transmutation'

        class Sanctuary:
            def __init__(self):
                self.name = 'Sanctuary'
                self.school = 'Abjuration'

        class Snare:
            def __init__(self):
                self.name = 'Snare'
                self.school = 'Abjuration'

        class TashasCausticBrew:
            def __init__(self):
                self.name = "Tasha's Caustic Brew"
                self.school = 'Conjuration'

    class Level2:
        def __init__(self):
            pass

        class Aid:
            def __init__(self):
                self.name = 'Aid'
                self.school = 'Abjuration'

        class AirBubble:
            def __init__(self):
                self.name = 'Air Bubble'
                self.school = 'Abjuration'  # Placeholder school, please update accordingly

        class AlterSelf:
            def __init__(self):
                self.name = 'Alter Self'
                self.school = 'Transmutation'

        class ArcaneLock:
            def __init__(self):
                self.name = 'Arcane Lock'
                self.school = 'Abjuration'

        class Blur:
            def __init__(self):
                self.name = 'Blur'
                self.school = 'Illusion'

        class ContinualFlame:
            def __init__(self):
                self.name = 'Continual Flame'
                self.school = 'Evocation'

        class Darkvision:
            def __init__(self):
                self.name = 'Darkvision'
                self.school = 'Transmutation'

        class EnhanceAbility:
            def __init__(self):
                self.name = 'Enhance Ability'
                self.school = 'Transmutation'

        class EnlargeReduce:
            def __init__(self):
                self.name = 'Enlarge/Reduce'
                self.school = 'Transmutation'

        class HeatMetal:
            def __init__(self):
                self.name = 'Heat Metal'
                self.school = 'Transmutation'

        class Invisibility:
            def __init__(self):
                self.name = 'Invisibility'
                self.school = 'Illusion'

        class KineticJaunt:
            def __init__(self):
                self.name = 'Kinetic Jaunt'
                self.school = 'Transmutation'  # Placeholder school, please update accordingly

        class LesserRestoration:
            def __init__(self):
                self.name = 'Lesser Restoration'
                self.school = 'Abjuration'

        class Levitate:
            def __init__(self):
                self.name = 'Levitate'
                self.school = 'Transmutation'

        class MagicMouth:
            def __init__(self):
                self.name = 'Magic Mouth'
                self.school = 'Illusion'

        class MagicWeapon:
            def __init__(self):
                self.name = 'Magic Weapon'
                self.school = 'Transmutation'

        class ProtectionFromPoison:
            def __init__(self):
                self.name = 'Protection from Poison'
                self.school = 'Abjuration'

        class Pyrotechnics:
            def __init__(self):
                self.name = 'Pyrotechnics'
                self.school = 'Transmutation'  # Placeholder school, please update accordingly

        class RopeTrick:
            def __init__(self):
                self.name = 'Rope Trick'
                self.school = 'Transmutation'  # Placeholder school, please update accordingly

        class SeeInvisibility:
            def __init__(self):
                self.name = 'See Invisibility'
                self.school = 'Divination'

        class Skywrite:
            def __init__(self):
                self.name = 'Skywrite'
                self.school = 'Transmutation'  # Placeholder school, please update accordingly

        class SpiderClimb:
            def __init__(self):
                self.name = 'Spider Climb'
                self.school = 'Transmutation'

        class VortexWarp:
            def __init__(self):
                self.name = 'Vortex Warp'
                self.school = 'Transmutation'  # Placeholder school, please update accordingly

        class Web:
            def __init__(self):
                self.name = 'Web'
                self.school = 'Conjuration'


class ArtificerSpellList:
    def __init__(self):
        self.cantrip_spell_names = [
            'AcidSplash',
            'BoomingBlade',
            'CreateBonfire',
            'DancingLights',
            'FireBolt',
            'Frostbite',
            'GreenFlameBlade',
            'Guidance',
            'Light',
            'LightningLure',
            'MageHand',
            'MagicStone',
            'Mending',
            'Message',
            'PoisonSpray',
            'Prestidigitation',
            'RayOfFrost',
            'Resistance',
            'ShockingGrasp',
            'SpareTheDying',
            'SwordBurst',
            'ThornWhip',
            'Thunderclap'
        ]

        self.level1_spell_names = [
            'AbsorbElements',
            'Alarm',
            'ArcaneWeaponUA',
            'Catapult',
            'CureWounds',
            'DetectMagic',
            'DisguiseSelf',
            'ExpeditiousRetreat',
            'FaerieFire',
            'FalseLife',
            'FeatherFall',
            'Grease',
            'Identify',
            'Jump',
            'Longstrider',
            'PurifyFoodAndDrink',
            'Sanctuary',
            'Snare',
            'TashasCausticBrew'
        ]

        self.level2_spell_names = [
            'Aid',
            'AirBubble',
            'AlterSelf',
            'ArcaneLock',
            'Blur',
            'ContinualFlame',
            'Darkvision',
            'EnhanceAbility',
            'EnlargeReduce',
            'HeatMetal',
            'Invisibility',
            'KineticJaunt',
            'LesserRestoration',
            'Levitate',
            'MagicMouth',
            'MagicWeapon',
            'ProtectionFromPoison',
            'Pyrotechnics',
            'RopeTrick',
            'SeeInvisibility',
            'Skywrite',
            'SpiderClimb',
            'VortexWarp',
            'Web'
        ]

        self.level3_spell_names = []

        self.level4_spell_names = []

        self.level5_spell_names = []

        self.cantrips = []
        self.level1 = []
        self.level2 = []
        self.level3 = []
        self.level4 = []
        self.level5 = []

    def load(self):
        for spell_name in self.cantrip_spell_names:
            # Use getattr to get the class from the spells.Level0 by name
            spell_class = getattr(Spells.Level0, spell_name, None)
            if spell_class:
                # Instantiate the class and append to the cantrips list
                self.cantrips.append(spell_class())
            else:
                print(f"Spell {spell_name} not found in Level0 spells.")

        for spell_name in self.level1_spell_names:
            # Use getattr to get the class from the spells.Level0 by name
            spell_class = getattr(Spells.Level1, spell_name, None)
            if spell_class:
                # Instantiate the class and append to the cantrips list
                self.level1.append(spell_class())
            else:
                print(f"Spell {spell_name} not found in Level0 spells.")

        for spell_name in self.level2_spell_names:
            # Use getattr to get the class from the spells.Level0 by name
            spell_class = getattr(Spells.Level2, spell_name, None)
            if spell_class:
                # Instantiate the class and append to the cantrips list
                self.level2.append(spell_class())
            else:
                print(f"Spell {spell_name} not found in Level0 spells.")


"""
artificer_spell_list = ArtificerSpellList()
artificer_spell_list.load()

for spell in artificer_spell_list.level2:
    print(f"{spell.name}: {spell.school}")
"""