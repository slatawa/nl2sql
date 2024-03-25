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

import Sidebar from "@/navigation/Sidebar"
import MainContent from "@/templates/MainContent"
import { User } from "firebase/auth"
import "@/styles/global.css"

interface AuthenticatedProps {
  user: User
}

const Authenticated: React.FunctionComponent<AuthenticatedProps> = ({
  user,
}) => {
  return (
    <div className="from-primary to-primary/90 flex min-h-screen gap-x-4 overflow-x-hidden bg-gradient-to-b p-0 shadow md:py-3 md:pr-3">
      <div className="hide-scrollbar hidden shrink-0 overflow-y-scroll md:block">
        <Sidebar />
      </div>

      <div className="flex-grow">
        <MainContent user={user} />
      </div>
    </div>
  )
}

export default Authenticated
