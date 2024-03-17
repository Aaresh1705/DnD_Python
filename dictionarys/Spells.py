class ParrentParrentSpell:
    def __init__(self):
        self.name = ''
        self.type = None
        self.school = None
        self.casting_time = None
        self.range = None
        self.target = None
        self.components = None
        self.duration = None
        self.classes = None
        self.damage = None
        self.damage_type = None
        self.save = None

    def action_description(self, level):
        action_description = [
            f'{self.type} {self.school}',
            f'Casting time: {self.casting_time}',
            f'Range: {self.range}',
            f'Target: {self.target}',
            f'Duration: {self.duration}'
        ] if self.target else [
            f'{self.type} {self.school}',
            f'Casting time: {self.casting_time}',
            f'Range: {self.range}',
            f'Duration: {self.duration}'
        ]

        if self.damage:
            dam = f'Damage: {self.damage} {self.damage_type}'
            action_description.append(dam)
            if self.save:
                save = f'Save: {self.save}'
                action_description.append(save)
            else:
                action_description.append('There is no save')

        return action_description


class ParrentCantrip(ParrentParrentSpell):
    def __init__(self):
        super().__init__()
        self.type = 'Cantrip'


class ParrentLevel1(ParrentParrentSpell):
    def __init__(self):
        super().__init__()
        self.type = 'Level 1'


class ParrentLevel2(ParrentParrentSpell):
    def __init__(self):
        super().__init__()
        self.type = 'Level 2'


class ParrentLevel3(ParrentParrentSpell):
    def __init__(self):
        super().__init__()
        self.type = 'Level 3'


class ParrentLevel4:
    def __init__(self):
        super().__init__()
        self.type = 'Level 4'


class ParrentLevel5:
    def __init__(self):
        super().__init__()
        self.type = 'Level 5'


class ParrentLevel6:
    def __init__(self):
        super().__init__()
        self.type = 'Level 6'


class ParrentLevel7:
    def __init__(self):
        super().__init__()
        self.type = 'Level 7'


class ParrentLevel8:
    def __init__(self):
        super().__init__()
        self.type = 'Level 8'


class ParrentLevel9:
    def __init__(self):
        super().__init__()
        self.type = 'Level 9'


class Spells:
    def __init__(self):
        pass

    class Level0:
        def __init__(self):
            self.level = 0

        class AcidSplash(ParrentCantrip):
            def __init__(self):
                super().__init__()
                self.name = 'Acid Splash'
                self.school = 'Conjuration'
                self.casting_time = 'Action'
                self.range = 60
                self.duration = 'Instantaneous'
                self.components = 'V, S'
                self.image = f'images/spells/{self.name}.png'

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

        class BoomingBlade(ParrentCantrip):
            def __init__(self):
                super().__init__()
                self.name = 'Booming Blade'
                self.school = 'Evocation'
                self.casting_time = 'Action'
                self.range = 'Self (5-foot radius)'
                self.duration = '1 round'
                self.components = 'V, M (a weapon)'
                self.image = f'images/spells/{self.name}.png'

                self.description = (
                    "As part of the action used to cast this spell, you must make a melee attack with a weapon "
                    "against one creature within the spell's range, otherwise the spell fails. On a hit, the target "
                    "suffers the weapon attack's normal effects, and it becomes sheathed in booming energy until the "
                    "start of your next turn. If the target willingly moves before then, it immediately takes 1d8 "
                    "thunder damage, and the spell ends."
                )
                self.higher_levels = (
                    "At 5th level, the melee attack deals an extra 1d8 thunder damage to the target on a hit, and "
                    "the damage the target takes for moving increases to 2d8. Both damage rolls increase by 1d8 at "
                    "11th level and 17th level."
                )

            def damage(self, level):
                # The damage dealt if the target moves
                move_damage = '1d8'  # This is the damage at level 1-4
                # The additional damage dealt on hit at higher levels
                hit_damage = '0d8'  # No additional damage at level 1-4

                if level >= 17:
                    move_damage = '4d8'
                    hit_damage = '3d8'
                elif level >= 11:
                    move_damage = '3d8'
                    hit_damage = '2d8'
                elif level >= 5:
                    move_damage = '2d8'
                    hit_damage = '1d8'

                return hit_damage, move_damage

        class CreateBonfire(ParrentCantrip):
            def __init__(self):
                super().__init__()
                self.name = 'Create Bonfire'
                self.school = 'Conjuration'
                self.casting_time = 'Action'
                self.range = '60 feet'
                self.duration = 'Concentration, up to 1 minute'
                self.components = 'V, S'
                self.image = f'images/spells/{self.name}.png'

                self.description = (
                    "You create a bonfire on ground that you can see within range. Until the spell ends, the bonfire "
                    "fills a 5-foot cube. Any creature in the bonfire’s space when you cast the spell must succeed on a "
                    "Dexterity saving throw or take 1d8 fire damage. A creature must also make the saving throw when it "
                    "enters the bonfire’s space for the first time on a turn or ends its turn there."
                )
                self.higher_levels = (
                    "The spell’s damage increases by 1d8 when you reach 5th level (2d8), 11th level (3d8), and "
                    "17th level (4d8)."
                )

            def damage(self, level):
                if level >= 17:
                    return '4d8'
                elif level >= 11:
                    return '3d8'
                elif level >= 5:
                    return '2d8'
                else:
                    return '1d8'

        class DancingLights(ParrentCantrip):
            def __init__(self):
                super().__init__()
                self.name = 'Dancing Lights'
                self.school = 'Evocation'
                self.casting_time = 'Action'
                self.range = '120 feet'
                self.duration = 'Concentration, up to 1 minute'
                self.components = 'V, S, M (a bit of phosphorus or wychwood, or a glowworm)'
                self.image = f'images/spells/{self.name}.png'

                self.description = (
                    "You create up to four torch-sized lights within range, making them appear as torches, lanterns, or "
                    "glowing orbs that hover in the air for the duration. You can also combine the four lights into one "
                    "glowing vaguely humanoid form of Medium size. Whichever form you choose, each light sheds dim light in "
                    "a 10-foot radius."
                )

                self.higher_levels = (
                    "You can create an additional light when you reach 5th level (5 lights), 11th level (6 lights), and "
                    "17th level (7 lights)."
                )

        class FireBolt(ParrentCantrip):
            def __init__(self):
                super().__init__()
                self.name = 'Fire Bolt'
                self.school = 'Evocation'
                self.casting_time = '1 Action'
                self.range = '120 feet'
                self.duration = 'Instantaneous'
                self.components = 'V, S'
                self.damage = self.calculate_damage(0)
                self.damage_type = 'Fire'
                self.image = f'images/spells/{self.name}.png'

                self.description = (
                    "You hurl a mote of fire at a creature or object within range.",
                    "Make a ranged spell attack against the target.",
                    "On a hit, the target takes 1d10 fire damage.",
                    "A flammable object hit by this spell ignites if it ",
                    "isn't being worn or carried."
                )

                self.higher_levels = (
                    "This spell’s damage increases by 1d10 when you reach 5th level (2d10), 11th level (3d10), and "
                    "17th level (4d10)."
                )

            def calculate_damage(self, level):
                if level >= 17:
                    return '4d10'
                elif level >= 11:
                    return '3d10'
                elif level >= 5:
                    return '2d10'
                else:
                    return '1d10'

            def action_description(self, level):
                self.damage = self.calculate_damage(level)

                return super().action_description(level)

        class Frostbite(ParrentCantrip):
            def __init__(self):
                super().__init__()
                self.name = 'Frostbite'
                self.school = 'Evocation'
                self.casting_time = 'Action'
                self.range = '60 feet'
                self.duration = 'Instantaneous'
                self.components = 'V, S'
                self.image = f'images/spells/{self.name}.png'

                self.description = (
                    "You cause numbing frost to form on one creature that you can see within range. The target must make a "
                    "Constitution saving throw. On a failed save, the target takes 1d6 cold damage, and it has disadvantage "
                    "on the next weapon attack roll it makes before the end of its next turn."
                )

                self.higher_levels = (
                    "The spell’s damage increases by 1d6 when you reach 5th level (2d6), 11th level (3d6), and 17th level "
                    "(4d6)."
                )

            def damage(self, level):
                if level >= 17:
                    return '4d6'
                elif level >= 11:
                    return '3d6'
                elif level >= 5:
                    return '2d6'
                else:
                    return '1d6'

        class GreenFlameBlade(ParrentCantrip):
            def __init__(self):
                super().__init__()
                self.name = 'Green-Flame Blade'
                self.school = 'Evocation'
                self.casting_time = 'Action'
                self.range = 'Self'
                self.duration = 'Instantaneous'
                self.components = 'V, M (a weapon)'
                self.image = f'images/spells/{self.name}.png'

                self.description = (
                    "As part of the action used to cast this spell, you must make a melee attack with a weapon against "
                    "one creature within the spell's range, otherwise the spell fails. On a hit, the target suffers the "
                    "weapon attack's normal effects, and you can cause green fire to leap from the target to a different "
                    "creature of your choice that you can see within 5 feet of it. The second creature takes fire damage "
                    "equal to your spellcasting ability modifier."
                )

                self.higher_levels = (
                    "The fire damage increases when you reach higher levels. At 5th level, the melee attack deals an extra "
                    "1d8 fire damage to the target, and the fire damage to the second creature increases to 1d8 + your "
                    "spellcasting ability modifier. Both damage rolls increase by 1d8 at 11th level and 17th level."
                )

        class Guidance(ParrentCantrip):
            def __init__(self):
                super().__init__()
                self.name = 'Guidance'
                self.school = 'Divination'
                self.casting_time = 'Action'
                self.range = 'Touch'
                self.duration = 'Concentration, up to 1 minute'
                self.components = 'V, S'
                self.image = f'images/spells/{self.name}.png'

                self.description = (
                    "You touch one willing creature. Once before the spell ends, the target can roll a d4 and add the "
                    "number rolled to one ability check of its choice. It can roll the die before or after making the "
                    "ability check. The spell then ends."
                )

                self.higher_levels = (
                    "When you cast this spell using a spell slot of 2nd level or higher, the duration increases to 10 minutes."
                )

        class Light(ParrentCantrip):
            def __init__(self):
                super().__init__()
                self.name = 'Light'
                self.school = 'Evocation'
                self.casting_time = 'Action'
                self.range = 'Touch'
                self.duration = '1 hour'
                self.components = 'V, M (a firefly or phosphorescent moss)'
                self.image = f'images/spells/{self.name}.png'

                self.description = (
                    "You touch one object that is no larger than 10 feet in any dimension. Until the spell ends, the "
                    "object sheds bright light in a 20-foot radius and dim light for an additional 20 feet. The light can "
                    "be colored as you like. Completely covering the object with something opaque blocks the light. The "
                    "spell ends if you cast it again or dismiss it as an action."
                )

                self.higher_levels = (
                    "When you cast this spell using a spell slot of 2nd level or higher, the duration increases to 1 day."
                )

        class LightningLure(ParrentCantrip):
            def __init__(self):
                super().__init__()
                self.name = 'Lightning Lure'
                self.school = 'Evocation'
                self.casting_time = 'Action'
                self.range = '15 feet'
                self.duration = 'Instantaneous'
                self.components = 'V, S'
                self.image = f'images/spells/{self.name}.png'

                self.description = (
                    "You create a lash of lightning energy that strikes at one creature of your choice that you can see "
                    "within range. The target must succeed on a Strength saving throw or be pulled up to 10 feet in a "
                    "straight line toward you and then take 1d8 lightning damage if it is within 5 feet of you."
                )

                self.higher_levels = (
                    "The damage increases by 1d8 when you reach 5th level (2d8), 11th level (3d8), and 17th level (4d8)."
                )

            def damage(self, level):
                if level >= 17:
                    return '4d8'
                elif level >= 11:
                    return '3d8'
                elif level >= 5:
                    return '2d8'
                else:
                    return '1d8'

        class MageHand(ParrentCantrip):
            def __init__(self):
                super().__init__()
                self.name = 'Mage Hand'
                self.school = 'Conjuration'
                self.casting_time = '1 Action'
                self.range = '30 feet'
                self.duration = '1 minute'
                self.components = 'V, S'
                self.image = f'images/spells/{self.name}.png'

                self.description = (
                    "A spectral, floating hand appears at a point you choose within range.",
                    "The hand lasts for the duration or until you dismiss it as an action.",
                    "The hand vanishes if it is ever more than 30 feet away",
                    "from you or if you cast this spell again.",
                    "You can use your action to control the hand. You can use",
                    "the hand to manipulate an object,",
                    "open an unlocked door or container,",
                    "stow or retrieve an item from an open container,",
                    "or pour the contents out of a vial."
                )

                self.higher_levels = (
                    "When you cast this spell using a spell slot of 5th level or higher, the duration increases to 10 minutes."
                )

        class MagicStone(ParrentCantrip):
            def __init__(self):
                super().__init__()
                self.name = 'Magic Stone'
                self.school = 'Transmutation'
                self.casting_time = '1 bonus action'
                self.range = 'Touch'
                self.duration = '1 minute'
                self.components = 'V, S'
                self.image = f'images/spells/{self.name}.png'

                self.description = (
                    "You touch one to three pebbles and imbue them with magic. You or someone else can make a ranged spell "
                    "attack with one of the pebbles by throwing it or hurling it with a sling. If thrown, it has a range of "
                    "30 feet. If someone else attacks with the pebble, that attacker adds your spellcasting ability modifier, "
                    "not the attacker’s, to the attack roll. On a hit, the target takes bludgeoning damage equal to 1d6 + your "
                    "spellcasting ability modifier. Hit or miss, the spell then ends on the stone."
                )

                self.higher_levels = (
                    "When you cast this spell using a spell slot of 2nd level or higher, the number of pebbles you can affect "
                    "with this spell increases by one for each slot level above 1st."
                )

        class Mending(ParrentCantrip):
            def __init__(self):
                super().__init__()
                self.name = 'Mending'
                self.school = 'Transmutation'
                self.casting_time = '1 minute'
                self.range = 'Touch'
                self.duration = 'Instantaneous'
                self.components = 'V, S, M (two lodestones)'
                self.image = f'images/spells/{self.name}.png'

                self.description = (
                    "This spell repairs a single break or tear in an object you touch, such as a broken key, a torn cloak, or "
                    "a leaking wineskin. As long as the break or tear is no longer than 1 foot in any dimension, you mend it. "
                    "Leaving out any missing pieces."
                )

        class Message(ParrentCantrip):
            def __init__(self):
                super().__init__()
                self.name = 'Message'
                self.school = 'Transmutation'
                self.casting_time = '1 action'
                self.range = '120 feet'
                self.duration = '1 round'
                self.components = 'V, S, M (a short piece of copper wire)'
                self.image = f'images/spells/{self.name}.png'

                self.description = (
                    "You point your finger toward a creature within range and whisper a message. The target (and only the "
                    "target) hears the message and can reply in a whisper that only you can hear."
                )

                self.higher_levels = (
                    "When you cast this spell using a spell slot of 3rd level or higher, the duration of the spell increases "
                    "by 10 minutes for each slot level above 2nd."
                )

        class PoisonSpray(ParrentCantrip):
            def __init__(self):
                super().__init__()
                self.name = 'Poison Spray'
                self.school = 'Conjuration'
                self.casting_time = 'Action'
                self.range = '10 feet'
                self.duration = 'Instantaneous'
                self.components = 'V, S'
                self.image = f'images/spells/{self.name}.png'

                self.description = (
                    "You extend your hand toward a creature you can see within range and project a puff of noxious gas from "
                    "your palm. The creature must succeed on a Constitution saving throw or take 1d12 poison damage."
                )

                self.higher_levels = (
                    "The spell’s damage increases by 1d12 when you reach 5th level (2d12), 11th level (3d12), and 17th level "
                    "(4d12)."
                )

            def damage(self, level):
                if level >= 17:
                    return '4d12'
                elif level >= 11:
                    return '3d12'
                elif level >= 5:
                    return '2d12'
                else:
                    return '1d12'

        class Prestidigitation(ParrentCantrip):
            def __init__(self):
                super().__init__()
                self.name = 'Prestidigitation'
                self.school = 'Transmutation'
                self.casting_time = 'Action'
                self.range = '10 feet'
                self.duration = '1 hour'
                self.components = 'V, S'
                self.image = f'images/spells/{self.name}.png'

                self.description = (
                    "This spell is a minor magical trick that novice spellcasters use for practice. You create one of the "
                    "following magical effects within range: - You create an instantaneous, harmless sensory effect, such "
                    "as a shower of sparks, a puff of wind, faint musical notes, or an odd odor. - You instantaneously "
                    "light or snuff out a candle, a torch, or a small campfire. - You instantaneously clean or soil an "
                    "object no larger than 1 cubic foot. - You chill, warm, or flavor up to 1 cubic foot of nonliving "
                    "material for 1 hour. - You make a color, a small mark, or a symbol appear on an object or a surface "
                    "for 1 hour. - You create a nonmagical trinket or an illusory image that can fit in your hand and "
                    "that lasts until the end of your next turn."
                )

                self.higher_levels = (
                    "When you cast this spell using a spell slot of 2nd level or higher, you can affect one additional "
                    "cubic foot of material for each slot level above 1st."
                )

        class RayOfFrost(ParrentCantrip):
            def __init__(self):
                super().__init__()
                self.name = 'Ray of Frost'
                self.school = 'Evocation'
                self.casting_time = '1 action'
                self.range = '60 feet'
                self.duration = 'Instantaneous'
                self.components = 'V, S'
                self.image = f'images/spells/{self.name}.png'

                self.description = (
                    "A frigid beam of blue-white light streaks toward a creature within range. Make a ranged spell attack "
                    "against the target. On a hit, it takes 1d8 cold damage, and its speed is reduced by 10 feet until the "
                    "start of your next turn."
                )

                self.higher_levels = (
                    "This spell’s damage increases by 1d8 when you reach 5th level (2d8), 11th level (3d8), and 17th level (4d8)."
                )

        class Resistance(ParrentCantrip):
            def __init__(self):
                super().__init__()
                self.name = 'Resistance'
                self.school = 'Abjuration'
                self.casting_time = '1 action'
                self.range = 'Touch'
                self.duration = 'Concentration, up to 1 minute'
                self.components = 'V, S, M (a miniature cloak)'
                self.image = f'images/spells/{self.name}.png'

                self.description = (
                    "You touch one willing creature. Once before the spell ends, the target can roll a d4 and add the number "
                    "rolled to one saving throw of its choice. It can roll the die before or after making the saving throw. "
                    "The spell then ends."
                )

                self.higher_levels = (
                    "When you cast this spell using a spell slot of 3rd level or higher, you can target one additional "
                    "creature for each slot level above 2nd."
                )

        class ShockingGrasp(ParrentCantrip):
            def __init__(self):
                super().__init__()
                self.name = 'Shocking Grasp'
                self.school = 'Evocation'
                self.casting_time = '1 action'
                self.range = 'Touch'
                self.duration = 'Instantaneous'
                self.components = 'V, S'
                self.image = f'images/spells/{self.name}.png'

                self.description = (
                    "Lightning springs from your hand to deliver a shock to a creature you try to touch. Make a melee spell "
                    "attack against the target. You have advantage on the attack roll if the target is wearing armor made of "
                    "metal. On a hit, the target takes 1d8 lightning damage, and it can’t take reactions until the start of "
                    "its next turn."
                )

                self.higher_levels = (
                    "The spell’s damage increases by 1d8 when you reach 5th level (2d8), 11th level (3d8), and 17th level (4d8)."
                )

        class SpareTheDying(ParrentCantrip):
            def __init__(self):
                super().__init__()
                self.name = 'Spare the Dying'
                self.school = 'Necromancy'
                self.casting_time = '1 action'
                self.range = 'Touch'
                self.duration = 'Instantaneous'
                self.components = 'V, S'
                self.image = f'images/spells/{self.name}.png'

                self.description = (
                    "You touch a living creature that has 0 hit points. The creature becomes stable. This spell has no effect "
                    "on undead or constructs."
                )

                self.higher_levels = None  # No effect at higher levels

        class SwordBurst(ParrentCantrip):
            def __init__(self):
                super().__init__()
                self.name = 'Sword Burst'
                self.school = 'Conjuration'
                self.casting_time = '1 action'
                self.range = '5 feet'
                self.duration = 'Instantaneous'
                self.components = 'V, M (a sword blade or small piece of metal)'
                self.image = f'images/spells/{self.name}.png'

                self.description = (
                    "You create a momentary circle of spectral blades that sweep around you. Each creature within range, "
                    "other than you, must succeed on a Dexterity saving throw or take 1d6 force damage."
                )

                self.higher_levels = (
                    "The spell’s damage increases by 1d6 when you reach 5th level (2d6), 11th level (3d6), and 17th level (4d6)."
                )

        class ThornWhip(ParrentCantrip):
            def __init__(self):
                super().__init__()
                self.name = 'Thorn Whip'
                self.school = 'Transmutation'
                self.casting_time = '1 action'
                self.range = '30 feet'
                self.duration = 'Instantaneous'
                self.components = 'V, S, M (the stem of a plant with thorns)'
                self.image = f'images/spells/{self.name}.png'

                self.description = (
                    "You create a long, vine-like whip covered in thorns that lashes out at your command toward a creature "
                    "in range. Make a melee spell attack against the target. If the attack hits, the creature takes 1d6 "
                    "piercing damage, and if the creature is Large or smaller, you pull the creature up to 10 feet closer to "
                    "you."
                )

                self.higher_levels = (
                    "This spell’s damage increases by 1d6 when you reach 5th level (2d6), 11th level (3d6), and 17th level (4d6)."
                )

        class Thunderclap(ParrentCantrip):
            def __init__(self):
                super().__init__()
                self.name = 'Thunderclap'
                self.school = 'Evocation'
                self.casting_time = '1 action'
                self.range = 'Self (5-foot radius)'
                self.duration = 'Instantaneous'
                self.components = 'V, S'
                self.image = f'images/spells/{self.name}.png'

                self.description = (
                    "You create a burst of thunderous sound that can be heard up to 100 feet away. Each creature within range "
                    "other than you must succeed on a Constitution saving throw or take 1d6 thunder damage."
                )

                self.higher_levels = (
                    "This spell’s damage increases by 1d6 when you reach 5th level (2d6), 11th level (3d6), and 17th level (4d6)."
                )

    class Level1:
        class AbsorbElements(ParrentLevel1):
            def __init__(self):
                super().__init__()
                self.name = 'Absorb Elements'
                self.school = 'Abjuration'
                self.casting_time = '1 reaction'
                self.range = 'Self'
                self.duration = '1 round'
                self.components = 'S'
                self.image = f'images/spells/{self.name}.png'

                self.description = (
                    "The spell captures some of the incoming energy, lessening its effect on you and storing it for your next "
                    "melee attack. You have resistance to the triggering damage type until the start of your next turn. Also, "
                    "the first time you hit with a melee attack on your next turn, the target takes an extra 1d6 damage of the "
                    "triggering type, and the spell ends."
                )

                self.higher_levels = None  # No effect at higher levels

        class Alarm:
            def __init__(self):
                self.name = 'Alarm'
                self.school = 'Abjuration'
                self.casting_time = '1 minute'
                self.range = '30 feet'
                self.duration = '8 hours'
                self.components = 'V, S, M (a tiny bell and a piece of fine silver wire)'
                self.image = f'images/spells/{self.name}.png'

                self.description = (
                    "You set an alarm against unwanted intrusion. Choose a door, a window, or an area within range that is no "
                    "larger than a 20-foot cube. Until the spell ends, an alarm alerts you whenever a tiny or larger creature "
                    "touches or enters the warded area. When you cast the spell, you can designate creatures that won’t set off "
                    "the alarm. You also choose whether the alarm is mental or audible."
                )

                self.higher_levels = None  # No effect at higher levels

        class ArcaneWeaponUA:
            def __init__(self):
                self.name = 'Arcane Weapon (UA)'
                self.school = 'Transmutation'
                self.casting_time = '1 bonus action'
                self.range = 'Self'
                self.duration = 'Concentration, up to 1 hour'
                self.components = 'V, S'
                self.image = f'images/spells/{self.name}.png'

                self.description = (
                    "You channel arcane energy into one simple or martial weapon you’re holding, and choose a damage type: acid, "
                    "cold, fire, lightning, poison, or thunder. Until the spell ends, you deal an extra 1d6 damage of the chosen "
                    "type to any target you hit with the weapon. If the weapon isn’t magical, it becomes a magic weapon for the "
                    "spell’s duration."
                )

                self.higher_levels = None  # No effect at higher levels

        class Catapult:
            def __init__(self):
                self.name = 'Catapult'
                self.school = 'Transmutation'
                self.casting_time = '1 action'
                self.range = '60 feet'
                self.duration = 'Instantaneous'
                self.components = 'S'
                self.image = f'images/spells/{self.name}.png'

                self.description = (
                    "Choose one object weighing 1 to 5 pounds within range that isn’t being worn or carried. The object "
                    "flies in a straight line up to 90 feet in a direction you choose before falling to the ground, stopping "
                    "early if it impacts against a solid surface. If the object would strike a creature, that creature must "
                    "make a Dexterity saving throw. On a failed save, the object strikes the target and stops moving. When the "
                    "object strikes something, the object and what it strikes each take 3d8 bludgeoning damage."
                )

                self.higher_levels = (
                    "When you cast this spell using a spell slot of 2nd level or higher, the maximum weight of objects that "
                    "you can target with this spell increases by 5 pounds, and the damage increases by 1d8, for each slot level "
                    "above 1st."
                )

        class CureWounds:
            def __init__(self):
                self.name = 'Cure Wounds'
                self.school = 'Evocation'
                self.casting_time = '1 action'
                self.range = 'Touch'
                self.duration = 'Instantaneous'
                self.components = 'V, S'
                self.image = f'images/spells/{self.name}.png'

                self.description = (
                    "A creature you touch regains a number of hit points equal to 1d8 + your spellcasting ability modifier. "
                    "This spell has no effect on undead or constructs."
                )

                self.higher_levels = (
                    "When you cast this spell using a spell slot of 2nd level or higher, the healing increases by 1d8 for each "
                    "slot level above 1st."
                )

        class DetectMagic(ParrentLevel1):
            def __init__(self):
                super().__init__()
                self.name = 'Detect Magic'
                self.school = 'Divination'
                self.casting_time = '1 action'
                self.range = 'Self'
                self.duration = 'Concentration, up to 10 minutes'
                self.components = 'V, S'
                self.image = f'images/spells/{self.name}.png'

                self.description = (
                    "For the duration, you sense the presence of magic within 30 feet of you. If you sense magic in this way, "
                    "you can use your action to see a faint aura around any visible creature or object in the area that bears "
                    "magic, and you learn its school of magic, if any."
                )

                self.higher_levels = None  # No effect at higher levels

        class DisguiseSelf:
            def __init__(self):
                self.name = 'Disguise Self'
                self.school = 'Illusion'
                self.casting_time = '1 action'
                self.range = 'Self'
                self.duration = '1 hour'
                self.components = 'V, S'
                self.image = f'images/spells/{self.name}.png'

                self.description = (
                    "You make yourself--including your clothing, armor, weapons, and other belongings on your person--look "
                    "different until the spell ends or until you use your action to dismiss it. You can seem 1 foot shorter or "
                    "taller and can appear thin, fat, or in between. You can’t change your body type, so you must adopt a form "
                    "that has the same basic arrangement of limbs. Otherwise, the extent of the illusion is up to you."
                )

                self.higher_levels = None  # No effect at higher levels

        class ExpeditiousRetreat:
            def __init__(self):
                self.name = 'Expeditious Retreat'
                self.school = 'Transmutation'
                self.casting_time = '1 bonus action'
                self.range = 'Self'
                self.duration = 'Concentration, up to 10 minutes'
                self.components = 'V, S'
                self.image = f'images/spells/{self.name}.png'

                self.description = (
                    "This spell allows you to move at an incredible pace. When you cast this spell, and then as a bonus action "
                    "on each of your turns until the spell ends, you can take the Dash action."
                )

                self.higher_levels = None  # No effect at higher levels

        class FaerieFire:
            def __init__(self):
                self.name = 'Faerie Fire'
                self.school = 'Evocation'
                self.casting_time = '1 action'
                self.range = '60 feet'
                self.duration = 'Concentration, up to 1 minute'
                self.components = 'V'
                self.image = f'images/spells/{self.name}.png'

                self.description = (
                    "Each object in a 20-foot cube within range is outlined in blue, green, or violet light (your choice). "
                    "Any creature in the area when the spell is cast is also outlined in light if it fails a Dexterity saving "
                    "throw. For the duration, objects and affected creatures shed dim light in a 10-foot radius."
                )

                self.higher_levels = None  # No effect at higher levels

        class FalseLife:
            def __init__(self):
                self.name = 'False Life'
                self.school = 'Necromancy'
                self.casting_time = '1 action'
                self.range = 'Self'
                self.duration = '1 hour'
                self.components = 'V, S, M (a small amount of alcohol or distilled spirits)'
                self.image = f'images/spells/{self.name}.png'

                self.description = (
                    "You gain 1d4 + 4 temporary hit points for the duration."
                )

                self.higher_levels = (
                    "When you cast this spell using a spell slot of 2nd level or higher, you gain 5 additional temporary hit "
                    "points for each slot level above 1st."
                )

        class FeatherFall:
            def __init__(self):
                self.name = 'Feather Fall'
                self.school = 'Transmutation'
                self.casting_time = '1 reaction, which you take when you or a creature within 60 feet of you falls'
                self.range = '60 feet'
                self.duration = '1 minute'
                self.components = 'V, M (a small feather or piece of down)'
                self.image = f'images/spells/{self.name}.png'

                self.description = (
                    "Choose up to five falling creatures within range. A falling creature's rate of descent slows to 60 feet "
                    "per round until the spell ends. If the creature lands before the spell ends, it takes no falling damage "
                    "and can land on its feet, and the spell ends for that creature."
                )

                self.higher_levels = None  # No effect at higher levels

        class Grease:
            def __init__(self):
                self.name = 'Grease'
                self.school = 'Conjuration'
                self.casting_time = '1 action'
                self.range = '60 feet'
                self.duration = '1 minute'
                self.components = 'V, S, M (a bit of pork rind or butter)'
                self.image = f'images/spells/{self.name}.png'

                self.description = (
                    "Slick grease covers the ground in a 10-foot square centered on a point within range and turns it into "
                    "difficult terrain for the duration. When the grease appears, each creature standing in its area must "
                    "succeed on a Dexterity saving throw or fall prone. A creature that enters the area or ends its turn there "
                    "must also succeed on a Dexterity saving throw or fall prone."
                )

                self.higher_levels = None  # No effect at higher levels

        class Identify(ParrentLevel1):
            def __init__(self):
                super().__init__()
                self.name = 'Identify'
                self.school = 'Divination'
                self.casting_time = '1 minute'
                self.range = 'Touch'
                self.duration = 'Instantaneous'
                self.components = 'V, S, M (a pearl worth at least 100 gp and an owl feather)'
                self.image = f'images/spells/{self.name}.png'

                self.description = (
                    "You choose one object that you must touch throughout the casting of the spell. If it is a magic item "
                    "or some other magic-imbued object, you learn its properties and how to use them, whether it requires "
                    "attunement to use, and how many charges it has, if any. You learn whether any spells are affecting the "
                    "item and what they are. If the item was created by a spell, you learn which spell created it."
                )

                self.higher_levels = None  # No effect at higher levels

        class Jump:
            def __init__(self):
                self.name = 'Jump'
                self.school = 'Transmutation'
                self.casting_time = '1 action'
                self.range = 'Touch'
                self.duration = '1 minute'
                self.components = 'V, S, M (a grasshopper’s hind leg)'
                self.image = f'images/spells/{self.name}.png'

                self.description = (
                    "You touch a creature. The creature’s jump distance is tripled until the spell ends."
                )

                self.higher_levels = (
                    "When you cast this spell using a spell slot of 2nd level or higher, you can target one additional "
                    "creature for each slot level above 1st."
                )

        class Longstrider:
            def __init__(self):
                self.name = 'Longstrider'
                self.school = 'Transmutation'
                self.casting_time = '1 action'
                self.range = 'Touch'
                self.duration = '1 hour'
                self.components = 'V, S, M (a pinch of dirt)'
                self.image = f'images/spells/{self.name}.png'

                self.description = (
                    "You touch a creature. The target’s speed increases by 10 feet until the spell ends."
                )

                self.higher_levels = (
                    "When you cast this spell using a spell slot of 2nd level or higher, you can target one additional "
                    "creature for each slot level above 1st."
                )

        class PurifyFoodAndDrink:
            def __init__(self):
                self.name = 'Purify Food and Drink'
                self.school = 'Transmutation'
                self.casting_time = '1 action'
                self.range = '10 feet'
                self.duration = 'Instantaneous'
                self.components = 'V, S'
                self.image = f'images/spells/{self.name}.png'

                self.description = (
                    "All nonmagical food and drink within a 5-foot-radius sphere centered on a point of your choice within "
                    "range is purified and rendered free of poison and disease."
                )

                self.higher_levels = None  # No effect at higher levels

        class Sanctuary:
            def __init__(self):
                self.name = 'Sanctuary'
                self.school = 'Abjuration'
                self.casting_time = '1 bonus action'
                self.range = '30 feet'
                self.duration = '1 minute'
                self.components = 'V, S, M (a small silver mirror)'
                self.image = f'images/spells/{self.name}.png'

                self.description = (
                    "You ward a creature within range against attack. Until the spell ends, any creature who targets the warded "
                    "creature with an attack or a harmful spell must first make a Wisdom saving throw. On a failed save, the "
                    "creature must choose a new target or lose the attack or spell. This spell doesn’t protect the warded "
                    "creature from area effects, such as the explosion of a fireball."
                )

                self.higher_levels = None  # No effect at higher levels

        class Snare:
            def __init__(self):
                self.name = 'Snare'
                self.school = 'Abjuration'
                self.casting_time = '1 minute'
                self.range = 'Touch'
                self.duration = 'Until dispelled or triggered'
                self.components = 'V, S, M (25 feet of rope, which the spell consumes)'
                self.image = f'images/spells/{self.name}.png'

                self.description = (
                    "When you cast this spell, you create a magic booby trap that can be made from any amount of rope. "
                    "The rope must be within your reach throughout the casting of the spell. When you finish casting, the "
                    "rope disappears and turns into a snare. "
                    "The snare is nearly invisible, requiring a successful Intelligence (Investigation) check against your "
                    "spell save DC to be discerned."
                )

                self.higher_levels = None  # No effect at higher levels

        class TashasCausticBrew(ParrentLevel1):
            def __init__(self):
                super().__init__()
                self.name = "Tasha's Caustic Brew"
                self.school = 'Conjuration'
                self.casting_time = '1 action'
                self.range = '60 feet'
                self.duration = 'Instantaneous'
                self.components = 'V, S, M (a bit of rotten food)'
                self.image = f'images/spells/{self.name}.png'

                self.description = (
                    "You hurl a bubble of acid. Choose one creature you can see within range, or choose two creatures you can "
                    "see within range that are within 5 feet of each other. A target must succeed on a Dexterity saving throw "
                    "or take 2d4 acid damage."
                )

                self.higher_levels = (
                    "When you cast this spell using a spell slot of 2nd level or higher, the damage increases by 1d4 for each "
                    "slot level above 1st."
                )

    class Level2:
        class Aid:
            def __init__(self):
                self.name = 'Aid'
                self.school = 'Abjuration'
                self.casting_time = '1 action'
                self.range = '30 feet'
                self.duration = '8 hours'
                self.components = 'V, S, M (a tiny strip of white cloth)'
                self.image = f'images/spells/{self.name}.png'

                self.description = (
                    "Your spell bolsters your allies with toughness and resolve. Choose up to three creatures within range. "
                    "Each target’s hit point maximum and current hit points increase by 5 for the duration."
                )

                self.higher_levels = None  # No effect at higher levels

        class AirBubble:
            def __init__(self):
                self.name = 'Air Bubble'
                self.school = 'Abjuration'
                self.casting_time = '1 action'
                self.range = '30 feet'
                self.duration = '1 hour'
                self.components = 'V, S, M (a soap bubble)'
                self.image = f'images/spells/{self.name}.png'

                self.description = (
                    "This spell creates a bubble of clean air that surrounds the caster, allowing them to breathe normally "
                    "in any environment."
                )

                self.higher_levels = None  # No effect at higher levels

        class AlterSelf:
            def __init__(self):
                self.name = 'Alter Self'
                self.school = 'Transmutation'
                self.casting_time = '1 action'
                self.range = 'Self'
                self.duration = '1 hour'
                self.components = 'V, S'
                self.image = f'images/spells/{self.name}.png'

                self.description = (
                    "You assume a different form. When you cast the spell, choose one of the following options, the effects "
                    "of which last for the duration of the spell."
                    "\n- Aquatic Adaptation: You adapt your body to an aquatic environment, sprouting gills and growing webbing "
                    "between your fingers."
                    "\n- Change Appearance: You transform your appearance. You decide what you look like, including your height, "
                    "weight, facial features, sound of your voice, hair length, coloration, and distinguishing characteristics, "
                    "if any. You can make yourself appear as a member of another race, though none of your statistics change."
                    "\n- Natural Weapons: You grow claws, fangs, spines, horns, or a different natural weapon of your choice. "
                    "Your unarmed strikes deal 1d6 bludgeoning, piercing, or slashing damage, as appropriate to the natural "
                    "weapon you chose, and you are proficient with your unarmed strikes."
                )

                self.higher_levels = None  # No effect at higher levels

        class ArcaneLock:
            def __init__(self):
                self.name = 'Arcane Lock'
                self.school = 'Abjuration'
                self.casting_time = '1 action'
                self.range = 'Touch'
                self.duration = 'Until dispelled'
                self.components = 'V, S, M (gold dust worth at least 25 gp, which the spell consumes)'
                self.image = f'images/spells/{self.name}.png'

                self.description = (
                    "You touch a closed door, window, gate, chest, or other entryway, and it becomes locked for the duration. "
                    "You and the creatures you designate when you cast this spell can open the object normally. You can also set "
                    "a password that, when spoken within 5 feet of the object, suppresses this spell for 1 minute. Otherwise, it "
                    "is impassable until it is broken or the spell is dispelled or suppressed."
                )

                self.higher_levels = None  # No effect at higher levels

        class Blur:
            def __init__(self):
                self.name = 'Blur'
                self.school = 'Illusion'
                self.casting_time = '1 action'
                self.range = 'Self'
                self.duration = '1 minute'
                self.components = 'V'
                self.image = f'images/spells/{self.name}.png'

                self.description = (
                    "Your body becomes blurred, shifting and wavering to all who can see you. For the duration, any creature "
                    "has disadvantage on attack rolls against you. An attacker is immune to this effect if it doesn’t rely on "
                    "sight, as with blindsight, or can see through illusions, as with truesight."
                )

                self.higher_levels = None  # No effect at higher levels

        class ContinualFlame:
            def __init__(self):
                self.name = 'Continual Flame'
                self.school = 'Evocation'
                self.casting_time = '1 action'
                self.range = 'Touch'
                self.duration = 'Until dispelled'
                self.components = 'V, S, M (ruby dust worth 50 gp, which the spell consumes)'
                self.image = f'images/spells/{self.name}.png'

                self.description = (
                    "A flame, equivalent in brightness to a torch, springs forth from an object that you touch. The effect "
                    "looks like a regular flame, but it creates no heat and doesn’t use oxygen. A continual flame can be covered "
                    "or hidden but not smothered or quenched."
                )

                self.higher_levels = None  # No effect at higher levels

        class Darkvision:
            def __init__(self):
                self.name = 'Darkvision'
                self.school = 'Transmutation'
                self.casting_time = '1 action'
                self.range = 'Touch'
                self.duration = '8 hours'
                self.components = 'V, S, M (either a pinch of dried carrot or an agate)'
                self.image = f'images/spells/{self.name}.png'

                self.description = (
                    "You touch a willing creature to grant it the ability to see in the dark. For the duration, that creature "
                    "has darkvision out to a range of 60 feet."
                )

                self.higher_levels = None  # No effect at higher levels

        class EnhanceAbility:
            def __init__(self):
                self.name = 'Enhance Ability'
                self.school = 'Transmutation'
                self.casting_time = '1 action'
                self.range = 'Touch'
                self.duration = 'Concentration, up to 1 hour'
                self.components = 'V, S, M (fur or a feather from a beast)'
                self.image = f'images/spells/{self.name}.png'

                self.description = (
                    "You touch a creature and bestow upon it a magical enhancement. Choose one of the following effects; the "
                    "target gains that effect until the spell ends."
                    "\n- Bear’s Endurance: The target has advantage on Constitution checks. It also gains 2d6 temporary hit points, "
                    "which are lost when the spell ends."
                    "\n- Bull’s Strength: The target has advantage on Strength checks, and his or her carrying capacity doubles."
                    "\n- Cat’s Grace: The target has advantage on Dexterity checks. It also doesn’t take damage from falling 20 "
                    "feet or less if it isn’t incapacitated."
                    "\n- Eagle’s Splendor: The target has advantage on Charisma checks."
                    "\n- Fox’s Cunning: The target has advantage on Intelligence checks."
                    "\n- Owl’s Wisdom: The target has advantage on Wisdom checks."
                )

                self.higher_levels = None  # No effect at higher levels

        class EnlargeReduce:
            def __init__(self):
                self.name = 'Enlarge Reduce'
                self.school = 'Transmutation'
                self.casting_time = '1 action'
                self.range = '30 feet'
                self.duration = '1 minute'
                self.components = 'V, S, M (powdered iron)'
                self.image = f'images/spells/{self.name}.png'

                self.description = (
                    "You cause a creature or an object you can see within range to grow larger or smaller for the duration. "
                    "Choose either a creature or an object that is neither worn nor carried. If the target is unwilling, it "
                    "can make a Constitution saving throw. On a success, the spell has no effect."
                    "\n- Enlarge: The target’s size doubles in all dimensions, and its weight is multiplied by eight. This "
                    "growth increases its size by one category—from Medium to Large, for example. If there isn’t enough room "
                    "for the target to double its size, the creature or object attains the maximum possible size in the space "
                    "available. Until the spell ends, the target also has advantage on Strength checks and Strength saving "
                    "throws. The target’s weapons also grow to match its new size. While these weapons are enlarged, the "
                    "target’s attacks with them deal 1d4 extra damage."
                    "\n- Reduce: The target’s size is halved in all dimensions, and its weight is reduced to one-eighth of normal. "
                    "This reduction decreases its size by one category—from Medium to Small, for example. Until the spell ends, "
                    "the target also has disadvantage on Strength checks and Strength saving throws. The target’s weapons also "
                    "shrink to match its new size. While these weapons are reduced, the target’s attacks with them deal 1d4 "
                    "less damage (this can’t reduce the damage below 1)."
                )

                self.higher_levels = None  # No effect at higher levels

        class HeatMetal(ParrentLevel2):
            def __init__(self):
                super().__init__()
                self.name = 'Heat Metal'
                self.school = 'Transmutation'
                self.casting_time = '1 action'
                self.range = '60 feet'
                self.duration = 'Concentration, up to 1 minute'
                self.components = 'V, S, M (a piece of iron and a flame)'
                self.image = f'images/spells/{self.name}.png'

                self.description = (
                    "Choose a manufactured metal object, such as a metal weapon or a suit of heavy or medium metal armor, "
                    "that you can see within range. You cause the object to glow red-hot. Any creature in physical contact "
                    "with the object takes 2d8 fire damage when you cast the spell. Until the spell ends, you can use a bonus "
                    "action on each of your subsequent turns to cause this damage again."
                    "\nIf a creature is holding or wearing the object and takes the damage from it, the creature must succeed "
                    "on a Constitution saving throw or drop the object if it can. If it doesn’t drop the object, it has "
                    "disadvantage on attack rolls and ability checks until the start of your next turn."
                )

                self.higher_levels = None  # No effect at higher levels

        class Invisibility:
            def __init__(self):
                self.name = 'Invisibility'
                self.school = 'Illusion'
                self.casting_time = '1 action'
                self.range = 'Touch'
                self.duration = 'Concentration, up to 1 hour'
                self.components = 'V, S, M (an eyelash encased in gum arabic)'
                self.image = f'images/spells/{self.name}.png'

                self.description = (
                    "A creature you touch becomes invisible until the spell ends. Anything the target is wearing or carrying "
                    "is invisible as long as it is on the target’s person. The spell ends for a target that attacks or casts "
                    "a spell."
                )

                self.higher_levels = None  # No effect at higher levels

        class KineticJaunt:
            def __init__(self):
                self.name = 'Kinetic Jaunt'
                self.school = 'Transmutation'
                self.casting_time = '1 action'
                self.range = 'Self'
                self.duration = 'Instantaneous'
                self.components = 'V'
                self.image = f'images/spells/{self.name}.png'

                self.description = (
                    "When you cast this spell, you can use your reaction to teleport up to 30 feet to an unoccupied space you "
                    "can see. Alternatively, you can choose a point within range, and a spectral hand teleports up to 30 feet "
                    "to that spot. If you are within range of the hand, you can use your reaction to teleport up to 30 feet to "
                    "an unoccupied space you can see."
                )

                self.higher_levels = None  # No effect at higher levels

        class LesserRestoration:
            def __init__(self):
                self.name = 'Lesser Restoration'
                self.school = 'Abjuration'
                self.casting_time = '1 action'
                self.range = 'Touch'
                self.duration = 'Instantaneous'
                self.components = 'V, S'
                self.image = f'images/spells/{self.name}.png'

                self.description = (
                    "You touch a creature and can end either one disease or one condition afflicting it. The condition can be "
                    "blinded, deafened, paralyzed, or poisoned."
                )

                self.higher_levels = None  # No effect at higher levels

        class Levitate:
            def __init__(self):
                self.name = 'Levitate'
                self.school = 'Transmutation'
                self.casting_time = '1 action'
                self.range = '60 feet'
                self.duration = 'Concentration, up to 10 minutes'
                self.components = 'V, S, M (either a small leather loop or a piece of golden wire bent into a cup shape with '
                'a long shank on one end)'
                self.image = f'images/spells/{self.name}.png'

                self.description = (
                    "One creature or object of your choice that you can see within range rises vertically, up to 20 feet, "
                    "and remains suspended there for the duration. The spell can levitate a target that weighs up to 500 pounds. "
                    "An unwilling creature that succeeds on a Constitution saving throw is unaffected."
                )

                self.higher_levels = None  # No effect at higher levels

        class MagicMouth:
            def __init__(self):
                self.name = 'Magic Mouth'
                self.school = 'Illusion'
                self.casting_time = '1 minute'
                self.range = '30 feet'
                self.duration = 'Until dispelled'
                self.components = 'V, S, M (a small bit of honeycomb and jade dust worth at least 10 gp)'
                self.image = f'images/spells/{self.name}.png'

                self.description = (
                    "You implant a message within an object in range, a message that is uttered when a trigger condition is "
                    "met. Choose an object that you can see and that isn’t being worn or carried by another creature. Then speak "
                    "the message, which must be 25 words or less, though it can be delivered over as long as 10 minutes. "
                    "Finally, determine the circumstance that will trigger the spell to deliver your message."
                )

                self.higher_levels = None  # No effect at higher levels

        class MagicWeapon:
            def __init__(self):
                self.name = 'Magic Weapon'
                self.school = 'Transmutation'
                self.casting_time = '1 bonus action'
                self.range = 'Touch'
                self.duration = '1 hour'
                self.components = 'V, S'
                self.image = f'images/spells/{self.name}.png'

                self.description = (
                    "You touch a nonmagical weapon. Until the spell ends, that weapon becomes a magic weapon with a +1 bonus "
                    "to attack rolls and damage rolls."
                )

                self.higher_levels = None  # No effect at higher levels

        class ProtectionFromPoison:
            def __init__(self):
                self.name = 'Protection from Poison'
                self.school = 'Abjuration'
                self.casting_time = '1 action'
                self.range = 'Touch'
                self.duration = '1 hour'
                self.components = 'V, S'
                self.image = f'images/spells/{self.name}.png'

                self.description = (
                    "You touch a creature. If it is poisoned, you neutralize the poison. If more than one poison afflicts "
                    "the target, you neutralize one poison that you know is present, or you neutralize one at random."
                )

                self.higher_levels = None  # No effect at higher levels

        class Pyrotechnics:
            def __init__(self):
                self.name = 'Pyrotechnics'
                self.school = 'Transmutation'
                self.casting_time = '1 action'
                self.range = '60 feet'
                self.duration = 'Instantaneous'
                self.components = 'V, S'
                self.image = f'images/spells/{self.name}.png'

                self.description = (
                    "Choose an area of flame that you can see and that can fit within a 5-foot cube within range. You can "
                    "extinguish the fire in that area, and you create either fireworks or smoke when you do so."
                    "\n- Fireworks: The target explodes with a dazzling display of colors. Each creature within 10 feet of the "
                    "target must succeed on a Constitution saving throw or become blinded until the end of your next turn."
                    "\n- Smoke: Thick black smoke spreads out from the fire in a 20-foot radius, moving around corners. The "
                    "area of the smoke is heavily obscured. The smoke persists for 1 minute or until a strong wind disperses it."
                )

                self.higher_levels = None  # No effect at higher levels

        class RopeTrick(ParrentLevel2):
            def __init__(self):
                super().__init__()
                self.name = 'Rope Trick'
                self.school = 'Transmutation'
                self.casting_time = '1 action'
                self.range = 'Touch'
                self.duration = '1 hour'
                self.components = 'V, S, M (powdered corn extract and a twisted loop of parchment)'
                self.image = f'images/spells/{self.name}.png'

                self.description = (
                    "You touch a length of rope that is up to 60 feet long. One end of the rope then rises into the air until "
                    "the whole rope hangs perpendicular to the ground. At the upper end of the rope, an invisible entrance opens "
                    "to an extradimensional space that lasts until the spell ends."
                    "\nThe extradimensional space can be reached by climbing to the top of the rope. The space can hold as many "
                    "as eight Medium or smaller creatures. The rope can be pulled into the space, making the rope disappear from "
                    "view outside the space."
                )

                self.higher_levels = None  # No effect at higher levels

        class SeeInvisibility:
            def __init__(self):
                self.name = 'See Invisibility'
                self.school = 'Divination'
                self.casting_time = '1 action'
                self.range = 'Self'
                self.duration = '1 hour'
                self.components = 'V, S, M (a pinch of talc and a small sprinkling of powdered silver)'
                self.image = f'images/spells/{self.name}.png'

                self.description = (
                    "For the duration, you see invisible creatures and objects as if they were visible, and you can see into "
                    "the Ethereal Plane. Ethereal creatures and objects appear ghostly and translucent."
                )

                self.higher_levels = None  # No effect at higher levels

        class Skywrite:
            def __init__(self):
                self.name = 'Skywrite'
                self.school = 'Transmutation'
                self.casting_time = '1 action'
                self.range = 'Sight'
                self.duration = 'Instantaneous'
                self.components = 'V, S, M (a bit of soot and a few drops of water)'
                self.image = f'images/spells/{self.name}.png'

                self.description = (
                    "You cause up to ten words to form in a part of the sky you can see. The words appear to be made of cloud "
                    "and remain in place for the duration. The words dissipate when the spell ends. A strong wind can disperse "
                    "the clouds and end the spell early."
                )

                self.higher_levels = None  # No effect at higher levels

        class SpiderClimb(ParrentLevel2):
            def __init__(self):
                super().__init__()
                self.name = 'Spider Climb'
                self.school = 'Transmutation'
                self.casting_time = '1 action'
                self.range = 'Touch'
                self.duration = 'Concentration, up to 1 hour'
                self.components = 'V, S, M (a drop of bitumen and a spider)'
                self.image = f'images/spells/{self.name}.png'

                self.description = (
                    "Until the spell ends, one willing creature you touch gains the ability to move up, down, and across "
                    "vertical surfaces and upside down along ceilings, while leaving its hands free."
                )

                self.higher_levels = None  # No effect at higher levels

        class VortexWarp(ParrentLevel2):
            def __init__(self):
                super().__init__()
                self.name = 'Vortex Warp'
                self.school = 'Transmutation'
                self.casting_time = '1 action'
                self.range = 'Self'
                self.duration = 'Instantaneous'
                self.components = 'V, S, M (a small object like a tiny fan)'
                self.image = f'images/spells/{self.name}.png'

                self.description = (
                    "When you cast this spell, you can use your reaction to teleport up to 30 feet to an unoccupied space "
                    "you can see. Alternatively, you can choose a point within range, and a spectral hand teleports up to 30 "
                    "feet to that spot. If you are within range of the hand, you can use your reaction to teleport up to 30 feet "
                    "to an unoccupied space you can see."
                )

                self.higher_levels = (
                    "When you cast this spell using a spell slot of 2nd level or higher, the damage increases by 1d4 for each "
                    "slot level above 1st."
                )

        class Web:
            def __init__(self):
                self.name = 'Web'
                self.school = 'Conjuration'
                self.casting_time = '1 action'
                self.range = '60 feet'
                self.duration = 'Concentration, up to 1 hour'
                self.components = 'V, S, M (a bit of spiderweb)'
                self.image = f'images/spells/{self.name}.png'

                self.description = (
                    "You conjure a mass of thick, sticky webbing at a point of your choice within range. The webs fill a 20-foot "
                    "cube from that point for the duration. The webs are difficult terrain and lightly obscure their area."
                )

                self.higher_levels = None  # No effect at higher levels


class GenericSpellList:
    def __init__(self):
        self.spells = {'0': [], '1': [], '2': [], '3': [], '4': [], '5': []}

    def load(self):
        pass

    def spell_class_from_name(self, spell_names: list[str]) -> list[ParrentParrentSpell]:
        spell_classes = []
        for spell_name in spell_names:
            for spells in self.spells.values():
                for spell in spells:
                    spell: ParrentParrentSpell
                    if spell.name == spell_name:
                        spell_classes.append(spell)

        return spell_classes

    def reload_spell_objects(self):
        for level, spell_list in self.spells.items():
            for i, spell_obj in enumerate(spell_list):
                # Get the spell's class name
                class_name = spell_obj.__class__.__name__
                # Find the new class in the appropriate Spells level module
                level_module = getattr(Spells, f'Level{level}', None)
                if level_module and hasattr(level_module, class_name):
                    new_class = getattr(level_module, class_name)
                    # Re-instantiate the spell class with the current attributes
                    init_params = new_class.__init__.__code__.co_varnames
                    spell_attributes = {k: v for k, v in spell_obj.__dict__.items() if k in init_params}
                    new_spell_obj = new_class(**spell_attributes)
                    # Replace the old spell object with the new one
                    self.spells[level][i] = new_spell_obj
                else:
                    print(f"Spell class {class_name} not found in Level{level} spells.")

    @property
    def cantrips(self):
        return self.spells['0']

    @property
    def level1_spells(self):
        return self.spells['1']

    @property
    def level2_spells(self):
        return self.spells['2']

    @property
    def level3_spells(self):
        return self.spells['3']

    @property
    def level4_spells(self):
        return self.spells['4']

    @property
    def level5_spells(self):
        return self.spells['5']

    @property
    def level6_spells(self):
        return self.spells['6']

    @property
    def level7_spells(self):
        return self.spells['7']

    @property
    def level8_spells(self):
        return self.spells['8']

    @property
    def level9_spells(self):
        return self.spells['9']


class ArtificerSpellList(GenericSpellList):
    def __init__(self):
        super().__init__()

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

        self.load()

    def load(self):
        for spell_name in self.cantrip_spell_names:
            # Use getattr to get the class from the spells.Level0 by name
            spell_class = getattr(Spells.Level0, spell_name, None)
            if spell_class:
                # Instantiate the class and append to the cantrips list
                self.spells['0'].append(spell_class())
            else:
                print(f"Spell {spell_name} not found in Level0 spells.")

        for spell_name in self.level1_spell_names:
            # Use getattr to get the class from the spells.Level0 by name
            spell_class = getattr(Spells.Level1, spell_name, None)
            if spell_class:
                # Instantiate the class and append to the cantrips list
                self.spells['1'].append(spell_class())
            else:
                print(f"Spell {spell_name} not found in Level0 spells.")

        for spell_name in self.level2_spell_names:
            # Use getattr to get the class from the spells.Level0 by name
            spell_class = getattr(Spells.Level2, spell_name, None)
            if spell_class:
                # Instantiate the class and append to the cantrips list
                self.spells['2'].append(spell_class())
            else:
                print(f"Spell {spell_name} not found in Level0 spells.")
