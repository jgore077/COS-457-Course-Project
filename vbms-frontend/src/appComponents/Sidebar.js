import React, { useState,useEffect } from "react";
import * as FaIcons from "react-icons/fa";
import * as AiIcons from "react-icons/ai";
import "./Sidebar.css";
import { IconContext } from "react-icons";
import Players from "../dataComponents/Players";
import Announcements from "../dataComponents/Announcements";
import Games from "../dataComponents/Games";



function Sidebar() {

  let [gamesProps,setGamesProps]=useState({})
  let [announcementsProps,setAnnouncementProps]=useState({})
  let [playerProps,setPlayerProps]=useState({})
  let map={
    'players':<Players/>,
    'games':<Games/>,
    'announcements':<Announcements/>,
  }
  let [navState,setNavState]=useState('players')

  
  const [sidebar, setSidebar] = useState(false);
  useEffect(() => {

}, [navState]);

  const showSidebar = () => setSidebar(!sidebar);

  return (
    <div class='sidebar'>
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

          </ul>
        </nav>
      </IconContext.Provider>
      <div class='content'>{map[navState]}</div>
    </div>
  );
}

export default Sidebar;