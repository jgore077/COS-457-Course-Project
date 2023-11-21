import React,{useState,useEffect,useRef}from 'react'

import Players from './Players'
import Announcement from './Announcements'
import Games from './Games'
import Practice from './Practices'

import { FaSearch } from "react-icons/fa";
import { TextField,InputAdornment,Select,MenuItem,InputLabel,FormControl,FormHelperText } from '@mui/material'
function Search(props) {
  const [query,setQuery]=useState('')
  const [searchMethod,setSearchMethod]=useState('Broad Search')
  const [sidebarState,setSidebarState]=useState(props.sidebarState)

  const inputRef = useRef(null);

  const handleQuery=() => {
    inputRef.current.blur()
    console.log('test')
  }
  const handleChange=(e) => {
    setSearchMethod(e.target.value)
    console.log(e)
  }

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
    <div class='center' >
    <FormControl sx={{ m: 1, width: '30ch' }}>
      
        <Select
        
          id="demo-simple-select"
          value={searchMethod}
          onChange={handleChange}
        >
          <MenuItem value={'Broad Search'}>Broad Search</MenuItem>
          <MenuItem value={'Precision Search'}>Precision Search</MenuItem>
          <MenuItem value={'Match Search'}>Match Search</MenuItem>
          <MenuItem value={'News Search'}>New Search</MenuItem>
        </Select>
        <FormHelperText>Select Your Search Method!</FormHelperText>
      </FormControl>
    <TextField
    id="input-with-icon-textfield"
    inputRef={inputRef}
    label={<p style={{color:'black',fontSize:'1.5em'}} >Search!</p>}
    sx={{ m: 1, width: '30ch' }}
    onKeyDown={(e) => {
      if (e.key === 'Enter') {
       handleQuery()
      }
    }}
    onChange={(e) => {
      setQuery(e.target.value)
    }}
    
    style={{
      zIndex: sidebarState ? -1 : 0
    }}
    InputProps={{
      startAdornment: (
        <InputAdornment position="start">
         <FaSearch style={{color:'black'}} size={'1.5em'}/>
        </InputAdornment>
        
      ),
      endAdornment:(
        <InputAdornment  position="end">
         <p onClick={handleQuery}
         style={{color:'blue','user-select': 'none','cursor':'pointer'}} >Go!</p>
        </InputAdornment>
      )
    }}
    variant="standard"
  />
  </div>
  )
}

export default Search