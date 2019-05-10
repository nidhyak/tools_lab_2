import React from 'react';
import web3 from './web3';
import lottereum from './lottereum';

class App extends React.Component {
  constructor(props){
    super(props);
    this.state = {
      gameIDs: '',
      gameCount: '',
      currentDeposit: '',
      gameLength: '',
      isActive: '',
      ownerCut: '',
      gameID: '',
      betValue: '',
      userInput: '',
      winner: '',
      winnings: ''
    };
  };

  componentDidMount() {
    this.updateState();
    setInterval(this.updateState.bind(this), 1000);
  };

  //async updateState() {
  updateState() {
    console.log("UPDATING STATE");
    lottereum.methods.showGameCount().call().then(res => this.setState({gameCount: parseInt(res)})).catch(err => console.log(err));
    lottereum.methods.gameIDs(this.state.gameCount-1).call().then(res => this.setState({gameIDs: parseInt(res)})).catch(err => console.log(err));
    lottereum.methods.currentDeposit().call().then(res => this.setState({currentDeposit: parseInt(res)})).catch(err => console.log(err));
    lottereum.methods.gameLength().call().then(res => this.setState({gameLength: parseInt(res)})).catch(err => console.log(err));
    lottereum.methods.isActive().call().then(res => this.setState({isActive: res})).catch(err => console.log(err));
    lottereum.methods.ownerCut().call().then(res => this.setState({ownerCut: parseInt(res)})).catch(err => console.log(err));
    /*
    lottereum.methods.gameIDs(0).call((err, result) => {
      if (result != null){
        this.setState({gameIDs: parseInt(result)});
      } else {
        console.log(err);
      }
    });
    lottereum.methods.showGameCount().call((err, result) => {
      if (result != null){
        this.setState({gameCount: parseInt(result)});
      } else {
        console.log(err);
      }
    });
    lottereum.methods.currentDeposit().call((err, result) => {
      if (result != null){
        this.setState({currentDeposit: parseInt(result)});
      } else {
        console.log(err);
      }
    });
    lottereum.methods.gameLength().call((err, result) => {
      if (result != null){
        this.setState({gameLength: parseInt(result)});
      } else {
        console.log(err);
      }
    });
    lottereum.methods.isActive().call((err, result) => {
      if (result != null){
        this.setState({isActive: result});
      } else {
        console.log(err);
      }
    });
    lottereum.methods.ownerCut().call((err, result) => {
      if (result != null){
        this.setState({ownerCut: parseInt(result)});
      } else {
        console.log(err);
      }
    });
    */
    //const accounts = await web3.eth.getAccounts();
    //const gameIDs = await lottereum.methods.gameIDs(0).call(
    //  {from: accounts[0], gas: 4000000}, (error, result) => {
    //    console.log("error: " + error);
    //    console.log("result: " + result);
    //  }
    //);
    //const gameIDs = await lottereum.methods.gameIDs(0).call();
    //const gameCount = await lottereum.methods.showGameCount().call();
    //const currentDeposit = await lottereum.methods.currentDeposit().call();
    //const gameLength = await lottereum.methods.gameLength().call();
    //const isActive = await lottereum.methods.isActive().call();
    //const ownerCut = await lottereum.methods.ownerCut().call();
    //this.setState({
    //  gameIDs, gameCount, currentDeposit, gameLength, isActive, ownerCut
    //});
    //lottereum.methods.gameIDs((err, result) => {
    //  console.log(result);
    //  if (result != null){
    //    this.setState({gameIds: parseInt(result)});
    //  }
    //});
    //lottereum.methods.showGameCount((err, result) => {
    //  console.log(result);
    //  if (result != null){
    //    this.setState({gameCount: parseInt(result)});
    //  }
    //});
    //lottereum.methods.currentDeposit((err, result) => {
    //  if (result != null){
    //    this.setState({currentDeposit: parseInt(result)});
    //  }
    //});
    //lottereum.methods.gameLength().call((err, result) => {
    //  if (result != null){
    //    this.setState({gameLength: parseInt(result)});
    //  }
    //});
    //lottereum.methods.isActive((err, result) => {
    //  if (result != null){
    //    this.setState({isActive: result});
    //  }
    //});
    //lottereum.methods.ownerCut((err, result) => {
    //  if (result != null){
    //    this.setState({ownerCut: parseInt(result)});
    //  }
    //});
  };

  onStartGameSubmit = async (event) => {
    event.preventDefault();
    const accounts = await web3.eth.getAccounts();
    await lottereum.methods.startGame().send({
      from: accounts[0],
      gas: 4000000
    });
  }

  onBuyTicketSubmit = async (event) => {
    event.preventDefault();
    const accounts = await web3.eth.getAccounts();
    const bytesInput = web3.utils.fromAscii(this.state.userInput);
    console.log(bytesInput);
    await lottereum.methods.buyTicket(
      this.state.gameID,
      bytesInput
    ).send({
      from: accounts[0],
      value: this.state.betValue,
      gas: 4000000
    });
  }

  onResolveGameSubmit = async (event) => {
    event.preventDefault();
    const accounts = await web3.eth.getAccounts();
    const bytesInput = web3.utils.fromAscii(this.state.userInput);
    await lottereum.methods.resolveGame(
      this.state.gameID,
      bytesInput
    ).send({
      from: accounts[0],
      gas: 4000000
    });
  }

  onGetPayoutSubmit = async (event) => {
    event.preventDefault();
    const accounts = await web3.eth.getAccounts();
    await lottereum.methods.getPayout(this.state.gameID).send({
      from: accounts[0],
      gas: 4000000
    });
    let logWinner = lottereum.methods.LogWinner();
    logWinner.watch(this.setState({winner: logWinner._address, winnings: logWinner._winnings}));
    //lottereum.methods.logWinner().call().then(res => this.setState({winner: res._address, winnings: res._winnings})).catch(err => console.log(err));
  }

  render() {
    return (
      <div>
        <h2>Lottereum</h2>
        <p>Latest Game ID: {this.state.gameIDs}</p>
        <p>Running Games: {this.state.gameCount}</p>
        <p>Current Honesty Deposit: {this.state.currentDeposit}</p>
        <p>Game Length: {this.state.gameLength} seconds</p>
        <p>Lottery Active: {this.state.isActive}</p>
        <p>Owner&rsquo;s Cut: {this.state.ownerCut}&#37;</p>
        <hr />
        <div>
          <p>Winner: {this.state.winner}</p>
          <p>Winnings: {this.state.winnings}</p>
        </div>
        <hr />
        <div>
          <p>Game ID: {this.state.gameID}</p>
          <p>Bet: {this.state.betValue}</p>
          <p>Secret: {this.state.userInput}</p>
        </div>
        <div>
          <div>
            <label>Game ID</label>
            <input placeholder="0123456789" value={this.state.gameID} onChange={event=>this.setState({gameID: event.target.value})} />
          </div>
          <div>
            <label>Bet</label>
            <input placeholder={this.state.currentDeposit} value={this.state.betValue} onChange={event=>this.setState({betValue: event.target.value})} />
          </div>
          <div>
            <label>Secret Bytes</label>
            <input placeholder="0xdeadbeef" value={this.state.userInput} onChange={event=>this.setState({userInput: event.target.value})} />
          </div>
        </div>
        <div>
          <button onClick={this.onStartGameSubmit}>Start Game</button>
          <button onClick={this.onBuyTicketSubmit}>Buy Ticket</button>
          <button onClick={this.onResolveGameSubmit}>Resolve Game</button>
          <button onClick={this.onGetPayoutSubmit}>Get Payout</button>
        </div>
      </div>
    );
  }
};

export default App;

