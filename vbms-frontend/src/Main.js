import React, { useState,useEffect,createContext,useContext} from "react";
import * as FaIcons from "react-icons/fa";
import * as AiIcons from "react-icons/ai";
import "./Sidebar.css";
import { IconContext } from "react-icons";
import {Players} from "./dataComponents/Players";
import {Announcements} from "./dataComponents/Announcements";
import {Games} from "./dataComponents/Games";
import Search from "./dataComponents/Search";
import {Practices} from "./dataComponents/Practices";
import Profile from "./dataComponents/Profile";

const ReloadContext = createContext();

export const useReloadContext = () => {
  return useContext(ReloadContext);
};

export function ReloadProvider({ children }) {
  const [reloadFlag, setReloadFlag] = useState(false);

  const reload = () => {
    setReloadFlag(!reloadFlag);
  };

  return (
    <ReloadContext.Provider value={{ reload }}>
      {children}
    </ReloadContext.Provider>
  );
}

function Main(props) {
  console.log(props.authCookie)
  console.log(props.decodedAuthToken)
  const [sidebar, setSidebar] = useState(false);
  let map={
    'players':<Players authCookie={props.authCookie}/>,
    'games':<Games authCookie={props.authCookie} decodedAuthToken={props.decodedAuthToken} sidebarState={sidebar} game={true}/>,
    'announcements':<Announcements authCookie={props.authCookie} decodedAuthToken={props.decodedAuthToken} sidebarState={sidebar}/>,
    'practices':<Practices authCookie={props.authCookie} decodedAuthToken={props.decodedAuthToken} sidebarState={sidebar} />,
    'search':<Search authCookie={props.authCookie} decodedAuthToken={props.decodedAuthToken} sidebarState={sidebar}/>,
    'profile':<Profile authCookie={props.authCookie} decodedAuthToken={props.decodedAuthToken} sidebarState={sidebar}/>
  }
  let [navState,setNavState]=useState('search')
  

  useEffect(() => {
    
  }, [navState]);

  
  const showSidebar = () => setSidebar(!sidebar);
  return (
    <div class='sidebar' style={{position:'relative'}}>
      <IconContext.Provider value={{ color: "undefined" }}>
        <div className="navbar">
        
            <FaIcons.FaBars onClick={showSidebar} size={'2em'} />
          
        <span class='centered-title'>{navState[0].toUpperCase() + navState.slice(1)}</span>
        </div>
        <nav className={sidebar ? "nav-menu active" : "nav-menu"}>
          <ul className="nav-menu-items">
          
            <li style={{borderBottom:'solid'}}className="navbar-toggle">
                <span style={{paddingRight:60,fontSize:24}}>Menu</span>
                <AiIcons.AiOutlineClose size={'2em'}  onClick={showSidebar}/>
            </li>
            <li id='search' class='clickable' onClick={(e) => {
              setNavState(e.target.id)
              showSidebar()
            }}>
                Search
            </li>
            <li id='players' class='clickable' onClick={(e) => {
              setNavState(e.target.id)
              showSidebar()
            }}>
                Players
            </li>
            <li id='announcements' class='clickable' onClick={(e) => {
              setNavState(e.target.id)
              showSidebar()
            }}>
                Announcements
            </li>
            <li id='games' class='clickable' onClick={(e) => {
              setNavState(e.target.id)
              showSidebar()
            }}>
                Games
            </li>
            <li id='practices' class='clickable' onClick={(e) => {
              setNavState(e.target.id)
              showSidebar()
            }}>
                Practices
            </li>
            <hr/>
            <li id='profile' class='clickable' onClick={(e) => {
              setNavState(e.target.id)
              showSidebar()
            }}>
                Profile
            </li>

          </ul>
        </nav>
      </IconContext.Provider>
      <ReloadProvider>
      <div class='content'>{map[navState]}</div>
      </ReloadProvider>
      
    </div>
  );
}

export default Main;