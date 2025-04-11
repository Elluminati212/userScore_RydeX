"use client";

import {
  Sidebar,
  SidebarContent,
  SidebarFooter,
  SidebarGroup,
  SidebarGroupLabel,
  SidebarHeader,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
  SidebarSeparator,
  SidebarTrigger,
  SidebarInset,
} from "@/components/ui/sidebar";
import {Card, CardContent, CardDescription, CardHeader, CardTitle} from "@/components/ui/card";
import {Icons} from "@/components/icons";

export function Dashboard() {
  return (
    <>
      <Sidebar className="w-60">
        <SidebarHeader>
          <CardTitle>TripSurgeAI</CardTitle>
          <CardDescription>
            Intelligent Trip Analysis and Surge Pricing
          </CardDescription>
        </SidebarHeader>
        <SidebarContent>
          <SidebarGroup>
            <SidebarGroupLabel>Navigation</SidebarGroupLabel>
            <SidebarMenu>
              <SidebarMenuItem>
                <SidebarMenuButton href="#">
                  <Icons.home className="mr-2 h-4 w-4"/>
                  <span>Dashboard</span>
                </SidebarMenuButton>
              </SidebarMenuItem>
              <SidebarMenuItem>
                <SidebarMenuButton href="#">
                  <Icons.search className="mr-2 h-4 w-4"/>
                  <span>Surge Analysis</span>
                </SidebarMenuButton>
              </SidebarMenuItem>
              <SidebarMenuItem>
                <SidebarMenuButton href="#">
                  <Icons.settings className="mr-2 h-4 w-4"/>
                  <span>Settings</span>
                </SidebarMenuButton>
              </SidebarMenuItem>
            </SidebarMenu>
          </SidebarGroup>
        </SidebarContent>
        <SidebarFooter>
          <SidebarSeparator/>
          <p className="text-xs text-muted-foreground">
            Powered by Firebase Studio
          </p>
        </SidebarFooter>
      </Sidebar>
      <SidebarInset>
        <Card className="m-4">
          <CardHeader>
            <CardTitle>Welcome</CardTitle>
            <CardDescription>
              Here you can view Trip surge details.
            </CardDescription>
          </CardHeader>
          <CardContent>
            {/* Main content of the dashboard */}
          </CardContent>
        </Card>
      </SidebarInset>
    </>
  );
}
