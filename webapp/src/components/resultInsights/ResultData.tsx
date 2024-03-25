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

import { IResultData } from "@/utils/types"
import {
  SortingState,
  createColumnHelper,
  flexRender,
  getCoreRowModel,
  getSortedRowModel,
  useReactTable,
} from "@tanstack/react-table"
import React, { useEffect, useState } from "react"
import { useTranslation } from "react-i18next"
interface ResultDataProps {
  tableData: any
}

const ResultData: React.FC<ResultDataProps> = ({ tableData }) => {
  const { t } = useTranslation()

  const columnHelper = createColumnHelper<any>()

  const columns = [
    columnHelper.accessor("question", {
      header: () => <span>{t("Question")}</span>,
      cell: (info) => {
        const question = info.getValue()
        return <span className="text-justify text-sm">{question}</span>
      },
      footer: (info) => info.column.id,
    }),
    columnHelper.accessor("data", {
      header: () => <span>{t("Data")}</span>,
      cell: (info) => {
        const data = info.getValue()
        return (
          <>
            <span className="flex justify-center gap-1 text-justify text-sm">
              {!data ? (
                <span className="flex gap-1 text-sm font-semibold">
                  In Progress
                  <span className="loading loading-bars loading-xs text-primary"></span>
                </span>
              ) : (
                data
              )}
            </span>
          </>
        )
      },
      footer: (info) => info.column.id,
    }),
    columnHelper.accessor("sql", {
      header: () => <span>{t("SQL")}</span>,
      cell: (info) => {
        const sql = info.getValue()
        return (
          <>
            <span className="flex justify-center gap-1 text-justify text-sm">
              {!sql ? (
                <span className="flex gap-1 text-sm font-semibold">
                  In Progress
                  <span className="loading loading-bars loading-xs text-primary"></span>
                </span>
              ) : (
                sql
              )}
            </span>
          </>
        )
      },
      footer: (info) => info.column.id,
    }),
  ]

  const [data, setData] = useState<IResultData[]>([])
  const [sorting, setSorting] = useState<SortingState>([])

  const table = useReactTable({
    data,
    columns,
    state: {
      sorting,
    },
    onSortingChange: setSorting,
    getCoreRowModel: getCoreRowModel(),
    getSortedRowModel: getSortedRowModel(),
  })

  useEffect(() => {
    setData(tableData)
  }, [tableData])

  return (
    <div className="bg-base-100 mt-4 w-full overflow-auto">
      <table className="divide-base-200 border-base-200 table w-full divide-y rounded-md border">
        <thead className="bg-base-200">
          {table.getHeaderGroups().map((headerGroup) => (
            <tr key={headerGroup.id}>
              {headerGroup.headers.map((header) => {
                return (
                  <th
                    key={header.id}
                    colSpan={header.colSpan}
                    className="rounded-none p-2"
                  >
                    {header.isPlaceholder ? null : (
                      <div
                        {...{
                          className: header.column.getCanSort()
                            ? "cursor-pointer select-none"
                            : "",
                          onClick: header.column.getToggleSortingHandler(),
                        }}
                      >
                        {flexRender(
                          header.column.columnDef.header,
                          header.getContext(),
                        )}
                        {{
                          asc: (
                            <span className="i-heroicons-arrow-up ml-1 inline-block h-3 w-3" />
                          ),
                          desc: (
                            <span className="i-heroicons-arrow-down ml-1 inline-block h-3 w-3" />
                          ),
                        }[header.column.getIsSorted() as string] ?? null}
                      </div>
                    )}
                  </th>
                )
              })}
            </tr>
          ))}
        </thead>
        <tbody className="divide-base-200 bg-base-100 divide-y-2 text-center">
          {!data.length ? (
            <tr>
              <td colSpan={3} className="p-6">
                Please search to see records!
              </td>
            </tr>
          ) : (
            <>
              {table.getRowModel().rows.map((row) => (
                <tr key={row.id}>
                  {row.getVisibleCells().map((cell) => (
                    <td key={cell.id} className="p-2">
                      {flexRender(
                        cell.column.columnDef.cell,
                        cell.getContext(),
                      )}
                    </td>
                  ))}
                </tr>
              ))}
            </>
          )}
        </tbody>
      </table>
    </div>
  )
}

export default ResultData
