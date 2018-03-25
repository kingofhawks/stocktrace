import React, { Component } from 'react';
import logo from './logo.svg';
import './App.css';
import BasicExample from './Router'


class App extends Component {
  render() {
    return (
      <div className="App">
        <header className="App-header">
          <img src={logo} className="App-logo" alt="logo" />
          <h1 className="App-title">Welcome to Value</h1>
        </header>
        <p className="App-intro">
          Value on the road...
        </p>
        <BasicExample/>
      </div>
    );
  }
}

export default App;
