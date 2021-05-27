# mitum-py-util

'mitum-py-util' will introduce the usage of mitum-currency for python.

## Installation

Recommended requirements for 'mitum-py-util' are,

* python v3.9 or later.
* rlp v2.0.1
* base58 v2.1.0
* pybase64 v1.1.4
* ecdsa v0.13.3
* bitcoinaddress v0.1.5
* bitcoin-utils v0.4.11
* eth_keys v0.3.3
* stellar_sdk v3.3.2
* pytz v2021.1
* datetime v4.3

```
$ python --version
Python 3.9.2

$ git clone https://github.com/ProtoconNet/mitum-py-util.git

$ cd mitum-py-util

$ python setup.py install
```

## Generate New Operation

### Operations

'mitum-py-util' provides three operations to be generated,

* Create-Accounts
    Create an account corresponding to any public key with a pre-registered account.
* Key-Updater
    Update the public key of the account to something else.
* Transfers
    Transfer tokens from the account to another account.

'mitum-currency' supports various kinds of operations, but 'mitum-py-util' will provide these frequently used operations.

### Prerequisite

Before generating new operation, you should check below,

* 'private key' of source account to generate signatures (a.k.a signing key)
* 'public address' of source account
* 'public key' of target account
* 'network id'

Notice that the package name of 'mitum-py-util' is 'mitumc' for python codes.

### Generate Create-Accounts 

To generate an operation, 'currency id' and 'initial amount' must be set. With source account, you can create and register new account of target public key.

#### Usage

```
generate_create_accounts(network_id, source_private_key, source_address, amount, target_keys)
```

* 'amount' must be 2-length tuple in (big, currency id) format.
* 'target_keys' must be a list of 2-length tuple in (target_public_key, weight) format.

#### Example

```
>>> from mitumc.operation import generate_create_accounts

>>> source_private_key = "L1oTaxcPztdqAU7ZzrHMWLnX2iUm6MhMW3RxT5YByiEpceDbUhPE-0112:0.0.1"
>>> source_address = "8AwAwFAaboopKDH7Nriq9Sq2eb2xjThMBFtWWCt3iebG-a000:0.0.1"
>>> target_public_key = "27LZo3wxW5T9VH5Da1La9bCSg1VfnaKtNvb3Gmg115N6X-0113:0.0.1"

>>> network_id = "mitum"

>>> amount = (100, "MCC")

>>> target_key = (target_public_key, 100)
>>> target_keys = list()
>>> target_keys.append(target_key)

>>> createAccounts = generate_create_accounts(network_id, source_private_key, source_address, amount, targets)
```

You can create json file of the operation by to_json(file_name) method.

```
>>> createAccounts.to_json("create_account.json")
```

Then the result will be,

```
{
    "memo": "",
    "_hint": "a006:0.0.1",
    "fact": {
        "_hint": "a005:0.0.1",
        "hash": "HQHU6HN9yKLpq29Wg2EcM4Lft9qzAXTMQWu9tJLGjXkA",
        "token": "MjAyMS0wNS0yN1QwMjozNzoxNy44NTc2MjgrMDA6MDA=",
        "sender": "8AwAwFAaboopKDH7Nriq9Sq2eb2xjThMBFtWWCt3iebG-a000:0.0.1",
        "items": [
            {
                "_hint": "a025:0.0.1",
                "keys": {
                    "_hint": "a004:0.0.1",
                    "hash": "CHmkPR6GqTZfxrs1ptoWupsgvzkgvNdE7ZzhvimGUErg",
                    "keys": [
                        {
                            "_hint": "a003:0.0.1",
                            "weight": 100,
                            "key": "27LZo3wxW5T9VH5Da1La9bCSg1VfnaKtNvb3Gmg115N6X-0113:0.0.1"
                        }
                    ],
                    "threshold": 100
                },
                "amounts": [
                    {
                        "_hint": "a022:0.0.1",
                        "amount": "100",
                        "currency": "MCC"
                    }
                ]
            }
        ]
    },
    "hash": "EW8fuvRoHmXpKCuXCU5gc1kR12baZSRdXYPYkkomAd2W",
    "fact_signs": [
        {
            "_hint": "0150:0.0.1",
            "signer": "sMs6R5BF9EsVcGV6enuwVZ4hv4H4y48RNy2yPJg6F6RH-0113:0.0.1",
            "signature": "381yXZW8oWYsqkwriNG2zPZKSc7nUAnYQytMaJi8uzk6EwD4KU5d4t3pkf7hjZjJyLskeyKhyCwVpfLfDtJUYzGtxuVry1Gy",
            "signed_at": "2021-05-27T02:37:18.620253Z"
        }
    ]
}
```

### Generate Key-Updater

Key-Updater literally supports to update cource public key to something else.

#### Usage

```
generate_key_updater(network_id, source_private_key, source_address, target_public_key, weight, currency_id)
```

* Every arguments must be single instance. (not tuple, list or somethine else...)

#### Example

```
>>> from mitumc.operation import generate_key_updater

>>> source_private_key = "L1oTaxcPztdqAU7ZzrHMWLnX2iUm6MhMW3RxT5YByiEpceDbUhPE-0112:0.0.1"
>>> source_address = "8AwAwFAaboopKDH7Nriq9Sq2eb2xjThMBFtWWCt3iebG-a000:0.0.1"
>>> target_public_key = "27LZo3wxW5T9VH5Da1La9bCSg1VfnaKtNvb3Gmg115N6X-0113:0.0.1"

>>> network_id = "mitum"

>>> keyUpdater = generate_key_updater(network_id, source_private_key, source_address, target_public_key, 100, "MCC")
>>> keyUpdater.to_json("key_updater.json")
```

### Generate Transfers

To generate an operation, you must prepare target address, not public key. Transfers supports to send tokens to another account.

#### Usage

```
generate_transfers(network_id, source_private_key, source_address, target_address, amount)
```

* 'amount' must be 2-length tuple in (big, currency id) format.

#### Example

```
>>> from mitumc.operation import generate_transfers

>>> source_private_key = "L1oTaxcPztdqAU7ZzrHMWLnX2iUm6MhMW3RxT5YByiEpceDbUhPE-0112:0.0.1"
>>> source_address = "8AwAwFAaboopKDH7Nriq9Sq2eb2xjThMBFtWWCt3iebG-a000:0.0.1"
>>> target_address = "CHmkPR6GqTZfxrs1ptoWupsgvzkgvNdE7ZzhvimGUErg-a000:0.0.1"

>>> network_id = "mitum"

>>> amount = (100, "MCC")

>>> transfers = generate_transfers(network_id, source_private_key, source_address, target_address, amount)
>>> transfers.to_json("transfers.json")
``

## Generate New Seal

Supports you to generate a seal json file such that the seal is able to consist of several operations. Those operations can be any type 'mitum-py-util' provides.

### Prerequisite

To generate a seal, 'mitum-py-util' requires,

* 'signing key'
* 'a list of pre-constructed operations' not empty

Registration of 'signing key' is not neccessary.

### Usage

```
generate_seal(file_name, network_id, signing_key, operations)
```

* 'signing key' must be a private key of 'mitum-currency' kepair.
* Every elements of operations list must be pre-constructed by 'generate_create_accounts', 'generate_key_updater', or 'generate_transfers'

### Example

```
>>> from mitumc.operation import generate_seal, generate_create_accounts, generate_key_updater, generate_transfers

>>> source_prv = "L5GTSKkRs9NPsXwYgACZdodNUJqCAWjz2BccuR4cAgxJumEZWjok-0112:0.0.1"
>>> source_addr = "8PdeEpvqfyL3uZFHRZG5PS3JngYUzFFUGPvCg29C2dBn-a000:0.0.1"

>>> ac1_prv = "SBGISVULOQA6BPEYF4OS2JGMBST7HYCBSL3TA2QRVGRNBMVWIZVE6336-0110:0.0.1"
>>> ac1_pub = "GBYLIBJYZP6ZIYPFGOZSXSAPMRDA6XXRKNSMOMRCKNV2YZ35DGRPEQ35-0111:0.0.1"
>>> ac2_addr = "8dsqP9dUPKv3TjJg6DCKJ7NE7vsMx47Gc4VrseEcyXtt-a000:0.0.1"
>>> ac3_pub = "GCV6WZ5U7HXFOXWTMLUXCG4PW3KP2YYTMAPZDE3IIVWQY7Q6SYPG63TZ-0111:0.0.1"

>>> createAccounts = generate_create_accounts("mitum", source_prv, source_addr, (100, "MCC"), [(ac1_pub, 100)])
>>> keyUpdater = generate_key_updater("mitum", ac1_prv, ac1_addr, ac3_pub, 100, "MCC")
>>> transfers = generate_transfers("mitum", source_prv, source_addr, ac2_addr, (100, "MCC"))

>>> operations = [createAccounts, keyUpdater, transfers]
>>> network_id = "mitum"

>>> generate_seal("seal.json", network_id, source_prv, operations)
```

Then the result will be,

```
{
    "_hint": "0151:0.0.1",
    "hash": "6Rmp2NfB4bbqAXLYjaMmhA3WR7yLBVZRsUERvqY4BmHm",
    "body_hash": "9bdLGeBZq9VJzo2hqRTQvZgHHazZy38SeaJN6kHAN9dU",
    "signer": "rcrd3KA2wWNhKdAP8rHRzfRmgp91oR9mqopckyXRmCvG-0113:0.0.1",
    "signature": "AN1rKvtjRAmo6w1j5GfWiQcvQq3kDUC5nw6D7oFKtwUqbitGxy3eBTKDrJ7oMbPg11fd7mn2PKWQnYo3MPbNbNh8pPGF1WjCL",
    "signed_at": "2021-05-27T03:09:28.235041Z",
    "operations": [
        {
            "memo": "",
            "_hint": "a006:0.0.1",
            "fact": {
                "_hint": "a005:0.0.1",
                "hash": "7fAEFHFGNYZwhTGsnZnFfHDECvyMncTje1xViqe8tjNf",
                "token": "MjAyMS0wNS0yN1QwMzowOToyNi4xMDI1NDkrMDA6MDA=",
                "sender": "8PdeEpvqfyL3uZFHRZG5PS3JngYUzFFUGPvCg29C2dBn-a000:0.0.1",
                "items": [
                    {
                        "_hint": "a025:0.0.1",
                        "keys": {
                            "_hint": "a004:0.0.1",
                            "hash": "8HQt6CfBVgMhLmPxcataTF2CXHuw2Km32FAcW7FXmQZ3",
                            "keys": [
                                {
                                    "_hint": "a003:0.0.1",
                                    "weight": 100,
                                    "key": "GBYLIBJYZP6ZIYPFGOZSXSAPMRDA6XXRKNSMOMRCKNV2YZ35DGRPEQ35-0111:0.0.1"
                                }
                            ],
                            "threshold": 100
                        },
                        "amounts": [
                            {
                                "_hint": "a022:0.0.1",
                                "amount": "100",
                                "currency": "MCC"
                            }
                        ]
                    }
                ]
            },
            "hash": "5vJ8e7EgrHke3THBdDBbZycb92WnPjLgsLFaMPyGSHj9",
            "fact_signs": [
                {
                    "_hint": "0150:0.0.1",
                    "signer": "rcrd3KA2wWNhKdAP8rHRzfRmgp91oR9mqopckyXRmCvG-0113:0.0.1",
                    "signature": "AN1rKvtiNYxMz2wAx2Ep5mt1LBBYfANPjF3UasrcAEYVgiXFEhkFV5SUrbJFpj114B91MN1v6MEkPdrGSLf3PGLSpY54bJ515",
                    "signed_at": "2021-05-27T03:09:26.885598Z"
                }
            ]
        },
        {
            "memo": "",
            "_hint": "a010:0.0.1",
            "fact": {
                "_hint": "a009:0.0.1",
                "hash": "HV2RCKFemyqiwa9Zao9poroMJjy6Eki4hZv7NYwScM8E",
                "token": "MjAyMS0wNS0yN1QwMzowOToyNi44ODU1OTgrMDA6MDA=",
                "target": "8HQt6CfBVgMhLmPxcataTF2CXHuw2Km32FAcW7FXmQZ3-a000:0.0.1",
                "keys": {
                    "_hint": "a004:0.0.1",
                    "hash": "4ZSnntvo16Bfc7USqAdTiQQ3KwsM7TmMCWZigxSmTnut",
                    "keys": [
                        {
                            "_hint": "a003:0.0.1",
                            "weight": 100,
                            "key": "GCV6WZ5U7HXFOXWTMLUXCG4PW3KP2YYTMAPZDE3IIVWQY7Q6SYPG63TZ-0111:0.0.1"
                        }
                    ],
                    "threshold": 100
                },
                "currency": "MCC"
            },
            "hash": "3QCVBAAWSsy2U9U44SVzmBY1Rvb5FTW2BMHWQuKVLsiw",
            "fact_signs": [
                {
                    "_hint": "0150:0.0.1",
                    "signer": "GBYLIBJYZP6ZIYPFGOZSXSAPMRDA6XXRKNSMOMRCKNV2YZ35DGRPEQ35-0111:0.0.1",
                    "signature": "62z2QMLjBYwGy8nhd1kMSiFkjP1iXUd9jXcHSsXBU6RWvrxwfnG7fxz6gfFZc8YvtjMnATdhZFXFdxSHoGS3u6tc",
                    "signed_at": "2021-05-27T03:09:26.885598Z"
                }
            ]
        },
        {
            "memo": "",
            "_hint": "a002:0.0.1",
            "fact": {
                "_hint": "a001:0.0.1",
                "hash": "2hVtFF1MLHBYAR8jjc4hLfCn8vRYhFmNRNQoZZrQrUyf",
                "token": "MjAyMS0wNS0yN1QwMzowOToyNi44ODU1OTgrMDA6MDA=",
                "sender": "8PdeEpvqfyL3uZFHRZG5PS3JngYUzFFUGPvCg29C2dBn-a000:0.0.1",
                "items": [
                    {
                        "_hint": "a027:0.0.1",
                        "receiver": "8dsqP9dUPKv3TjJg6DCKJ7NE7vsMx47Gc4VrseEcyXtt-a000:0.0.1",
                        "amounts": [
                            {
                                "_hint": "a022:0.0.1",
                                "amount": "100",
                                "currency": "MCC"
                            }
                        ]
                    }
                ]
            },
            "fact_signs": [
                {
                    "_hint": "0150:0.0.1",
                    "signer": "rcrd3KA2wWNhKdAP8rHRzfRmgp91oR9mqopckyXRmCvG-0113:0.0.1",
                    "signature": "AN1rKvtZRPgcujuUDj62M862srjfFvxR57tbVbq4dFrGPGnrwoCwem3ZTJCuCLGVRCtJVz1Q4BWPSk5MpGg6G2jMu4HE9g8Q7",
                    "signed_at": "2021-05-27T03:09:27.643334Z"
                }
            ],
            "hash": "JAet6C6X7Towd7eq5jUXydZKCq3naVcmhVuDcoky7WA6"
        }
    ]
}
```

## Send Seal to Network

Created seal json files will be used to send seals by 'mitum-currency'.

Use below command to send them to the target network. (See 'mitum-currency' for details)

```
$ bin/mc seal send --network-id=$NETWORK_ID $SIGNING_KEY --seal=seal.json
```

* seal.json is your seal file.

## Hash Functions

'mitumc.hash' module supports sha2(sha256) and sha3(sum256) hashing.

#### Example

mitumc_hash.py
```
>>> from mitumc.hash import sha256, sum256

>>> msg = b'mitum'
>>> sha2_hash = sha256(msg)
>>> sha3_hash = sum256(msg)

>>> print(sha2_hash.digest)
>>> print(sha2_hash.hash)
>>> print(sha3_hash.digest)
>>>print(sha3_hash.hash)
```

The result will be,

```
$ python mitumc_hash.py
b'\xf7.\xd28\xfd\xc1+\xfc\x1d\xa9\xcdb9y\x8cF+RW4\x89)\x99\xcb\xdc\xf5\xbe\xf5\xa7J\xf2\x95'
Hdu7PqjA1p55GAcBiULmCAfzoksdwW1oSxaMH83kw9BJ
b'jf\x10J>\xb9O]\x14\xab}d,r\x88(B\xab\x9a\xb1x\x18\x04\xeb\x10!\x9f\xebY\xa5v"'
8ALUvxZ5Q1qQEsPUcHsoAzuzEp8Bm4HQpYqNNSafjDAR
```