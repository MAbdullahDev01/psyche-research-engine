import type { Metadata } from "next";
import "./globals.css";
import { ClerkProvider } from "@clerk/nextjs";

export const metadata: Metadata = { title:"Psyche Research Engine", description:"A calm research instrument for discovering and organizing psychological literature." };

export default function RootLayout({children}:LayoutProps<"/">){return <html lang="en" className="h-full antialiased"><body className="min-h-full"><ClerkProvider>{children}</ClerkProvider></body></html>}
