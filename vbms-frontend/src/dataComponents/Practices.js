import React from 'react'
import Modal from '../Modal'
import * as AiIcons from "react-icons/ai";
function Practices(props) {
  return (
    <div class='center'>Practices
         {(props.decodedAuthToken.role==='admin' && !props.sidebarState)?<div class='add-button-container'>
          <Modal type='Practice' trigger={<AiIcons.AiOutlinePlusSquare class='add-button' size={'2em'} />}/>
        </div>:undefined}
    </div>
  )
}

function Practice() {
    return (
      <div>Practice</div>
    )
  }

export default Practices