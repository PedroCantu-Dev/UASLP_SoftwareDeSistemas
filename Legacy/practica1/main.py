import sys
from antlr4 import *
from antlr4.InputStream import InputStream

from dist.CalculatorGrammarLexer import CalculatorGrammarLexer
from dist.CalculatorGrammarParser import CalculatorGrammarParser
from dist.CalculatorGrammarVisitor import CalculatorGrammarVisitor



if __name__ == '__main__':
    if len(sys.argv) > 1:
        input_stream = FileStream(sys.argv[1])
    else:
        input_stream = InputStream(sys.stdin.readline())

    lexer = CalculatorGrammarLexer(input_stream)
    token_stream = CommonTokenStream(lexer)
    parser = CalculatorGrammarParser(token_stream)
    tree = parser.prog()

    #lisp_tree_str = tree.toStringTree(recog=parser)
    #print(lisp_tree_str)

    visitor = CalculatorGrammarVisitor()
    visitor.visit(tree)


# def get_username():
#     from pwd import getpwuid
#     from os import getuid
#     return getpwuid(getuid())[ 0 ]

  
# class MyVisitor(CalculatorGrammarVisitor):
#     def visitNumberExpr(self, ctx):
#         value = ctx.getText()
#         return int(value)

#     def visitParenExpr(self, ctx):
#         return self.visit(ctx.expr())

#     def visitInfixExpr(self, ctx):
#         l = self.visit(ctx.left)
#         r = self.visit(ctx.right)

#         op = ctx.op.text
#         operation =  {
#         '+': lambda: l + r,
#         '-': lambda: l - r,
#         '*': lambda: l * r,
#         '/': lambda: l / r,
#         }
#         return operation.get(op, lambda: None)()

#     def visitByeExpr(self, ctx):
#         print(f"goodbye {get_username()}")
#         sys.exit(0)

#     def visitHelloExpr(self, ctx):
#         return (f"{ctx.getText()} {get_username()}")


# if __name__ == "__main__":
#     while 1:
#         data =  InputStream(input(">>> "))
#         # lexer
#         lexer = CalculatorGrammarLexer(data)
#         stream = CommonTokenStream(lexer)
#         # parser
#         parser = CalculatorGrammarParser(stream)
#         tree = parser.expr()
#         # evaluator
#         visitor = MyVisitor()
#         output = visitor.visit(tree)
#         print(output)