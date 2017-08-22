# first we decide on the type of tokens
# we also take eof to indicate the input for lexical analysis is over
VAR, INTEGER, EQUAL, PLUS, MINUS, MULT, DIV, SPACE, PRINT, EOF = 'VAR', 'INTEGER', 'EQUAL', 'PLUS', 'MINUS', 'MULT', 'DIV', 'SPACE', 'PRINT', 'EOF'
var_list = []


class Token(object):
    def __init__(self, type, value):
        # token type like INTEGER, VARIABLE etc are taken
        self.type = type
        # token value can be 0,1,2...'+','-'...' '... a variable etc
        self.value = value

    def __str__(self):
        # will return token in String format like Token(Variable,'x')
        return 'Token({type},{value})'.format(
            type=self.type,
            value=repr(self.value)
        )

    def __repr__(self):
        return self.__str__()


class Variable(Token):
    # inherits the attributes of Token and is a separate class because also has a stored value
    def __init__(self, type, value, st_val):
        self.__stored_val = st_val
        self.type = type
        self.value = value

    # as mentioned earlier this will format the Variable tokens in string format
    def __str__(self):
        return 'Variable({type},{value},{stored_val})'.format(
            type=self.type,
            value=repr(self.value),
            stored_val=self.__stored_val
        )

    def __repr__(self):
        return self.__str__()

    # enabling encapsulation
    # setter for variable stored value
    def __set__stored__val(self, st_val):
        self.__stored_val = st_val
        # getter for variable value

    def __get__stored__val(self):
        return self.__stored_val


class Interpreter(object):
    def __init__(self, text):
        # input statement like 'x=3+5'
        self.text = text
        # self.pos maintains the index positions of the input
        self.pos = 0
        # current instance of token
        self.current_token = None

    def error(self):
        raise Exception('Error parsing input')

    def get_next_token(self):
        '''
        this method acts a lexical analyzer and it verifies the sentence by breaking it into individual tokens.
        :return:
        '''
        text = self.text
        # checking if the index has reached the end of the input
        if self.pos > len(text) - 1:
            return Token(EOF, None)
        # extracting character at the given position to decide what token is to be formed
        current_char = text[self.pos]

        # converting digit to integer to assist with mathematial operations
        # then the next character of the input is pointed at and the position pointer is inceremented
        # the Integer token is returned as well
        if current_char.isdigit():
            token = Token(INTEGER, int(current_char))
            self.pos += 1
            return token

        print_dictionary = {0: 'p',
                            1: 'r',
                            2: 'i',
                            3: 'n',
                            4: 't'}

        if current_char == 'p':
            i = 1
            flag = 0
            while True:
                self.pos += 1
                current_char = text[self.pos]
                if current_char == print_dictionary[i]:
                    i += 1
                    if current_char == 't':
                        break
                else:
                    flag = 1
                    break

            if flag == 1:
                self.error()
            token = Token(PRINT, 'print')
            self.pos += 1
            return token

        # checking for a variable Token
        if current_char.isalpha():
            token = Token(VAR, current_char)
            self.pos += 1
            return token

        # checking for =, space and arithmetic operators and returning the appropriate token

        if current_char == '=':
            token = Token(EQUAL, current_char)
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
        # error handling
        self.error()

    def eat(self, token_type):
        # comparing the passed token with the current token
        # if it matches the token is consumed and the next token is assigned to the current token
        # otherwise there is an error
        if self.current_token.type == token_type:
            self.current_token = self.get_next_token()
        elif self.token_type == PRINT:
            self.current_token = self.get_next_token()
        else:
            self.error()

    def expr(self, c):
        self.current_token = self.get_next_token()
        # first token is set as the current token
        first = self.current_token

        if first.value == 'print':

            self.eat(PRINT)
            first = self.current_token
            while first.value == ' ':
                self.eat(SPACE)
                first = self.current_token

            # checking if the first value is just an integer
            # then we proceed to solve the expression
            if isinstance(first.value, int):

                left = first
                self.eat(INTEGER)
                # this loop enables the integers to have multiple digits
                while self.current_token.type == INTEGER:
                    left.type = self.current_token.type
                    left.value = left.value * 10 + self.current_token.value
                    self.eat(INTEGER)

                op = self.current_token
                # checking if there is only one integer after print and no operator
                if op.type == EOF:
                    print(left.value)
                    return left.value
                # this loop enables the expression to contain n number of numbers in the expression
                while True:
                    # checking for spaces in between operands and operators
                    while op.value == ' ':
                        self.eat(SPACE)
                        op = self.current_token
                    # understanding the type of calculation that will happen between left and right based on the token
                    if op.value == '+':
                        self.eat(PLUS)
                    elif op.value == '-':
                        self.eat(MINUS)
                    elif op.value == '*':
                        self.eat(MULT)
                    elif op.value == '/':
                        self.eat(DIV)
                    # now we work with the operand on the right side of the operator
                    right = self.current_token
                    # checking for space otherwise the integer is utilised
                    while right.value == ' ':
                        self.eat(SPACE)
                        right = self.current_token

                    self.eat(INTEGER)
                    # enables the use of multiple digit integers on the right side of the operator
                    while self.current_token.type == INTEGER:
                        right.type = self.current_token.type
                        right.value = right.value * 10 + self.current_token.value
                        self.eat(INTEGER)
                    # performong the calculation
                    if op.value == '+':
                        result = left.value + right.value
                    elif op.value == '-':
                        result = left.value - right.value
                    elif op.value == '*':
                        result = left.value * right.value
                    elif op.value == '/':
                        result = left.value / right.value
                    # final value is stored in left to enable multi operator calculations
                    left.value = result

                    op = self.current_token
                    # if the next token indicates EOF we terminate
                    if op.type == EOF:
                        break
                    else:
                        left.value = result

                print(left.value)

                return left.value

            else:

                left = first

                while left.value == ' ':
                    self.eat(SPACE)
                    left = self.current_token
                if isinstance(left.value, int):
                    self.eat(INTEGER)
                else:
                    for i in range(0, 100):
                        col_1 = var_list[i][0]
                        col_2 = var_list[i][1]
                        if left.value == col_1:
                            left = Token(INTEGER, int(col_2))
                            self.eat(VAR)
                            break

                while self.current_token.type == INTEGER:
                    left.type = self.current_token.type
                    left.value = left.value * 10 + self.current_token.value
                    self.eat(INTEGER)
                op = self.current_token
                # checking if there is only one variable after print and no operator
                if op.type == EOF:
                    print(left.value)
                    return left.value

                while True:

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
                    else:
                        result = left.value
                        var_list.insert(c, [first.value, result])

                        return result

                    right = self.current_token

                    while right.value == ' ':
                        self.eat(SPACE)
                        right = self.current_token

                    if isinstance(right.value, int):
                        self.eat(INTEGER)
                    else:
                        for i in range(0, 100):
                            col_1 = var_list[i][0]
                            col_2 = var_list[i][1]
                            if right.value == col_1:
                                right = Token(INTEGER, int(col_2))
                                self.eat(VAR)
                                break

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

                    left.value = result

                    op = self.current_token
                    if op.type == EOF:
                        break
                    else:
                        left.value = result

                # now we create a variable object with its identifier and value
                var_list.insert(c, [first.value, result])

                print(result)

                return result

        # now checking for a variable as the starting token
        else:
            # we initialise the variable token with a 0 value
            first = Variable(VAR, first.value, 0)
            self.eat(VAR)
            next = self.current_token
            # we check for spaces like the previous case
            # otherwise we utilise the assignment operator
            while next.value == ' ':
                self.eat(SPACE)
                next = self.current_token

            self.eat(EQUAL)
            # Now like in the previous case of just integers we calculate the assignment value
            left = self.current_token

            while left.value == ' ':
                self.eat(SPACE)
                left = self.current_token
            if isinstance(left.value, int):
                self.eat(INTEGER)
            else:
                for i in range(0, 100):
                    col_1 = var_list[i][0]
                    col_2 = var_list[i][1]
                    if left.value == col_1:
                        left = Token(INTEGER, int(col_2))
                        self.eat(VAR)
                        break

            while self.current_token.type == INTEGER:
                left.type = self.current_token.type
                left.value = left.value * 10 + self.current_token.value
                self.eat(INTEGER)

            op = self.current_token

            while True:

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
                else:
                    result = left.value
                    var_list.insert(c, [first.value, result])

                    return result

                right = self.current_token

                while right.value == ' ':
                    self.eat(SPACE)
                    right = self.current_token

                if isinstance(right.value, int):
                    self.eat(INTEGER)
                else:
                    for i in range(0, 100):
                        col_1 = var_list[i][0]
                        col_2 = var_list[i][1]
                        if right.value == col_1:
                            right = Token(INTEGER, int(col_2))
                            self.eat(VAR)
                            break

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

                left.value = result

                op = self.current_token
                if op.type == EOF:
                    break
                else:
                    left.value = result

            # now we create a variable object with its identifier and value
            var_list.insert(c, [first.value, result])

            return result


def main():
    # main function that regulates the entire interpreter
    c = 0
    while True:
        try:

            text = input('lang> ')
        except EOFError:
            break
        if not text:
            continue
        interpreter = Interpreter(text)

        result = interpreter.expr(c)
        c += 1


if __name__ == '__main__':
    main()
