

const_property_namelist={
    'HP':{'EN':'HP','CHS':'生命值'},
    'ATK':{'EN':'ATK','CHS':'攻击力'},
    'DEF':{'EN':'DEF','CHS':'防御力'},
    'EG':{'EN':'EG','CHS':'充能效率'},
    'EM':{'EN':'Elemental Mastery','CHS':'元素精通'},
    'CrR':{'EN':'Crit Rate','CHS':'暴击率'},
    'CrD':{'EN':'Crit Damage','CHS':'暴击伤害'},
    'Inc':{'EN':'DMG Bonus','CHS':'伤害加成'},
    'RES':{'EN':'RES','CHS':'抗性'},
    'LV':{'EN':'Level','CHS':'等级'}
}

const_element_namelist={
    'Wind':{'EN':'anemo','CHS':'风'},
    'Rock':{'EN':'geo','CHS':'岩'},
    'Fire':{'EN':'pyro','CHS':'火'},
    'Ice':{'EN':'cryo','CHS':'冰'},
    'Water':{'EN':'hydro','CHS':'水'},
    'Elec':{'EN':'electro','CHS':'雷'},
    'Grass':{'EN':'dendro','CHS':'草'},
    'Phys':{'EN':'physics','CHS':'物理'}
}
const_action_namelist={
    'A':{'EN':'Normal Attack','CHS':'普通攻击'},
    'Z':{'EN':'Charged Attack','CHS':'重击'},
    'P':{'EN':'Plunging Attack','CHS':'下落攻击'},
    'E':{'EN':'Elemental Skill','CHS':'元素战技'},
    'Q':{'EN':'Elemental Burst','CHS':'元素爆发'},
}
const_DMGtype_namelist={
    'A_DMG':{'EN':'Normal Attack damage','CHS':'普通攻击伤害'},
    'Z_DMG':{'EN':'Charged Attack damage','CHS':'重击伤害'},
    'P_DMG':{'EN':'Plunging Attack damage','CHS':'下落攻击伤害'},
    'E_DMG':{'EN':'Elemental Skill damage','CHS':'元素战技伤害'},
    'Q_DMG':{'EN':'Elemental Burst damage','CHS':'元素爆发伤害'},
}

class Const:
    '''define the name of property as const'''
    
    def __init__(self,lang='CHS') -> None:
        self.setattr(lang)

    @classmethod
    def setattr(cls,lang):
        'set as class method to become static between different file'
        assert lang in const_property_namelist['HP'].keys(),'invalid input language'
        cls.lang = lang
        cls.const_map = {}
        for name in const_property_namelist.keys():
            setattr(cls,name,const_property_namelist[name][lang])
            cls.const_map[name] = const_property_namelist[name][lang]

        for name in const_element_namelist.keys():
            setattr(cls,name,const_element_namelist[name][lang])
            cls.const_map[name] = const_element_namelist[name][lang]

Const.setattr('CHS')
    

class Property:
    '''store the data that show on panel/on board'''
    def __init__(self,data:dict) -> None:
        '''
        structure of data:
        {
            'basic_board':{},key in const_property_namelist
            'board':{},key in const_property_namelist
            'Inc':{},key in const_element_namelist
            'RES':{},key in const_element_namelist
            when initialize,do not check
        }
        '''
        self.basic_board = {}
        self.basic_board.update(data.get('basic_board',{}))
        self.board = {}
        self.board.update(data.get('board',{}))
        self.Inc = {}
        self.Inc.update(data.get('Inc',{}))
        self.RES = {}
        self.RES.update(data.get('RES',{}))
        self.key_list = ['basic_board','board','Inc','RES']
        for key in data.keys():
            if key in self.key_list:
                continue
            self.set(key,data[key])

    def set(self,item:str,value:float):
        if item.startswith('basic '):
            item = item[6:]
            # assert in const_property_namelist
            self.basic_board[item] = value
        elif item.endswith(' Inc'):
            item = item[:-4]
            self.Inc[item] = value
        elif item.endswith(' RES'):
            item = item[:-4]
            self.RES[item] = value
        else:
            self.board[item] = value
    
    def get(self,item:str,get_value:bool=True)->float:
        if item.startswith('basic '):
            item = item[6:]
            # assert in const_property_namelist
            result = self.basic_board.get(item,0)
        elif item.endswith(' Inc'):
            item = item[:-4]
            result = self.Inc.get(item,0)
        elif item.endswith(' RES'):
            item = item[:-4]
            result = self.RES.get(item,0.1)
        else:
            result = self.board.get(item,0)
        if get_value:
            return float(result)
        else:
            return result
        
    def __add__(self,other):
        assert isinstance(other,Property),"?"
        f=lambda d1,d2:{key:d1.get(key,0)+d2.get(key,0)for key in d1.keys() | d2.keys()}
        return Property({key:f(self.__getattribute__(key),other.__getattribute__(key))
                         for key in self.key_list})
    
    def __sub__(self,other):
        assert isinstance(other,Property),"??"
        f=lambda d1,d2:{key:d1.get(key,0)-d2.get(key,0)for key in d1.keys() | d2.keys()}
        return Property({key:f(self.__getattribute__(key),other.__getattribute__(key))
                         for key in self.key_list})
    def copy(self):
        return Property({key:self.__getattribute__(key).copy() for key in self.key_list})
    def copy_from(self,other):
        assert isinstance(other,Property),"???"
        self.basic_board.update(other.basic_board)
        self.board.update(other.board)
        self.Inc.update(other.Inc)
        self.RES.update(other.RES)

class BDF:
    '''Basic Damage Function'''
    def __init__(self,func) -> None:
        if type(func)==str:
            func = self.tokenize(func)
        assert type(func)==dict,'invalid damage function'
        self.func = func
    def tokenize(self,s:str):
        s_list = s.split('+')
        rec = {}
        for item in s_list:
            item = item.strip()
            item = item.split('%')
            if len(item)==1:
                rec['ATK'] = float(item[0].strip())/100
            else:
                item = [item[0].strip(),item[1].strip()]
                for key in const_property_namelist.keys():
                    if(item[1] == Const.const_map[key])or(item[1]==key):
                        rec[key] = float(item[0])/100
                        break
        return rec
    def __call__(self, actor_prop:Property):
        sum = 0
        for key,value in self.func.items():
            prop_key = actor_prop.get(key)
            prop_key_percent = actor_prop.get(key+' percent')
            if prop_key_percent:
                prop_key += prop_key_percent + actor_prop.get('basic '+key)
            sum += prop_key*value
        return sum



class Parameter(Property):
    '''
    Inc:{
        element:const_element_namelist,
        action:const_action_namelist,
        DMG_type:const_DMGtype_namelist,
        all:'all'
    }
    '''
    pass

class Buff():
    # buff = {'on_stage':Parameter({}),'off_stage':Parameter({})}
    on_stage = 'on_stage'
    off_stage = 'off_stage'
    all_stage = 'all_stage'
    def __init__(self, data: dict = {},ddl:float=-1) -> None:
        self.buff = {}
        for key in ['on_stage','off_stage']:
            self.buff[key] = Parameter(data.get(key,{}))
        if data.get('all_stage',{}):
            self.buff['on_stage'] += Parameter(data['all_stage'])
            self.buff['off_stage'] += Parameter(data['all_stage'])
        self.ddl = ddl
    def add_buff(self,new_buff):
        assert isinstance(new_buff,Buff),'invalid buff'
        for key in ['on_stage','off_stage']:
            self.buff[key]+= new_buff.buff[key]
    def __add__(self,other):
        assert isinstance(other,Buff),'invalid buff'
        result = Buff()
        result.add_buff(self)
        result.add_buff(other)
        return result
    def add_single_buff(self,stat:str,item:str,value:float):
        assert stat in ['on_stage','off_stage','all_stage']
        if stat=='all_stage':
            self.add_buff(Buff({'on_stage':{item:value}}))
            self.add_buff(Buff({'off_stage':{item:value}}))
        else:
            self.add_buff(Buff({stat:{item:value}}))

    def set_buff(self,stat:str,item:str,value:float):
        assert stat in ['on_stage','off_stage','all_stage']
        if stat=='all_stage':
            self.buff['on_stage'].set(item,value)
            self.buff['off_stage'].set(item,value)
        else:
            self.buff[stat].set(item,value)
    def remove_buff(self,new_buff):
        assert isinstance(new_buff,Buff),'invalid buff'
        for key in ['on_stage','off_stage']:
            self.buff[key]-= new_buff.buff[key]

class ACal:
    '''active calculator,serve for buff calculation'''
    def __init__(self,func:dict,data_base:Parameter,add:list=[]) -> None:
        '''
        func:{
            property:num,
            'other':num,
        }
        use data in data_base,return sum(each_property*each_num)+other
        '''
        self.func = func
        self.data_base = data_base
        self.add = add
    def __call__(self) -> float:
        result = self.func.get('other',0)
        for key,value in self.func.items():
            prop_key = self.data_base.get(key)
            prop_key_percent = self.data_base.get(key+' percent')
            if prop_key_percent:
                prop_key += prop_key_percent + self.data_base.get('basic '+key)
            result += prop_key*value
        if self.add!=[]:
            result += sum([sum(each) for each in self.add])
        return result
    def __add__(self,other):
        if isinstance(other,ACal):
            if self.data_base==other.data_base:
                func = {key:self.func.get(key,0)+other.func.get(key,0)for key in self.func.keys() | other.func.keys()}
                return ACal(func,self.data_base,self.add+other.add)
            else:
                return ACal(self.func,self.data_base,self.add+[other])
        else:
            func = self.func.copy()
            func['other'] = func.get('other',0)+other
            return ACal(func,self.data_base,self.add)

    def __radd__(self,other):
        assert not isinstance(other,ACal),'ACal error'
        func = self.func.copy()
        func['other'] = func.get('other',0)+other
        return ACal(func,self.data_base,self.add)
    def __float__(self) -> float:
        return self.__call__()
    def __repr__(self) -> str:
        return str(self.__call__())
    __str__= __repr__

  
        

if __name__=='__main__':
    print(Const.HP)
    cfg = Const('CHS')
    print(cfg.HP)
    cfg.setattr('EN')
    print(cfg.HP)