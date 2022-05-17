from typing import List, Callable, Any
import inspect

class Inlet:
	def __init__(self):
		self.handles:List = []

	""" add listeners """
	def onTrigger(self, handle):
		self.handles.append(handle)


class Outlet:
	def __init__(self):
		self._value = None
		self.targets:List[Inlet] = []

	def target(self, inlet:Inlet):
		self.targets.append(inlet)
		for handle in inlet.handles:
			handle(value)


	def trigger(self, props:Any):
		self._value = props
		for inlet in self.targets:
			for handle in inlet.handles:
				handle(value)


class Attribute:
	def __init__(self):
		self.value = None
		self.handles = []

	def set(self, val:Any):
		for handle in self.handles:
			handle(self.value, val)
		self.value = val

	def onChange(self, handle:Callable):
		self.handles.append(handle)


class Node:
	def __init__(self):
		pass

	def onUICreate(self, element):
		pass


class Value(Node):
	def __init__(self, val:Any=None):
		super().__init__()
		self.value = Attribute()
		self.out = Outlet()

		@self.value.onChange
		def _(old_value, new_value):
			self.out.trigger(new_value)

		self.value.set(val)


class Operator(Node):
	def __init__(self, f:Callable):
		sig = inspect.signature(f)
		
		self.parameters = dict()
		self.f:Callable = f

		for param in sig.parameters.values():
			inlet = Inlet()
			setattr(self, param.name, inlet)
			@inlet.onTrigger
			def _(value, param=param):
				self.update(param, value)

		setattr(self, "out", Outlet())

	def update(self, param, value):
		self.parameters[param.name] = value
		try:
			result = self.f(**self.parameters)
			self.out.trigger(result)
		except TypeError as err:
			print("EvaluateWarning:", err)


class PrintNode(Node):
	def __init__(self):
		self.input = Inlet()
		self.input.onTrigger(self.update)

	def update(self, props):
		print(f"A + B = {props}")