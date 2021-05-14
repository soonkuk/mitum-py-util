# CreateAccontsFact hashing test
print("-" * 10 + "<CreateAccountsFact Hashing Test>" + "-" * 10)
exec(open('./test/hash/ca_fact.py').read())

# KeyUpdaterFact hashing test
print('\n')
print("-" * 10 + "<KeyUpdaterFact Hashing Test>" + "-" * 10)
exec(open('./test/hash/ku_fact.py').read())

# TransfersFact hashing test
print('\n')
print("-" * 10 + "<TransfersFact Hashing Test>" + "-" * 10)
exec(open('./test/hash/tf_fact.py').read())