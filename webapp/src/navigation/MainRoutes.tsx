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

import RouteList from "@/navigation/RouteList"
import { INavigationItem } from "@/utils/types"

// These are i18n link names, put the label in the common.json file
const links: INavigationItem[] = [
  {
    name: "link.dashboard",
    href: "/dashboard",
    show: () => true,
    icon: <div className="i-heroicons-home text-primary-content h-8 w-8" />,
  },
  // {
  //   name: "link.users",
  //   href: "/users",
  //   show: () => true,
  //   icon: (
  //     <div className="i-heroicons-user-group text-primary-content h-8 w-8" />
  //   ),
  // },
  // {
  //   name: "link.firestore",
  //   href: "/firestore",
  //   show: () => true,
  //   icon: <div className="i-heroicons-fire text-primary-content h-8 w-8" />,
  // },
  // {
  //   name: "link.icons",
  //   href: "/icons",
  //   show: () => true,
  //   icon: <div className="i-heroicons-photo text-primary-content h-8 w-8" />,
  // },
]

const MainRoutes = () => {
  return <RouteList links={links} />
}

export default MainRoutes
