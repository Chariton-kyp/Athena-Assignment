"use client";

import { useTranslations } from "next-intl";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from "recharts";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Skeleton } from "@/components/ui/skeleton";
import { useStats } from "@/lib/hooks/use-stats";

const TYPE_COLORS: Record<string, string> = {
  FORM: "#3b82f6",
  EMAIL: "#10b981",
  INVOICE: "#f59e0b",
};

export function TypeChart() {
  const { data: stats, isLoading, error } = useStats();
  const t = useTranslations("extraction");
  const tDashboard = useTranslations("dashboard");

  if (isLoading) {
    return (
      <Card>
        <CardHeader>
          <CardTitle>{tDashboard("recordsByType")}</CardTitle>
        </CardHeader>
        <CardContent>
          <Skeleton className="h-[250px] w-full" />
        </CardContent>
      </Card>
    );
  }

  if (error || !stats) {
    return (
      <Card>
        <CardHeader>
          <CardTitle>{tDashboard("recordsByType")}</CardTitle>
        </CardHeader>
        <CardContent className="flex h-[250px] items-center justify-center">
          <p className="text-muted-foreground">Unable to load chart</p>
        </CardContent>
      </Card>
    );
  }

  const typeLabels: Record<string, string> = {
    FORM: t("forms"),
    EMAIL: t("emails"),
    INVOICE: t("invoices"),
  };

  const data = Object.entries(stats.by_type || {}).map(([type, value]) => ({
    name: typeLabels[type] || type,
    count: value,
    fill: TYPE_COLORS[type] || "#6b7280",
  }));

  if (data.length === 0) {
    return (
      <Card>
        <CardHeader>
          <CardTitle>{tDashboard("recordsByType")}</CardTitle>
        </CardHeader>
        <CardContent className="flex h-[250px] items-center justify-center">
          <p className="text-muted-foreground">No records to display</p>
        </CardContent>
      </Card>
    );
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle>{tDashboard("recordsByType")}</CardTitle>
      </CardHeader>
      <CardContent>
        <ResponsiveContainer width="100%" height={250}>
          <BarChart data={data} layout="vertical">
            <CartesianGrid strokeDasharray="3 3" horizontal={false} />
            <XAxis type="number" />
            <YAxis dataKey="name" type="category" width={80} />
            <Tooltip
              formatter={(value: number) => [value, "Records"]}
              contentStyle={{
                backgroundColor: "hsl(var(--background))",
                border: "1px solid hsl(var(--border))",
                borderRadius: "8px",
              }}
            />
            <Bar
              dataKey="count"
              radius={[0, 4, 4, 0]}
              fill="#3b82f6"
            />
          </BarChart>
        </ResponsiveContainer>
      </CardContent>
    </Card>
  );
}
