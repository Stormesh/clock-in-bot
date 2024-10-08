import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Clock In",
  description: "A simple clock-in app for Discord",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body>
        {children}
      </body>
    </html>
  );
}
