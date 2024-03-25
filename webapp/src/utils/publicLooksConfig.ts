import { LookConfig } from "@/utils/types"

export const PUBLIC_LOOKS_CONFIG: Record<string, LookConfig[]> = {
  "How many people are enrolled in CalFresh?": [
    {
      url: `${import.meta.env.VITE_PUBLIC_LOOKER_DEPLOYED_END_POINT}/embed/public/5dBpWPDd9NSmQvyZN3ZHk2pWNpPTQDPC`,
    },
  ],
  "How many of them live in Los Angeles County?": [
    {
      url: `${import.meta.env.VITE_PUBLIC_LOOKER_DEPLOYED_END_POINT}/embed/public/rNxtY9fRgFdhm5CHNyRYny5mdH76zHMR`,
    },
  ],
  "How has participation in CalFresh changed since 2015?": [
    {
      url: `${import.meta.env.VITE_PUBLIC_LOOKER_DEPLOYED_END_POINT}/embed/public/yd3jdCGmcWXGr4zNwxFj5hCQbxdXx5Sc`,
    },
  ],
  "How have these race and ethnicity trends changed over time?": [
    {
      url: `${import.meta.env.VITE_PUBLIC_LOOKER_DEPLOYED_END_POINT}/embed/public/cvdR2BQC2n83JFMVPXcDQ8s9BSBG3mwG`,
    },
  ],
  "What county has the greatest enrollment in WIC per capita?": [
    {
      url: `${import.meta.env.VITE_PUBLIC_LOOKER_DEPLOYED_END_POINT}/embed/public/D2vV4G8CPHs9Nsp8yR7MnDxrHsPrb4cx`,
    },
  ],
  "Which county has the greatest proportion of CalFresh recipients co-enrolled in at least one additional program?":
    [
      {
        url: `${import.meta.env.VITE_PUBLIC_LOOKER_DEPLOYED_END_POINT}/embed/public/SKW3ZHvrbvgRymFBmYsMGyKzr5vskNBx`,
      },
    ],
  "What about three or more additional programs?": [
    {
      url: `${import.meta.env.VITE_PUBLIC_LOOKER_DEPLOYED_END_POINT}/embed/public/wDj9DptBnw28d8cS5qPq8nMWJjFxH855`,
    },
  ],
  "Which programs have the highest co-enrollment with CalFresh?": [
    {
      url: `${import.meta.env.VITE_PUBLIC_LOOKER_DEPLOYED_END_POINT}/embed/public/sB5YRVDHvY9stBns5RgpTdS7kBkjNDKx`,
    },
  ],
  "How do CalFresh program participation trends differ by race and ethnicity?":
    [
      {
        url: `${import.meta.env.VITE_PUBLIC_LOOKER_DEPLOYED_END_POINT}/embed/public/sxS4NyTDV3xChF6Z9gPWJbkbyBXsKpBK`,
      },
    ],
  "Which five counties have the lowest number of WIC authorized vendors compared to WIC participants?":
    [
      {
        url: `${import.meta.env.VITE_PUBLIC_LOOKER_DEPLOYED_END_POINT}/embed/public/t67vhCM8RKmkSDfczQvw65gddNpM8r52`,
      },
    ],
  "How do infant mortality rates, low birthweight rates, and preterm and very preterm rates compare to WIC enrollment rates by county?":
    [
      {
        url: `${import.meta.env.VITE_PUBLIC_LOOKER_DEPLOYED_END_POINT}/embed/public/Thx8twD29RMjW3SFNKStkRkJy82hxxpV`,
      },
    ],
  "How many Black individuals are served across CalHHS programs?": [
    {
      url: `${import.meta.env.VITE_PUBLIC_LOOKER_DEPLOYED_END_POINT}/embed/public/T7rvbCk69MS7SvcpSmJ4d2VRk4zSvYvn`,
    },
  ],
  "What is the breakdown by program?": [
    {
      url: `${import.meta.env.VITE_PUBLIC_LOOKER_DEPLOYED_END_POINT}/embed/public/BrYCrWRZTkDtKwj3VFcrHDkZfMQM5Z69`,
    },
  ],
  "Has this changed over time?": [
    {
      url: `${import.meta.env.VITE_PUBLIC_LOOKER_DEPLOYED_END_POINT}/embed/public/Mp6SJTC8ybjFsNqkgqShQdrjgCJsDnkD`,
    },
  ],
  "Change over time by program?": [
    {
      url: `${import.meta.env.VITE_PUBLIC_LOOKER_DEPLOYED_END_POINT}/embed/public/p69RPXt7jBb7t3dsgR7Pk6BFtnwXBCnX`,
    },
  ],
  "Which counties have the highest and lowest ratios of providers to enrolled participants in Medi-Cal?":
    [
      {
        url: `${import.meta.env.VITE_PUBLIC_LOOKER_DEPLOYED_END_POINT}/embed/public/bgNbF5YX4DkBzHCrGnn92fZWDH5vPgT3`,
      },
      {
        url: `${import.meta.env.VITE_PUBLIC_LOOKER_DEPLOYED_END_POINT}/embed/public/FVD9rDzZThSN7sjBzdfg5kr4Y73Wb3xy`,
      },
    ],
  "What is the ratio of non-suspended doctors to Medi-Cal members by County?": [
    {
      url: `${import.meta.env.VITE_PUBLIC_LOOKER_DEPLOYED_END_POINT}/embed/public/k7RDvQsfvFT4PkRjFDC35qwZXKHsJDDT`,
    },
  ],
  "What about the ratio to licensed facilities?": [
    {
      url: `${import.meta.env.VITE_PUBLIC_LOOKER_DEPLOYED_END_POINT}/embed/public/vT7QK3fBvh9pWzgkrWPgK8p3rHPz2C53`,
    },
  ],
  default: [
    {
      url: "",
    },
  ],
}
