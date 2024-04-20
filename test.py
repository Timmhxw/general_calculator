from backend.character.yunjin import Yunjin
from backend.character.furina import Furina
from backend.character.noelle import Noelle
from backend.character.wulang import Wulang
from backend.basic import Relic_data,Weapon_data,functional
from backend.basic.base import Enemy,Buff
if __name__=='__main__':
    noelle = Noelle({'ATK': 1317, 'DEF': 2350,'CrR':0.835,'CrD':2.338,'Rock Inc':0.466},
                    Q_level=13)
    wulang = Wulang(E_level=13,num=6)
    yunjin = Yunjin({'DEF':2736},Q_level=13,num=6)
    fufu = Furina(num=1)
    relic = Relic_data.get_Relic_buff(1,noelle)
    weapon = Weapon_data.get_Weapon_buff(1,1,noelle)
    # buff generate
    rock2 = [
        Buff('all_stage','Rock dec RES',0.2),
        Buff('all_stage','Inc',0.15),
    ]
    fufu.use_Q()
    wulang.use_Q()
    yunjin.use_Q()
    noelle.stat = 'on_stage'
    noelle.Q_buff()
    
    for i in range(4):
        print(functional.DMG_calculator(noelle,Enemy(),noelle.A[i]))
    