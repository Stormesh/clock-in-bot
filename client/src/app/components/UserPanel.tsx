import { auth } from "@/src/auth";
import React from "react";
import SignOutButton from "@components/SignOutButton";
import PanelButton from "./PanelButton";
import { Permissions } from "../lib/enums";

const UserPanel = async () => {
  const session = await auth();

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
