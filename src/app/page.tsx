"use client";

import {Toaster} from "@/components/ui/toaster";
import {Dashboard} from "@/components/dashboard";
import {SidebarProvider} from "@/components/ui/sidebar";

export default function Home() {
  return (
    <SidebarProvider>
      <Dashboard />
      <Toaster />
    </SidebarProvider>
  );
}
