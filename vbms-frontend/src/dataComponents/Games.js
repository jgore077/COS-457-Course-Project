import React,{useEffect,useState} from 'react'
import Modal from '../Modal';
import dayjs from 'dayjs';
import * as AiIcons from "react-icons/ai";
import * as FaIcons from "react-icons/fa";
import './dataComponents.css'
import { esES } from '@mui/x-date-pickers';
function Games(props) {

  const [gamesList,setGamesList]=useState([])
  useEffect(()=>{
    fetch('/games',{
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      }
    }).then((response)=>{
      response.json().then(function(data)
      {
        
        setGamesList(data.games)
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
    <div class='player-wrapper'>
    {/* <Game role={props.decodedAuthToken.role} gamedata={{
  "game_id": 60,
  "location": "USM",
  "description": "USM v.s. Merrimack College! Located at USM on 2023-11-29 10:08:26.",
  "gamedate": "2023-11-29 10:08:26",
  "opponent": "Merrimack College",
  "game_score": "4-1"
  }} /> */}
    {gamesList.map((element) =>  {
          return <Game role={props.decodedAuthToken.role} gamedata={element}/>
        })}
    </div>
    {(props.decodedAuthToken.role==='admin' && !props.sidebarState)?<div class='add-button-container'>
        <Modal type='Game' trigger={<AiIcons.AiOutlinePlusSquare class='add-button' size={'2em'}/>}/>
      </div>:undefined}
      
    </div>
  
  )
}


// If the user is an administrator then the game should be rendered with a x in the top right corner so that they can cancel it same goes for announcements
// their should also be a pencil to edit existing games
export function Game(prop) {
  function convertTo12HourFormat(time24) {
    // Split the input time string into hours and minutes
    const [hour, minute,seconds] = time24.split(':');
  
    // Parse the hour and minute as integers
    const hourInt = parseInt(hour, 10);
    const minuteInt = parseInt(minute, 10);
  
    // Determine whether it's AM or PM
    const period = hourInt >= 12 ? 'PM' : 'AM';
  
    // Convert to 12-hour format
    let hour12 = hourInt % 12;
    if (hour12 === 0) {
      hour12 = 12; // 0 should be converted to 12 in 12-hour format
    }
  
    // Format the result as a string
    const time12 = `${hour12.toString().padStart(2, '0')}:${minuteInt.toString().padStart(2, '0')} ${period}`;
    
    return time12;
  }
  
    let date_and_time =prop.gamedata.gamedate.split(' ')
    let location = prop.gamedata.location
    let opponent = prop.gamedata.opponent
    let description= prop.gamedata.description
    let score= prop.gamedata.game_score
    console.log(date_and_time)
    return (
    <div class='center'>
      {prop.role==='admin'?
      <div class='game-top'>
       {/* This will delete the game later on and the update modal should be disabled after the game day*/}
      <AiIcons.AiOutlineClose  size={'1.5em'}/>
      <Modal type='Game'
        id={prop.gamedata.game_id} 
        description={prop.gamedata.description} 
        opponent={prop.gamedata.opponent} 
        location={prop.gamedata.location} 
        trigger={<FaIcons.FaPencilAlt size={'1.5em'}/>}/>
      </div>:
      undefined
      }
      {dayjs(date_and_time[0]).format('MM/DD/YYYY')} at {convertTo12HourFormat(date_and_time[1])}
      <div class='game'>
        <h3>Score (Home-Away)</h3>
        {score}
        <h3>Location</h3>
        {location}
        <br/>
        <h3>Opponent</h3>
        {opponent}
        <span>
        <h4>Description:</h4>
        {description}
        </span>
        
      </div>
    </div>
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