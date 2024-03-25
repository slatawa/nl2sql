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

import { classNames } from "@/utils/dom"
import { IResultData } from "@/utils/types"
import { HandThumbUpIcon, HandThumbDownIcon } from "@heroicons/react/24/outline"
import { useState } from "react"

interface DataTableProps {
  tableData: IResultData
}

const ResultDataDisplay: React.FC<DataTableProps> = ({ tableData }) => {
  const [isLike, setIsLike] = useState<boolean>(false)
  const [isDislike, setIsDislike] = useState<boolean>(false)
  const [isSQL, setIsSQL] = useState<boolean>(false)

  const responseLike = (state: boolean) => {
    setIsLike(state)
    setIsDislike(false)
  }
  const responseDislike = (state: boolean) => {
    setIsDislike(state)
    setIsLike(false)
  }

  const showSQL = (state: boolean) => {
    setIsSQL(state)
  }

  if (!tableData) return
  return (
    <div className="p-4">
      <div className="rounded-lg p-6">
        {/* <div className="text-lg">
          <span className="font-bold">Question:</span> {tableData.question}
        </div> */}
        {tableData.data && (
          <div className="text-lg">
            {/* <span className="font-bold">Answer:</span>  */}
            <span className="font-semibold">{tableData.data}</span>
          </div>
        )}
        <div className="relative mx-4 flex gap-4 py-2">
          <button
            className="text px-4 text-sm font-bold"
            onClick={() => responseLike(isLike ? false : true)}
          >
            <HandThumbUpIcon
              title="Good response"
              className={classNames(
                "h-8 w-8 p-1",
                isLike ? "text-success" : "",
              )}
            />
          </button>
          <button
            className="text text-sm font-bold"
            onClick={() => responseDislike(isDislike ? false : true)}
          >
            <HandThumbDownIcon
              title="Good response"
              className={classNames(
                "h-8 w-8 p-1",
                isDislike ? "text-error" : "",
              )}
            />
          </button>
          {tableData.sql && (
            <button
              className="text px-4 text-sm font-bold"
              onClick={() => showSQL(isSQL ? false : true)}
            >
              <div className="badge badge-primary badge-outline">Show SQL</div>
            </button>
          )}
        </div>

        {tableData.sql && isSQL && (
          <div tabIndex={0} className="no-border collapse-open collapse">
            <div className="collapse-content bg-base-200 overflow-x-scroll py-2">
              <pre>
                {tableData.sql
                  .replaceAll(/\sfrom\s/gi, "\nFROM ")
                  .replaceAll(/\swhere\s/gi, "\nWHERE ")
                  .replaceAll(/\sand\s/gi, "\nAND ")
                  .replaceAll(/\sgroup by\s/gi, "\nGROUP BY ")
                  .replaceAll(/\sorder by\s/gi, "\nORDER BY ")
                  .replaceAll(/\slimit\s/gi, "\nLIMIT ")}
              </pre>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}

export default ResultDataDisplay
