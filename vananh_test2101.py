a = {
	"key1" : "a",
	"key2" : "b"
}
b = {
	"key3" : "c",
	"key4" : "d"
}
for k,v in a.items():
	b[k] = v
'''
for k,v in b.items():
	print(k,"--",v)
'''
c = {**b,**a}
c["key5"] = "e"
for k,v in c.items():
	print(k,"*******",v)
