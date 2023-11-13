import React,{useState} from 'react';
import Popup from 'reactjs-popup';
import { DemoContainer } from '@mui/x-date-pickers/internals/demo';
import { AdapterDayjs } from '@mui/x-date-pickers/AdapterDayjs';
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';
import { DateTimePicker } from '@mui/x-date-pickers/DateTimePicker';
import './Modal.css'
import dayjs from 'dayjs';

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
  let [dateTime,setDateTime]=useState(dayjs())

  return(
  <Popup
    trigger={props.trigger}
    modal
    nested
  >
    {close => (
      <div className="modal">
        <button className="close" onClick={close}>
          &times;
        </button>
        <div className="header"> Create a Game! </div>
        
        <div className="content">
            Location
            <br/> 
            <textarea id='location' type='text' size="30" style={{width:'95%'}}/>
            <br/>
            Description
            <br/> 
            <textarea id='description' type='text' size="30" style={{width:'95%'}}/>
            <br/>
            {props.practice?<div>Opponent<br/><input id='opponent' type='text' size="30" style={{width:'95%'}}/><br/></div>:undefined}
  
            
            <LocalizationProvider dateAdapter={AdapterDayjs}>
                <DemoContainer components={['DateTimePicker']}>
                    <DateTimePicker label="Choose a date!" onChange={(newValue) => setDateTime(newValue)} defaultValue={dateTime}/>
                </DemoContainer>
            </LocalizationProvider>
        </div>
        <div className="actions">
          
          <button
            className="button"
            onClick={() => {
              let location   =document.getElementById('location')
              let description=document.getElementById('description')
              let opponent   =document.getElementById('opponent')
              let incompleted=[]
              if(location.value.length==0){
                incompleted.push(location)
              }
              if(description.value.length==0){
                incompleted.push(description)
              }
              if(props.practice){
                if(opponent.value.length==0){
                  incompleted.push(opponent)
                }
              }
              // I need to add some checking for valid fields here. I plan on using my old css and vanilla js
              console.log(location.value);
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
              console.log(dateTime)
              close();
            }}
          >
            Create Game
          </button>
        </div>
      </div>
    )}
  </Popup>
)};