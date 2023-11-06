import React from 'react';
import Popup from 'reactjs-popup';
import { DemoContainer } from '@mui/x-date-pickers/internals/demo';
import { AdapterDayjs } from '@mui/x-date-pickers/AdapterDayjs';
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';
import { DateTimePicker } from '@mui/x-date-pickers/DateTimePicker';
import './Modal.css'

// https://www.npmjs.com/package/@mui/x-date-pickers
// https://mui.com/x/react-date-pickers/date-time-picker/
// I can use these to create date time pickers
// There should also be an edit button which will reopen the modal and allow users to change the data

// i have this (dateTime picker) now but I still need to get the date out and save it in the db
// https://mui.com/x/react-date-pickers/date-time-picker/
// I should set the default value to the users current time

// The trigger for the modal can be any valid html it appears, This makes me want to use an Icon for both the edit and create
export default () => (
  <Popup
    trigger={<button className="button"> Open Modal </button>}
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
            <input type='text' size="30"/>
            <br/>
            
            <LocalizationProvider dateAdapter={AdapterDayjs}>
                
                <DemoContainer components={['DateTimePicker']}>
                    <DateTimePicker label="Choose a date!" />
                </DemoContainer>
            </LocalizationProvider>
        </div>
        <div className="actions">
          
          <button
            className="button"
            onClick={() => {
              console.log('modal closed ');
              close();
            }}
          >
            Create Game
          </button>
        </div>
      </div>
    )}
  </Popup>
);