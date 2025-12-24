"use client";

import { useParams, useRouter } from "next/navigation";
import { useTranslations } from "next-intl";
import { ArrowLeft } from "lucide-react";
import { Button } from "@/components/ui/button";
import { RecordDetail } from "@/components/records/record-detail";

export default function RecordDetailPage() {
  const params = useParams();
  const router = useRouter();
  const recordId = params.id as string;
  const t = useTranslations("records");

  const handleBack = () => {
    // Use browser history to go back to the previous page
    // This preserves dashboard state when coming from search results
    if (window.history.length > 1) {
      router.back();
    } else {
      // Fallback to records page if no history
      router.push("/records");
    }
  };

  return (
    <div className="space-y-6">
      {/* Page Header */}
      <div className="flex items-center gap-2">
        <Button variant="ghost" size="icon" onClick={handleBack}>
          <ArrowLeft className="h-4 w-4" />
        </Button>
        <h1 className="text-3xl font-bold tracking-tight">{t("recordDetails")}</h1>
      </div>

      {/* Record Detail */}
      <RecordDetail recordId={recordId} />
    </div>
  );
}

