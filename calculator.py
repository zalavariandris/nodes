import nodes
from typing import Any, Callable, Union
Numeric = Union[int, float, complex] # consider include np.number
import inspect



def plus(A:int,B:int)->int:
	return A+B


if __name__ == "__main__":
	import sys
	print("Python version", sys.version, "\n")
	A = nodes.Value(10)
	B = nodes.Value(10)
	Plus = nodes.Operator(plus)
	A.out.target(Plus.A)
	B.out.target(Plus.B)

	Print = nodes.PrintNode()
	Plus.out.target(Print.input)

	A.value.set(1)
	B.value.set(2)

