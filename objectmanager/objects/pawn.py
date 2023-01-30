from objectmanager.objects.piece import boardItem

class pawnEquipment:
    def __init__(self, place, armor, damage, Erange, equipmentType, name) -> None:
        self.place = place
        self.armor = armor
        self.damage = damage
        self.Erange = Erange
        self.equipmentType = equipmentType
        self.name = name

    def __repr__(self) -> str:
        return """
            {}
             +ARM: {}  
             +DMG: {} """.format(str(self.name), self.armor, self.damage)

class pawnCarry:
    def __init__(self) -> None:
        self.kit = {
            "head": pawnEquipment("head", 1, 0, 0, "armor", "Cap"),
            "body": pawnEquipment("body", 2, 0, 0, "armor", "Shirt"),
            "melee": pawnEquipment("melee", 0, 1, 1, "meleeWeapon", "Axe"),
            "ranged": pawnEquipment("ranged", 1, 0, 3, "armor", "None"),
            "legs": pawnEquipment("legs", 1, 0, 1,"armor", "Pants")
        }
    
    def __repr__(self) -> str:
        return str(self.kit)

    def equip(self, item: pawnEquipment):
        self.kit[item.place] = item

    def getStats(self):
        armor = self.kit["head"].armor + self.kit["body"].armor + self.kit["melee"].armor \
            + self.kit["ranged"].armor + self.kit["legs"].armor
        meleedmg = self.kit["melee"].damage
        rangeddmg = self.kit["ranged"].damage

        stats = {
            "armor": armor,
            "melee": meleedmg,
            "ranged": rangeddmg
        }
        return stats

    def getArmor(self):
        armor = self.kit["head"].armor + self.kit["body"].armor + self.kit["melee"].armor \
            + self.kit["ranged"].armor + self.kit["legs"].armor
        return armor
    
    def getMeleeDMG(self):
        return self.kit["melee"].damage

    def getMeleeDist(self):
        return self.kit["melee"].Erange

    def getRangedDMG(self):
        return self.kit["ranged"].damage

    def getRangedDist(self):
        return self.kit["ranged"].Erange
    
    def getWalkRange(self):
        return self.kit["legs"].Erange

        
class pawnStats:
    def __init__(self) -> None:
        pass

class pawn(boardItem):
    def __init__(self, name, fullname, age, image, owner) -> None:
        super().__init__()
        self.name = name
        self.description = self.name
        self.equipment: pawnCarry = pawnCarry()
        
        self.health = self.equipment.getArmor()
        self.range = self.equipment.getWalkRange()
        self.strength = self.equipment.getMeleeDMG()
        self.ranged_strength = self.equipment.getRangedDMG()
        self.shoot_range = self.equipment.getRangedDist()
        self.melee_range = self.equipment.getMeleeDist()

        self.fullname = fullname
        self.owner = owner
        self.age = age
        self.image = image
        self.color = owner.color
        

    def __str__(self) -> str:
        return self.name

    def move(self, loc):
        self.loc = loc

    def set_loc(self, loc):
        self.loc = loc
        self.log_event(loc)
        return self.loc

    def set_image(self, image):
        self.image = image
        return self.image

    def set_age (self, age):
        self.age = age
        return self.age
        
    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.destroyed = True

class enemy(pawn):
    def __init__(self, name, fullname, age, image, owner) -> None:
        super().__init__(name,fullname,age,image,owner)
        self.owner = owner
        self.description = "An NPC, hostile"