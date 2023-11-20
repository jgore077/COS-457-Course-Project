import React,{useEffect,useState} from 'react'
import '../Authentication.css'
import Modal from '../Modal'
import dayjs from 'dayjs';
import * as AiIcons from "react-icons/ai";
import * as FaIcons from "react-icons/fa";
import './dataComponents.css'
function Announcements(props) {
  console.log(props)
  const [announcementsList,setAnnouncementsList]=useState([])
  
  
  useEffect(()=>{
    fetch('/announcements',{
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      }
    }).then((response)=>{
      response.json().then(function(data)
      {
        setAnnouncementsList(data.announcements)
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
        {announcementsList.map((element) =>  {
          console.log(props.decodedAuthToken.uid)
          return <Announcement role={props.decodedAuthToken.role} datetime={element.datetime} description={element.description} id={element.id}/>
        })}
      {(props.decodedAuthToken.role==='admin' && !props.sidebarState)?<div class='add-button-container'>
          <Modal user_id= {props.decodedAuthToken.uid} type='Announcement' trigger={<AiIcons.AiOutlinePlusSquare class='add-button' size={'2em'} />}/>
        </div>:undefined}
    </div>
  )
}

function Announcement(prop) {
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
  let date_and_time=prop.datetime.split(' ')
  return (
    <div class='center'>
      {prop.role==='admin'?
      <div class='game-top'>
       {/* This will delete the game later on and the update modal should be disabled after the game day*/}
      <AiIcons.AiOutlineClose  size={'1.5em'}/>
      <Modal type='Announcement'
        id={prop.id} 
        description={prop.description} 

        trigger={<FaIcons.FaPencilAlt size={'1.5em'}/>}/>
      </div>:
      undefined
      }
      {dayjs(date_and_time[0]).format('MM/DD/YYYY')} at {convertTo12HourFormat(date_and_time[1])}
      <div class='game'>
        <h4>Description:</h4>
        {prop.description}  
      </div>
    </div>
  )
}

export default Announcements