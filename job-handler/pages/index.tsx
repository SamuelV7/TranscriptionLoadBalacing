import { Button, OutlinedInput, Stack, TextField, Typography } from '@mui/material'
import React, { use, useState } from 'react'

export default function Home() {
  const [id, setID] = useState("")
  const [sermonTitle, setSermonTitle] = useState("")
  const [link, setLink] = useState("")

  const handleSubmit = async (e: any) =>{
    let data = await fetch('/api/submit', {
      method: 'POST', 
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({'title': sermonTitle, 'link': link}),})
    let redis_id = await data.json()
    console.log(redis_id.name)
    setID(redis_id.name)
  }
  return (
    <>
      <Stack spacing={3}>
        <Typography>
          Grace Life London - Scribe Service
        </Typography>
        <Typography fontSize='4xl'>
          Enter Youtube Link from Grace Life London to Transcribe
        </Typography>
        <Stack direction="row">
          <TextField placeholder='Title Of Sermon'
            value={sermonTitle} 
            onChange={e => setSermonTitle(e.target.value)}>
          </TextField>
          <TextField placeholder='Enter link here' 
            value={link} 
            onChange={e => setLink(e.target.value)}>
          </TextField>
          <Button onClick={e => handleSubmit(e)}>Transcribe</Button>
        </Stack>
        <Typography fontSize='3xl'>
          {id}
        </Typography>
      </Stack>
    </>    
  )
}
