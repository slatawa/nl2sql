// Copyright 2024 Google LLC
//
// Licensed under the Apache License, Version 2.0 (the License);
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     https://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

import InfoModal from "@/components/resultInsights/InfoModal"
import { classNames } from "@/utils/dom"
import axios from "axios"
import { useEffect, useState } from "react"
import { v4 as uuidv4 } from "uuid"
import { IResultData } from "@/utils/types"
import ResultDataDisplay from "@/components/resultInsights/ResultDataDisplay"
import Loading from "@/navigation/Loading"
import { questionsArr } from "@/utils/data"
import { PUBLIC_LOOKS_CONFIG } from "@/utils/publicLooksConfig"

interface HistoricalProps {
  sendQuestionToParent?: (() => void) | undefined
  visibleLooker: () => void
}

const HistoricalData: React.FC<HistoricalProps> = ({
  sendQuestionToParent,
  visibleLooker,
}) => {
  const [modalState, setModalState] = useState(false)
  const [question, setQuestion] = useState("")
  const [isLoading, setLoading] = useState<boolean>(false)
  const [resultData, setResultData] = useState<IResultData[]>([])
  const [displayVisualization, setDislayVisualization] =
    useState<boolean>(false)
  const [toggleColor, setToggleColor] = useState<boolean>(false)

  const normalizeText = (text?: string) => {
    return text?.toLowerCase().replace(/[^a-z0-9\s]/g, "") ?? ""
  }

  const normalizedQuestion = normalizeText(question)

  const defaultAnswer: IResultData = {
    data: "Whoa there! This question is venturing into non Proof of Concept territory. Please request expanding capabilities with the NL2SQL team.",
    question,
    sql: "",
    status: false,
    unique_id: "",
  }

  const handleClick = (state: boolean) => {
    setModalState(state)
  }
  const handleSetQuestion = (e: React.ChangeEvent<HTMLInputElement>) => {
    setResultData([])
    visibleLooker(false)
    setQuestion(e.target.value)

  }

  const getResults = async (url: string) => {
    try {
      const response = await axios.get(url)
      const contentType = response.headers["content-type"]
      if (contentType?.includes("application/json")) {
        const result: IResultData[] = response.data.filter(
          (item: IResultData) => item.question === question,
        )
        if (!result.length) {
          setResultData([defaultAnswer])
          return
        }
        setResultData(result)
      } else {
        console.error("Unexpected response type:", contentType)
        throw new Error("Unexpected response type")
      }
    } catch (error) {
      console.error("Fetching questions failed, using dummy data", error)
    } finally {
      setLoading(false)
      if (!resultData.length)
        return (
          <span className="flex justify-center text-sm font-semibold">
            No records found!
          </span>
        )
    }
  }

  const handleQuestion = async () => {
    visibleLooker(false)
    setResultData([])
    setToggleColor(false)
    setLoading(true)

    const url: string = import.meta.env.VITE_PUBLIC_QA_API_ENPOINT_1
    const payload = {
      question: question,
      unique_id: uuidv4(),
    }
  
    const apiConfig = {
      headers: {
        "Content-Type": "application/json;charset=UTF-8",
      },
      displayVisualization,
    }
    await axios
      .post(url, payload, apiConfig)
      .then(async (res) => {
        if (res.status === 200) {
          await getResults(import.meta.env.VITE_PUBLIC_QA_API_ENPOINT_2)
        }
      })
      .catch((error) => {
        console.error(error)
        setTimeout(() => {
          setResultData([defaultAnswer])
          setLoading(false)
        }, 2000)
        return
      })
      .finally(() => setLoading(false))
  }

  const tableView = () => {
    return <ResultDataDisplay tableData={resultData[0]} />
  }

  const toggleChange = (value: boolean) => {
    setToggleColor(value)
    visibleLooker(value)
  }

  useEffect(() => {
    if (sendQuestionToParent) {
      sendQuestionToParent(question)
    }

    if (question) {
      const matchingKey = Object.keys(PUBLIC_LOOKS_CONFIG).find(
        (key) => normalizeText(key) === normalizedQuestion,
      )
      if (matchingKey) {
        setDislayVisualization(true)
      } else {
        setDislayVisualization(false)
      }
    } else {
      setDislayVisualization(false)
    }
  }, [question])

  return (
    <>
      <div className="my-4">
        <div className="text-primary flex text-5xl font-semibold">
          Hello, Data Analysis Executive
        </div>
        <div className="text-base-content mt-4 flex text-3xl font-semibold opacity-60">
          How can I help you today?
        </div>
      </div>
      <form
        className="relative mt-8 flex items-center justify-center gap-4"
        onSubmit={(e: React.SyntheticEvent) => {
          e.preventDefault()
          handleQuestion()
        }}
      >
        <div
          className="i-heroicons-information-circle text-primary h-8 w-8 cursor-pointer"
          onClick={() => setModalState(true)}
        />
        <div className="relative flex-grow">
          <div className="i-heroicons-magnifying-glass text-base-content/50 pointer-events-none absolute left-3 top-4 h-6 w-6" />
          <input
            className="placeholder:text-dim w-full max-w-5xl rounded-full border py-3 pl-12 pr-5 text-lg"
            placeholder="Enter your question here..."
            id="searchWidgetTrigger"
            type="text"
            autoComplete="off"
            value={question}
            onChange={handleSetQuestion}
          />
        </div>
        <button
          type="submit"
          id="handleTransportationSubmit"
          className={classNames(
            "btn btn-primary text-primary-content",
            !question || isLoading ? "btn-disabled" : "",
          )}
        >
          Search
        </button>
      </form>
      {isLoading && (
        <div className="py-8">
          <Loading />
        </div>
      )}
      {!!resultData?.length && tableView()}

      {displayVisualization && !!resultData?.length && (
        <div className="px-10">
          <div className="text-lg">
            Would you like a visualization of this answer?
          </div>
          <div className="py-2">
            <button
              className="text w-fit px-4 text-sm font-bold"
              onClick={() => toggleChange(toggleColor ? false : true)}
            >
              <div className="badge badge-primary badge-outline">
                Show Visualization
              </div>
            </button>
          </div>
        </div>
      )}

      <div>
        {modalState && (
          <div className="fixed bottom-0 left-0 right-0 top-0 z-50 flex items-center justify-center">
            <InfoModal
              modalState={modalState}
              handleClick={handleClick}
              title="Sample question(s)"
              data={questionsArr}
              customWidth="w-auto"
            />
          </div>
        )}
      </div>
    </>
  )
}

export default HistoricalData
