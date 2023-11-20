import React,{useState,useEffect,createContext} from 'react'
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

  useEffect(() => {
      
      if(!isAuthTokenPresent){
        return
      }
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



  return (
    <div>
      {/* <Main/> */}
     {isLoggedIn?<Main authCookie={authCookie} decodedAuthToken={decodedAuthToken}/>:<Authentication/>}
     {/* <TestComponent/> */}
    </div>
  )
}

export default App;