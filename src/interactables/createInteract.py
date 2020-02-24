import league
from interactables.container import Container

class createInteract():
    def __init__(self, engine=None, player=None):
        self.engine = engine
        self.player = player

    def createBeartrapContainer(self, z, x, y):
        temp = Container(z,x,y,'beartrap')
        self.player.interactables.add(temp)
        self.engine.drawables.add(temp)
        self.engine.objects.append(temp)
    
    def createLanternContainer(self, z, x, y):
        temp = Container(z,x,y,'lantern')
        self.player.interactables.add(temp)
        self.engine.drawables.add(temp)
        self.engine.objects.append(temp)

    def createRandcidMeatContaier(self, z, x, y):
        temp = Container(z,x,y,'rancidmeat')
        self.player.interactables.add(temp)
        self.engine.drawables.add(temp)
        self.engine.objects.append(temp)




