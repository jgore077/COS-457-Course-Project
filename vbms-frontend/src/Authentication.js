import React, { useState } from 'react';
import { CookiesProvider, useCookies,updateCookies } from "react-cookie";
import Signup from './appComponents/Signup';
import Login from './appComponents/Login';
import './Authentication.css'

const Authentication = () => {
    const [isSignUp, setIsSignUp] = useState(false);
    const [cookies, setCooki] = useCookies(["user"]);
    
    // Once the application is migrated to a server I should set the secure attribute of the cookie in order to prevent sniffers
  
    //const [authCookie,setAuth]= useState(["user"])
   
    return (
        <div class='center'>
              <h3>VolleyBall Management System</h3>        
            

              <button onClick={() =>isSignUp?setIsSignUp(false):setIsSignUp(true)}>Press to Switch to {isSignUp?'Log in':'Sign up'}</button>

      
            
            {!isSignUp? <Login/>:<Signup/>}

        </div>
    );

};

export default Authentication;