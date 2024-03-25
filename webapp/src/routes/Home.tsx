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

import { logEvent } from "@/utils/firebase"
import { useEffect } from "react"
import { useNavigate } from "react-router-dom"

interface HomeProps {}

const Home: React.FunctionComponent<HomeProps> = ({}) => {
  // Track custom events
  const handleClick = () => logEvent("button_clicked")
  const navigate = useNavigate()

  useEffect(() => {
    navigate("/dashboard")
  })

  return (
    <>
      <button onClick={() => handleClick()} className="btn ml-8">
        Click me
      </button>

      <button className="btn btn-primary ml-8">Click me</button>

      <button className="btn btn-outline btn-primary ml-8">Click me</button>

      <div className="form-control w-full max-w-xs">
        <label className="label" htmlFor="testinput">
          <span className="label-text">Your email address</span>
          <span className="label-text-alt">Alt label</span>
        </label>
        <input
          id="testinput"
          type="text"
          placeholder="Type here"
          className="input input-bordered input-warning w-full max-w-xs"
        />
        <label className="label">
          <span className="label-text-alt text-error">Validation message</span>
        </label>
      </div>
    </>
  )
}

export default Home
