import React,{useState,useEffect,useRef}from 'react'

import './dataComponents.css'

import {Player} from './Players'
import {Announcement} from './Announcements'
import {Game} from './Games'
import {Practice} from './Practices'

import { FaSearch,FaAngleRight } from "react-icons/fa";
import { TextField,InputAdornment,Select,MenuItem,InputLabel,FormControl,FormHelperText } from '@mui/material'
import { DateTimeField } from '@mui/x-date-pickers/DateTimeField';
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';
import { AdapterDayjs } from '@mui/x-date-pickers/AdapterDayjs';
function Search(props) {
  const precision_search_map={
    'Announcements':['Description','Date-time'],
    'Games':['Description','Date-time','Location','Opponent'],
    'Practices':['Description','Date-time','Location'],
    'Players':['Username','Email'],

  }
 
  const [gamesList,setGamesList]=useState(undefined)
  const [announcementsList,setAnnouncementsList]=useState(undefined)
  const [practiceList,setPracticeList]=useState(undefined)
  const [playerList,setPlayerList]=useState(undefined)

  const search_array_map={
    'Announcements':announcementsList,
    'Games':gamesList,
    'Practices':practiceList,
    'Players':playerList,
  }

  const [query,setQuery]=useState('')
  const [searchMethod,setSearchMethod]=useState('Match Search')
  const [sidebarState,setSidebarState]=useState(true)
  const [dateTimeValue,setDateTimeValue]=useState(undefined)


  const [table,setTable]=useState('Announcements')
  const [attribute,setAttribute]=useState(precision_search_map[table][0]);

  const inputRef = useRef(null);

  const handleQuery=(e) => {
    inputRef.current.blur()
    console.log(searchMethod)
    console.log(table)
    console.log(attribute)
    fetch('/search',{
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body:JSON.stringify({query:query,method:searchMethod,table:table,attribute:attribute,datetime:dateTimeValue})
    }).then((response)=>{
      response.json().then(function(data)
      {
        setAnnouncementsList(data['announcements'])
        setGamesList(data['games'])
        setPlayerList(data['players'])
        setPracticeList(data['practices'])
        
      });
      }).catch(function(error){
        console.log(error)
      })
    .catch((error)=>{
        console.log(error)
    })
  }
  const handleChange=(e) => {
    setSearchMethod(e.target.value)
  }
  const handleTable=(e) => {
    setTable(e.target.value)
    setAttribute(precision_search_map[e.target.value][0])
  }

  const handleAttribute=(e) => {
    setAttribute(e.target.value)
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

  function Result(props) {
    const [displayResults,setDisplayResults]=useState(false)
    let name =props.name
    let rendered_data;
    console.log(props.data)
    console.log(props.decodedAuthToken)
    function renderResults(dataList){
      switch(name) {
        case 'Games':
          rendered_data=props.data.map((element) =>  {
            return <Game role={props.decodedAuthToken.role} gamedata={element}/>
          })
          break
        case 'Announcements':
          rendered_data=props.data.map((element) =>  {
            return <Announcement role={props.decodedAuthToken.role} datetime={element.datetime} description={element.description} id={element.id}/>
          })
          break;
        case 'Practices':
          rendered_data=props.data.map((element) =>  {
            return <Practice role={props.decodedAuthToken.role} practice={element}/>
          })
          break;
        default:
          rendered_data=props.data.map((element) =>  {
            return <Player username={element.username} email={element.email}/>
          })
          break;
      } 
      return rendered_data
    }
    
    return (
      <div>
      <div 
      style={{width:'75vw',display:'flex',justifyContent:'space-between',backgroundColor:'lightgrey',padding:10}}
      onClick={() => {
        setDisplayResults(!displayResults)
      }}
      >{name} 
      <span>
        {search_array_map[name].length} Results <FaAngleRight style={{ transform: displayResults ?  'rotate(90deg)' : 'rotate(0deg)', transition:'.2s'}}/></span></div>
      <div style={{ display: displayResults ?'inline':'none'}}>
        {renderResults(props.data)}
      </div>
      </div>
    )
  }
  return (
    <div class='center' style={{ zIndex: sidebarState ? -1 : 0}} >
    <FormControl style={{ zIndex: sidebarState ? -1 : 0}} sx={{ m: 1, width: '30ch' }}>
      
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
    {searchMethod==='Precision Search'?
    <div>
    <FormControl style={{ zIndex: sidebarState ? -1 : 0}} sx={{ m: 1, width: '15ch' }}>  
      <Select 
        id="demo-simple-select"
        value={table}
        onChange={handleTable}
      >
  
        <MenuItem value={'Announcements'}>Announcements</MenuItem>
        <MenuItem value={'Games'}>Games</MenuItem>
        <MenuItem value={'Practices'}>Practices</MenuItem>
        <MenuItem value={'Players'}>Players</MenuItem>
      </Select>
      <FormHelperText>Select Your Table!</FormHelperText>
    </FormControl>
    <FormControl style={{ zIndex: sidebarState ? -1 : 0}} sx={{ m: 1, width: '15ch' }}>  
      <Select 
        id="demo-simple-select"
        value={attribute}
        onChange={handleAttribute}
      >
        {precision_search_map[table].map((element) =>  {
          return <MenuItem value={element}>{element}</MenuItem>
        })}
      </Select>
      <FormHelperText>Select Your Field!</FormHelperText>
    </FormControl>
    
    </div>
    :undefined}
    {searchMethod=='News Search'|| searchMethod=='Match Search'?
  <LocalizationProvider dateAdapter={AdapterDayjs}>
  <DateTimeField
  style={{ zIndex: sidebarState ? -1 : 0}} sx={{ m: 1, width: '30ch' }}
  label="Enter A Date! (Optional Field)"
  value={dateTimeValue}
  onChange={(newValue) => setDateTimeValue(newValue)}
    />
  </LocalizationProvider>
  :undefined}
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
         style={{color:'blue','cursor':'pointer'}} >Go!</p>
        </InputAdornment>
      )
    }}
    variant="standard"
  />
   { Object.keys(precision_search_map).map((element) =>  {
          console.log('this is the token from search'+props.decodedAuthToken.role)
          if(search_array_map[element]==undefined){
            return
          }
          return <Result decodedAuthToken={props.decodedAuthToken} name={element} data={search_array_map[element]}/>
        })}
  </div>
  )
}






export default Search