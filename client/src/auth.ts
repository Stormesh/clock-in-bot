//Auth.js
import NextAuth from "next-auth";
import Credentials from "next-auth/providers/credentials";
// Your own logic for dealing with plaintext password strings; be careful!
import { signInSchema } from "./app/lib/zod";
import { compare } from "bcryptjs";
import { getUser } from "./app/lib/data";
import { ZodError } from "zod";
import { PopulatedUser } from "./app/lib/models";

export const { handlers, signIn, signOut, auth } = NextAuth({
  providers: [
    Credentials({
      // You can specify which fields should be submitted, by adding keys to the `credentials` object.
      // e.g. domain, username, password, 2FA token, etc.
      credentials: {
        username: { label: "Username", type: "text", placeholder: "Username" },
        password: {
          label: "Password",
          type: "password",
          placeholder: "Password",
        },
      },
      authorize: async (credentials) => {
        try {
          const { username, password } = await signInSchema.parseAsync(
            credentials
          );

          // logic to verify if the user exists
          const user: PopulatedUser = await getUser(username);

          if (!user) {
            // No user found, so this is their first attempt to login
            // Optionally, this is also the place you could do a user registration
            throw new Error("Invalid credentials.");
          }

          // logic to verify if the password is correct
          const passwordsMatch = await compare(password, user.password);

          if (!passwordsMatch) {
            throw new Error("Invalid password.");
          }

          console.log(user);

          // return user object with their profile data
          return { id: user._id, name: user.username, roleId: user.roleId };
        } catch (error) {
          if (error instanceof ZodError) {
            throw new Error(error.issues[0].message);
          }
          throw new Error("Invalid credentials.");
        }
      },
    }),
  ],
  secret: process.env.NEXTAUTH_SECRET,
  pages: {
    signIn: "/login",
  },
  session: {
    strategy: "jwt",
  },
  callbacks: {
    async session({ session, token }) {
      if (token?.sub && token?.name && token?.roleId) {
        session.user.id = token.sub;
        session.user.name = token.name;
        session.user.roleId = token.roleId;
      }
      return session;
    },
    async jwt({ token, user }) {
      if (user) {
        token.id = user.id;
        token.name = user.name;
        token.roleId = user.roleId;
      }
      return token;
    },
  },
});