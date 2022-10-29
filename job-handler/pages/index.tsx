import {Box, Button, Center, Heading, HStack, Input, Text, VStack} from '@chakra-ui/react'
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
      <VStack spacing={3}>
        <Center p='5'>
          <Box>
            <Heading>
              Grace Life London - Scribe Service
            </Heading>
          </Box>
        </Center>
        <Text fontSize='4xl'>
          Enter Youtube Link from Grace Life London to Transcribe
        </Text>
        <HStack>
          <Input placeholder='Title Of Sermon'
            value={sermonTitle} 
            onChange={e => setSermonTitle(e.target.value)}>
          </Input>
          <Input placeholder='Enter link here' 
            value={link} 
            onChange={e => setLink(e.target.value)}>
          </Input>
        </HStack>
        <Button onClick={e => handleSubmit(e)}>Transcribe</Button>
        <Text fontSize='3xl'>
          {id}
        </Text>
      </VStack>
    </>    
  )
}
