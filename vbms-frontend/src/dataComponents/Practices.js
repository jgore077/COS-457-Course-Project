import React,{useState,useEffect} from 'react'
import Modal from '../Modal'
import * as AiIcons from "react-icons/ai";
import * as FaIcons from "react-icons/fa";
import dayjs from 'dayjs';
function Practices(props) {
  const [practiceList,setPracticeList]=useState([])
  useEffect(()=>{
    fetch('/practices',{
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      }
    }).then((response)=>{
      response.json().then(function(data)
      {
        console.log(data.practices)
        setPracticeList(data.practices)
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

    {practiceList.map((element) =>  {
          return <Practice role={props.decodedAuthToken.role} practice={element}/>
        })}
         {(props.decodedAuthToken.role==='admin' && !props.sidebarState)?<div class='add-button-container'>
          <Modal type='Practice' trigger={<AiIcons.AiOutlinePlusSquare class='add-button' size={'2em'} />}/>
        </div>:undefined}
    </div>
  )
}

export function Practice(prop) {
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
    let id= prop.practice.id
    let date_and_time =prop.practice.datetime.split(' ')
    let location = prop.practice.location
    let description= prop.practice.description
    return (
      <div class='center'>
      {prop.role==='admin'?
      <div class='game-top'>
       {/* This will delete the game later on and the update modal should be disabled after the game day*/}
      <AiIcons.AiOutlineClose  size={'1.5em'}/>
      <Modal type='Game'
        id={id} 
        description={description} 
        location={location} 
        trigger={<FaIcons.FaPencilAlt size={'1.5em'}/>}/>
      </div>:
      undefined
      }
      {dayjs(date_and_time[0]).format('MM/DD/YYYY')} at {convertTo12HourFormat(date_and_time[1])}
      <div class='game'>
        <h3>Location</h3>
        {location}
        <h4>Description:</h4>
        {description}
  
      </div>
    </div>
    )
  }

export default Practices