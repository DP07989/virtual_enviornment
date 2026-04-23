import random


numbers = [0,0,0,0,0]

dictionary = {
    1:"€",
    2:"ß",
    3:"Ø",
    4:"@",
    5:"*",
    6:"®",
    7:"7"

}

balance = 100
bonus = 2
money_spent = 0

has_won = False
spin_counter = 0
while has_won == False:
    print("Balance: "+str(balance) +"\n"+ "Bonus: "+str(bonus) +"\n" )
    #a = input("PRESS ENTER TO SPIN!")
    print("PRESS ENTER TO SPIN!")
    spin_counter = spin_counter+1
    
    for i,number in enumerate(numbers):
        numbers[i] = random.randrange(1,8)    

    result = [dictionary[num] for num in numbers]
    print(result)
    
    if all(n % 7 == 0 for n in numbers):
        print("!!!You won!!!")
        balance = balance + money_spent*bonus
        has_won = True
    else:
        print("You lost")
        balance = balance - 5
        money_spent = money_spent+5
        bonus = bonus*1.01    


print("Final Balance:"+str(balance))
print("Money Spent:"+str(money_spent))
print("Final Bonus:"+str(bonus))
print("Number of spins:"+str(spin_counter))
    
