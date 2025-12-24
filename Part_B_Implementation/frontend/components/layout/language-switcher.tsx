"use client";

import { useLocale } from "next-intl";
import { Globe } from "lucide-react";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";

const languages = [
  { code: "en", name: "English", flag: "🇬🇧" },
  { code: "el", name: "Ελληνικά", flag: "🇬🇷" },
] as const;

export function LanguageSwitcher() {
  const currentLocale = useLocale();

  const handleLocaleChange = (newLocale: string) => {
    if (newLocale === currentLocale) return;

    // Set cookie that will be read by the server
    document.cookie = `NEXT_LOCALE=${newLocale};path=/;max-age=31536000`;
    // Hard reload to ensure server reads the new cookie
    window.location.reload();
  };

  const currentLanguage = languages.find((lang) => lang.code === currentLocale);

  return (
    <Select value={currentLocale} onValueChange={handleLocaleChange}>
      <SelectTrigger className="w-auto gap-2 border-none bg-transparent shadow-none focus:ring-0">
        <Globe className="h-4 w-4" />
        <SelectValue>
          <span className="hidden sm:inline">
            {currentLanguage?.flag} {currentLanguage?.code.toUpperCase()}
          </span>
          <span className="sm:hidden">{currentLanguage?.flag}</span>
        </SelectValue>
      </SelectTrigger>
      <SelectContent>
        {languages.map((lang) => (
          <SelectItem key={lang.code} value={lang.code}>
            <span className="mr-2">{lang.flag}</span>
            {lang.name}
          </SelectItem>
        ))}
      </SelectContent>
    </Select>
  );
}
