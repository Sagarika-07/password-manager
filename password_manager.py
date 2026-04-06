import random
import string
import sqlite3

conn=sqlite3.connect("passwords.db")
cur=conn.cursor()
cur.execute("create table if not exists store(site text,username text,password text)")
conn.commit()

def gen(length,use_special):
    if length<4:
        return "Length should be at least 4"
    chars=string.ascii_letters+string.digits
    if use_special:
        chars+=string.punctuation

    l=random.choice(string.ascii_lowercase)
    u=random.choice(string.ascii_uppercase)
    d=random.choice(string.digits)
    s=random.choice(string.punctuation) if use_special else random.choice(string.ascii_lowercase)

    rem=''.join(random.choice(chars) for _ in range(length-4))
    p=list(l+u+d+s+rem)
    random.shuffle(p)
    return ''.join(p)

def strength(p):
    s=0
    if any(c.islower() for c in p): s+=1
    if any(c.isupper() for c in p): s+=1
    if any(c.isdigit() for c in p): s+=1
    if any(c in string.punctuation for c in p): s+=1
    if s<=2: return "Weak"
    elif s==3: return "Medium"
    else: return "Strong"

def add():
    site=input("Site: ")
    user=input("Username: ")
    length=int(input("Length: "))
    use_special=input("Special (y/n): ")=="y"

    p=gen(length,use_special)
    print("Generated:",p)
    print("Strength:",strength(p))

    cur.execute("insert into store values(?,?,?)",(site,user,p))
    conn.commit()

def view():
    for r in cur.execute("select * from store"):
        print(r)

while True:
    print("1.Generate+Save 2.View 3.Exit")
    ch=input()

    if ch=="1":
        add()
    elif ch=="2":
        view()
    elif ch=="3":
        break

conn.close()