from . import common
from .base import Buff,sum_of_buffs,Character,Enemy,Action
from decimal import Decimal
cfg = common.Const
def decimal_add(*float_list):
    return float(sum([Decimal(str(each))for each in float_list]))

 

def DMG_calculator(attacker:Character,defender:Enemy,action:Action):
    def get_buff(item:str):
        return sum_of_buffs(Buff.get_buff(item,attacker.stat,action)+attacker.get_private_buff(item,action))
    # first multiple area:Basic damage
    basic_DMG = action.DMG_func(secondary_call=False) + get_buff('basic DMG')
    if(action.element in ['grass','elec']):
        pass
    
    # second multiple area:Crit
    CrR = min(1,attacker.parm.get('CrR')+get_buff('CrR'))
    CrD = attacker.parm.get('CrD')+get_buff('CrD')
    Crit_DMG = 1+CrD
    Expert_DMG = 1+CrD*CrR

    # third multiple area:damage Inc
    # DMG_Inc = 1+attacker.get(element+' Inc')+attacker.get(action+' Inc')+attacker.get(DMG_type+' Inc')+attacker.get('all Inc')
    DMG_Inc = decimal_add(1,attacker.parm.get(action.element+' Inc'),get_buff(action.element+' Inc'),get_buff('Inc'))
    
    # fourth multiple area:reaction
    reaction_frac = 1
    if action.element in ['ice','fire','water']:
        pass

    # fifth multiple area:DEF&RES
    RES = defender.parm.get(action.element+' RES') - get_buff(action.element+' dec RES')
    if RES<=0:
        RES = (1-RES/2)
    elif RES<=0.75:
        RES = (1-RES)
    else:
        RES = (1+RES*4)
    DEF = (100.0+attacker.parm.get('LV'))/(200.0+defender.parm.get('LV')+attacker.parm.get('LV'))
    RES_DEF = RES*DEF

    total_crit_DMG = basic_DMG * Crit_DMG * DMG_Inc * reaction_frac * RES_DEF
    total_expert_DMG = basic_DMG * Expert_DMG * DMG_Inc * reaction_frac * RES_DEF
    return {'total_crit_DMG':total_crit_DMG,'total_expert_DMG':total_expert_DMG}

