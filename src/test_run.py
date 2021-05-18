print()

# CreateAccontsFact hashing test
print('\n')
print("-" * 20 + "< CreateAccountsFact Hashing Test >" + "-" * 20)
exec(open('./test/hash/ca_fact.py').read())

# CreateAccounts hashing test
print('\n')
print("-" * 20 + "< CreateAccounts     Hashing Test >" + "-" * 20)
exec(open('./test/hash/ca_hash.py').read())

# KeyUpdaterFact hashing test
print('\n')
print("-" * 20 + "< KeyUpdaterFact     Hashing Test >" + "-" * 20)
exec(open('./test/hash/ku_fact.py').read())

# TransfersFact hashing test
print('\n')
print("-" * 20 + "< TransfersFact      Hashing Test >" + "-" * 20)
exec(open('./test/hash/tf_fact.py').read())

# BTC sign test
print('\n')
print("-" * 20 + "< BTC                Sign    Test >" + "-" * 20)
exec(open('./test/sign/btc_test.py').read())

print('\n')