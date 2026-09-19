"use client";

import { UserButton } from "@clerk/nextjs";
import Link from "next/link";

export default function WorkspaceHeader() {
  return (
    <header className="border-b border-slate-200 bg-white">
      <div className="mx-auto flex max-w-6xl items-center justify-between px-6 py-4">
        <Link href="/dashboard" className="font-semibold tracking-tight text-slate-950">
          Psyche Research Engine
        </Link>
        <UserButton />
      </div>
    </header>
  );
}
