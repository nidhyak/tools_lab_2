pragma solidity >=0.5.0 <0.6.0;

contract Lottereum {

    address payable owner;                      // owner of lottery
    uint256 public ownerCut;                    // owner's cut in percent
    uint256 public minDeposit;                  // min honesty deposit (wei)
    uint256 public currentDeposit;              // honesty deposit (wei)
    uint256 public depositChange;               // honesty deposit flux (wei)
    uint256 public gameLength;                  // length of game (e.g. 1 hour)
    bool public isActive = true;                // active lottery
    uint256[] public gameIDs;                   // list of gameIDs
    mapping(uint256 => uint256) gameIDIndex;    // gameID => index
    mapping(uint256 => Game) games;             // gameID => game

    struct Game {
        uint256 jackpot;                        // collected bets
        uint256 deposit;                        // current deposit rate
        uint256 depositPot;                     // collected deposits
        uint256 playerCount;                    // total players
        uint256 endTime;                        // start time + gameLength
        uint256 resolveTime;                    // endTime + gameLength
        bool isActive;                          // lottery status
        mapping(address => Ticket) entries;     // player => ticket
        address payable[] honestPlayers;        // list of honestPlayers
        bytes32[] userInputs;                   // list of reveals
        bytes32 combinedInput;                  // combined input randomization
        address payable winner;                 // winner
    }
    
    struct Ticket {
        uint256 bet;                            // input amount - deposit
        bytes32 inputHash;                      // hash of player input
        uint256 timestamp;                      // time of entry
    }

    event LogLottery(
        address _owner,
        uint256 _ownerCut,
        uint256 _minDeposit,
        uint256 _currentDeposit,
        uint256 _depositChange,
        uint256 _gameLength
    );

    event LogGame(
        uint256 indexed _gameID,
        uint256 _deposit,
        uint256 _endTime,
        uint256 _resolveTime
    );

    event LogTicket(
        address _address,
        uint256 _gameID,
        uint256 _bet,
        uint256 _time
    );

    event LogResolve(
        address indexed _address,
        uint256 indexed _gameID,
        bytes32 _userInput
    );

    event LogWinner(
        address indexed _address,
        uint256 indexed _gameID,
        uint256 _winnings,
        uint256 _time
    );

    constructor (
        uint256 _ownerCut,
        uint256 _minDeposit,
        uint256 _currentDeposit,
        uint256 _depositChange,
        uint256 _gameLength
    ) 
        public 
    {
        require(_ownerCut < 100, "Owner's cut must be less than 100");
        require(_gameLength >= 1 minutes, "Game length must be >= 60");
        owner = msg.sender;
        ownerCut = _ownerCut;
        minDeposit = _minDeposit;
        currentDeposit = _currentDeposit;
        depositChange = _depositChange;
        gameLength = _gameLength;
        emit LogLottery(
            owner,
            ownerCut,
            minDeposit,
            currentDeposit,
            depositChange,
            gameLength
        );
    }

    modifier ownerOnly() {
        require(msg.sender == owner, "Only the lottery owner can use this");
        _;
    }

    modifier activeOnly() {
        require(isActive, "The lottery must be active");
        _;
    }

    /* Phase 1 - Collect bets from buyTicket() calls */
    function startGame() public activeOnly {
        uint256 gameID = now;
        Game storage game = games[gameID];
        gameIDIndex[gameID] = gameIDs.length;
        gameIDs.push(gameID);
        game.isActive = true;
        game.deposit = currentDeposit;
        game.endTime = gameID + gameLength;
        game.resolveTime = game.endTime + gameLength;
        emit LogGame(gameID, game.deposit, game.endTime, game.resolveTime);
    }

    function buyTicket(uint256 _gameID, bytes32 _userInput) public payable {
        Game storage game = games[_gameID];
        // close game if exceed endTime on buyTicket attempt
        if (game.endTime < now) { game.isActive = false; }
        // only allow buyTicket if game is active
        require(game.isActive, "Buy-in period is over");
        // check if bet exceeds deposit amount
        require(msg.value > game.deposit, "Bet amount must exceed deposit");
        uint256 bet = msg.value - game.deposit;
        game.depositPot += game.deposit;
        game.jackpot += bet;
        game.playerCount++;
        // hash _userInput
        game.entries[msg.sender] = Ticket(
            msg.value,
            keccak256(abi.encode(_userInput)),
            now
        );
        emit LogTicket(msg.sender, _gameID, bet, now);
    }

    /* Phase 2 - Collect initial userInputs for honesty check */
    function resolveGame (uint256 _gameID, bytes32 _userInput) public { 
        Game storage game = games[_gameID];
        // close game if exceed endTime on resolveGame attempt
        if (game.endTime < now) { game.isActive = false; }
        // only allow resolving if game is closed
        require(!game.isActive, "Buy-in period is not over yet");
        // only allow resolving if within resolution period
        require(game.resolveTime > now, "Game resolution period is over");
        // hash _userInput
        bytes32 inputHash = keccak256(abi.encode(_userInput));
        // check for honest player
        if (inputHash == game.entries[msg.sender].inputHash) {
            // use _userInput in "randomizer"
            game.combinedInput = mergeHash(game.combinedInput, _userInput);
            // track _userInputs
            game.userInputs.push(_userInput);
            // add honest player to list
            game.honestPlayers.push(msg.sender);
            emit LogResolve(msg.sender, _gameID, _userInput);
        }
    }

    /* Phase 3 - Select winner, distribute refunds, send payout */
    function getPayout(uint256 _gameID) public {
        Game storage game = games[_gameID];
        // only allow payout if game has resolved
        require(game.resolveTime < now, "Game resolution is not over yet");
        // handle payout once by finding a winner
        if (game.winner == address(0)) {
            // increase honesty deposit if game has dishonest players
            if (game.honestPlayers.length < game.playerCount) {
                currentDeposit += depositChange;
            } else if (game.playerCount > 0) {
                // decrease deposit if all players are honest
                if (currentDeposit > minDeposit) {
                    currentDeposit -= depositChange;
                }
            }
            if (game.honestPlayers.length == 0) {
                // deposit and jackpot go to owner if no honest players
                owner.transfer(game.depositPot);
                owner.transfer(game.jackpot);
            } else {
                // distribute deposit
                uint256 share = game.depositPot / game.honestPlayers.length;
                for (uint256 i = 0; i < game.honestPlayers.length; i++) {
                    game.honestPlayers[i].transfer(share);
                    game.depositPot -= share;
                }
                // remainder of deposit goes to owner
                owner.transfer(game.depositPot);
                /* Choose winner */
                // (combinedInput MOD jackpot) + 1 to get random value within
                // jackpot range
                uint256 combinedRandom = (
                    (uint256(game.combinedInput) % game.jackpot) + 1
                );
                //start summing bets until exceeds MOD
                // need to loop until hits user.. otherwise with dishonestplayer affecting sum
                uint256 idx = 0;
                uint256 betSum = 0;
                // don't stop until winner is found as dishonest player will
                // affect sum of jackpot
                while (game.winner == address(0)) {
                    // loop index
                    idx = idx % game.honestPlayers.length;
                    // sum the bet by each player
                    betSum += game.entries[game.honestPlayers[idx]].bet;
                    // winner chosen when sum of bets exceed combinedRandom
                    if (betSum >= combinedRandom) {
                        game.winner = game.honestPlayers[idx];
                    }
                    idx++;
                }
                // pay owner
                uint256 cut = (game.jackpot * ownerCut) / 100;
                owner.transfer(cut);
                game.jackpot -= cut;
                // pay winner
                game.winner.transfer(game.jackpot);
                emit LogWinner(game.winner, _gameID, game.jackpot, now);
            }
            closeGame(_gameID);
        }
    }

    function closeGame(uint256 _gameID) internal {
        // find index of _gameID in gameIDs
        uint256 index = gameIDIndex[_gameID];
        if (gameIDs.length > 1) {
            // update index of tail gameID
            gameIDIndex[gameIDs[gameIDs.length-1]] = index;
            // copy tail of gameIDs to replace index
            gameIDs[index] = gameIDs[gameIDs.length-1];
        }
        // shorten tail and cleanup for gas refund
        gameIDs.length--;
        delete gameIDIndex[_gameID];
        delete games[_gameID];
    }

    function mergeHash(bytes32 b1, bytes32 b2) internal pure returns (bytes32){
        bytes memory merged = new bytes(64);
        uint256 idx = 0;
        // zip the inputs
        for (uint256 i = 0; i < 32; i++) {
            merged[idx] = b1[i];
            idx++;
            merged[idx] = b2[i];
            idx++;
        }
        // hash the merged inputs
        return keccak256(merged);
    }

    function() external payable {}

    function showGameCount() public view returns (uint256) {
        return gameIDs.length;
    }

    function toggleActive() public ownerOnly {
        isActive = !isActive;
    }

    function kill() public ownerOnly {
        selfdestruct(owner);
    }
}
