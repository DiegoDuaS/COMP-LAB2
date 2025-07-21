from SimpleLangListener import SimpleLangListener
from SimpleLangParser import SimpleLangParser
from custom_types import IntType, FloatType, StringType, BoolType

class TypeCheckListener(SimpleLangListener):

  def __init__(self):
    self.errors = []
    self.types = {}

  def enterMulDivModPow(self, ctx: SimpleLangParser.MulDivModPowContext):
    pass

  def exitMulDivModPow(self, ctx: SimpleLangParser.MulDivModPowContext):
    left_type = self.types[ctx.expr(0)]
    right_type = self.types[ctx.expr(1)]
    operator = ctx.op.text

    # No se permiten booleanos en operaciones
    if isinstance(left_type, BoolType) or isinstance(right_type, BoolType):
        self.errors.append(f"Boolean values are not allowed in '{operator}' operation: {left_type}, {right_type}")
        self.types[ctx] = None
        return
    # Reglas para nuevas operaciones
    if operator == '%' and (not isinstance(left_type, IntType) or not isinstance(right_type, IntType)):
        self.errors.append(f"Modulo (%) requires integer operands: {left_type}, {right_type}")
        self.types[ctx] = None
        return
    if operator == '^' and not (self.is_valid_arithmetic_operation(left_type, right_type)):
        self.errors.append(f"Exponentiation (^) requires numeric operands: {left_type}, {right_type}")
        self.types[ctx] = None
        return
    if not self.is_valid_arithmetic_operation(left_type, right_type):
        self.errors.append(f"Unsupported operand types for '{operator}': {left_type} and {right_type}")
        self.types[ctx] = None
        return
    if isinstance(left_type, FloatType) or isinstance(right_type, FloatType):
        self.types[ctx] = FloatType()
    else:
        self.types[ctx] = IntType()


  def enterAddSub(self, ctx: SimpleLangParser.AddSubContext):
    pass

  def exitAddSub(self, ctx: SimpleLangParser.AddSubContext):
    left_type = self.types[ctx.expr(0)]
    right_type = self.types[ctx.expr(1)]
    if not self.is_valid_arithmetic_operation(left_type, right_type):
      self.errors.append(f"Unsupported operand types for + or -: {left_type} and {right_type}")
    self.types[ctx] = FloatType() if isinstance(left_type, FloatType) or isinstance(right_type, FloatType) else IntType()

  def enterInt(self, ctx: SimpleLangParser.IntContext):
    self.types[ctx] = IntType()

  def enterFloat(self, ctx: SimpleLangParser.FloatContext):
    self.types[ctx] = FloatType()

  def enterString(self, ctx: SimpleLangParser.StringContext):
    self.types[ctx] = StringType()

  def enterBool(self, ctx: SimpleLangParser.BoolContext):
    self.types[ctx] = BoolType()

  def enterParens(self, ctx: SimpleLangParser.ParensContext):
    pass

  def exitParens(self, ctx: SimpleLangParser.ParensContext):
    self.types[ctx] = self.types[ctx.expr()]

  def is_valid_arithmetic_operation(self, left_type, right_type):
    if isinstance(left_type, (IntType, FloatType)) and isinstance(right_type, (IntType, FloatType)):
      return True
    return False
