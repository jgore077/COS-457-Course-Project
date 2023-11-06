import React,{useState} from 'react'
import Games from './dataComponents/Games'
import Announcements from './dataComponents/Announcements'
import Popup from 'reactjs-popup';
import Modal from './Modal';
function TestComponent() {
    // We also need to send cancellation messages
    // I created this component to test the idea of the main component having all these states and maps
    // These are all states that determine the data stored inside the components so that once a user visits them they wont completely loose all data
    let [gamesProps,setGamesProps]=useState({a:'1',b:'2',c:'3'})
    let [announcementsProps,setAnnouncementProps]=useState({a:'1',b:'2',c:'3'})
    let [inputState,setInputState]=useState('')
    let map={
        'games':<Games props={gamesProps}/>,
        'announcements':<Announcements props={announcementsProps}/>, 
    }
 // I may want to send an existing copy of the data over so the flask server can send smaller requests or none at all (For games and announcements)
 // So I was testing live updates to the components which actually seem to work
 // This means I can go forward and design the props to be built out

 // I should also pass user_id from the data returned from the server to better render the components with approriate roles
  return ( 
    <div>
        {map.games}
        <input type='text'onChange={(e) => {
            setInputState(e.target.value);
        }}
        onKeyDown={(e)=>{if(e.key==='Enter')gamesProps[inputState]=inputState; console.log('test') }}></input>
         <Modal/>
    </div>
  )
}

export default TestComponent