from ..basic import base
from ..basic import common
Basic_value90 ={

}
Q_Dmg_Inc_Magn = {1:0.07,2: 0.09, 3: 0.11, 4:0.13, 5: 0.15, 6: 0.17,
                   7:0.19,8: 0.21, 9: 0.23,10:0.25,11: 0.27, 12: 0.29,
                   13: 0.31}
class Furina(base.Character):
    def __init__(self, data: dict={}, A_level: int = 10, E_level: int = 10, Q_level: int = 10, num: int = 6) -> None:
        super().__init__(data, A_level, E_level, Q_level, num, Basic_value90,element='Water')
    def use_Q(self):
        self.Q = []    
        if self.num>=1:
            self.Q.append(base.Buff('all_stage','Inc',Q_Dmg_Inc_Magn[self.Q_level]*4))
            # init Q_Dmg_Inc_Magn[self.Q_level]*1.5
        else:
            self.Q.append(base.Buff('all_stage','Inc',Q_Dmg_Inc_Magn[self.Q_level]*3))