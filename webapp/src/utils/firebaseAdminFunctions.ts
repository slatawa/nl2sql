import * as firebaseAdmin from "firebase-admin"
import { getApp } from "@/utils/firebaseAdmin"
import { NextApiRequest, NextApiResponse } from "next"
//@ts-ignore
import NextCors from "nextjs-cors"

const validUserDomains = ["sakunchala.altostrat.com", "google.com"]
export const enableCors = async (req: NextApiRequest, res: NextApiResponse) => {
  await NextCors(req, res, {
    // Options
    methods: ["GET", "PUT", "PATCH", "POST", "DELETE", "OPTIONS"],
    //TODO Need to lock the origin
    origin: "*",
    optionsSuccessStatus: 200,
  })
}

export const verifyUser = async (req: NextApiRequest) => {
  let token = req.cookies.token

  if (!token && req.headers.authorization) {
    token = req.headers.authorization.split(/\s+/)[1]
  }

  if (!token) {
    throw new Error("No token found")
  }

  return await decodeToken(token)
}

export const decodeToken = async (token: string) => {
  try {
    return await firebaseAdmin.auth(getApp()).verifyIdToken(token)
  } catch (error) {
    console.error(error)
    return null
  }
}

const getDomainFromEmail = (email: string) => {
  const [_, domain] = email.split("@")
  return domain ?? null
}

export const isvalidDomainForUser = (email: string): boolean => {
  if (!email) return false
  const domain = getDomainFromEmail(email)
  if (!domain) return false
  return validUserDomains.includes(domain)
}
