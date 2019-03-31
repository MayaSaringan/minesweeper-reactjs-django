


function Square(props) {
  var temp=""
  let className ="square "
  if (props.value==null){
    className +="inactive "
  }else {
    className +="active "
    if (props.value==1000){
      temp="💣"
      className+="bomb"
    }else if (props.value!=0) temp = props.value
  }
  return (
    <button className={className} onClick={props.onClick} onContextMenu={props.onContextMenu}>
      {temp}
    </button>
  );
}

class Board extends React.Component {
  constructor(props) {
    super(props)
    this.state={
      id:null,
      size:0,
      squares:Array(0),
      ongoing:true,
    }

    fetch("/"+this.props.value +"/")
         .then(res=>res.json())
         .then(
           (result) => {
             this.setState({
               id:result['id'],
               size:result['size'],
               squares:result['board'].slice(),
             })

             console.log("board square")
             console.log(this.state.squares)
             //this.render()
           }
         )

  }

  handleLoss(){
    //fetch all bomb locs
    alert("Game over")
    const squares = this.state.squares.slice();
    console.log("/"+this.state.id+"/lost/")
    fetch("/"+this.state.id+"/lost/")
       .then(res=>res.json())
       .then(
         (result) => {
           console.log(result)
           result.forEach((coords)=>{
             squares[coords.y][coords.x] = 1000

           })

           this.setState({squares: squares,ongoing:false});




         }
       )

  }
  handleExpand(x,y){
    const squares = this.state.squares.slice();
    //squares[x][y] = 1;
    //get(( val for square at x and y from server api
    //for each neighbour of This
    if (x-1>=0) this.handleClick(x-1,y)
    if (x-1>=0 && y-1>=0) this.handleClick(x-1,y-1)
    if (x-1>=0 && y+1<this.state.size) this.handleClick(x-1,y+1)
    if (y-1>=0) this.handleClick(x,y-1)
    if (x+1<this.state.size) this.handleClick(x+1,y)
    if (x+1<this.state.size && y-1>=0) this.handleClick(x+1,y-1)
    if (x+1<this.state.size && y+1>=0) this.handleClick(x+1,y+1)
    if (y+1>=0) this.handleClick(x,y+1)
    /*
    fetch("/"+this.state.id+"/expand/square?x="+x+"&y="+y+"")
       .then(res=>res.json())
       .then(
         (result) => {
           console.log(result)
           result.forEach((coords)=>{
             squares[coords.y][coords.x] = coords.value

           })
           this.setState({squares: squares});




         }
       )*/

  }

  handleClick(x,y) {

     const squares = this.state.squares.slice();
     //squares[x][y] = 1;
     //get(( val for square at x and y from server api
     if (this.state.squares[y][x]!=null) return
     fetch("/"+this.state.id+"/square?x="+x+"&y="+y+"")
        .then(res=>res.json())
        .then(
          (result) => {
            //check if loss
            //if (result.value=null ) return
            if (result.value==1000) this.handleLoss();
            else if(result.value==0){
              squares[y][x] = result.value

              this.setState({squares: squares});
              this.handleExpand(x,y);

            }else{
              squares[y][x] = result.value

              this.setState({squares: squares});
            }



          }
        )

   }
  handleRightClick(e,x,y){
    e.preventDefault();
    const squares = this.state.squares.slice();
    //squares[x][y] = 1;
    //get(( val for square at x and y from server api
    if (this.state.squares[y][x]!=null) return
    fetch("/"+this.state.id+"/square?x="+x+"&y="+y+"")
       .then(res=>res.json())
       .then(
         (result) => {
           //check if loss
           //if (result.value=null ) return
           if (result.value==1000) this.defuseBomb();
           else if(result.value==0){
             squares[y][x] = result.value

             this.setState({squares: squares});
             this.handleExpand(x,y);

           }else{
             squares[y][x] = result.value

             this.setState({squares: squares});
           }



         }
       )
  }
  renderSquare(x,y) {
  //  console.log(x+" "+y+"="+this.state.squares[x][y])
    return(
      <Square
        value={this.state.squares[y][x]}
        onClick={() => this.handleClick(x,y)}
        onContextMenu={(e)=>this.handleRightClick(e,x,y)}
        key = {x+"-"+y}
      />
    );
  }
  render() {
    const rows = [];
    console.log(this.state.squares)
    this.state.squares.forEach((item,x)=> {
      //console.log("row");
      const cols = []
      this.state.squares[x].forEach((item,y)=>
        cols.push( this.renderSquare(x,y))
      )
      rows.push(
        <div className = "board-row" key = {"row-"+x}>
          {cols}
        </div>
      )
    })
    return (
      <div>
        {rows}
      </div>
    );
  }
}


class Game extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      id: this.props.value
    };
  }
  render() {
    return (
      <div className="game">
        <div className="game-board">
          <Board value={this.state.id}/>
        </div>
        <a href="/"><div  className = "gameChoice">Back</div></a>
      </div>
    );
  }
}

// ========================================

ReactDOM.render(
  <Game value={id} />,
  document.getElementById('root')
);
