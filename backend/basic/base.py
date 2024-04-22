from . import common
class Attack:
    def __init__(self,damage_func,action_tag:str='A',element:str='Phys',damage_tag:str='') -> None:
        '''
            damage_func:ACal
            action_tag:'A','Z','P','E','Q'
            element:'Phys'or seven elements
            damage_tag:'XXX_DMG',default action_tag+'_DMG'
        '''
        if damage_tag=='':
            damage_tag = action_tag+'_DMG'
        assert isinstance(damage_func,ACal)
        self.DMG_func = damage_func
        self.action_tag = action_tag
        self.element = element
        self.damage_tag = damage_tag
        self.element_forced = False
        self.force_element_buff = None
    
    def force_element(self,buff,new_element:str):
        assert isinstance(buff,Buff)
        self.element_forced = True
        self.element = new_element
        self.force_element_buff = buff

    def check_if_element_forced(self):
        if not self.element_forced:
            return False
        # check if buff alive
        # if alive,return True,else cover as Phys
        self.element_forced = False
        self.element = 'Phys'
        return False
    
    def cover_element(self,new_element):
        if not self.check_if_element_forced():
            self.element = new_element
    
    def get_element(self):
        self.check_if_element_forced() # exam if element is forced 
        return self.element

class Actor:
    def __init__(self,data:dict={},
                    LV:int=93,
                    **others
                ) -> None:
        data['LV'] = data.get('LV',LV)
        self.parm = common.Parameter(data)

class Enemy(Actor):
    def  __init__(self, data: dict={}, LV: int = 93, **others) -> None:
        super().__init__(data, LV, **others)
        self.tag = 'enemy'

class Character(Actor):
    def __init__(self,data:dict={},
                    A_level:int=10,E_level:int=10,Q_level:int=10,
                    num:int=6,
                    Basic_value90:dict={},
                    LV:int=90,
                    element:str='empty',
                    stat:str='off_stage',
                    **others
                ) -> None:
        super().__init__(data, LV, **others)
        self.tag = 'friend'
        self.element = element
        self.stat = stat
        self.private_buff = {'on_stage':{},'off_stage':{}}
        self.num = num
        self.A_level = A_level
        self.E_level = E_level
        self.Q_level = Q_level
        for key,value in Basic_value90.items():
            self.parm.set('basic '+key,value)

    def add_private_buff(self,new_buff):
        assert isinstance(new_buff,Buff),"invalid adding to private buff"
        stat,item = new_buff.stat,new_buff.item
        if new_buff.stat == "all_stage":
            for stat in ["on_stage","off_stage"]:
                self.private_buff[stat][item] = self.private_buff[stat].get(item,[])
                self.private_buff[stat][item].append(new_buff)
        else:
            self.private_buff[stat][item] = self.private_buff[stat].get(item,[])
            self.private_buff[stat][item].append(new_buff)
    def get_private_buff(self,item,action:Attack=None):
        queue = self.private_buff[self.stat].get(item,[])
        result = []
        remove_buff = []
        for each in queue:
            assert isinstance(each,Buff)
            if each.meet_condition(action):
                result.append(each)
                if(each.times==0)or(each.ddl==0):#ddl tobe fix:
                    remove_buff.append(each)
        if remove_buff:
            self.remove_buff(item,remove_buff)
        return result
    def remove_buff(self,item:str,buff_list:list):
        for stat in ["on_stage","off_stage"]:
            temp = self.private_buff[stat][item]
            self.private_buff[stat][item] = list(set(temp)-set(buff_list))
    # to be DIY
    def use_E(self):
        return []
    def use_Q(self):
        return []
    def state_machine(self,action_name:str):
        '''
        action_name is among[A,Z,P,F(mean flash),E,Q]
        return list of attack or buff
        '''
        self.last_action = action_name
        if action_name == 'E':
            return self.use_E()
        elif action_name == 'Q':
            return self.use_Q()
        else:
            return []


from decimal import Decimal

def decimal_add(*float_list):
    if len(float_list)==1:
        float_list = float_list[0]
    if len(float_list)==0:
        return 0
    return float(sum([Decimal(str(each))for each in float_list]))

class Buff:
    on_stage = 'on_stage'
    off_stage = 'off_stage'
    all_stage = 'all_stage'
    public_buff = {on_stage:{},off_stage:{}}
    public_buff_rec = []
    def __init__(self, stat:str,item:str,value,ddl:float=-1,times:int=-1,
                 condition:dict={},private:bool=False,addition_flag:bool=False):
        '''
        condition only use for action_tag and damage_tag 
        '''
        assert stat in ["on_stage","off_stage","all_stage"]
        self.stat = stat
        self.item = item
        self.value = value
        self.ddl = ddl # to be fix
        if ddl>0:
            common.Timestamp.calc_end_timestamp(self.ddl)
        self.times = times 
        self.condition = condition
        self.private = private
        self.addition_flag = addition_flag
        if not private:
            self.add_to_public(self)
        
    def meet_condition(self,action:Attack=None):
        if (self.condition=={}):
            pass
        elif action==None:
            return False
        else:
            for key,value in self.condition.items():
                if action.__getattribute__(key) not in value:
                    return False
        if self.times>0:
            self.times -= 1
        return True
    
    @classmethod
    def add_to_public(cls,new_buff):
        assert isinstance(new_buff,Buff),"invalid adding to public buff"
        index = len(cls.public_buff_rec)
        cls.public_buff_rec.append(new_buff)
        stat,item = new_buff.stat,new_buff.item
        if new_buff.stat == "all_stage":
            for stat in ["on_stage","off_stage"]:
                cls.public_buff[stat][item] = cls.public_buff[stat].get(item,[])
                cls.public_buff[stat][item].append(index)
        else:
            cls.public_buff[stat][item] = cls.public_buff[stat].get(item,[])
            cls.public_buff[stat][item].append(index)
    @classmethod
    def get_buff(cls,item,stat='on_stage',action:Attack=None):
        assert stat in ["on_stage","off_stage"]
        queue = cls.public_buff[stat].get(item,[])
        result = []
        remove_buff = []
        for each in queue:
            buff = cls.public_buff_rec[each]
            assert isinstance(buff,Buff)
            if buff.meet_condition(action):
                result.append(buff)
                if(buff.times==0)or(buff.ddl==0):#ddl tobe fix:
                    remove_buff.append(each)
        if remove_buff:
            cls.remove_buff(item,remove_buff)
        return result
    @classmethod
    def remove_buff(cls,item:str,buff_list:list):
        for stat in ["on_stage","off_stage"]:
            temp = cls.public_buff[stat].get(item,[])
            if temp != []:
                cls.public_buff[stat][item] = list(set(temp)-set(buff_list))
    
class ACal:
    '''active calculator,serve for buff calculation'''
    def __init__(self,func:dict,data_base:Character,has_condition:bool=False) -> None:
        '''
        func:{
            property:num,
            'other':num,
        }
        use data in data_base.parm,return sum(each_property*each_num)+other
        has condition mean that the under-calculate buff can conditionally calculate buff twice
        '''
        self.func = func
        self.data_base = data_base
        self.has_condition = has_condition

    def __call__(self,secondary_call:bool=True) -> float:
        result = self.func.get('other',0)
        for key,value in self.func.items():
            prop_key = self.data_base.parm.get(key)+\
                sum_of_buffs(Buff.get_buff(key,self.data_base.stat)+\
                    self.data_base.get_private_buff(key),secondary_call,self.has_condition)
            prop_key_percent = sum_of_buffs(Buff.get_buff(key+' percent',self.data_base.stat)+\
                                    self.data_base.get_private_buff(key+' percent'),secondary_call,self.has_condition)
            if prop_key_percent:
                prop_key += prop_key_percent*self.data_base.parm.get('basic '+key)
            result += prop_key*value
        return result

def sum_of_buffs(input:list,secondary_calc:bool=False,condition_flag:bool=False)->float:
    '''
    input list of buff,return float type result\n
    solving twice calculating problem:\n
    calculating sum of buff(input) for B(single item in parameter)\n
    each buff may be calc-ed from A(buff.value is ACal class),called buff1\n
    A is another item in parameter,also may be buffed(called buff2)\n
    if buff2 doesn't have addition_flag,calc\n
    if buff2 has,divide for several condition:
        if buff2.item == 'HP',calc\n
        if buff2.item == 'EG'('充能效率'),dismiss\n
        otherwise, if buff1 has condition,calc,else dismiss\n
    so that,for buff1 in input,call its value(ACal class)\n
    later,dump back to this function to calc buff2,as secondary_calc=True
    '''
    result = []
    for each in input:
        assert isinstance(each,Buff)
        if isinstance(each.value,ACal):
            if not secondary_calc:# each is buff1
                result.append(each.value(secondary_call=True))
            else: #buff2
                if each.item == 'HP':
                    result.append(each.value(secondary_call=True))
                elif(each.item!='EG')and(condition_flag):
                    result.append(each.value(secondary_call=True))
        elif isinstance(each.value,float)or isinstance(each.value,int):
            result.append(each.value)
    return decimal_add(tuple(result))