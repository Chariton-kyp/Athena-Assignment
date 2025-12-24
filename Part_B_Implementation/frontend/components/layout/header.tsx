"use client";

import Link from "next/link";
import { Menu } from "lucide-react";
import { NotificationIndicator } from "@/components/notifications/notification-indicator";
import { LanguageSwitcher } from "@/components/layout/language-switcher";
import { Button } from "@/components/ui/button";

interface HeaderProps {
  onMenuClick?: () => void;
}

export function Header({ onMenuClick }: HeaderProps) {
  return (
    <header className="sticky top-0 z-40 w-full border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
      <div className="flex h-16 items-center px-4 md:px-6">
        {/* Mobile menu button */}
        <Button
          variant="ghost"
          size="icon"
          className="mr-2 md:hidden"
          onClick={onMenuClick}
        >
          <Menu className="h-5 w-5" />
          <span className="sr-only">Toggle menu</span>
        </Button>

        {/* Logo */}
        <Link href="/" className="flex items-center space-x-2">
          <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-primary">
            <span className="text-lg font-bold text-primary-foreground">T</span>
          </div>
          <span className="hidden font-bold sm:inline-block">
            TechFlow Solutions
          </span>
        </Link>

        {/* Right side actions */}
        <div className="ml-auto flex items-center space-x-2">
          {/* Notifications */}
          <NotificationIndicator />

          {/* Language selector */}
          <LanguageSwitcher />
        </div>
      </div>
    </header>
  );
}
