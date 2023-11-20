import React,{useState,useContext} from 'react';
import Popup from 'reactjs-popup';
import { DemoContainer } from '@mui/x-date-pickers/internals/demo';
import { AdapterDayjs } from '@mui/x-date-pickers/AdapterDayjs';
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';
import { DateTimePicker } from '@mui/x-date-pickers/DateTimePicker';
import './Modal.css'
import dayjs from 'dayjs';
import { useReloadContext } from "./Main.js";

// https://www.npmjs.com/package/@mui/x-date-pickers
// https://mui.com/x/react-date-pickers/date-time-picker/
// I can use these to create date time pickers
// There should also be an edit button which will reopen the modal and allow users to change the data

// i have this (dateTime picker) now but I still need to get the date out and save it in the db
// https://mui.com/x/react-date-pickers/date-time-picker/
// I should set the default value to the users current time

// The trigger for the modal can be any valid html it appears, This makes me want to use an Icon for both the edit and create
// I made the trigger part of the props so I can use the big button at the end bottom of the page

// i may add some conditional renders and states

// I need a prop for game or practice,
export default (props) => { 
  const { reload } = useReloadContext();
  const handleReload = () => {
    reload();
  };
  let [dateTime,setDateTime]=useState(dayjs())
  let [descriptionValue,setDescription]=useState(props.description)
  let [locationValue,setLocation]=useState(props.location)
  let [opponentValue,setOpponent]=useState(props.opponent)
  let statement =props.id!=undefined?'Update':'Create'
  return(
  <Popup
    onClose={handleReload}
    trigger={props.trigger}
    modal
    nested
  >
    {close => (
      <div className="modal">
        <button className="close" onClick={close}>
          &times;
        </button>
        <div className="header" style={{paddingTop:15}}> {statement} a {props.type}! </div>
        
        <div className="content">
            {props.type==='Game' |props.type==='Practice'?<div>Location<br/><textarea id='location' type='text' size="30" defaultValue={props.location} onChange={(e)=>{setLocation(e.target.value)}} style={{width:'95%'}}/><br/></div>:undefined}
            Description
            <br/> 
            <textarea id='description' type='text' size="30" style={{width:'95%'}} defaultValue={props.description} onChange={(e)=>{setDescription(e.target.value)}}/>
            <br/>
            {props.type==='Game'?<div>Opponent<br/><input id='opponent' type='text' size="30" defaultValue={props.opponent} onChange={(e)=>{setOpponent(e.target.value)}} style={{width:'95%'}}/><br/></div>:undefined}
  
            {props.type==='Game' || props.type==='Practice'?
            <LocalizationProvider dateAdapter={AdapterDayjs}>
                <DemoContainer components={['DateTimePicker']}>
                    <DateTimePicker label="Choose a date!" onChange={(newValue) => setDateTime(newValue)} defaultValue={dateTime}/>
                </DemoContainer>
            </LocalizationProvider>
            :undefined}
        </div>
        <div className="actions">
          
          <button
            className="button"
            onClick={() => {
              let location   =document.getElementById('location')
              let description=document.getElementById('description')
              let opponent   =document.getElementById('opponent')
              let incompleted=[]
              if(location&&location.value.length==0){
                incompleted.push(location)
              }
              if(description.value.length==0){
                incompleted.push(description)
              }
              if(props.type=='Game'){
                if(opponent&&opponent.value.length==0){
                  incompleted.push(opponent)
                }
              }
              // I need to add some checking for valid fields here. I plan on using my old css and vanilla js
            
              incompleted.forEach(element => {
                element.classList.add('flashing-border')
              });
              setTimeout(function() {
                incompleted.forEach(element => {
                    element.classList.remove('flashing-border')
                });
                 }, 2000);
              if(incompleted.length!=0){
                return
              }
              let route_string=props.type.toLowerCase()
              if(props.id!=undefined){
                route_string='/update'+route_string
              }
              else{
                route_string='/create'+route_string
              }
              console.log(route_string)
              close();
              console.log(props.location? props.location : locationValue)
              fetch(route_string,{
                method: "POST",
                headers: {
                  "Content-Type": "application/json",
                },
                body:JSON.stringify({
                  id:props.id,
                  description: descriptionValue,
                  location:locationValue,
                  opponent:opponentValue,
                  datetime:dateTime,
                  user_id:props.user_id
                })
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
            }}
          >
            {statement} {props.type}
          </button>
        </div>
      </div>
    )}
  </Popup>
)};