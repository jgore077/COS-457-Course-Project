import React,{useEffect,useState} from 'react'
import './dataComponents.css'
function Players(props) {
  const [playerList,setPlayerList]=useState([])
  // Theres an error in this function but I cant figure out the cause
  useEffect(()=>{
    fetch('/players',{
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      }
    }).then((response)=>{
      response.json().then(function(data)
      {
        setPlayerList(data.players)
        console.log(playerList)
      });
      }).catch(function(error){
        console.log(error)
      })
    .catch((error)=>{
        console.log(error)
    })
  },[])

  return (
    <div class='center'>
      <div class='player-wrapper'>
        {playerList.map((element) =>  {
          return <Player username={element.username} email={element.email}/>
        })}
      </div>
    </div>
  )
}
// Role should be included
export function Player(prop){
    return (
        <div class='playertext'>
          <h4 class='player-bottom-margin'>Username</h4>
          <span class='player-bottom-margin'>{prop.username}</span>
          <br/>
          <h4 class='player-bottom-margin' style={{marginTop:5}}>Email</h4>
          <a href={'mailto:'+prop.email}>{prop.email}</a>
        </div>
      )
}

export default Players