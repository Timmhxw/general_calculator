## 反应流程 Reaction function
### 攻击动作 attack action
入参为action、攻击对象附着队列 element_list（判断是否有冻）、攻击对象类别（是否允许碎冰）  
处理碎冰：冻->max(冻-8,0)  
判断是否发生攻击动作连携，如果是，压入action_query_buffer

### 元素附着 element addon
入参为action与被攻击对象actor  
调用action.check判断附着序列当前是否可附着，且攻击对象是否可被附着（排除物件盾）  
判断结束后action.next  
返回是否成功附着

### 元素反应 element reaction
入参为攻击对象附着队列 element_list、后手元素element_addon与被攻击对象actor 
结算二级反应，发生的反应压入reaction_list  
记录攻击对象的反应抵抗效果  
取element_addon与element_list中的元素依照反应优先级与是否反应抵抗进行反应判断与剩余元素量结算，发生的反应压入reaction_list。结算后手元素是否残留，若是，压入actor 的 element_list_buffer，并刷新element_origin。

### 反应效果 reaction affect
入参为action、反应列表reaction_list、buff、debuff、被攻击对象actor  
记录攻击对象元素伤害免疫效果与反应免疫效果
结算reaction_list中各反应伤害
- 从action的property中提取available parameter，与buff中相应parameter 相加
- 结合反应类型与actor面板，计算反应伤害
- 若发生原绽放反应，生成新actor种子；发生扩散生成新的action（默认全体触发）；发生范围剧变反应结算范围伤害
- 调用action.actor如果有友方tag，结算命座、天赋、武器、圣遗物等额外效果
- 当伤害来源和被攻击对象相同时，考虑是否伤害为0
若未发生增幅、激化反应，调用action.damage_func补充计算action原伤害  
判断是否触发伤害连携及反应连携


## 时间轴 Timer
根据输入的动作指令action_order，编排实际发生的动作序列。  
基础参数sample_freq = 60，当前时间点序号time_index 初始为0  
当前实际时间点 time = time_index/sample_freq  
当前动作序列action_query  
当前我方增益buff,当前敌方减益debuff 初始化为元素共鸣  
debuff为dict，只记录减防减抗  
当前场上可交互对象actor_list,后台伤害summoned_list  
现有增益序列 buff_list，保存各非持久buff、debuff的时间及效果  

- 判断action_order的队首是否可用，若可，出队并结算：action添加到action_query，buff与debuff添加或直接结算（如治疗）
- 各Summoned结算周期性伤害能否添加到action_query
- 调用Reaction function，结算action_query每个action
- 各Summoned结算剩余时间
- 各actor结算自附着。随机抽取element_list_buffer中的某一元素，与element_list中的元素依照反应优先级与是否反应抵抗进行反应判断与剩余元素量结算，发生的反应压入reaction_list。调用reaction affect结算反应效果。结算后手元素是否残留，若是，加入element_list。以此结算element_list_buffer中所有元素。
- 结算持续伤害与附着衰减
- 结算buff_list剩余时间
- 结算角色命座、天赋、武器、圣遗物等额外效果


