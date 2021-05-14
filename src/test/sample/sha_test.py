import mitum.hash.sha as sha

targets = [b'Hello, world!', b'TARGET1', b'TARGET2']

for tar in targets:
    print(sha.sha256(tar))