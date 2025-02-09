import { auth } from "@/src/auth";
import React from "react";

const page = async () => {
  const session = await auth();
  return (
    <div className="flex justify-center items-center">
      <h1 className="text-white text-4xl text-center">Welcome to the Admin Page, <span className="font-bold">{session?.user.name}</span></h1>
    </div>
  );
};

export default page;
