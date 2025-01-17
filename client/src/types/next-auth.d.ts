import { DefaultSession } from "next-auth";

declare module "next-auth" {
  interface Session {
    user: User & DefaultSession["user"];
  }
  interface User {
    roleId: IRole;
  }
}

// eslint-disable-next-line @typescript-eslint/no-unused-vars
import { JWT } from "next-auth/jwt";
import { IRole } from "../app/lib/models";

declare module "next-auth/jwt" {
  interface JWT {
    roleId: IRole;
  }
}
