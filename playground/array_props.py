class UnderClass:
    myType: str = 'zero'
    name: str = 'default'


class MyTestClass:
    _objs: list[UnderClass] = []

    def add(self, itm: UnderClass):
        if itm.myType == 'one':

            #     # 1
            #     if self.find_one():
            #         self.del_one()
            # 2
            tmp_one = self.find_one()
            if tmp_one:
                self.del_obj(tmp_one)
        self._objs.append(itm)


        self.print_obj()



    def find_one(self):
        for i in self._objs:
            if i.myType == 'one':
                return i

    def del_obj(self, itm: UnderClass):
        self._objs = [i for i in self._objs if i!=itm]

    def del_one(self):
        self._objs = [i for i in self._objs if i.myType!='one']  # 💩


    def print_obj(self):
        print([f't:{x.myType} n:{x.name}' for x in self._objs])

uc_a_0 = UnderClass()
uc_a_0.myType = 'zero'
uc_a_0.name = '0_gen'

uc_b_0 = UnderClass()
uc_b_0.myType = 'one'
uc_b_0.name = '0_gen'

uc_c_0 = UnderClass()
uc_c_0.myType = 'two'
uc_c_0.name = '0_gen'

ok = MyTestClass()
ok.add(uc_a_0)
ok.add(uc_b_0)
ok.add(uc_c_0)

uc_b_1 = UnderClass()
uc_b_1.myType = 'one'
uc_b_1.name = '1_gen'

ok.add(uc_b_1)