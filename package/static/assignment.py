age= input('How Old Are You?')
party= input('Your Political Party ')
if age.isdigit():
    formated_age= int(age)
    if age >='70' or party.upper()=='APC':
        print('You Can Win If You Contest')
    else:
        print('You Cannot Win..Do Not Contest')
else:
    print('You Need To Supply Age In Number')

