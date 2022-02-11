class Enum:
 def __init__(self,*args,**kwargs):
  self.attr_count=0
  for s in args:
   setattr(self,s.upper(),self.attr_count)
   if 'globals' in kwargs:
    kwargs['globals']['STATE_'+s.upper()]=self.attr_count
   self.attr_count+=1
 def __len__(self):
  return self.attr_count
 def __getitem__(self,name):
  return getattr(self,name.upper())
 def __setitem__(self,name,value):
  raise NotImplementedError("You can't change an enum item's value")
# Created by pyminifier (https://github.com/liftoff/pyminifier)
