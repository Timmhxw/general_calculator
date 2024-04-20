from .base import Character,Buff,ACal
weapons_list = {'赤角':1,'螭骨':2, '天空':3, '白影':4, '无工':5, '狼末':6, '黑岩':7,'西风':8}
basic_ATK = {1:542,2:510,3:674,4:510,5:608,6:608,7:510,8:510}

#攻击
ATK_wugong_on = {1:0.4,2: 0.5, 3: 0.6, 4: 0.7, 5: 0.8}
ATK_wugong_off = {1:0.2,2: 0.25, 3: 0.3, 4: 0.35, 5: 0.4}
ATK_langmo_on = {1:0.4,2: 0.5, 3: 0.6, 4: 0.7, 5: 0.8}
ATK_heiyan_on = {1:0.36,2:0.45,3: 0.54,4:0.63, 5: 0.72}
ATK_baiying_on = {1:0.24,2: 0.30,3: 0.36, 4: 0.42, 5: 0.48}

#防御
DEF_baiying_on = {1:0.24,2: 0.30, 3: 0.36, 4: 0.42, 5: 0.48}

#伤害加成
Dmg_Inc_chigu_on = {1:0.3,2: 0.35, 3: 0.4, 4: 0.45, 5: 0.5}
Dmg_Inc_tiankong_on = {1:0.08,2: 0.1, 3: 0.12, 4: 0.14, 5: 0.16}

#伤害数值加成
Dmg_Num_Inc_D_chijiao = {1:0.4,2: 0.5, 3: 0.6, 4: 0.7, 5: 0.8}


#额外伤害
Other_Dmg_tiankong_on = {1:0.8,2: 1, 3: 1.2, 4: 1.4, 5: 1.6}

def get_Weapon_buff(Weapon:int,Weapon_num:int,owner:Character):
    buff_list = []
    if Weapon == weapons_list['赤角']:
        buff_list.append(Buff('on_stage','basic DMG',
                              ACal(
                                {
                                    'DEF':Dmg_Num_Inc_D_chijiao[Weapon_num]
                                },owner,has_condition=True
                            ),
                            condition={'action_tag':['A','Z']},private=True))
        
    elif Weapon == weapons_list['螭骨']:
        buff_list.append(Buff('all_stage','Inc',Dmg_Inc_chigu_on[Weapon_num],
                              private=True
        ))
    elif Weapon == weapons_list['天空']:
        buff_list.append(Buff('all_stage','Inc',Dmg_Inc_tiankong_on[Weapon_num],
                              private=True
        ))
        buff_list.append(Buff('on_stage','other DMG',
                              ACal(
                                {
                                    'ATK',Other_Dmg_tiankong_on[Weapon_num]
                                },owner,has_condition=True
                            ),
                            condition={'action_tag':['A','Z']},private=True))

    elif Weapon == weapons_list['白影']:
        buff_list.append(Buff('all_stage','ATK percent',ATK_baiying_on[Weapon_num],
                              private=True
        ))
        buff_list.append(Buff('all_stage','DEF percent',DEF_baiying_on[Weapon_num],
                              private=True
        ))
    elif Weapon == weapons_list['无工']:
        buff_list.append(Buff('all_stage','ATK percent',ATK_wugong_on[Weapon_num],
                              private=True
        ))
    elif Weapon == weapons_list['狼末']:
        buff_list.append(Buff('all_stage','ATK percent',ATK_langmo_on[Weapon_num],
                              private=True
        ))
    elif Weapon == weapons_list['黑岩']:
        buff_list.append(Buff('all_stage','ATK percent',ATK_heiyan_on[Weapon_num],
                              private=True
        ))
    elif Weapon == weapons_list['西风']:
        pass
    for buff in buff_list:
        buff:Buff
        if buff.private:
            owner.add_private_buff(buff)
    return buff_list