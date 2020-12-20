import 'semantic-ui-less/semantic.less';
import React, { Component } from "react";
import { HashRouter, Route } from "react-router-dom";

import Header from "./components/header";
import Home from "./components/home";
import Lovers from "./components/lovers";
import Producers from "./components/producers";

function App() {
  return (
    <HashRouter>
      <Header />
      <Route exact path="/" component={Home} />
      <Route path="/lovers" component={Lovers} />
      <Route path="/producers" component={Producers} />
    </HashRouter>
  );
}

export default App;
