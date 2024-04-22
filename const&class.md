## element 常量
七元素、物理

## Property 类
记录面板数据(白值与绿值)，伤害加成与抗性部分的key可调用element

## Parameter(Property) 派生类
添加基础伤害增加值、攻速增加、面板数据百分比增加等参数

## Buff 类
记录增益
Buff.buff(Dict[str,Parameter])：键值有前台、后台、全场
Buff.ddl:剩余时间（序列长度），-1表示持久


## Actor 类
记录可交互对象的参数
### 属性：
- Actor.property(Property)
- Actor.resist_list：反应抵抗列表
- Actor.addon_list：可附着元素列表，默认'all'
- Actor.immuno_list：免疫列表，包括伤害免疫与反应免疫
- Actor.element_list：附着列表
- Actor.element_list_buffer：B类附着列表
- Actor.element_origin：元素来源（带附着时间点序号）
- Actor.tag：判断敌我、中立
- Actor.transformative_list：记录受到的剧变反应
### 方法：
- Actor.generate_action(Attack)->Attack 由输入的模板生成相应的动作，可由子类负责实现


## Attack 类
### 属性：
- Attack.property(Property)
- Attack.actor(Actor)
- Attack.target(Actor)
- Attack.action_tag：普攻、重击、下落攻击、e、q
- Attack.element
- Attack.damage_tag：结算为何种类型的伤害
- Attack.addon_vector(uint8)：附着序列
- Attack.addon_vector_point: 附着指针
- Attack.addon_reset_time:附着重置时间
- Attack.last_index：记录上一次作用的时间序号

### 方法：
- Attack.check：判断当前是否能附着，考虑重置与指针位置
- Attack.next：移动附着指针
- Attack.damage_func：直伤公式

## Summoned(Actor) 派生类 召唤物
- Summoned.ddl：剩余时间（序列长度），-1表示持久
- Summoned.property_frozen(Dict[bool])：锁面板记录
- Summoned.duration：触发间隔
- Summoned.skill(List[dict]):[  
 &ensp;{  
    &ensp;&ensp;'trigger':str 触发方式（伤害，反应，时间）  
    &ensp;&ensp;'duration': 触发间隔  
    &ensp;&ensp;'action':Attack 提供Attack模板  
    &ensp;&ensp;'last moment'：记录上次施法时间  
&ensp;}  
]


## Enemy(Actor) 派生类
Enemy.tag == 'enemy'
### 属性：
- Enemy.affected_list：记录曾被攻击的action，当Timer添加action到action_query时先查询并更新该列表

## Character(Actor) 派生类
Character.tag == 'friend'
### 属性：
- Character.skill(List[dict]):[
&ensp;{  
    &ensp;&ensp;'buff':Buff 对己方提供的增益效果  
    &ensp;&ensp;'debuff':Buff 对敌方提供的减益效果  
    &ensp;&ensp;'action':Attack 提供的Attack模板  
    &ensp;&ensp;'state machine'：记录前后摇、上次施法时间、多段直伤公式  
    &ensp;&ensp;'summoned creation':Summoned 召唤物（后台伤害其实也能丢到这类）  
&ensp;}  
]
- Character.state machine：记录前后摇、上次施法时间、上次施法动作，多段直伤公式
- Character.weapon：记录武器效果
- Character.relic: 记录圣遗物效果  
- Character.personal：记录天赋、命座效果
- 

### 方法：
- Character.load_model：导入角色模型
- Character.load_data：导入角色面板等数据