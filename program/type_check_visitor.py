from SimpleLangParser import SimpleLangParser
from SimpleLangVisitor import SimpleLangVisitor
from custom_types import IntType, FloatType, StringType, BoolType

class TypeCheckVisitor(SimpleLangVisitor):

  def visitMulDivModPow(self, ctx: SimpleLangParser.MulDivModPowContext):
    left_type = self.visit(ctx.expr(0))
    right_type = self.visit(ctx.expr(1))
    operator = ctx.op.text
    
    #No se permiten booleanos en operaciones
    if isinstance(left_type, BoolType) or isinstance(right_type, BoolType):
        raise TypeError(f"Cannot use boolean in '{operator}' operation: {left_type}, {right_type}")

    if not isinstance(left_type, (IntType, FloatType)) or not isinstance(right_type, (IntType, FloatType)):
        raise TypeError(f"Unsupported operand types for {operator}: {left_type} and {right_type}")

    # Errores de tipo en las nuevas operaciones 
    if operator == '%' and (not isinstance(left_type, IntType) or not isinstance(right_type, IntType)):
        raise TypeError(f"Modulo operator (%) requires int operands, got {left_type} and {right_type}")

    if operator == '^' and (not isinstance(left_type, (IntType, FloatType)) or not isinstance(right_type, (IntType, FloatType))):
        raise TypeError(f"Exponentiation (^) requires numeric operands, got {left_type} and {right_type}")

    # Retornar tipo resultante
    return FloatType() if isinstance(left_type, FloatType) or isinstance(right_type, FloatType) else IntType()


  def visitAddSub(self, ctx: SimpleLangParser.AddSubContext):
    left_type = self.visit(ctx.expr(0))
    right_type = self.visit(ctx.expr(1))
    operator = ctx.op.text

    if isinstance(left_type, StringType) or isinstance(right_type, StringType):
        if isinstance(left_type, StringType) and isinstance(right_type, StringType):
            return StringType()
        else:
            raise TypeError(f"Cannot add String with non-String type: {left_type}, {right_type}")

    if isinstance(left_type, (IntType, FloatType)) and isinstance(right_type, (IntType, FloatType)):
        return FloatType() if isinstance(left_type, FloatType) or isinstance(right_type, FloatType) else IntType()

    raise TypeError(f"Unsupported operand types for {operator}: {left_type}, {right_type}")
  
  def visitInt(self, ctx: SimpleLangParser.IntContext):
    return IntType()

  def visitFloat(self, ctx: SimpleLangParser.FloatContext):
    return FloatType()

  def visitString(self, ctx: SimpleLangParser.StringContext):
    return StringType()

  def visitBool(self, ctx: SimpleLangParser.BoolContext):
    return BoolType()

  def visitParens(self, ctx: SimpleLangParser.ParensContext):
    return self.visit(ctx.expr())
