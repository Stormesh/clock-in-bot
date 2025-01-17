import React from "react";
import Signup from "./components/Signup";
import { SessionProvider } from "next-auth/react";
import { auth } from "@/src/auth";
import Warning from "../components/Warning";

const page = async () => {
  const session = await auth();

  if (!session?.user.roleId.permissions?.includes("sign-up")) {
    return (
      <Warning
        text="You do not have permission to access this page"
        link="/"
        linkText="Go back"
      />
    );
  }

  return (
    <SessionProvider>
      <Signup />
    </SessionProvider>
  );
};

export default page;
