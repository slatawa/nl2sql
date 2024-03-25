import * as firebaseAdmin from "firebase-admin"
import { envOrFail } from "@/utils/env"
import { applicationDefault } from "firebase-admin/app"
import { getFirestore } from "firebase-admin/firestore"

const APP_NAME = "[DEFAULT]"

// Connect to the emulator if we're in development
// if (process.env.NODE_ENV === "development") {
//   console.debug("Initializing Firebase Admin in dev mode")
//   process.env["FIRESTORE_EMULATOR_HOST"] = "localhost:8080"
// }

const projectId = envOrFail(
  "NEXT_PUBLIC_FIREBASE_PROJECT_ID",
  import.meta.env.VITE_FIREBASE_PROJECT_ID,
)

const credential = applicationDefault()
const config: firebaseAdmin.AppOptions = {
  credential,
  databaseURL: `https://${projectId}.firebaseio.com`,
  projectId,
}

const getApp = () => {
  return (
    firebaseAdmin.apps.find((a) => a?.name === APP_NAME) ||
    firebaseAdmin.initializeApp(config)
  )
}

const db = getFirestore(getApp())

export { firebaseAdmin, getApp, db }
