from .base import Character,Buff
Relics_list = {'角斗士':1,'逆飞':2, '华馆':3, '华馆（面板已叠满）':4,'猎人':5}
def get_Relic_buff(Relic_index:int,owner:Character):
    buff_list = []
    if Relic_index == Relics_list['角斗士']:
        buff_list.append(Buff('on_stage','Inc',0.35,
                    condition={'action_tag':'A'},private=True))
        
    elif Relic_index == Relics_list['逆飞']:
        buff_list.append(Buff('on_stage','Inc',0.4,
                    condition={'action_tag':['A','Z']},private=True))
    elif Relic_index == Relics_list["华馆"]:
        buff_list.append(Buff('all_stage','Rock Inc',0.24,
                    private=True))
        buff_list.append(Buff('all_stage','DEF',0.24,
                    private=True))
    elif Relic_index == Relics_list["华馆（面板已叠满）"]:
        buff_list.append(Buff('all_stage','Rock Inc',0.24,
                    private=True))
        buff_list.append(Buff('all_stage','DEF percent',0.24,
                    private=True))
        owner.parm.set('Rock Inc',-0.24)
        owner.parm.set('DEF percent',-0.24)
    elif Relic_index == Relics_list["猎人"]:
        buff_list.append(Buff('all_stage','Inc',0.15,
                    condition={'action_tag':['A','Z']},private=True))
        buff_list.append(Buff('all_stage','CrR',0.36,
                    private=True))
    for buff in buff_list:
        buff:Buff
        if buff.private:
            owner.add_private_buff(buff)
    return buff_list