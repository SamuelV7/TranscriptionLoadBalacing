// Next.js API route support: https://nextjs.org/docs/api-routes/introduction
import type { NextApiRequest, NextApiResponse } from 'next'
import redis from "./lib/redis"
type Data = {
  name: string
}

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse<Data>
) {
  let data = req.body
  // console.log(data)
  data.title = data.title+"-"+Date.now()
  // check if already in database
  let dataExists = await redis.get(data.link)
  if (dataExists == null){
    redis.lpush('sermon-scribe-queue', JSON.stringify(data))
    redis.set(data.link, "pending")
    return res.status(200).json({'name': 'Already Submitted'})
  }
  res.status(200).json({'name': data.title})
}
