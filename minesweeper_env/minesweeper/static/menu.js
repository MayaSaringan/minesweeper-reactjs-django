
class Menu extends React.Component{

  render(){
    return(


      <div className="menu">
        <h1>Welcome</h1>   
        <a href="/create/" >
          <div  className = "gameChoice">New Game</div>
        </a>
      </div>
    )
  }
}

ReactDOM.render(
  <Menu/>,
  document.getElementById('menu')
);
