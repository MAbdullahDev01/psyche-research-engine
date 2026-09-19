"use client";

import { SignInButton, SignUpButton, useAuth } from '@clerk/nextjs';
import Link from 'next/link';

export default function Navbar(){
  const { isLoaded, isSignedIn } = useAuth();

  return(
    <nav className='flex items-center justify-between p-4 bg-gray-800 text-white'>

      {/* Brand name */}
      <div className='flex items-center space-x-4'>
        <Link href="/">Pysche Research Engine</Link>
      </div>

      {/* In page links */}
      <div className='flex items-center space-x-4'>
        {isLoaded && isSignedIn && <Link href="/dashboard" className="text-sm hover:text-cyan-300">Dashboard</Link>}
      </div>

      {/* Auth links */}
      <div className='flex items-center space-x-4'>
        {isLoaded && !isSignedIn && <SignInButton />}
        {isLoaded && !isSignedIn && <SignUpButton />}
      </div>
    </nav>
  )
}