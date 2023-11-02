import React,{useState} from 'react'
import '../Authentication.css'
import { CookiesProvider, useCookies } from "react-cookie";
function Login() {


  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');

  const [usernameError, setUsernameError] = useState('');
  const [passwordError, setPasswordError] = useState('');
  const [cookies, setCookie] = useCookies(["user"]);
  
  //setCookie("bumblesmitz",'this cookie is a test',{ path: "/",sameSite:'Strict'});
  return (
    <div class='center'>
      <div class='center formStyle' style={{marginTop:30}}>
          <input class='button' placeholder='Username' type='text' onChange={(e) => setUsername(e.target.value)}/>
          <p class='error'>{usernameError}</p>
          <input class='button' placeholder='Password' type="password" onChange={(e) => setPassword(e.target.value)}/>
          <p class='error'>{passwordError}</p>
      </div>
    
    <input onClick={()=>{
      let data={
        username:username,
        password:password,
      }
      fetch('/login',{
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body:JSON.stringify(data),
      }).then((response)=>{
        response.json().then(function(data)
        {
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
      value=' Press to Submit'
    />

    </div>
  )
}

export default Login