import React,{useState,useEffect} from 'react'
import { CookiesProvider, useCookies,withCookies } from "react-cookie";
import Main from './Main';
import Authentication from './Authentication';
import TestComponent from './TestComponent';
function App() {

  const [cookies] = useCookies(['authToken']);
  const [isAuthTokenPresent, setAuthTokenPresent] = useState(Boolean(cookies.authToken));
  const [isLoggedIn, setLoginPresent] = useState(false);
  const [mainProps,setMainProps]= useState({})
  const [authCookie,setAuthCookie]=useState(cookies.authToken)
  const [decodedAuthToken,setDecodedToken]=useState({})
  // I also need to add token expiry here
  //use effect for polling the cookie value


  // I need to redesign the system with refreshes insted of polling
  useEffect(() => {
    const checkCookiePresence = () => {
      const currentAuthToken = getCookie('authToken');
      setAuthTokenPresent(Boolean(currentAuthToken));
   
    };
    // This code is for the user signing out
    if(isLoggedIn && !isAuthTokenPresent){
      setDecodedToken({})
      setLoginPresent(false)
    }
    const interval = setInterval(checkCookiePresence, 1000); // Check every second

    // Cleanup: Clear the interval when the component is unmounted
    return () => clearInterval(interval);
  }, [isAuthTokenPresent]);

  //use effect for validating auth tokens and loading into the main component

  // I need to fix quite a few bugs in the overall system especially ones revolving around logging in
  useEffect(() => {
      
      if(!isAuthTokenPresent){
        return
      }
      // fetch('/userinfo').then((response) => {
      //   console.log(response.status )
      //   if(response.status==204){
      //     //this is if the authToken was incorrect or non-existent so user still needs to login
      //     return
      //   }
      //   response.json().then((data) => {
      //     console.log (data)
      //     setLoginPresent(true)
      //   }).catch((error) => {
          
      //   })
      // }).catch((error) => {
        
      // })
      // ^^^^^^^^^^^^^^^ I commented out the code above because I moved to a more sophisticated way of doing it so that I can store a decoded token 
      // I also might want to add a refresh instead of polling because thats a bit insane but it works for now
      // I should also probably add some code for failure to connect
    fetch('/decode',{
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body:JSON.stringify({'authToken':authCookie}),
    }).then((response)=>{
      if(response.status==204){
          return
           }
      response.json().then(function(data)
        {
          setDecodedToken(data)
          setLoginPresent(true)
        });
        }).catch(function(error){
          console.log(error)
        })
    .catch((error)=>{
  
    })
  }, [isAuthTokenPresent]);


  function getCookie(name) {
    
    const value = `; ${document.cookie}`;

    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
    return null;
  }


  return (
    <div>
      {/* <Main/> */}
     {isLoggedIn?<Main authCookie={authCookie} decodedAuthToken={decodedAuthToken}/>:<Authentication/>}
     {/* <TestComponent/> */}
    </div>
  )
}

export default App;