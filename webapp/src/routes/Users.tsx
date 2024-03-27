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

import Loading from "@/navigation/Loading"
import { fetchUsers } from "@/utils/api"
import { IUser } from "@/utils/types"
import { useQuery } from "@tanstack/react-query"
import { AxiosError } from "axios"

interface UsersProps {}

const Users: React.FC<UsersProps> = () => {
  const { isLoading, error, data: users } = useQuery(["Users"], fetchUsers)

  if (isLoading) return <Loading />

  if (error) {
    let message = "Uh oh, something went wrong"
    if (error instanceof AxiosError) {
      message = error.response?.data?.message ?? error.message
    }

    return <div className="text-error">{message}</div>
  }

  return (
    <>
      <h1 className="mb-4 text-lg font-semibold">
        Using React Query to fetch from API
      </h1>
      {((users ?? []) as IUser[]).map((user) => (
        <div key={`${user.firstName}${user.lastName}`}>
          {user.firstName} {user.lastName}
        </div>
      ))}
    </>
  )
}

export default Users
