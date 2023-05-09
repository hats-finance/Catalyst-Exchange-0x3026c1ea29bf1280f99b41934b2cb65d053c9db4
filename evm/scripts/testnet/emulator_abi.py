abi = [
    {
        'inputs': [
            {
                'internalType': "bytes32",
                'name': "localChannelId",
                'type': "bytes32"
            }
        ],
        'name': "constructor",
        'stateMutability': "nonpayable",
        'type': "constructor"
    },
    {
        'anonymous': False,
        'inputs': [
            {
                'indexed': False,
                'internalType': "bytes",
                'name': "acknowledgement",
                'type': "bytes"
            }
        ],
        'name': "Acknowledgement",
        'type': "event"
    },
    {
        'anonymous': False,
        'inputs': [
            {
                'indexed': True,
                'internalType': "address",
                'name': "previousOwner",
                'type': "address"
            },
            {
                'indexed': True,
                'internalType': "address",
                'name': "newOwner",
                'type': "address"
            }
        ],
        'name': "OwnershipTransferred",
        'type': "event"
    },
    {
        'anonymous': False,
        'inputs': [
            {
                'components': [
                    {
                        'components': [
                            {
                                'internalType': "bytes32",
                                'name': "portId",
                                'type': "bytes32"
                            },
                            {
                                'internalType': "bytes32",
                                'name': "channelId",
                                'type': "bytes32"
                            }
                        ],
                        'internalType': "struct IbcEndpoint",
                        'name': "src",
                        'type': "tuple"
                    },
                    {
                        'components': [
                            {
                                'internalType': "bytes32",
                                'name': "portId",
                                'type': "bytes32"
                            },
                            {
                                'internalType': "bytes32",
                                'name': "channelId",
                                'type': "bytes32"
                            }
                        ],
                        'internalType': "struct IbcEndpoint",
                        'name': "dest",
                        'type': "tuple"
                    },
                    {
                        'internalType': "uint64",
                        'name': "sequence",
                        'type': "uint64"
                    },
                    {
                        'internalType': "bytes",
                        'name': "data",
                        'type': "bytes"
                    },
                    {
                        'components': [
                            {
                                'internalType': "uint64",
                                'name': "block",
                                'type': "uint64"
                            },
                            {
                                'internalType': "uint64",
                                'name': "timestamp",
                                'type': "uint64"
                            }
                        ],
                        'internalType': "struct IbcTimeout",
                        'name': "timeout",
                        'type': "tuple"
                    }
                ],
                'indexed': False,
                'internalType': "struct IbcPacket",
                'name': "packet",
                'type': "tuple"
            }
        ],
        'name': "Packet",
        'type': "event"
    },
    {
        'inputs': [],
        'name': "LOCALCHANNELID",
        'outputs': [
            {
                'internalType': "bytes32",
                'name': "",
                'type': "bytes32"
            }
        ],
        'stateMutability': "view",
        'type': "function"
    },
    {
        'inputs': [
            {
                'internalType': "address",
                'name': "targetContract",
                'type': "address"
            },
            {
                'internalType': "bytes",
                'name': "acknowledgement",
                'type': "bytes"
            },
            {
                'components': [
                    {
                        'components': [
                            {
                                'internalType': "bytes32",
                                'name': "portId",
                                'type': "bytes32"
                            },
                            {
                                'internalType': "bytes32",
                                'name': "channelId",
                                'type': "bytes32"
                            }
                        ],
                        'internalType': "struct IbcEndpoint",
                        'name': "src",
                        'type': "tuple"
                    },
                    {
                        'components': [
                            {
                                'internalType': "bytes32",
                                'name': "portId",
                                'type': "bytes32"
                            },
                            {
                                'internalType': "bytes32",
                                'name': "channelId",
                                'type': "bytes32"
                            }
                        ],
                        'internalType': "struct IbcEndpoint",
                        'name': "dest",
                        'type': "tuple"
                    },
                    {
                        'internalType': "uint64",
                        'name': "sequence",
                        'type': "uint64"
                    },
                    {
                        'internalType': "bytes",
                        'name': "data",
                        'type': "bytes"
                    },
                    {
                        'components': [
                            {
                                'internalType': "uint64",
                                'name': "block",
                                'type': "uint64"
                            },
                            {
                                'internalType': "uint64",
                                'name': "timestamp",
                                'type': "uint64"
                            }
                        ],
                        'internalType': "struct IbcTimeout",
                        'name': "timeout",
                        'type': "tuple"
                    }
                ],
                'internalType': "struct IbcPacket",
                'name': "packet",
                'type': "tuple"
            }
        ],
        'name': "ack",
        'outputs': [],
        'stateMutability': "nonpayable",
        'type': "function"
    },
    {
        'inputs': [
            {
                'internalType': "address",
                'name': "targetContract",
                'type': "address"
            },
            {
                'components': [
                    {
                        'components': [
                            {
                                'internalType': "bytes32",
                                'name': "portId",
                                'type': "bytes32"
                            },
                            {
                                'internalType': "bytes32",
                                'name': "channelId",
                                'type': "bytes32"
                            }
                        ],
                        'internalType': "struct IbcEndpoint",
                        'name': "src",
                        'type': "tuple"
                    },
                    {
                        'components': [
                            {
                                'internalType': "bytes32",
                                'name': "portId",
                                'type': "bytes32"
                            },
                            {
                                'internalType': "bytes32",
                                'name': "channelId",
                                'type': "bytes32"
                            }
                        ],
                        'internalType': "struct IbcEndpoint",
                        'name': "dest",
                        'type': "tuple"
                    },
                    {
                        'internalType': "uint64",
                        'name': "sequence",
                        'type': "uint64"
                    },
                    {
                        'internalType': "bytes",
                        'name': "data",
                        'type': "bytes"
                    },
                    {
                        'components': [
                            {
                                'internalType': "uint64",
                                'name': "block",
                                'type': "uint64"
                            },
                            {
                                'internalType': "uint64",
                                'name': "timestamp",
                                'type': "uint64"
                            }
                        ],
                        'internalType': "struct IbcTimeout",
                        'name': "timeout",
                        'type': "tuple"
                    }
                ],
                'internalType': "struct IbcPacket",
                'name': "packet",
                'type': "tuple"
            }
        ],
        'name': "execute",
        'outputs': [],
        'stateMutability': "nonpayable",
        'type': "function"
    },
    {
        'inputs': [],
        'name': "owner",
        'outputs': [
            {
                'internalType': "address",
                'name': "",
                'type': "address"
            }
        ],
        'stateMutability': "view",
        'type': "function"
    },
    {
        'inputs': [],
        'name': "registerPort",
        'outputs': [],
        'stateMutability': "nonpayable",
        'type': "function"
    },
    {
        'inputs': [],
        'name': "renounceOwnership",
        'outputs': [],
        'stateMutability': "nonpayable",
        'type': "function"
    },
    {
        'inputs': [
            {
                'internalType': "bytes32",
                'name': "channelId",
                'type': "bytes32"
            },
            {
                'internalType': "bytes",
                'name': "payload",
                'type': "bytes"
            },
            {
                'internalType': "uint64",
                'name': "timeoutBlockHeight",
                'type': "uint64"
            }
        ],
        'name': "sendIbcPacket",
        'outputs': [],
        'stateMutability': "nonpayable",
        'type': "function"
    },
    {
        'inputs': [
            {
                'internalType': "address",
                'name': "targetContract",
                'type': "address"
            },
            {
                'components': [
                    {
                        'components': [
                            {
                                'internalType': "bytes32",
                                'name': "portId",
                                'type': "bytes32"
                            },
                            {
                                'internalType': "bytes32",
                                'name': "channelId",
                                'type': "bytes32"
                            }
                        ],
                        'internalType': "struct IbcEndpoint",
                        'name': "src",
                        'type': "tuple"
                    },
                    {
                        'components': [
                            {
                                'internalType': "bytes32",
                                'name': "portId",
                                'type': "bytes32"
                            },
                            {
                                'internalType': "bytes32",
                                'name': "channelId",
                                'type': "bytes32"
                            }
                        ],
                        'internalType': "struct IbcEndpoint",
                        'name': "dest",
                        'type': "tuple"
                    },
                    {
                        'internalType': "uint64",
                        'name': "sequence",
                        'type': "uint64"
                    },
                    {
                        'internalType': "bytes",
                        'name': "data",
                        'type': "bytes"
                    },
                    {
                        'components': [
                            {
                                'internalType': "uint64",
                                'name': "block",
                                'type': "uint64"
                            },
                            {
                                'internalType': "uint64",
                                'name': "timestamp",
                                'type': "uint64"
                            }
                        ],
                        'internalType': "struct IbcTimeout",
                        'name': "timeout",
                        'type': "tuple"
                    }
                ],
                'internalType': "struct IbcPacket",
                'name': "packet",
                'type': "tuple"
            }
        ],
        'name': "timeout",
        'outputs': [],
        'stateMutability': "nonpayable",
        'type': "function"
    },
    {
        'inputs': [
            {
                'internalType': "address",
                'name': "newOwner",
                'type': "address"
            }
        ],
        'name': "transferOwnership",
        'outputs': [],
        'stateMutability': "nonpayable",
        'type': "function"
    }
]