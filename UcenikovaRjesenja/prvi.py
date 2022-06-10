#zad2

n=int(input())
m=int(input())
a=set()
b=set()
for i in range(1,n+1):
    if n%i==0:
        a|={i}
for j in range(1,m+1):
    if m%j==0:
        b|={j}
presjek=a&b
print(max(presjek))




    
