import { auth } from "@/src/auth";
import Link from "next/link";
import React from "react";
import SignOutButton from "./SignOutButton";

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
            <Link
              href="/signup"
              className="inline-block bg-fuchsia-900 mx-2 hover:bg-fuchsia-500 hover:scale-110 transition-all duration-300 text-white font-bold py-2 px-4 rounded mt-4 select-none"
            >
              Sign up
            </Link>
          )}
        {session?.user?.roleId &&
          session?.user.roleId.permissions?.some(
            (permission) =>
              permission === "delete-user" || permission === "update-user"
          ) && (
            <Link
              href="/secretpanel"
              className="bg-blue-900 mx-2 hover:bg-blue-500 hover:scale-110 transition-all duration-300 text-white font-bold py-2 px-4 rounded mt-4 select-none"
            >
              Admin
            </Link>
          )}
        <SignOutButton />
      </div>
    </div>
  );
};

export default UserPanel;
