
class Boolean_model():
    
    
    @staticmethod
    def tokenize(query):
        return [token.lower() for token in query.lower().split()]
    @staticmethod
    def infix_to_postfix(tokens):
        output = []
        operator_stack = []
    
        for token in tokens:
            if token.isalnum() and token not in ("and","not","or") :  # Operand
                # output.append(int(token))
                output.append(token)
            
            else:  # Operator
                while operator_stack and Boolean_model.operator_precedence(operator_stack[-1]) >= Boolean_model.operator_precedence(token):
                    output.append(operator_stack.pop())
                operator_stack.append(token)
    
        while operator_stack:
            output.append(operator_stack.pop())
    
        return output
    @staticmethod
    def operator_precedence(operator):
        precedence = {'not': 3, 'and': 2, 'or': 1}
        return precedence.get(operator, 0)
    
    @staticmethod# 0 or 1 and 0 not
    def evaluate(query):
        
        postfix_expression = Boolean_model.infix_to_postfix(Boolean_model.tokenize(query))
        
        operand_stack = []
    
        for token in postfix_expression:
            if token.isalnum() and token not in ("and","not","or"):  # Operand
                operand_stack.append(token)
            else:  # Operator
                if token == 'not':
                    if operand_stack:
                        operand = operand_stack.pop()
                        result = Boolean_model.perform_not(operand)
                        operand_stack.append(result)
                    else:
                        raise ValueError("Invalid expression: Missing operand for NOT")
                else:  # AND or OR
                    if len(operand_stack) >= 2:
                        operand2 = operand_stack.pop()
                        operand1 = operand_stack.pop()
                        result = Boolean_model.perform_operation(operand1, operand2, token)
                        operand_stack.append(result)
                    else:
                        raise ValueError(f"Invalid expression: Not enough operands for {token}")
    
        if len(operand_stack) != 1:
            raise ValueError("Invalid expression: Too many operands")
    
        return operand_stack[0]

    @staticmethod
    def perform_not(operand):
        # Implement NOT operation
        return int(not int(operand))
    @staticmethod
    def perform_operation(operand1, operand2, operator):
        # Implement AND or OR operation
        
        return int(int(operand1) or int(operand2)) if operator=="or" else int(int(operand1) and int(operand2))


if __name__ =="__main__":
    
    # print(perform_operation(1,0,"and",1))
    # print(perform_not(1,1))
    tokens = Boolean_model.tokenize("0 or 1 and 0 not")
    # tokens = tokenize("1 or 0 and 0")
    
    # pile = infix_to_postfix(tokens)
    # print(pile)
    # print(Boolean_model.evaluate("not 1 or 0 and not 0"))
    print(Boolean_model.evaluate("not 1 or 0 and not 0"))
    