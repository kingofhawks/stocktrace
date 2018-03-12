import React, { Component } from 'react';
import logo from './logo.svg';
import './App.css';
import BasicExample from './Router'


class App extends Component {
  render() {
      var code = '000101';
    return (
      <div className="App">
        <header className="App-header">
          <img src={logo} className="App-logo" alt="logo" />
          <h1 className="App-title">Welcome to React</h1>
        </header>
        <p className="App-intro">
          To get started, edit <code>src/App.js</code> and save it to reload.
        </p>
        <BasicExample/>
      </div>
    );
  }
}

export default App;
