import React from "react";
import Signup from "@components/signup/Signup";
import { SessionProvider } from "next-auth/react";
import { auth } from "@/src/auth";
import Warning from "@components/Warning";
import { Permissions } from "../lib/enums";
import { getRoleNamesAction } from "../actions/roles";
import { hasPermission } from "../lib/utils";

export const dynamic = "force-dynamic";

const page = async () => {
  const roleNames = await getRoleNamesAction();

  const session = await auth();
  const sessionUser = session?.user;

  if (!sessionUser || !hasPermission(sessionUser, Permissions.SignUp)) {
    return <Warning />;
  }

  return (
    <SessionProvider>
      <Signup initialRoleNames={roleNames} />
    </SessionProvider>
  );
};

export default page;
