def is_valid_cpf(cpf):
    cpf = cpf.replace('.', '').replace('-', '')
    if len(cpf) != 11 or cpf == cpf[0] * 11:
        return False
    sum1 = 0
    for i in range(9):
        sum1 += int(cpf[i]) * (10 - i)
    rest1 = (sum1 * 10) % 11
    if rest1 == 10 or rest1 == 11:
        rest1 = 0
    if rest1 != int(cpf[9]):
        return False
    sum2 = 0
    for i in range(10):
        sum2 += int(cpf[i]) * (11 - i)
    rest2 = (sum2 * 10) % 11
    if rest2 == 10 or rest2 == 11:
        rest2 = 0
    if rest2 != int(cpf[10]):
        return False
    return True
