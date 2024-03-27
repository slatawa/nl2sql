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

import { useState } from "react"
import HistoricalData from "@/components/resultInsights/HistoricalData"
import LookerDisplay from "@/components/visualization/LookerDisplay"

interface DashboardProps {}

const Dashboard: React.FunctionComponent<DashboardProps> = () => {
  const [question, setQuestion] = useState<string>("")
  const [isVisualization, setVisualization] = useState<boolean>(false)

  const handleQuestion = (question_: string) => {
    setQuestion(question_)
  }

  const handleLooker = (state: boolean) => {
    setVisualization(state)
  }

  return (
    <>
      <div className="border-primary bg-base-100 min-h-[calc(100vh-6rem)] rounded-md border-2 border-opacity-30 px-8 py-4 shadow-xl">
        <HistoricalData
          sendQuestionToParent={handleQuestion}
          visibleLooker={handleLooker}
        />
        {!!isVisualization && <LookerDisplay question={question} />}
      </div>
    </>
  )
}
export default Dashboard
