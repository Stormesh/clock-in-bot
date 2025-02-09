import { auth } from "@/src/auth";
import React from "react";
import SignOutButton from "@components/SignOutButton";
import PanelButton from "./PanelButton";

const UserPanel = async () => {
  const session = await auth();

  return (
    <div className="flex flex-col justify-center items-center">
      <h2 className="text-center text-xl text-white font-sans">
        Welcome <br />
        <span className="font-bold text-3xl">{session?.user?.name}!</span>
      </h2>
      <div className="flex justify-center items-center">
        {session?.user?.roleId &&
          session?.user?.roleId.permissions?.includes("sign-up") && (
            <PanelButton text="Sign Up" color="bg-fuchsia-900" hoverColor="hover:bg-fuchsia-500" isLink link="/signup" />
          )}
        {session?.user?.roleId &&
          session?.user.roleId.permissions?.some(
            (permission) =>
              permission === "delete-user" || permission === "update-user"
          ) && (
            <PanelButton text="Admin" color="bg-blue-900" hoverColor="hover:bg-blue-500" isLink link="/admin" />
          )}
        <SignOutButton />
      </div>
    </div>
  );
};

export default UserPanel;
