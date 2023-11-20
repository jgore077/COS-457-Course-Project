import React,{useEffect,useState, useRef} from 'react'
import { Button,TextField,FormControl,MenuItem,FormHelperText,Select } from '@mui/material'
import {useCookies} from "react-cookie";
import './dataComponents.css'


function Profile(props) {
  const [userInfo,setUserInfo]=useState({})

  const [sidebarState,setSidebarState]=useState(true)

  const [cookies, setCookie, removeCookie] = useCookies(['authToken']);

  const [phoneNumber,setPhoneNumber]=useState('')
  const [shirtState,setShirtState]= useState('')
  const [commuterStatus,setCommuterStatus] =useState(false)

  const inputRef = useRef(null);

  
  useEffect(()=>{
    fetch('/userinfo',{
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body:JSON.stringify({authCookie:props.authCookie})
    }).then((response)=>{
      console.log(response.status)
      response.json().then(function(data)
      {
      console.log(data)
        setUserInfo(data)
        setShirtState(data.shirt)
        setCommuterStatus(data.commuter)
        
      });
      }).catch(function(error){
        console.log(error)
      })
    .catch((error)=>{
        console.log(error)
    })
    
  },[])
  // This block exists so that stuff doesnt overlap
  useEffect(() => {
    if(props.sidebarState){
      console.log('sidebar is open')
      setSidebarState(true)
    }
    else{
      setTimeout(() => {
        setSidebarState(false);
    }, 350);
    }
  }, [props.sidebarState]);

  return (
    <div class='center' style={{gap:50}}>
      {/* <div style={{display:'flex',flexDirection:'column',gap:100 }}> */}
      <h2>{userInfo.username}</h2>
      <TextField
          inputRef={inputRef}
          placeholder={userInfo.number}
          helperText="Change Your Phone Number!"
        
          onKeyDown={(e) => {
            if (e.key === 'Enter') {
              inputRef.current.blur()
              fetch('/phone',{
                method: "POST",
                headers: {
                  "Content-Type": "application/json",
                },
                body:JSON.stringify({authCookie:props.authCookie,phone:e.target.value})
              }).then((response)=>{
                console.log(response.status)
                response.json().then(function(data)
                {
               
                  
                });
                }).catch(function(error){
                  console.log(error)
                })
              .catch((error)=>{
                  console.log(error)
              })
            }
          }}
          onChange={(e) => {
            setPhoneNumber(e.target.value)
          }}
          
          style={{
            zIndex: sidebarState ? -1 : 0
          }}
        />
        {/* --------------------------------------------------- */}
      <FormControl style={{
        zIndex: sidebarState ? -1 : 0
        }}
        sx={{ m: 1, minWidth: 225 }}>
        <Select
          value={shirtState || ''} // Set default value
          onChange={(e) => {
            setShirtState(e.target.value)
            fetch('/shirt',{
              method: "POST",
              headers: {
                "Content-Type": "application/json",
              },
              body:JSON.stringify({authCookie:props.authCookie,shirt:e.target.value})
            }).then((response)=>{
              console.log(response.status)
              response.json().then(function(data)
              {
             
                
              });
              }).catch(function(error){
                console.log(error)
              })
            .catch((error)=>{
                console.log(error)
            })

          }}
          displayEmpty
          inputProps={{ 'aria-label': 'Shirt Size' }}
        >

          <MenuItem value={"XS"}>XS</MenuItem>
          <MenuItem value={"S"}>S</MenuItem>
          <MenuItem value={"M"}>M</MenuItem>
          <MenuItem value={"L"}>L</MenuItem>
          <MenuItem value={"XL"}>XL</MenuItem>
        </Select>
        <FormHelperText>Change Your Shirt Size!</FormHelperText>
      </FormControl>
      {/* --------------------------------------------------- */}
      <div class='center'>
        <b>Am I A Commuter?</b>
        <input style={{width:255}} value={commuterStatus?'Yes':'No'} type='button'
        onClick={() => {
          setCommuterStatus(!commuterStatus)
          fetch('/commuter',{
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body:JSON.stringify({authCookie:props.authCookie,commuter:!commuterStatus})
          }).then((response)=>{
            console.log(response.status)
            response.json().then(function(data)
            {
           
              
            });
            }).catch(function(error){
              console.log(error)
            })
          .catch((error)=>{
              console.log(error)
          })
        }}
        />
      </div>
      {/* ------------------------------------------------- */}
      <Button variant="contained" 
        onClick={() => {
        removeCookie('authToken')
        window.location.reload(false);
      }}
      style={{
        zIndex: sidebarState ? -1 : 0
      }}
      >Log Out</Button>
      {/* </div> */}
    </div>
  )
}

export default Profile