import ast
import operator
import sys
import readline
 # optional, improves REPL with history/navigation

# Map AST binary operators to python functions
_BIN_OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
    ast.FloorDiv: operator.floordiv,
    # bitwise ops intentionally not supported
}

_UNARY_OPS = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}

_ALLOWED_NODES = (
    ast.Expression,
    ast.BinOp,
    ast.UnaryOp,
    ast.Constant,   # Python 3.8+: numbers are Constant; older versions use Num
    ast.Num,
          # ast.Paren doesn't actually exist; parentheses are structure only
)

def eval_expr(expr: str):
    """
    Safely evaluate a math expression using ast.
    Allowed: numbers, + - * / % // **, parentheses, unary +/-
    Raises ValueError for invalid expressions.
    """
    try:
        node = ast.parse(expr, mode='eval')
    except SyntaxError as e:
        raise ValueError(f"Syntax error: {e}")

    def _eval(node):
        # Expression wrapper
        if isinstance(node, ast.Expression):
            return _eval(node.body)

        # Numbers
        if isinstance(node, ast.Constant):  # Python 3.8+
            if isinstance(node.value, (int, float)):
                return node.value
            raise ValueError(f"Unsupported constant: {node.value!r}")
        if isinstance(node, ast.Num):  # older Python
            return node.n

        # Binary operations
        if isinstance(node, ast.BinOp):
            left = _eval(node.left)
            right = _eval(node.right)
            op_type = type(node.op)
            if op_type in _BIN_OPS:
                try:
                    return _BIN_OPS[op_type](left, right)
                except ZeroDivisionError:
                    raise ValueError("Math error: division by zero")
            raise ValueError(f"Unsupported binary operator: {op_type.__name__}")

        # Unary operations (+ and -)
        if isinstance(node, ast.UnaryOp):
            op_type = type(node.op)
            if op_type in _UNARY_OPS:
                operand = _eval(node.operand)
                return _UNARY_OPS[op_type](operand)
            raise ValueError(f"Unsupported unary operator: {op_type.__name__}")

        # Anything else is disallowed
        raise ValueError(f"Unsupported expression: {ast.dump(node)}")

    result = _eval(node)
    # Normalize integer results that are actually whole numbers
    if isinstance(result, float) and result.is_integer():
        return int(result)
    return result


REPL_BANNER = (
    "Simple CLI Calculator — supports + - * / % // ** and parentheses.\n"
    "Type 'help' for commands. Use 'exit' or 'quit' to leave.\n"
)

HELP_TEXT = """Commands:
  help           Show this help text
  exit, quit     Exit the calculator
  history        Show last 50 expressions (if readline available)
  clear          Clear the screen (uses ANSI escape)
You can also run: python calculator.py "2*(3+4)/7" to evaluate a single expression.
"""

def repl():
    print(REPL_BANNER)
    while True:
        try:
            s = input("calc> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break

        if not s:
            continue

        # Commands
        cmd = s.lower()
        if cmd in ("exit", "quit"):
            break
        if cmd == "help":
            print(HELP_TEXT)
            continue
        if cmd == "history":
            try:
                i = 1
                hist_len = readline.get_current_history_length()
                start = max(1, hist_len - 50 + 1)
                for idx in range(start, hist_len + 1):
                    print(f"{idx - start + 1}: {readline.get_history_item(idx)}")
            except Exception:
                print("History not available.")
            continue
        if cmd == "clear":
            print("\033c", end="")  # ANSI clear screen
            continue

        # Try to evaluate expression
        try:
            result = eval_expr(s)
            print(result)
        except ValueError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")

def one_off(expr: str):
    try:
        result = eval_expr(expr)
        print(result)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(2)

def main(argv):
    if len(argv) > 1:
        # Join as one expression (so python calculator.py 2 + 2 works too)
        expr = " ".join(argv[1:])
        one_off(expr)
    else:
        repl()

if __name__ == "__main__":
    main(sys.argv)
