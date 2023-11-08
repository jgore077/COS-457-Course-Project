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
  // I also need to add token expiry here
  //use effect for polling the cookie value
  useEffect(() => {
    const checkCookiePresence = () => {
      const currentAuthToken = getCookie('authToken');
      setAuthTokenPresent(Boolean(currentAuthToken));
   
    };
    // This code is for the user signing out
    if(isLoggedIn && !isAuthTokenPresent){
      console.log('time to set to false')
      setLoginPresent(false)
    }
    const interval = setInterval(checkCookiePresence, 1000); // Check every second

    // Cleanup: Clear the interval when the component is unmounted
    return () => clearInterval(interval);
  }, [isAuthTokenPresent]);

  //use effect for validating auth tokens and loading into the main component
  useEffect(() => {
      
      if(!isAuthTokenPresent){
        return
      }
      fetch('/userinfo').then((response) => {
        console.log(response.status )
        if(response.status==204){
          //this is if the authToken was incorrect or non-existent so user still needs to login
          return
        }
        response.json().then((data) => {
          console.log (data)
          setLoginPresent(true)
        }).catch((error) => {
          
        })
      }).catch((error) => {
        
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
      <Main/>
     {/* {isLoggedIn?<Main/>:<Authentication/>} */}
     {/* <TestComponent/> */}
    </div>
  )
}

export default App;