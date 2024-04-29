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

import { INavigationItem, IAppConfig } from "@/utils/types"
import { envOrFail } from "./env"

const projectId = envOrFail(
  "VITE_FIREBASE_PROJECT_ID",
  import.meta.env.VITE_FIREBASE_PROJECT_ID,
)

const GPS_RIT_DOMAINS: RegExp[] = [/@google\.com$/i, /@\w+\.altostrat\.com$/i]

const CUSTOMER_APPROVED_EMAILS: RegExp[] = [
  /^acolver@google.com$/i,
  /^aminaalsherif@google.com$/i,
  /^pratapram@google.com$/i,
  /^shailendrau@google.com$/i,
  /^tliakos@google.com$/i,
]

// Make sure you update your public/locales JSON files
export const AppConfig: IAppConfig = {
  siteName: "NL2SQL POC",
  locale: "en",
  logoPath: "/assets/images/google.png",
  simpleLogoPath: "/assets/images/google.png",
  imagesPath: "/assets/images",
  theme: "light",
  authProviders: ["google", "password"],
  authorizedDomains:
    projectId === "sl-test-project-353312" ? GPS_RIT_DOMAINS : CUSTOMER_APPROVED_EMAILS,
}

// // These are i18n link names, put the label in the common.json file
// export const MainNavigation: INavigationItem[] = [
//   { name: "link.about", href: "/about", show: () => true },
//   { name: "link.users", href: "/users", show: () => true },
//   { name: "link.firestore", href: "/firestore", show: () => true },
//   { name: "link.icons", href: "/icons", show: () => true },
//   { name: "link.table", href: "/table", show: () => true },
// ]

export const UserNavigation: INavigationItem[] = [
  { name: "link.profile", href: "/profile", show: () => true },
  { name: "link.settings", href: "/settings", show: () => true },
  { name: "link.signout", href: "/signout", show: () => true },
]

export const FooterNavigation: INavigationItem[] = [
  { name: "link.about", href: "/about", show: () => true },
]

// Full list of scopes: https://developers.google.com/identity/protocols/oauth2/scopes
export const OAuthScopes: string[] = []
