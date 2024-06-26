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

// uno.config.ts
import themes from "daisyui/src/theming"
import {
  defineConfig,
  presetIcons,
  presetTypography,
  presetUno,
  presetWebFonts,
} from "unocss"
import { presetDaisy } from "unocss-preset-daisy"

export default defineConfig({
  preflights: [
    {
      getCSS: ({ theme }) => {
        // console.log({ theme })
        return `
        * {
          min-width: 0;
          min-height: 0;
        }

        input {
          padding: 0rem 1rem;
          background-color: ${theme.colors.primary};
        }

        textarea {
          background-color: ${theme.colors.primary};
        }
      `
      },
    },
  ],
  presets: [
    presetUno(),
    presetIcons(),
    presetWebFonts(),
    presetTypography(),
    // presetAttributify({ /* preset options */}),
    presetDaisy({
      themes: [
        {
          light: {
            ...themes["[data-theme=light]"],
            "base-100": "#ffffff",
            "base-200": "#f2f3f5",
            "base-300": "#e9ebf0",
            primary: "#4285f4",
            "primary-content": "#edeff2",
            secondary: "#24c1e0",
            "secondary-content": "#e9f1f2",
            accent: "#1E2043",
            "accent-content": "#e4e4eb",
            neutral: "#1E2D43",
            "neutral-content": "#d5d7db",

            info: "#bfdbfe",
            "info-content": "#01152e",
            success: "#1E8E3E",
            "success-content": "#e9f0eb",
            warning: "#F9AB00",
            "warning-content": "#211700",
            error: "#D93025",
            "error-content": "#ede7e6",
          },
        },
      ],
    }),
    // ...custom presets
  ],
})
