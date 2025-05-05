// Create a new file: client/src/app/components/SessionProviderWrapper.tsx
"use client";

import { SessionProvider } from "next-auth/react";
import React from "react";

export default function SessionProviderWrapper({
  children,
}: {
  children: React.ReactNode;
}) {
  return <SessionProvider>{children}</SessionProvider>;
}
