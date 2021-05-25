import json

import base58
from mitumc.common import (Hint, Int, bconcat, getNewToken, iso8601TimeStamp,
                          parseAddress, parseISOtoUTC)
from mitumc.constant import THRESHOLDS, VERSION
from mitumc.hash import sha
from mitumc.hint import (BTC_PRIVKEY, ETHER_PRIVKEY, MC_ADDRESS, MC_AMOUNT,
                        MC_CREATE_ACCOUNTS_OP, MC_CREATE_ACCOUNTS_OP_FACT,
                        MC_CREATE_ACCOUNTS_SINGLE_AMOUNT, MC_KEY, MC_KEYS,
                        MC_KEYUPDATER_OP, MC_KEYUPDATER_OP_FACT,
                        MC_TRANSFERS_OP, MC_TRANSFERS_OP_FACT,
                        MC_TRNASFERS_ITEM_SINGLE_AMOUNT, SEAL, STELLAR_PRIVKEY)
from mitumc.key.base import Key, Keys, KeysBody, to_basekey
from mitumc.key.btc import to_btc_keypair
from mitumc.key.ether import to_ether_keypair
from mitumc.key.stellar import to_stellar_keypair
from mitumc.operation.base import Address, Amount, Memo
from mitumc.operation.create_accounts import (CreateAccounts,
                                             CreateAccountsBody,
                                             CreateAccountsFact,
                                             CreateAccountsFactBody,
                                             CreateAccountsItem)
from mitumc.operation.key_updater import (KeyUpdater, KeyUpdaterBody,
                                         KeyUpdaterFact, KeyUpdaterFactBody)
from mitumc.operation.transfers import (Transfers, TransfersBody, TransfersFact,
                                       TransfersFactBody, TransfersItem)


def to_keys(ks):

    key_list = list()
    for key, w in ks:
        t, k = parseAddress(key)
        key_list.append(
            Key(
                Hint(MC_KEY, VERSION),
                to_basekey(t, k),
                Int(w),
            )
        )
    
    keys_body = KeysBody(
        Hint(MC_KEYS, VERSION),
        Int(THRESHOLDS),
        key_list,
    )

    keys = Keys(
        keys_body.generate_hash(),
        keys_body,
    )

    return keys


def generate_create_accounts(net_id, pk, sender, amt, ks):
    
    keys = to_keys(ks)
    
    big, cid = amt
    amounts = list()
    amounts.append(
        Amount(
            Hint(MC_AMOUNT, VERSION),
            Int(big),
            cid,
        )
    )

    item = CreateAccountsItem(
        Hint(MC_CREATE_ACCOUNTS_SINGLE_AMOUNT, VERSION),
        keys,
        amounts,
    )
    item_list = list()
    item_list.append(item)

    h_sender, k_sender = parseAddress(sender)

    fact_body = CreateAccountsFactBody(
        Hint(MC_CREATE_ACCOUNTS_OP_FACT, VERSION),
        iso8601TimeStamp(),
        Address(
            Hint(h_sender, VERSION),
            k_sender,
        ),
        item_list,
    )

    fact = CreateAccountsFact(
        fact_body.generate_hash(),
        fact_body,
    )


    fact_sign = fact.newFactSign(net_id, pk)
    fact_sign_list = list()
    fact_sign_list.append(fact_sign)

    op_body = CreateAccountsBody(
        Memo(""),
        Hint(MC_CREATE_ACCOUNTS_OP, VERSION),
        fact,
        fact_sign_list,
    )

    op = CreateAccounts(
        op_body.generate_hash(),
        op_body,
    )

    return op


def generate_key_updater(net_id, pk, target, new_pubk, weight, cid):
    keys = to_keys([(new_pubk, weight)])

    _, k_target = parseAddress(target)

    fact_body = KeyUpdaterFactBody(
        Hint(MC_KEYUPDATER_OP_FACT, VERSION),
        iso8601TimeStamp(),
        Address(
            Hint(MC_ADDRESS, VERSION),
            k_target,
        ),
        cid,
        keys,
    )

    fact = KeyUpdaterFact(
        fact_body.generate_hash(),
        fact_body,
    )

    fact_sign = fact.newFactSign(net_id, pk)

    fact_sign_list = list()
    fact_sign_list.append(fact_sign)
    op_body = KeyUpdaterBody(
        Memo(""),
        Hint(MC_KEYUPDATER_OP, VERSION),
        fact,
        fact_sign_list,
    )

    op = KeyUpdater(
        op_body.generate_hash(),
        op_body,
    )

    return op


def generate_transfers(net_id, pk, sender, receiver, amt):
    
    big, cid = amt
    amounts = list()
    amounts.append(
        Amount(
            Hint(MC_AMOUNT, VERSION),
            Int(big),
            cid,
        )
    )

    h_receiver, k_receiver = parseAddress(receiver)
    item = TransfersItem(
        Hint(MC_TRNASFERS_ITEM_SINGLE_AMOUNT, VERSION),
        Address(
            Hint(h_receiver, VERSION),
            k_receiver,
        ),
        amounts,
    )
    item_list = list()
    item_list.append(item)

    h_sender, k_sender = parseAddress(sender)
    fact_body = TransfersFactBody(
        Hint(MC_TRANSFERS_OP_FACT, VERSION),
        iso8601TimeStamp(),
        Address(
            Hint(h_sender, VERSION),
            k_sender,
        ),
        item_list,
    )

    fact = TransfersFact(
        fact_body.generate_hash(),
        fact_body,
    )

    fact_sign = fact.newFactSign(net_id, pk)
    fact_sign_list = list()
    fact_sign_list.append(fact_sign)

    op_body = TransfersBody(
        Memo(""),
        Hint(MC_TRANSFERS_OP, VERSION),
        fact,
        fact_sign_list,
    )

    op = Transfers(
        op_body.generate_hash(),
        op_body,
    )

    return op

def generate_seal(file_name, net_id, pk, opers):
    type, key = parseAddress(pk)

    if type == BTC_PRIVKEY:
        kp = to_btc_keypair(key)
    elif type == ETHER_PRIVKEY:
        kp = to_ether_keypair(key)
    elif type == STELLAR_PRIVKEY:
        kp = to_stellar_keypair(key)

    signed_at = iso8601TimeStamp()
    bsigned_at = parseISOtoUTC(signed_at).encode()

    bsigner = kp.public_key.hinted().encode()

    bopers = bytearray()
    for op in opers:
        bopers += op.hash().digest

    body_hash = sha.sum256(bconcat(bsigner, bsigned_at, bopers))

    signature = kp.sign(bconcat(body_hash.digest, net_id.encode()))

    hash = sha.sum256(bconcat(body_hash.digest, signature))

    seal = {}
    seal['_hint'] = Hint(SEAL, VERSION).hint
    seal['hash'] = hash.hash
    seal['body_hash'] = body_hash.hash
    seal['signer'] = kp.public_key.hinted()
    seal['signature'] = base58.b58encode(signature).decode()
    seal['signed_at'] = getNewToken(signed_at)

    operations = list()
    for op in opers:
        operations.append(op.to_dict())
    seal['operations'] = operations

    with open(file_name, "w") as fp:
            json.dump(seal, fp)