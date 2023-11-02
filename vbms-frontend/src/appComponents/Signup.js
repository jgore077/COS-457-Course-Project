import React from 'react'
import { useState } from 'react'
import { CookiesProvider, useCookies } from "react-cookie";
import '../Authentication.css'
function Signup() {

  const [email, setEmail] = useState('');
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');

  // States for error messages corresponding to the above states
  const [emailError, setEmailError] = useState('');
  const [usernameError, setUsernameError] = useState('');
  const [passwordError, setPasswordError] = useState('');

  // There is an optional argument removeCookie for the state which will be used to log users out
  const [cookies, setCookie,removeCookie] = useCookies(["user"]);
  // Once the application is migrated to a server I should set the secure attribute of the cookie in order to prevent sniffers
  //setCookie("bumblesmitz",'this cookie is a test',{ path: "/",sameSite:'Strict'});
   //you can access cookies by doing cookies.COOKIE_NAME where COOKIE_NAME is the name of the cookie
   // if a cookie doesnt exist it will return undefined which can be used in determining if a user has ever logged in
   //console.log(cookies.doesntexist)
  return (
    <div class='center'>
      <div class='center formStyle' style={{marginTop:30}}>
          
          <input class='button'  placeholder='Email' type='text' onChange={(e) => setEmail(e.target.value)}/>
          <p class='error'>{emailError}</p>

          <input class='button' placeholder='Username' type='text' onChange={(e) => setUsername(e.target.value)} />
          <p class='error'>{usernameError}</p>
        
        
          <input 
            class='button' 
            placeholder='Password'
            type="password"
            onChange={(e) => setPassword(e.target.value)}
          />
          <p class='error'>{passwordError}</p>
        
        
        
      </div>
    <input
    onClick={()=>{
      let data={
        email:email,
        username:username,
        password:password,      
      }
      console.log(data)
      fetch('/signup',{
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body:JSON.stringify(data),
     }).then((response)=>{
      response.json().then(function(data)
      {
          setEmailError(data.email)
          setUsernameError(data.username)
          setPasswordError(data.password)
         
      });
      }).catch(function(error){
        console.log(error)
      })
      .catch((error)=>{
     
      })
    }} 
     class='submitButton' 
     type='button' 
     value=' Press to Submit'/>
    </div>
  )
}

export default Signup