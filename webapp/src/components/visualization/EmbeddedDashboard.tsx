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

import React, { useEffect, useState } from "react"
import axios, { AxiosResponse } from "axios"
import Loading from "@/navigation/Loading"

interface EmbeddedDashboardProps {
  id: number | string
  setError?: (errorMsg: string) => void
}

const EmbeddedDashboard: React.FC<EmbeddedDashboardProps> = ({
  id,
  setError,
}) => {
  const [loading, setLoading] = useState<boolean>(true)

  useEffect(() => {
    const embedCtrRef = document.getElementById("embedCtr")

    if (embedCtrRef) {
      const authUrl = `${import.meta.env.VITE_PUBLIC_LOOKER_DEPLOYED_END_POINT}/looker-sso/`

      axios
        .post(authUrl, { id: id })
        .then((response: AxiosResponse) => {
          const ssoUrl = response.data.url
          embedCtrRef.innerHTML = ""
          const iframe = document.createElement("iframe")
          iframe.src = ssoUrl
          iframe.style.width = "100%"
          iframe.style.height = "100vh"
          iframe.allowFullscreen = true
          embedCtrRef.appendChild(iframe)
        })
        .catch((error: any) => {
          console.error("Error fetching SSO URL", error)
          if (setError) {
            setError("Failed to load dashboard. Please try again later.")
          }
        })
        .finally(() => {
          setLoading(false)
        })
    }
  }, [id, setError])

  return (
    <div className="w-full">
      {loading && <Loading />}
      <div
        id="embedCtr"
        className="h-full w-full"
        style={{ height: "100vh" }}
      ></div>
    </div>
  )
}

export default EmbeddedDashboard
