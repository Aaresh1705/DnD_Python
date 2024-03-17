class Actions:
    class Empty:
        def __init__(self):
            self.id = 0
            self.name = 'Empty'
            self.description = ''

            self.image = 'images/Transparent.png'

    class EldritchCannon:
        def __init__(self):
            self.id = 1
            self.name = 'Eldritch Cannon'
            self.description = [
                "1 Action",
                "Using woodcarver's tools or smith's tools,",
                "you can take an action to magically create a Small or",
                "Tiny eldritch cannon in an unoccupied space on a",
                "horizontal surface within 5 feet of you. A Small",
                "eldritch cannon occupies its space, and a Tiny",
                "one can be held in one hand."
            ]
            self.image = 'images/actions/Eldritch Cannon.png'

        def action_description(self, player):
            return self.description

    class MagicalTinkering:
        def __init__(self):
            self.id = 2
            self.name = 'Magical Tinkering'
            self.description = [
                "1 Action",
                "you've learned how to invest a spark of magic",
                "into mundane objects. To use this ability,",
                "you must have thieves' tools or artisan's tools",
                "in hand. You then touch a Tiny nonmagical object",
                "as an action and give it one of four magical",
                "properties of your choice."
            ]
            self.image = 'images/actions/Magical Tinkering.png'

        def action_description(self, player):
            return self.description

    class InfuseItem:
        def __init__(self):
            self.id = 3
            self.name = 'Infuse Item'
            self.description = [
                "After long rest",
                "You've gained the ability to imbue mundane items",
                "with certain magical infusions, turning those",
                "objects into magic items."
            ]
            self.image = 'images/actions/Infuse Item.png'

        def action_description(self, player):
            return self.description

    class Tinker:
        def __init__(self):
            self.id = 4
            self.name = 'Tinker'
            self.description = [
                "1 Hour",
                "Using tinker's tools, you can spend 1 hour and 10 gp",
                "worth of materials to construct a "
                "Tiny clockwork device."
            ]
            self.image = 'images/actions/Tinker.png'

        def action_description(self, player):
            return self.description

    class TheRightToolForTheJob:
        def __init__(self):
            self.id = 5
            self.name = 'The Right Tool For The Job'
            self.description = [
                "1 hour",
                "With thieves' tools or artisan's tools in hand,",
                "you can magically create one set of artisan's tools",
                "in an unoccupied space within 5 feet of you.",
                "This creation requires 1 hour of uninterrupted work,",
                "which can coincide with a short or long rest.",
                "Though the product of magic, the tools are nonmagical,",
                "and they vanish when you use this feature again."
            ]
            self.image = 'images/actions/The Right Tool for the Job.png'

        def action_description(self, player):
            return self.description

    class FlashOfGenius:
        def __init__(self):
            self.id = 6
            self.name = 'Flash of Genius'
            self.description = [
                "When you or another creature you can see",
                "within 30 feet of you makes an ability check",
                "or a saving throw, you can use your reaction",
                "to add your Intelligence modifier to the roll."
            ]
            self.image = 'images/actions/Flash of Genius.png'

        def action_description(self, player):
            return self.description

    class Hit:
        def __init__(self, name='', desc='', img=''):
            self.id = 7
            self.name = name
            self.description = desc
            self.image = img

        def action_description(self, player):
            return self.description


ACTIONS_ID_DICT = {0: Actions.Empty, 1: Actions.EldritchCannon, 2: Actions.MagicalTinkering,
                   3: Actions.InfuseItem, 4: Actions.Tinker, 5: Actions.TheRightToolForTheJob,
                   6: Actions.FlashOfGenius, 7: Actions.Hit}
