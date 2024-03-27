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

import React, { useState } from "react"

interface InfoModalProps {
  modalState: boolean
  handleClick: Function
  title: string
  data: string[]
  customWidth: string
}

const InfoModal: React.FC<InfoModalProps> = ({
  modalState,
  handleClick,
  title,
  data,
  customWidth,
}) => {
  const handleClose = () => {
    console.log("Closing the InfoModal")
    handleClick()
  }

  const handleOk = () => {
    handleClick(false)
  }

  const handleCopy = async (text: string) => {
    
    await navigator.clipboard.writeText(text)
    setCopiedText(text)
    setShowTick(true)
    setTimeout(() => {
      setShowTick(false)
    }, 2000)
  }

  const [copiedText, setCopiedText] = useState("")
  const [showTick, setShowTick] = useState(false)

  return (
    <>
      {modalState && (
        <div className="bottom-0 left-0 right-0 top-0 z-50 z-50 flex items-center justify-center bg-opacity-50">
          <div
            className="absolute bottom-0 left-0 right-0 top-0 bg-black opacity-50"
            style={{ backdropFilter: "blur(20px)" }}
          ></div>
          <div
            className={`border-base-300 bg-base-100 relative rounded-2xl border p-4 shadow-xl ${customWidth}`}
          >
            <div className="flex justify-between">
              <h3 className="text-2xl font-semibold">{title}</h3>
              <div
                className="i-heroicons-x-mark h-6 w-6 cursor-pointer"
                onClick={handleClose}
              />
            </div>
            <div className="mt-4">
              {data.length > 0 ? (
                data?.map((item, index) => (
                  <div key={index} className="mb-2 flex items-center">
                    <p className="text-dim">
                      ({index + 1}) {item}
                    </p>
                    {showTick && copiedText === item ? (
                      <div className="i-heroicons-check-circle ml-2 h-5 w-10 text-green-500" />
                    ) : (
                      <div
                        className="i-heroicons-clipboard-document-check ml-2 h-5 w-10 cursor-pointer text-gray-500"
                        onClick={() => handleCopy(item)}
                      />
                    )}
                  </div>
                ))
              ) : (
                <p>No information available.</p>
              )}
            </div>
            <div className="mt-6 flex justify-center">
              <button
                className="btn-primary btn-sm btn text-primary-content mb-4 mt-1 flex gap-2"
                onClick={handleOk}
              >
                OK
              </button>
            </div>
          </div>
        </div>
      )}
    </>
  )
}

export default InfoModal
