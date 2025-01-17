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
      <body className="bg-gradient-to-tr bg-fixed from-[#151216] to-[#4d3e66]">
        {children}
      </body>
    </html>
  );
}
