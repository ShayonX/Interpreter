INTEGER, PLUS, MINUS, MULT, DIV, SPACE, EOF = 'INTEGER', 'PLUS', 'MINUS', 'MULT', 'DIV', 'SPACE', 'EOF'


class Token(object):
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __str__(self):
        return 'Token({type},{value})'.format(
            type=self.type,
            value=repr(self.value)
        )

    def __repr__(self):
        return self.__str__()


class Interpreter(object):
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_token = None

    def error(self):
        raise Exception('Error parsing input')

    def get_next_token(self):
        text = self.text
        if self.pos > len(text) - 1:
            return Token(EOF, None)

        current_char = text[self.pos]

        if current_char.isdigit():
            token = Token(INTEGER, int(current_char))
            self.pos += 1
            return token

        if current_char == ' ':
            token = Token(SPACE, current_char)
            self.pos += 1
            return token

        if current_char == '+':
            token = Token(PLUS, current_char)
            self.pos += 1
            return token

        if current_char == '-':
            token = Token(MINUS, current_char)
            self.pos += 1
            return token

        if current_char == '*':
            token = Token(MULT, current_char)
            self.pos += 1
            return token

        if current_char == '/':
            token = Token(DIV, current_char)
            self.pos += 1
            return token

        self.error()

    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = self.get_next_token()
        else:
            self.error()

    def expr(self):
        self.current_token = self.get_next_token()


        left = self.current_token
        self.eat(INTEGER)

        while self.current_token.type == INTEGER:
            left.type = self.current_token.type
            left.value = left.value * 10 + self.current_token.value
            self.eat(INTEGER)

        op = self.current_token

        while op.value == ' ':
            self.eat(SPACE)
            op = self.current_token

        if op.value == '+':
            self.eat(PLUS)
        elif op.value == '-':
            self.eat(MINUS)
        elif op.value == '*':
            self.eat(MULT)
        elif op.value == '/':
            self.eat(DIV)

        right = self.current_token

        while right.value == ' ':
            self.eat(SPACE)
            right = self.current_token

        self.eat(INTEGER)

        while self.current_token.type == INTEGER:
            right.type = self.current_token.type
            right.value = right.value * 10 + self.current_token.value
            self.eat(INTEGER)

        if op.value == '+':
            result = left.value + right.value
        elif op.value == '-':
            result = left.value - right.value
        elif op.value == '*':
            result = left.value * right.value
        elif op.value == '/':
            result = left.value / right.value

        return result


def main():
    while True:
        try:

            text = input('lang> ')
        except EOFError:
            break
        if not text:
            continue
        interpreter = Interpreter(text)
        result = interpreter.expr()
        print(result)


if __name__ == '__main__':
    main()
