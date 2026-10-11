"use client";

import { SignInButton, SignUpButton, useAuth } from "@clerk/nextjs";
import Link from "next/link";
import { useEffect, useState } from "react";

const navItems = [
  { label: "Research", href: "#research" },
  { label: "Understand", href: "#understand" },
  { label: "Write", href: "#write" },
];

export default function Navbar() {
  const { isLoaded, isSignedIn } = useAuth();
  const [isScrolled, setIsScrolled] = useState(false);
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const [activeSection, setActiveSection] = useState("research");

  useEffect(() => {
    const handleScroll = () => setIsScrolled(window.scrollY > 24);
    handleScroll();
    window.addEventListener("scroll", handleScroll, { passive: true });

    const sections = navItems
      .map(({ href }) => document.querySelector(href))
      .filter((section): section is Element => section !== null);
    const observer = new IntersectionObserver(
      (entries) => {
        const visibleSection = entries
          .filter((entry) => entry.isIntersecting)
          .sort((a, b) => b.intersectionRatio - a.intersectionRatio)[0];
        if (visibleSection) setActiveSection(visibleSection.target.id);
      },
      { rootMargin: "-18% 0px -65%", threshold: [0.1, 0.35, 0.6] },
    );
    sections.forEach((section) => observer.observe(section));

    return () => {
      window.removeEventListener("scroll", handleScroll);
      observer.disconnect();
    };
  }, []);

  const closeMenu = () => setIsMenuOpen(false);

  return (
    <header className={`fixed inset-x-0 top-0 z-50 transition duration-300 ${isScrolled ? "border-b border-[#ECE9E1] bg-[#FAF9F6]/95 shadow-[0_4px_20px_rgba(23,24,22,0.05)] backdrop-blur-md" : "bg-transparent"}`}>
      <nav aria-label="Primary navigation" className="mx-auto flex h-[76px] max-w-[1440px] items-center justify-between px-5 md:px-8 lg:px-16">
        <Link href="/" onClick={closeMenu} className="group flex items-center gap-3" aria-label="Psychology Research Lab home">
          <span className="pulse-dot h-2 w-2 rounded-full bg-[#315C4A]" />
          <span className="flex flex-col font-mono-ui text-[10px] font-semibold leading-[1.05] tracking-[.12em] text-[#171816]">
            <span>PSYCHOLOGY</span>
            <span className="text-[#6E7068]">RESEARCH LAB</span>
          </span>
        </Link>

        <div className="hidden items-center gap-8 md:flex">
          {navItems.map((item) => {
            const isActive = activeSection === item.href.slice(1);
            return <a key={item.href} href={item.href} className={`group relative py-2 text-sm transition-colors duration-200 ${isActive ? "text-[#315C4A]" : "text-[#363832] hover:text-[#315C4A]"}`}>
              {item.label}
              <span className={`absolute inset-x-0 -bottom-0.5 h-px origin-left bg-[#B56A3C] transition-transform duration-300 ${isActive ? "scale-x-100" : "scale-x-0 group-hover:scale-x-100"}`} />
            </a>;
          })}
        </div>

        <div className="hidden items-center gap-3 md:flex">
          {isLoaded && isSignedIn && <Link href="/dashboard" className="group inline-flex items-center gap-2 px-2 py-2 text-sm text-[#363832] transition-colors hover:text-[#315C4A]">Dashboard <span className="transition-transform group-hover:translate-x-1">→</span></Link>}
          {isLoaded && !isSignedIn && <SignInButton><button className="px-2 py-2 text-sm text-[#363832] transition-colors hover:text-[#315C4A]">Sign in</button></SignInButton>}
          {isLoaded && !isSignedIn && <SignUpButton><button className="group inline-flex items-center gap-2 rounded-[6px] border border-[#315C4A] bg-[#315C4A] px-4 py-2.5 text-sm font-semibold text-[#FAF9F6] transition duration-150 hover:-translate-y-px hover:bg-[#244536]">Start researching <span className="transition-transform group-hover:translate-x-1">→</span></button></SignUpButton>}
        </div>

        <button type="button" aria-expanded={isMenuOpen} aria-controls="mobile-navigation" aria-label={isMenuOpen ? "Close navigation menu" : "Open navigation menu"} onClick={() => setIsMenuOpen((open) => !open)} className="flex h-10 w-10 flex-col items-end justify-center gap-1.5 md:hidden">
          <span className={`h-px bg-[#171816] transition-all duration-300 ${isMenuOpen ? "w-5 -translate-y-px rotate-45" : "w-5"}`} />
          <span className={`h-px bg-[#171816] transition-all duration-300 ${isMenuOpen ? "w-5 -translate-y-1.5 -rotate-45" : "w-3"}`} />
        </button>
      </nav>

      <div id="mobile-navigation" className={`overflow-hidden border-t border-[#ECE9E1] bg-[#FAF9F6] transition-[max-height,opacity] duration-300 md:hidden ${isMenuOpen ? "max-h-80 opacity-100" : "max-h-0 border-t-transparent opacity-0"}`}>
        <div className="mx-auto flex max-w-[1440px] flex-col px-5 pb-6 pt-3">
          {navItems.map((item, index) => <a key={item.href} href={item.href} onClick={closeMenu} className="flex items-center justify-between border-b border-[#ECE9E1] py-4 text-lg text-[#363832] transition-colors hover:text-[#315C4A]" style={{ transitionDelay: isMenuOpen ? `${index * 45}ms` : "0ms" }}>{item.label}<span className="text-[#B56A3C]">↗</span></a>)}
          {isLoaded && isSignedIn && <Link href="/dashboard" onClick={closeMenu} className="pt-4 text-sm font-semibold text-[#315C4A]">Dashboard →</Link>}
          {isLoaded && !isSignedIn && <div className="flex items-center gap-4 pt-5"><SignInButton><button className="text-sm text-[#363832]">Sign in</button></SignInButton><SignUpButton><button className="rounded-[6px] bg-[#315C4A] px-4 py-2.5 text-sm font-semibold text-[#FAF9F6]">Start researching →</button></SignUpButton></div>}
        </div>
      </div>
    </header>
  );
}