import type { Metadata } from "next";
import "./globals.css";
import UserPanel from "./components/UserPanel";
import SessionProviderWrapper from "./components/SessionProviderWrapper";

export const metadata: Metadata = {
  title: "Clock In",
  description: "A simple clock-in app for Discord",
};

export default async function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {

  return (
    <html lang="en">
      <body className="dark:bg-zinc-800 bg-zinc-50 bg-fixed">
        <SessionProviderWrapper>
          <UserPanel />
        </SessionProviderWrapper>
        {children}
      </body>
    </html>
  );
}
