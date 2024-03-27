import { openDB } from "idb"
import { IResultData } from "@/utils/types"
const VERSION = 1
const collectionName = import.meta.env
  .VITE_PUBLIC_CDII_DEMO_LOCAL_CACHE_COLLECTION_NAME

const initDB = async () => {
  const db = await openDB(
    import.meta.env.VITE_PUBLIC_CDII_DEMO_LOCAL_CACHE_DB,
    VERSION,
    {
      upgrade(db) {
        if (!db.objectStoreNames.contains(collectionName)) {
          db.createObjectStore(collectionName, { keyPath: "unique_id" })
        }
      },
    },
  )
  return db
}

export const getAllDataFromDB = async (): Promise<IResultData[]> => {
  const db = await initDB()
  return db.transaction(collectionName).objectStore(collectionName).getAll()
}

export const saveMultipleDataToDB = async (data: IResultData[]) => {
  const db = await initDB()
  const tx = db.transaction(collectionName, "readwrite")
  for (const item of data) {
    tx.objectStore(collectionName).put(item)
  }
  await tx.done
}

export const getDataFromDB = async (question: string) => {
  const db = await initDB()
  return db
    .transaction(collectionName)
    .objectStore(collectionName)
    .get(question)
}

export const saveDataToDB = async (data: IResultData) => {
  const db = await initDB()
  const tx = db.transaction(collectionName, "readwrite")
  tx.objectStore(collectionName).put(data)
  await tx.done
}
