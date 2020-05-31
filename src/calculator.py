# -----------------------------------------------------------------------------
# calc.py
#
# A calculator parser that makes use of closures. The function make_calculator()
# returns a function that accepts an input string and returns a result.  All
# lexing rules, parsing rules, and internal state are held inside the function.
# -----------------------------------------------------------------------------

import sys, math

if sys.version_info[0] >= 3:
    raw_input = input

# Make a calculator function
def make_calculator():
    import ply.lex as lex
    import ply.yacc as yacc

    errors = []

    # ------- Internal calculator state

    variables = { }       # Dictionary of stored variables

    # ------- Calculator tokenizing rules

    tokens = (
        'NAME','NUMBER', 'LOG', 'LN', 'LG', 'SIN', 'COS', 'TAN', 'ASIN', 'ACOS', 'ATAN', 'SINH', 'COSH', 'TANH', 'ASINH', 'ACOSH', 'ATANH', 'SQRT', 'DEG', 'RAD', 'PI', 'E', 'MOD', 'FLOOR', 'CEIL', 'ROUND', 'ABS', 'XOR', 'HEX', 'OCT', 'SHIFTL', 'SHIFTR'
    ) # , 'BIN'

    literals = ['=','+','-','*','/', '^','(',')','{','}','[',']','%','~', '&', '|'] # '!',

    t_ignore = " \t"


    t_ABS = 'abs'
    t_LN = 'ln'
    t_LG = 'lg'
    t_LOG = 'log'
    t_SIN = 'sin'
    t_COS = 'cos'
    t_TAN = 'tan'
    t_ASIN = 'asin'
    t_ACOS = 'acos'
    t_ATAN = 'atan'
    t_SINH = 'sinh'
    t_COSH = 'cosh'
    t_TANH = 'tanh'
    t_ASINH = 'asinh'
    t_ACOSH = 'acosh'
    t_ATANH = 'atanh'
    t_SQRT = 'sqrt'
    t_DEG = 'deg'
    t_RAD = 'rad'
    t_MOD = 'mod'
    t_PI = 'pi'
    t_E = 'e'
    t_FLOOR = 'floor'
    t_CEIL = 'ceil'
    t_ROUND = 'round'
    t_XOR = 'xor'
    # t_BIN = 'bin'
    t_HEX = 'hex'
    t_OCT = 'oct'
    t_SHIFTL = '<<'
    t_SHIFTR = '>>'
    # t_NAME    = r'[a-zA-Z_][a-zA-Z0-9_]*'

    def t_NUMBER(t):
        r'\d+\.?\d*'
        t.value = float(t.value)
        return t

    def t_newline(t):
        r'\n+'
        t.lexer.lineno += t.value.count("\n")

    def t_error(t):
        if __name__ == '__main__':
          print("Illegal character '%s'" % t.value[0])
        errors.append("Illegal character '%s'" % t.value[0])
        t.lexer.skip(1)

    # Build the lexer
    lexer = lex.lex()

    # ------- Calculator parsing rules

    precedence = (
        ('left','+','-'),
        ('left','*','/','MOD'),
        ('left','^'),
        ('left','~', 'XOR', '&', '|', 'SHIFTL', 'SHIFTR'),
        ('left','LN','LOG','LG','SIN','COS','TAN','ASIN','ACOS','ATAN','SINH','COSH','TANH','ASINH','ACOSH','ATANH','SQRT', 'DEG', 'RAD', 'FLOOR', 'CEIL', 'ROUND', 'ABS', 'HEX', 'OCT'), # 'BIN',
        ('right','%'), # ,'!'
        ('right','UMINUS'),
    )

    def p_statement_assign(p):
        'statement : NAME "=" expression'
        variables[p[1]] = p[3]
        p[0] = None

    def p_statement_expr(p):
        'statement : expression'
        p[0] = p[1]

    def p_expression_binop(p):
        '''expression : expression '+' expression
                      | expression '-' expression
                      | expression '*' expression
                      | expression '/' expression
                      | expression '^' expression
                      | expression '&' expression
                      | expression '|' expression
                      | expression SHIFTL expression
                      | expression SHIFTR expression
                      | expression XOR expression
                      | expression MOD expression '''
        if p[2] == '+'  : p[0] = p[1] + p[3]
        elif p[2] == '-': p[0] = p[1] - p[3]
        elif p[2] == '*': p[0] = p[1] * p[3]
        elif p[2] == '/': p[0] = float(p[1]) / p[3]
        elif p[2] == '^': p[0] = p[1] ** p[3]
        elif p[2] == '&': p[0] = int(p[1]) & int(p[3])
        elif p[2] == '|': p[0] = int(p[1]) | int(p[3])
        elif p[2] == '>>': p[0] = int(p[1]) << int(p[3])
        elif p[2] == '<<': p[0] = int(p[1]) >> int(p[3])
        elif p[2] == 'xor': p[0] = int(p[1]) ^ int(p[3])
        elif p[2] == 'mod': p[0] = p[1] % p[3]

    def p_expression_uminus(p):
        "expression : '-' expression %prec UMINUS"
        p[0] = -p[2]

    def p_expression_not(p):
        "expression : '~' expression %prec UMINUS"
        p[0] = ~int(p[2])

    def p_expression_group(p):
        "expression : '(' expression ')'"
        p[0] = p[2]

    def p_expression_group_2(p):
        "expression : '{' expression '}'"
        p[0] = p[2]

    def p_expression_group_3(p):
        "expression : '[' expression ']'"
        p[0] = p[2]

    def p_expression_absolute(p):
        "expression : ABS expression"
        p[0] = math.fabs(p[2])

    def p_expression_number(p):
        "expression : NUMBER"
        p[0] = p[1]

    def p_expression_percent(p):
        "expression : expression '%'"
        p[0] = float(p[1]) / 100

    #def p_expression_factorial(p):
    #    "expression : expression '!'"
    #    p[0] = math.factorial(p[1])

    def p_expression_lg(p):
        "expression : LG expression"
        p[0] = math.log(p[2], 2)

    def p_expression_ln(p):
        "expression : LN expression"
        p[0] = math.log(p[2])

    def p_expression_log(p):
        "expression : LOG expression"
        p[0] = math.log(p[2])/math.log(10)

    def p_expression_sin(p):
        "expression : SIN expression"
        p[0] = math.sin(p[2])

    def p_expression_cos(p):
        "expression : COS expression"
        p[0] = math.cos(p[2])

    def p_expression_tan(p):
        "expression : TAN expression"
        p[0] = math.tan(p[2])

    def p_expression_asin(p):
        "expression : ASIN expression"
        p[0] = math.asin(p[2])

    def p_expression_acos(p):
        "expression : ACOS expression"
        p[0] = math.acos(p[2])

    def p_expression_atan(p):
        "expression : ATAN expression"
        p[0] = math.atan(p[2])

    def p_expression_sinh(p):
        "expression : SINH expression"
        p[0] = math.sinh(p[2])

    def p_expression_cosh(p):
        "expression : COSH expression"
        p[0] = math.cosh(p[2])

    def p_expression_tanh(p):
        "expression : TANH expression"
        p[0] = math.tanh(p[2])

    def p_expression_asinh(p):
        "expression : ASINH expression"
        p[0] = math.asinh(p[2])

    def p_expression_acosh(p):
        "expression : ACOSH expression"
        p[0] = math.acosh(p[2])

    def p_expression_atanh(p):
        "expression : ATANH expression"
        p[0] = math.atanh(p[2])

    def p_expression_sqrt(p):
        "expression : SQRT expression"
        p[0] = math.sqrt(p[2])

    def p_expression_deg(p):
        "expression : DEG expression"
        p[0] = math.degrees(p[2])

    def p_expression_rad(p):
        "expression : RAD expression"
        p[0] = math.radians(p[2])

    def p_expression_floor(p):
        "expression : FLOOR expression"
        p[0] = math.floor(p[2])

    def p_expression_ceil(p):
        "expression : CEIL expression"
        p[0] = math.ceil(p[2])

    def p_expression_round(p):
        "expression : ROUND expression"
        p[0] = round(p[2])

    #def p_expression_bin(p):
    #    "expression : BIN expression"
    #    p[0] = bin(int(p[2]))

    def p_expression_hex(p):
        "expression : HEX expression"
        p[0] = hex(int(p[2]))

    def p_expression_oct(p):
        "expression : OCT expression"
        p[0] = oct(int(p[2]))

    def p_expression_pi(p):
        "expression : PI"
        p[0] = math.pi

    def p_expression_e(p):
        "expression : E"
        p[0] = math.e

    def p_expression_name(p):
        "expression : NAME"
        try:
            #print('p')
            p[0] = variables[p[1]]
        except LookupError:
            if __name__ == '__main__':
              print("Undefined name '%s'" % p[1])
            errors.append("Undefined name '%s'" % p[1])
            p[0] = 0

    def p_error(p):
        if p:
            if __name__ == '__main__':
              print("Syntax error at '%s'" % p.value)
            errors.append("Syntax error at '%s'" % p.value)
        else:
            if __name__ == '__main__':
              print('Syntax error at EOF')
            errors.append('Syntax error at EOF')

    # Build the parser
    parser = yacc.yacc(debug=None)

    # ------- Input function

    def input(text):
        result = parser.parse(text,lexer=lexer)
        return result, errors

    return input

if __name__ == '__main__':
  # Make a calculator object and use it
  calc = make_calculator()

  while True:
      try:
          s = raw_input("calc > ")
      except EOFError:
          break
      r,e = calc(s)
      print(e)
      if r!=None:
          print(r)
