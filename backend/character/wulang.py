from ..basic import base
from ..basic import common
Basic_value90 ={

}
E_DEF_Magn = {1:206,2: 222, 3: 237, 4:258, 5: 273, 6: 289,
                   7:309,8: 330, 9: 350,10:371,11: 392, 12: 412,
                   13: 438}
class Wulang(base.Character):
    def __init__(self, data: dict = {}, A_level: int = 10, E_level: int = 10, Q_level: int = 10, num: int = 6) -> None:
        super().__init__(data, A_level, E_level, Q_level, num, Basic_value90,element='Rock')
        
        
    def use_E(self):
        self.E = []
        self.E.append(base.Buff('on_stage','DEF',E_DEF_Magn[self.E_level]))
        # with trigger
        self.E.append(base.Buff('on_stage','Rock Inc',0.15))
        if self.num==6:
            # if trigger
            self.E.append(base.Buff('on_stage','CrD',0.4))
    def use_Q(self):
        self.Q = []
        self.Q.append(base.Buff('all_stage','DEF percent',0.25))
        self.Q_buff = common.Buff(
            {'on_stage':{'DEF percent':0.25}}
        )
        self.use_E()
        