import redis, time

r = redis.Redis()

r.set("cle","valeur",ex=3)
print(r.exists("cle"))
time.sleep(1)
print(r.exists("cle"))
print(r.exists('clee'))
time.sleep(3)
print(r.exists('cle'))
print(r.get('cle'))