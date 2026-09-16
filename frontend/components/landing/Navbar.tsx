import Link from 'next/link';

export default function Navbar(){
  return(
    <nav className='flex items-center justify-between p-4 bg-gray-800 text-white'>

      {/* Brand name */}
      <div className='flex items-center space-x-4'>
        <Link href="/">Pysche Research Engine</Link>
      </div>

      {/* In page links */}
      <div className='flex items-center space-x-4'>
        <p>To be added</p>
      </div>

      {/* Auth links */}
      <div className='flex items-center space-x-4'>
        <Link href="auth/sign-in">Sign In</Link>
        <Link href="auth/sign-up">Sign Up</Link>
      </div>
    </nav>
  )
}