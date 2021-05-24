from mitum.common import Hint, Int, getNewToken, parseAddress
from mitum.constant import THRESHOLDS, VERSION
from mitum.hint import (MC_ADDRESS, MC_AMOUNT, MC_CREATE_ACCOUNTS_OP,
                        MC_CREATE_ACCOUNTS_OP_FACT,
                        MC_CREATE_ACCOUNTS_SINGLE_AMOUNT, MC_KEY, MC_KEYS,
                        MC_KEYUPDATER_OP, MC_KEYUPDATER_OP_FACT,
                        MC_TRANSFERS_OP, MC_TRANSFERS_OP_FACT,
                        MC_TRNASFERS_ITEM_SINGLE_AMOUNT)
from mitum.key.base import Key, Keys, KeysBody, to_basekey
from mitum.operation.base import Address, Amount, Memo
from mitum.operation.create_accounts import (CreateAccounts,
                                             CreateAccountsBody,
                                             CreateAccountsFact,
                                             CreateAccountsFactBody,
                                             CreateAccountsItem)
from mitum.operation.key_updater import (KeyUpdater, KeyUpdaterBody,
                                         KeyUpdaterFact, KeyUpdaterFactBody)
from mitum.operation.transfers import (Transfers, TransfersBody, TransfersFact,
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
        getNewToken(),
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
        getNewToken(),
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
        getNewToken(),
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
