from ..basic import base
from ..basic import common
Basic_value90 ={
    'DEF':734
}
Q_basicDmgDEF_Magn = {1:0.32,2: 0.35, 3: 0.37, 4:0.40, 5: 0.43, 6: 0.45,
            7:0.48,8: 0.51, 9: 0.55,10:0.58,11: 0.61, 12: 0.64,
            13: 0.68}

class Yunjin(base.Character):
    def __init__(self, data: dict={}, A_level: int = 10, E_level: int = 10, Q_level: int = 10, num: int = 6) -> None:
        super().__init__(data, A_level, E_level, Q_level, num, Basic_value90)
        
    def use_Q(self):
        self.Q = []
        self.Q.append(base.Buff(
            'on_stage','basic DMG',base.ACal(
                {'DEF':Q_basicDmgDEF_Magn[self.Q_level]+0.25*2},# assert num trigger=2
                self,has_condition=True
            ),times=30,condition={'action_tag':'A'},addition_flag=True
        )) 
        if self.num>=2:
            self.Q.append(base.Buff('on_stage','Inc',0.15,{'action_tag':'A'}))
        if self.num>=4:
            self.add_private_buff(base.Buff('all_stage','DEF percent',0.2,private=True))
        if self.num==6:
            self.Q.append(base.Buff('on_stage','A speed',0.12,{'action_tag':'A'}))
