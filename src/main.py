import json
from datetime import datetime

def format_card(card_number):
    if card_number:
        parts = card_number.split()
        if len(parts) >= 2:
            card_type = parts[0]
            last_four = parts[-1][-4:]
            masked_middle = '** '
            return f"{card_type} {masked_middle}**** {last_four}"
        else:
            return f"{card_number} ** **** "
    else:
        return "** **** "



def format_account(account_number):
    """Маскирует номер счета"""
    if account_number is None:
        return '** ****'
    elif not account_number.isdigit():
        return '** ****'
    else:
        return '** ' + account_number[-4:].zfill(4)



def get_last_five_executed_operations(things):
    executed_ops = [op for op in things if op.get('state') == 'EXECUTED']
    executed_ops.sort(key=lambda x: x['date'], reverse=True)
    return executed_ops[:5]

def print_operations(things):
    """Выводит информацию об операциях на экран"""
    for operation in things:
        date = datetime.strptime(operation['date'], '%Y-%m-%dT%H:%M:%S.%f').strftime('%d.%m.%Y')
        description = operation['description']
        amount = operation['operationAmount']['amount']
        currency = operation['operationAmount']['currency']['name']

        if 'from' in operation:
            from_info = operation['from'].split()
            from_card = format_card(' '.join(from_info))
        else:
            from_card = ''

        to_info = operation['to'].split()
        to_account = format_account(to_info[-1])

        print(f"{date} {description}")
        print(f"{from_card} -> {to_account}")
        print(f"{amount} {currency}")
        print()

if __name__ == "__main__":
    with open('operations.json', 'r', encoding='utf-8') as file:
        operations = json.load(file)

    last_five_operations = get_last_five_executed_operations(operations)
    print_operations(last_five_operations)