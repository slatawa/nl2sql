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

import LanguageChanger from "@/navigation/LanguageChanger"
import ThemeChanger from "@/navigation/ThemeChanger"
import { AppConfig } from "@/utils/AppConfig"
import { classNames } from "@/utils/dom"
import { INavigationItem } from "@/utils/types"
import { Disclosure, Menu } from "@headlessui/react"
import { User } from "firebase/auth"
import { useTranslation } from "react-i18next"
import { Link, useMatch } from "react-router-dom"

const Nav = ({
  user,
  mainRoutes,
  userRoutes,
}: {
  user: User
  mainRoutes: INavigationItem[]
  userRoutes: INavigationItem[]
}) => {
  const { t } = useTranslation()

  return (
    <>
      <div className="mb-8 min-h-full">
        <Disclosure as="nav" className="border-base-300 bg-base-100 border-b">
          {({ open }) => (
            <>
              <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
                <div className="flex h-16 items-center justify-between">
                  <div className="flex">
                    <Link to="/">
                      <div className="flex shrink-0 items-center">
                        <img
                          className="mr-4"
                          src={AppConfig.simpleLogoPath}
                          alt={t("app.title")}
                          height={33}
                          width={41}
                        />
                        <div className="text-base-content text-xl font-bold">
                          {t("app.title")}
                        </div>
                      </div>
                    </Link>

                    <div className="hidden sm:-my-px sm:ml-10 sm:flex sm:space-x-8">
                      {mainRoutes.map((item) => (
                        <Link
                          to={item.href}
                          key={item.name}
                          className={classNames(
                            useMatch(item.href)
                              ? "border-primary"
                              : "text-faint hover:text-normal text-base-content hover:border-base-300 border-transparent",
                            "text-base-content inline-flex items-center border-b-2 px-1 pt-1 text-sm font-medium",
                          )}
                          aria-current={
                            useMatch(item.href) ? "page" : undefined
                          }
                        >
                          {t(item.name)}
                        </Link>
                      ))}
                    </div>
                  </div>
                  <div className="hidden gap-x-2 sm:ml-6 sm:flex sm:items-center">
                    <ThemeChanger />
                    <LanguageChanger />

                    {/* Profile dropdown */}
                    <Menu as="div" className="relative ml-3">
                      <Menu.Button
                        data-testid="user-menu-button"
                        className="bg-base-100 focus:ring-primary flex max-w-xs items-center rounded-full text-sm focus:outline-none focus:ring-2 focus:ring-offset-2"
                      >
                        <span className="sr-only">Open user menu</span>
                        {user?.photoURL ? (
                          <img
                            data-testid="user-img"
                            className="h-8 w-8 rounded-full"
                            src={user.photoURL}
                            alt={user.displayName || ""}
                          />
                        ) : (
                          <div className="i-heroicons-user-circle text-base-content/75 h-10 w-10" />
                        )}
                      </Menu.Button>
                      <Menu.Items className="bg-base-100 ring-base-300 absolute right-0 z-10 mt-2 w-48 origin-top-right rounded-md py-1 shadow-lg ring-1 focus:outline-none">
                        {userRoutes.map((item) => {
                          const classes = (active: boolean) =>
                            classNames(
                              active
                                ? "text-primary bg-base-100"
                                : "text-base-content",
                              "block px-4 py-2 text-sm font-semibold cursor-pointer hover:text-primary",
                            )
                          if (item.ssr) {
                            return (
                              <Menu.Item key={item.name}>
                                {({ active }) => (
                                  <div>
                                    <Link to={item.href}>
                                      <a className={classes(active)}>
                                        {t(item.name)}
                                      </a>
                                    </Link>
                                  </div>
                                )}
                              </Menu.Item>
                            )
                          }
                          return (
                            <Menu.Item key={item.name}>
                              {({ active }) => (
                                <Link
                                  to={item.href}
                                  key={item.name}
                                  className={classes(active)}
                                >
                                  {t(item.name)}
                                </Link>
                              )}
                            </Menu.Item>
                          )
                        })}
                      </Menu.Items>
                    </Menu>
                  </div>
                  <div className="-mr-2 flex items-center sm:hidden">
                    {/* Mobile menu button */}
                    <Disclosure.Button className="bg-base-100 text-base-content hover:bg-base-200 hover:text-base-content focus:ring-primary inline-flex items-center justify-center rounded-md p-2 focus:outline-none focus:ring-2 focus:ring-offset-2">
                      <span className="sr-only">Open main menu</span>
                      {open ? (
                        <div
                          className="i-heroicons-x-mark h-6 w-6"
                          aria-hidden="true"
                        />
                      ) : (
                        <div
                          className="i-heroicons-bars-3 h-6 w-6"
                          aria-hidden="true"
                        />
                      )}
                    </Disclosure.Button>
                  </div>
                </div>
              </div>

              {/* Mobile Menu */}
              <Disclosure.Panel className="shadow-lg sm:hidden">
                <div className="space-y-1 pb-3 pt-2">
                  {mainRoutes.map((item) => (
                    <Link to={item.href} key={item.name}>
                      <Disclosure.Button
                        key={item.name}
                        as="div"
                        className={classNames(
                          useMatch(item.href)
                            ? "border-primary bg-base-100 text-primary"
                            : "text-base-content hover:border-base-300 hover:bg-base-200 border-transparent",
                          "block border-l-4 py-2 pl-3 pr-4 text-base font-medium",
                        )}
                        aria-current={useMatch(item.href) ? "page" : undefined}
                      >
                        {t(item.name)}
                      </Disclosure.Button>
                    </Link>
                  ))}
                </div>
                <div className="border-base-200 border-t pb-3 pt-4">
                  <div className="flex items-center px-4">
                    <div className="flex-shrink-0">
                      {user?.photoURL ? (
                        <img
                          data-testid="user-img-mobile"
                          className="h-8 w-8 rounded-full"
                          src={user.photoURL}
                          alt={user.displayName || ""}
                        />
                      ) : (
                        <></>
                      )}
                    </div>
                    <div className="ml-3">
                      <div className="text-base-content text-base font-medium">
                        {user?.displayName}
                      </div>
                      <div className="text-base-content text-sm font-medium">
                        {user.email}
                      </div>
                    </div>
                  </div>
                  <div className="mt-3 space-y-1">
                    {userRoutes.map((item) => (
                      <Link to={item.href} key={item.name}>
                        <Disclosure.Button
                          key={item.name}
                          as="div"
                          className="text-base-content hover:bg-base-200 hover:text-base-content block px-4 py-2 text-base font-medium"
                        >
                          {t(item.name)}
                        </Disclosure.Button>
                      </Link>
                    ))}
                  </div>
                </div>
              </Disclosure.Panel>
            </>
          )}
        </Disclosure>
      </div>
    </>
  )
}

export default Nav
