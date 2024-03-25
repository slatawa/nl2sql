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

import { useEffect, useState } from "react"
import { PUBLIC_LOOKS_CONFIG } from "@/utils/publicLooksConfig"
import { LookConfig } from "@/utils/types"
import Loading from "@/navigation/Loading"

interface LookerDisplayProps {
  question?: string | undefined
}

const LookerDisplay: React.FC<LookerDisplayProps> = ({ question }) => {
  const [isLoading, setIsLoading] = useState(true)
  const normalizeText = (text?: string) => {
    return text?.toLowerCase().replace(/[^a-z0-9\s]/g, "") ?? ""
  }

  const normalizedQuestion = normalizeText(question)
  let lookConfigs: LookConfig[]

  if (question) {
    const matchingKey = Object.keys(PUBLIC_LOOKS_CONFIG).find(
      (key) => normalizeText(key) === normalizedQuestion,
    )
    lookConfigs = matchingKey
      ? PUBLIC_LOOKS_CONFIG[matchingKey]
      : PUBLIC_LOOKS_CONFIG["default"]
  } else {
    lookConfigs = PUBLIC_LOOKS_CONFIG["default"]
  }

  const isDefaultLook =
    !question ||
    !Object.keys(PUBLIC_LOOKS_CONFIG).find(
      (key) => normalizeText(key) === normalizedQuestion,
    )

  // const iframeStyle = {
  //   width: lookConfigs[0]?.width ?? "100%",
  //   height: lookConfigs[0]?.height ?? "600px",
  //   border: "none",
  // }

  useEffect(() => {
    if (isDefaultLook) {
      setIsLoading(false)
    }
  }, [isDefaultLook])

  return (
    <div>
      <div className="m-2 my-4 text-justify text-lg font-semibold"></div>
      {isLoading && <Loading />}
      {/* {!isDefaultLook && (
        <iframe
          className="max-h-96 w-full"
          src={lookConfig.url}
          style={iframeStyle}
          title={question}
          onLoad={() => setIsLoading(false)}
        ></iframe>
      )} */}
      {!isDefaultLook &&
        lookConfigs.map((lookConfig) => {
          const iframeStyle = {
            width: lookConfig.width ?? "100%",
            height: lookConfig.height ?? "600px",
            border: "none",
          }

          return (
            <div key={lookConfig.url}>
              <iframe
                className="max-h-96 w-full"
                src={lookConfig.url}
                style={iframeStyle}
                title={question}
                onLoad={() => setIsLoading(false)}
              ></iframe>
            </div>
          )
        })}
    </div>
  )
}

export default LookerDisplay
