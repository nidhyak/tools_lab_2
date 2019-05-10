import web3 from './web3';

const address = '0x434255B9874d3b7FF43Db3ce9224f9Da9E02b220';
//const address = '0x6B2cea748e1eed428e5adc6c21d564ab9c75b2E1';
const abi = [
  {
    "constant": true,
    "inputs": [
      {
        "name": "",
        "type": "uint256"
      }
    ],
    "name": "gameIDs",
    "outputs": [
      {
        "name": "",
        "type": "uint256"
      }
    ],
    "payable": false,
    "stateMutability": "view",
    "type": "function"
  },
  {
    "constant": true,
    "inputs": [],
    "name": "isActive",
    "outputs": [
      {
        "name": "",
        "type": "bool"
      }
    ],
    "payable": false,
    "stateMutability": "view",
    "type": "function"
  },
  {
    "constant": true,
    "inputs": [],
    "name": "minDeposit",
    "outputs": [
      {
        "name": "",
        "type": "uint256"
      }
    ],
    "payable": false,
    "stateMutability": "view",
    "type": "function"
  },
  {
    "constant": true,
    "inputs": [],
    "name": "ownerCut",
    "outputs": [
      {
        "name": "",
        "type": "uint256"
      }
    ],
    "payable": false,
    "stateMutability": "view",
    "type": "function"
  },
  {
    "constant": true,
    "inputs": [],
    "name": "currentDeposit",
    "outputs": [
      {
        "name": "",
        "type": "uint256"
      }
    ],
    "payable": false,
    "stateMutability": "view",
    "type": "function"
  },
  {
    "constant": true,
    "inputs": [],
    "name": "depositChange",
    "outputs": [
      {
        "name": "",
        "type": "uint256"
      }
    ],
    "payable": false,
    "stateMutability": "view",
    "type": "function"
  },
  {
    "constant": true,
    "inputs": [],
    "name": "gameLength",
    "outputs": [
      {
        "name": "",
        "type": "uint256"
      }
    ],
    "payable": false,
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [
      {
        "name": "_ownerCut",
        "type": "uint256"
      },
      {
        "name": "_minDeposit",
        "type": "uint256"
      },
      {
        "name": "_currentDeposit",
        "type": "uint256"
      },
      {
        "name": "_depositChange",
        "type": "uint256"
      },
      {
        "name": "_gameLength",
        "type": "uint256"
      }
    ],
    "payable": false,
    "stateMutability": "nonpayable",
    "type": "constructor"
  },
  {
    "payable": true,
    "stateMutability": "payable",
    "type": "fallback"
  },
  {
    "anonymous": false,
    "inputs": [
      {
        "indexed": false,
        "name": "_owner",
        "type": "address"
      },
      {
        "indexed": false,
        "name": "_ownerCut",
        "type": "uint256"
      },
      {
        "indexed": false,
        "name": "_minDeposit",
        "type": "uint256"
      },
      {
        "indexed": false,
        "name": "_currentDeposit",
        "type": "uint256"
      },
      {
        "indexed": false,
        "name": "_depositChange",
        "type": "uint256"
      },
      {
        "indexed": false,
        "name": "_gameLength",
        "type": "uint256"
      }
    ],
    "name": "LogLottery",
    "type": "event"
  },
  {
    "anonymous": false,
    "inputs": [
      {
        "indexed": true,
        "name": "_gameID",
        "type": "uint256"
      },
      {
        "indexed": false,
        "name": "_deposit",
        "type": "uint256"
      },
      {
        "indexed": false,
        "name": "_endTime",
        "type": "uint256"
      },
      {
        "indexed": false,
        "name": "_resolveTime",
        "type": "uint256"
      }
    ],
    "name": "LogGame",
    "type": "event"
  },
  {
    "anonymous": false,
    "inputs": [
      {
        "indexed": false,
        "name": "_address",
        "type": "address"
      },
      {
        "indexed": false,
        "name": "_gameID",
        "type": "uint256"
      },
      {
        "indexed": false,
        "name": "_bet",
        "type": "uint256"
      },
      {
        "indexed": false,
        "name": "_time",
        "type": "uint256"
      }
    ],
    "name": "LogTicket",
    "type": "event"
  },
  {
    "anonymous": false,
    "inputs": [
      {
        "indexed": true,
        "name": "_address",
        "type": "address"
      },
      {
        "indexed": true,
        "name": "_gameID",
        "type": "uint256"
      },
      {
        "indexed": false,
        "name": "_userInput",
        "type": "bytes32"
      }
    ],
    "name": "LogResolve",
    "type": "event"
  },
  {
    "anonymous": false,
    "inputs": [
      {
        "indexed": true,
        "name": "_address",
        "type": "address"
      },
      {
        "indexed": true,
        "name": "_gameID",
        "type": "uint256"
      },
      {
        "indexed": false,
        "name": "_winnings",
        "type": "uint256"
      },
      {
        "indexed": false,
        "name": "_time",
        "type": "uint256"
      }
    ],
    "name": "LogWinner",
    "type": "event"
  },
  {
    "constant": false,
    "inputs": [],
    "name": "startGame",
    "outputs": [],
    "payable": false,
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "constant": false,
    "inputs": [
      {
        "name": "_gameID",
        "type": "uint256"
      },
      {
        "name": "_userInput",
        "type": "bytes32"
      }
    ],
    "name": "buyTicket",
    "outputs": [],
    "payable": true,
    "stateMutability": "payable",
    "type": "function"
  },
  {
    "constant": false,
    "inputs": [
      {
        "name": "_gameID",
        "type": "uint256"
      },
      {
        "name": "_userInput",
        "type": "bytes32"
      }
    ],
    "name": "resolveGame",
    "outputs": [],
    "payable": false,
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "constant": false,
    "inputs": [
      {
        "name": "_gameID",
        "type": "uint256"
      }
    ],
    "name": "getPayout",
    "outputs": [],
    "payable": false,
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "constant": true,
    "inputs": [],
    "name": "showGameCount",
    "outputs": [
      {
        "name": "",
        "type": "uint256"
      }
    ],
    "payable": false,
    "stateMutability": "view",
    "type": "function"
  },
  {
    "constant": false,
    "inputs": [],
    "name": "toggleActive",
    "outputs": [],
    "payable": false,
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "constant": false,
    "inputs": [],
    "name": "kill",
    "outputs": [],
    "payable": false,
    "stateMutability": "nonpayable",
    "type": "function"
  }
];

export default new web3.eth.Contract(abi, address);

