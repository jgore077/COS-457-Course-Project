import React,{useEffect,useState} from 'react'
import Modal from '../Modal';
import * as AiIcons from "react-icons/ai";
import * as FaIcons from "react-icons/fa";
function Games(props) {
  const [gamesList,setGamesList]=useState([])
  console.log((props.decodedAuthToken.role && !props.sidebarState))
  useEffect(()=>{
    fetch('/games',{
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      }
    }).then((response)=>{
      response.json().then(function(data)
      {
        console.log(data)
      });
      }).catch(function(error){
        console.log(error)
      })
    .catch((error)=>{
        console.log(error)
    })
  },[])
  return (
    // condition?true:false
    <div class='center'>
    <Game role={props.decodedAuthToken.role}/>
    {(props.decodedAuthToken.role==='admin' && !props.sidebarState)?<div class='add-button-container'>
        <Modal trigger={<AiIcons.AiOutlinePlusSquare class='add-button' size={'2em'} />}/>
      </div>:undefined}
      
    </div>
  
  )
}


// If the user is an administrator then the game should be rendered with a x in the top right corner so that they can cancel it same goes for announcements
// their should also be a pencil to edit existing games
function Game(prop) {
   console.log(prop.role)
  return (
    <div><Incrementer/></div>
  )
}



export function Incrementer() {
  const [homeCount, setHomeCount] = useState(0); // useState returns a pair. 'count' is the current state. 'setCount' is a function we can use to update the state.
  const [awayCount,setAwayCount]  = useState(0)
  



  return (
    <div class='scale'>
      <button onClick={() => {
        setHomeCount(function (prevCount) {
          if (prevCount == 25) {
            return 25;
          }
          return (prevCount += 1);
        });
      }}>+</button>
      {homeCount}
      <button onClick={() => {
        setHomeCount(function (prevCount) {
          if (prevCount > 0) {
            return (prevCount -= 1);
          } else {
            return (prevCount = 0);
          }
        });
      }}>-</button>
      <AiIcons.AiOutlineLine/>
      <button onClick={() => {
          setAwayCount(function (prevCount) {
            if (prevCount == 25) {
              return 25;
            }
            return (prevCount += 1);
          });
      }}>+</button>
      {awayCount}
      <button onClick={() => {
         setAwayCount(function (prevCount) {
          if (prevCount > 0) {
            return (prevCount -= 1);
          } else {
            return (prevCount = 0);
          }
        });
      }}>-</button>
      
    </div>
  );
}



export default Games