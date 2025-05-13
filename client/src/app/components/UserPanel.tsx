"use client";

import React from "react";
import SignOutButton from "@components/SignOutButton";
import SidebarButton from "./SidebarButton";
import { Permissions } from "../lib/enums";
import { faBusinessTime, faDoorOpen, faHome } from "@fortawesome/free-solid-svg-icons";
import { useSession } from "next-auth/react";
import { IconDefinition } from "@fortawesome/fontawesome-svg-core";
import { hasPermission, hasAnyPermission } from "../lib/utils";

const UserPanel = () => {
  const { data: session } = useSession();
  const user = session?.user;

  if (!user) return null;

  const renderSidebarButton = (text: string, icon: IconDefinition, href?: string) => (
    <SidebarButton
      key={text}
      text={text}
      icon={icon}
      href={href}
    />
  );

  return (
    <div className="flex flex-col justify-center items-center">
      <h2 className="text-center text-xl text-white font-sans">
        Welcome <br />
        <span className="font-bold text-3xl">{session?.user?.name}!</span>
      </h2>
      <div className="flex justify-center items-center mt-2">
        {session?.user?.roleId &&
          session?.user?.roleId.permissions?.includes(Permissions.SignUp) && (
            <PanelButton
              text="Sign Up"
              isLink
              link="/signup"
            />
          )}
        {session?.user?.roleId &&
          session?.user.roleId.permissions?.some(
            (permission) =>
              permission === Permissions.Delete ||
              permission === Permissions.Update
          ) && (
            <PanelButton
              text="Admin"
              isLink
              link="/admin"
            />
          )}
        <SignOutButton />
      </div>
    </div>
  );
};

export default UserPanel;
