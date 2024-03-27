import { NextApiHandler, NextApiRequest, NextApiResponse } from "next"
import {
  enableCors,
  verifyUser,
  isvalidDomainForUser,
} from "@/utils/firebaseAdminFunctions"

export function withAuth(handler: NextApiHandler) {
  return async (req: NextApiRequest, res: NextApiResponse) => {
    await enableCors(req, res)
    try {
      const user = await verifyUser(req)
      if (!user || !user.email) {
        return res.status(401).json({
          message: "Unauthorized",
        })
      }
      if (user.email && !isvalidDomainForUser(user.email)) {
        return res.status(401).json({
          message: "Unauthorized",
        })
      }
    } catch (_) {
      return res.status(401).json({
        message: "Unauthorized",
      })
    }

    return handler(req, res)
  }
}
