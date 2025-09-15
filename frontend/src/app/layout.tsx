import type { Metadata } from "next"
import "./globals.css"

export const metadata: Metadata = {
  title: "Jan Setu",
  description: "A crowd-sourced platform for reporting civic issues.",
}

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode
}>) {
  return (
    <html lang="en">
      <body className="antialiased">{children}</body>
    </html>
  )
}
