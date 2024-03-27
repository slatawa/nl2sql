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

import About from "@/routes/About"
import Firestore from "@/routes/FirestoreUsers"
import Home from "@/routes/Home"
import Icons from "@/routes/Icons"
import NotFound from "@/routes/NotFound"
import Profile from "@/routes/Profile"
import SignOut from "@/routes/SignOut"
import Signin from "@/routes/Signin"
import Table from "@/routes/Table"
import Users from "@/routes/Users"
import { User } from "firebase/auth"
import { Route, Routes } from "react-router-dom"
import AnalyticsOutlet from "./AnalyticsOutlet"
import Dashboard from "@/routes/Dashboard"

interface NoAuthAppRouterProps {}

interface AuthAppRouterProps {
  user: User
}

export const AuthAppRouter: React.FunctionComponent<AuthAppRouterProps> = ({
  user,
}) => {
  return (
    <Routes>
      <Route path="/" element={<AnalyticsOutlet />}>
        <Route path="/" element={<Home />} />
        <Route path="/about" element={<About />} />
        <Route path="/icons" element={<Icons />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/profile" element={<Profile user={user} />} />
        <Route path="/signout" element={<SignOut />} />
        <Route path="/table" element={<Table />} />
        <Route path={"/firestore"} element={<Firestore />} />
        <Route path={"/users"} element={<Users />} />
        <Route path="*" element={<NotFound />} />
      </Route>
    </Routes>
  )
}

export const NoAuthAppRouter: React.FunctionComponent<
  NoAuthAppRouterProps
> = () => {
  return (
    <Routes>
      <Route path="/" element={<AnalyticsOutlet />}>
        <Route path="/signin" element={<Signin />} />
      </Route>
    </Routes>
  )
}
