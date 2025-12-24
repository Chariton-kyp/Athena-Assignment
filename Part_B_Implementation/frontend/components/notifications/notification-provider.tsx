"use client";

import { createContext, useContext, ReactNode } from "react";
import { useNotifications, Notification } from "@/lib/hooks/use-notifications";

interface NotificationContextType {
  isConnected: boolean;
  notifications: Notification[];
  clearNotifications: () => void;
  sendMessage: (message: unknown) => void;
}

const NotificationContext = createContext<NotificationContextType | undefined>(undefined);

interface NotificationProviderProps {
  children: ReactNode;
}

export function NotificationProvider({ children }: NotificationProviderProps) {
  const notificationData = useNotifications({
    enabled: true,
    autoReconnect: true,
    reconnectInterval: 3000,
    maxReconnectAttempts: 10,
  });

  return (
    <NotificationContext.Provider value={notificationData}>
      {children}
    </NotificationContext.Provider>
  );
}

export function useNotificationContext(): NotificationContextType {
  const context = useContext(NotificationContext);
  if (context === undefined) {
    throw new Error("useNotificationContext must be used within a NotificationProvider");
  }
  return context;
}
