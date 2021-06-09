import json
import os
from time import time
from web3 import Web3


class Handler1:
    def __init__(self):
        self.contract_abi_path = "D:\\gr1_backend\\bagri_sdk\\build\\bagri.json"
        self.sender_address = '0x818eB70dCb5B7d1598eFA15d7aC16cB1009c690a'
        self.sender_private_key = '2e62f4062e1869654fa14b747898462230bf79ac506a4f16e8b84162c553fef6'
        self.contract_abi = json.load(open(self.contract_abi_path, "r"))['abi']
        self.endpoint = 'https://ropsten.infura.io/v3/e7031702228348699215c2d112be103b'
        self.web3 = Web3(Web3.HTTPProvider(self.endpoint))
        self.contract_address = '0xd27b8e5Dffa5034cB3C8C2c682DC0cAE63E14613'
        self.contract = self.web3.eth.contract(address=self.contract_address, abi=self.contract_abi)
    def getVerifySmartcontract(self, address):
        data = self.contract.functions.getBagri(address).call()
        return data
    def getCount(self, address, id):
        data = self.contract.functions.getCount(address, id).call()
        return data
    def getCountCustom(self, address):
        data = self.contract.functions.getCountCustom(address).call()
        return data
    def getDataCustom(self, address, id):
        data = self.contract.functions.getDataCustom(address, id).call()
        return data
    def getKeyQrCode(self, address):
        data = self.contract.functions.getKeyQrCode(address).call()
        return data
    def getQrCode(self, address, key):
        data = self.contract.functions.getQrCode(address, key).call()
        return data

    def set_QrCode(self, action_name, description, _keyQrcode, timeNow):
        nonce = self.web3.eth.getTransactionCount(self.sender_address)
        success = False
        while not success:
            try:
                _Qrcode = {'action_name':action_name, 'description':description, 'keyQrcode':_keyQrcode, 'timeNow':timeNow}
                tx_dict = self.contract.functions.setQrcode(_Qrcode)\
                    .buildTransaction({
                        'from': self.sender_address,
                        'gas': 800000,
                        'gasPrice': self.web3.toWei('200', 'gwei'),
                        'nonce': nonce,
                        'chainId': 3
                    })
                signed_tx = self.web3.eth.account.signTransaction(tx_dict, self.sender_private_key)
                tx_hash = self.web3.eth.sendRawTransaction(signed_tx.rawTransaction)
                success = True
            except Exception as ex:
                nonce += 1
        return (self.web3.toHex(tx_hash))