"use client";

import React from "react";
import SignOutButton from "@components/SignOutButton";
import SidebarButton from "./SidebarButton";
import { Permissions } from "../lib/enums";
import { faBusinessTime, faDoorOpen, faHome } from "@fortawesome/free-solid-svg-icons";
import { useSession } from "next-auth/react";
import { IconDefinition } from "@fortawesome/fontawesome-svg-core";

const UserPanel = () => {
  const { data: session } = useSession();
  const user = session?.user;

  if (!user) return null;

  const hasPermission = (permission: Permissions) =>
    user.roleId?.permissions?.includes(permission);

  const hasAnyPermission = (permissions: Permissions[]) =>
    permissions.some(p => user.roleId?.permissions?.includes(p));

  const renderSidebarButton = (text: string, icon: IconDefinition, link: string, isLink: boolean = true) => (
    <SidebarButton
      key={text}
      text={text}
      icon={icon}
      isLink={isLink}
      link={link}
    />
  );

  return (
    <div className="inline-flex flex-col dark:bg-zinc-900 bg-gray-100 w-64 h-screen fixed">
      <div className="flex flex-col">
        <h2 className="text-center text-xl dark:text-white font-sans">
          Welcome <br />
          <span className="font-bold text-3xl">{user.name}!</span>
        </h2>
        <hr className="border-t mx-6 mt-4 border-gray-400 dark:border-zinc-600" />
        <div className="my-5">
          {renderSidebarButton("Home", faHome, "")}
          {hasPermission(Permissions.SignUp) && renderSidebarButton("Sign Up", faDoorOpen, "signup")}
          {hasAnyPermission([Permissions.Delete, Permissions.Update]) && renderSidebarButton("Admin", faBusinessTime, "admin")}
          <SignOutButton />
        </div>
      </div>
    </div>
  );
};

export default UserPanel;
