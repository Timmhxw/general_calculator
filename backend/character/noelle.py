from ..basic import base,common
Q_DEF2ATK = {1:0.4,2: 0.43, 3: 0.46,4:0.5,5: 0.53, 6: 0.56,
                   7:0.6,8: 0.64, 9: 0.68,10:0.72,11: 0.76, 12: 0.8,
                   13: 0.85}
E_DMG = {1:1.20,2:1.29,3:1.38,4:1.50,5:1.59,6:1.68,7:1.80,8:1.92,
         9:2.04,10:2.16,11:2.28,12:2.40,13:2.55}
A_DMG = {1:{1:0.791,2: 0.856, 3: 0.92,4:1.01,5: 1.08, 6: 1.15,
                   7:1.25,8: 1.35, 9: 1.45,10:1.56,11:1.67 },
        2:{1:0.734,2: 0.793, 3: 0.853,4:0.938,5: 0.998, 6: 1.07,
                   7:1.16,8: 1.25, 9: 1.35,10:1.45,11: 1.55},
        3:{1:0.863,2: 0.933, 3: 1,4:1.1,5: 1.17, 6: 1.25,
                   7:1.36,8: 1.47, 9: 1.58,10:1.71,11: 1.83},
        4: {1:1.13,2: 1.23, 3: 1.32,4:1.45,5: 1.54, 6: 1.65,
                   7:1.79,8: 1.94, 9: 2.08,10:2.24,11: 2.4}
          }
Z_DMG = {
    1:{1:0.507,2:0.549,3:0.590,4:0.649,5:0.690,6:0.738,7:0.802,
       8:0.867,9:0.932,10:1.003,11:1.074},
    2:{1:0.905,2:0.978,3:1.050,4:1.160,5:1.230,6:1.320,7:1.430,
       8:1.550,9:1.660,10:1.790,11:1.910}
}
P_DMG = {
   1:{1:1.49,2:1.61,3:1.73,4:1.91,5:2.03,6:2.17,7:2.36,
       8:2.55,9:2.74,10:2.95,11:3.16},
    2:{1:1.86,2:2.01,3:2.17,4:2.38,5:2.53,6:2.71,7:2.95,
       8:3.18,9:3.42,10:3.68,11:3.94} 
}
Basic_value90 = {
    'ATK':214,
    'DEF':799,
    'HP':12071
}
class Noelle(base.Character):
    def __init__(self,data:dict,A_level:int=10,E_level:int=10,Q_level:int=10,num:int=6) -> None:
        super().__init__(data, A_level, E_level, Q_level, num, Basic_value90,element='Rock')
        self.A = []
        for i in A_DMG.keys():
            self.A.append(base.Attack(
                base.ACal({'ATK':A_DMG[i][A_level]},self),
                'A'
            ))
        self.Z = []
        for i in Z_DMG.keys():
            self.Z.append(base.Attack(
                base.ACal({'ATK':Z_DMG[i][A_level]},self),
                'Z'
            ))
        self.P = []
        for i in P_DMG.keys():
            self.P.append(base.Attack(
                base.ACal({'ATK':P_DMG[i][A_level]},self),
                'P'
            ))
        self.E = []
        self.E.append(base.Attack(
                base.ACal({'ATK':E_DMG[A_level]},self),
                'E',self.element
            ))
        self.Q_DEF2ATK = Q_DEF2ATK[Q_level]
        self.Z_cost = 40
        if num>=2:
            self.Z_cost *=0.8
            self.parm.set('Z Inc',0.15)
        if num == 6:
            self.Q_DEF2ATK += 0.5
        self.last_action = ''
    
    def use_Q(self):
        buff = base.Buff(
            'all_stage',
            'ATK',
            base.ACal(
                {'DEF':self.Q_DEF2ATK},
                self
            )(secondary_call=False),
            private=True
        )
        self.add_private_buff(buff)
        for each_action in self.A+self.Z+self.P:
            assert isinstance(each_action,base.Attack)
            each_action.force_element(buff,'Rock')
        return buff
    
    def state_machine(self,action_name:str):
        if action_name=='A':
            if self.last_action.startswith('A'):
                if self.last_action =='A4':
                    '''last attack'''
                    self.last_action = 'A1'
                    return self.A[0]
                else:
                    idx = int(self.last_action[-1])
                    self.last_action = 'A' + str(idx+1)
                    return self.A[idx]
            else:
                self.last_action = 'A1'
                return self.A[0]
        else:
            self.last_action = action_name
            if action_name == 'Z':
                # to fix
                return self.Z[0]
            elif action_name == 'P':
                return self.P[0]
            elif action_name == 'E':
                return self.E[0]
            elif action_name == 'Q':
                return self.use_Q()

