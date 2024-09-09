import random
# Generating reg number
def createRegNo():
    alphabet_list = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
    reg_num = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    random_letters = random.choices(alphabet_list, k=3)
    random_numbers = random.choices(reg_num, k=5)
    random_string = ''.join(random_letters)
    random_number = ''.join(random_numbers)

    print(f"{random_string}{random_number}")


createRegNo()