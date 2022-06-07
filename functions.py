#def nameOfFunction(param):
#    your code
#    return

def addition(num1, num2, num3):
    return num1 + num2 + num3

def division(num1, num2):
    if num2 == 0:
        return "Error: cannot divide by zero"
    else:
        return num1/num2

var1 = 10
var2 = 13
var3 = 352

result = addition(var1, var2, var3)
print ("Result of addition:", result)

result = division(var3, var2)
print("result of division:", result)


def Descending_Order(num):
    s = str(num)
    s = list(s)
    s = sorted(s)
   # s = reversed(s)
    s = ''.join(s)
    return int(s)

result = Descending_Order(4324523412)
print(result)

def Descending_Order1(num):
    return int("".join(sorted(str(num), reverse=True)))

result1 = Descending_Order1(4324523412)
print(result1)

def descending_order2(num):
    a = str(num)  # convert number to string
    b = sorted(a, reverse=True)  # sort the string with reverse=True; idk if there's any other way to sort numbers
    c = "".join(b)  # join the sorted string
    d = int(c)  # convert string into integer
    return d  # return the value

print(descending_order2(41234824593))

def converter(mpg):
  L_PER_G = 4.54609188 # L
  KM_PER_MI = 1.609344 # km
  return round(mpg * KM_PER_MI / L_PER_G, 2)

result_conv = converter(500)
print("Kilometros:", result_conv)
