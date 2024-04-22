import backend.basic.base as base
import backend.basic.functional as functional
from .common import Timestamp 
class Timeline:
    
    def __init__(self,team:list,enemy:list,queue:list) -> None:
        '''
        queue:[
            [character,['A'/'E'/'Q'/'Z'...]],mean that let a character walk on stage and do several actions
        ]
        '''
        
        assert len(team)<=4
        for each in team:
            assert isinstance(each,base.Character)
        self.team = team
        for each in enemy:
            assert isinstance(each,base.Enemy)
        self.enemy = enemy

        self.queue = []
        for character,actions in queue:
            assert isinstance(character,base.Character)
            assert character in self.team
            self.queue.append(character)
            for action in actions:
                assert action in ['A','Z','P','E','Q','F']
                self.queue.append(action)
        self.current_action = 'start'
        self.action_result = []
        self.current_character = team[0]
        self.current_character.stat = 'on_stage'

    def action(self):
        for action in self.queue:
            if isinstance(action,base.Character):
                self.current_character.stat = 'off_stage'
                action.stat = 'on_stage'
                self.current_character = action
                self.current_action = self.current_character.__class__.__name__ + ' on stage'
                print(self.current_action,end='\t')
            else:
                self.action_result = self.current_character.state_machine(action)
                print(self.current_character.last_action,end='\t')
                if not isinstance(self.action_result,list):
                    if self.action_result == None:
                        self.action_result = []
                    else:
                        self.action_result = [self.action_result]
                self.current_action = action

            yield
        self.current_action = 'end'
        yield

    def stream(self):
        action = self.action()
        while self.current_action != 'end':
            next(action)
            if self.current_action in ['A','Z','P','E','Q']:
                for each in self.action_result:
                    if isinstance(each,base.Buff):
                        # add timestamps
                        pass
                    else:
                        for enemy in self.enemy:
                            print(functional.DMG_calculator(self.current_character,enemy,each),end='\t')
            print()
    
        