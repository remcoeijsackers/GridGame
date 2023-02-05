# Game state monitoring
from src.gamemanager.players.owners import owner

from src.gamemanager.settings import debug
from src.gamemanager.players.npc import npc

import time 
class gameRound:
    """
    A singel round of gameplay
    """
    def __init__(self, id: int, players: (owner)) -> None:
        self.id = id
        self.players = players
        self.turns = []
        self.__setActions()
        self.roundLength = len(players)
        self.currentPlayer = self.__getNextPlayer()
    
    def getPlayerByID(self, id):
        return [d for d in self.players if d.id == id][0]

    def endPlayerTurn(self):
        self.currentPlayer.available_actions = 0

    def getCurrentPlayer(self) -> owner or npc or False:
        if len(self.turns) == self.roundLength and self.currentPlayer.available_actions <= 0:
            if debug:
                print("round end. played this round: {}".format(self.turns))
            return False

        if self.currentPlayer.available_actions > 0:
            if debug:
                print("still {}s turn. actions: {}".format(self.currentPlayer, self.currentPlayer.available_actions))
            return self.currentPlayer

        if self.currentPlayer.available_actions <= 0:
            nplayer = self.__getNextPlayer()
            self.currentPlayer = nplayer

            # if there is a owner with actions left, else send the end turn signal.
            if isinstance(nplayer, owner):
                if debug: 
                    print("switched to {}".format(nplayer))
                    print("{} actions: {}".format(nplayer, nplayer.available_actions))
                return nplayer
            else:
                if debug:
                    print("round end. played this round: {}".format(self.turns))
                return False

    def __setActions(self):
        for i in self.players:
            if len(i.units) > 0:
                i.available_actions = 3

    def __getNextPlayer(self) -> owner or False:
        options = [i.__dict__ for i in self.players if i not in self.turns]
        plstub = max(options, key=lambda x:x['available_actions'] > 0)

        # if there are no more players with more than 0 actions, send the end turn signal.
        if plstub.get("available_actions") == 0:
            return False
        
        pl:owner = [d for d in self.players if d.id == plstub.get('id')][0]
        self.turns.append(pl)
        pl.startTurn()
        return pl
    

class gameController:
    """
    Handles game state monitoring.
    """
    def __init__(self, players: (owner), game) -> None:
        self.players = players
        self.rounds: (gameRound) = []
        self.losers = []
        self.game = game
        self.startRound()
    
    def startRound(self) -> owner:
        Ground = gameRound(len(self.rounds)+1, self.players)
        if debug:
            print("starting round {}".format(Ground.id))
        self.rounds.append(Ground)
        return Ground.getCurrentPlayer()
    
    def makePlayerDecision(self, unit):
        """
        get a decision from an npc, and carry it out
        """
        
        if self.getCurrentPlayer() and isinstance(self.getCurrentPlayer(), npc):
            self.game.canvas.focus_set()
            npcaction = self.getCurrentPlayer().decide(unit)
            if npcaction[1] == "winner":
                return self.game.display_gameover(self.getCurrentPlayer())
            if npcaction[1] == "move":
                self.game.switch_mode_selectmove("")
                return self.game.select_move_click(npcaction[0])
            if npcaction[1] == "attack":
                self.game.switch_mode_melee_attack("")
                return self.game.melee_attack_click(npcaction[0])
            time.sleep(1)
            self.game.canvas.update()

        
            
    def playerAction(self, action):
        self.getCurrentPlayer().action()
        return self.checkGameState()

    def getCurrentPlayer(self) -> owner or npc:
        player = self.rounds[-1].getCurrentPlayer()
        if player:
            return player
        else:
            return self.startRound()

    def clearPlayers(self):
        for i in self.players:
            i.clear()
    
    def checkGameState(self):
        """
        Check if somebody won the game.
        """
        for i in self.players:
            if len(i.units) == 0:
                self.losers.append(i)
                del i
        if len(self.losers) == len(self.players) -1:
            return [True, self.players]
        else:
            return [False]

    def switch_player(self):
        self.rounds[-1].endPlayerTurn()
        return self.getCurrentPlayer()


